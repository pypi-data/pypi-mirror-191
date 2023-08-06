import argparse
import time
from hipnuc_usb_apiserver.hipnuc import hipnuc_module, hipnuc_protocol
from hipnuc_usb_apiserver.Config import Config as IMUConfig
import logging
from typing import Optional, List
import threading
import grpc
import datetime
import os.path as osp
import os

SERVER: Optional[grpc.server] = None


class Application:
    option: IMUConfig
    start_fifo_ev: threading.Event
    stop_local_ev: threading.Event
    imu_array: List[hipnuc_module]
    logger: logging.Logger
    local_recording_started: bool
    local_recording_thread: threading.Thread

    def __init__(self, cfg) -> None:
        if isinstance(cfg, IMUConfig):
            self.option = cfg
        elif isinstance(cfg, str):
            self.option = IMUConfig(cfg)
        elif isinstance(cfg, argparse.Namespace):
            self.option = IMUConfig(cfg.config)
        else:
            raise TypeError(
                "cfg must be IMUConfig, str, or argparse.Namespace")

        self.logger = logging.getLogger("hipnuc.main")
        self.logger.info("Starting hipnuc_usb_apiserver with %d IMUs",
                         len(self.option.serial))
        self.start_fifo_ev = threading.Event()
        self.stop_local_ev = threading.Event()
        self.imu_array = []
        self.local_recording_started = False
        self.local_recording_thread = None

    def start_thread(self):
        def update_hipnuc_sensor_thread():
            assert(self.option is not None)
            while True:
                self.start_fifo_ev.wait()

                self.logger.info("Connecting to %d IMUs",
                                 len(self.option.serial))
                self.imu_array = [hipnuc_module(c) for c in self.option.serial]
                time.sleep(1)
                hipnuc_protocol.sample_rate_timer_close()

                while True:
                    time.sleep(0.01)
                    if not self.start_fifo_ev.is_set():
                        self.logger.info("Closing %d IMUs",
                                         len(self.option.serial))
                        [imu.close() for imu in self.imu_array]
                        break

        threading.Thread(target=update_hipnuc_sensor_thread,
                         daemon=True).start()

    def start_fifo(self) ->  Optional[Exception]:
        if self.local_recording_started is True:
            return Exception("Local recording is already started")
        elif self.start_fifo_ev.is_set():
            return Exception("FIFO is already started")
        else:
            self.start_fifo_ev.set()
            return None

    def stop_fifo(self) ->  Optional[Exception]:
        if self.local_recording_started is True:
            return Exception("Local recording is already started")
        elif not self.start_fifo_ev.is_set():
            return Exception("FIFO is already stopped")
        else:
            self.start_fifo_ev.clear()
            return None
    
    @property
    def fifo_status(self):
        return self.start_fifo_ev.is_set()

    @property
    def local_status(self):
        return self.local_recording_started
    
    def shutdown(self):
        [imu.close() for imu in self.imu_array]

    def get(self):
        try:
            return [imu.get_module_data(0.01) for imu in self.imu_array]
        except:
            return [None for imu in self.imu_array]

    def get_by_index(self, idx: int):
        if idx >= len(self.imu_array):
            return None
        else:
            try:
                return self.imu_array[idx].get_module_data(0.01)
            except:
                return None

    def start_local(self, path: str) -> Optional[Exception]:
        if path is None or path == '':
            return Exception("Path is empty")
        if self.local_recording_started is True:
            return Exception("Local recording is already started")
        elif self.start_fifo_ev.is_set():
            return Exception("FIFO is already started")
        else:
            # Do something
            def record_csv(path: str):
                imu_array = [hipnuc_module(c) for c in self.option.serial]
                if not osp.exists(path):
                    self.logger.info(f"Creating directory: {path}")
                    os.makedirs(path)

                self.logger.info(f"Started measurement at: {datetime.datetime.utcnow().timestamp()}")
                logging.info(f'Saving measurement to {path}')

                # Create csv file
                [imu.create_csv(osp.join(path, f'{i}.csv')) for i, imu in enumerate(imu_array)]
                f_handles = [open(osp.join(path, f'{i}.csv'), 'a') for i, _ in enumerate(imu_array)]

                while True:
                    try:
                        msg_array = [imu.get_module_data(10) for imu in imu_array]
                        # print('-------------------')
                        # print(imu_array, msg_array, f_handles)
                        # print('-------------------')
                        #write to file as csv format, only work for 0x91, 0x62(IMUSOL), or there will be error
                        [imu.write2csv_handle(msg['data'], f) for imu, msg, f in zip(imu_array,msg_array, f_handles)]
                        
                        if self.stop_local_ev.is_set():
                            self.logger.info(f"Stopped measurement at: {datetime.datetime.utcnow().timestamp()}")
                            [imu.close() for imu in imu_array]
                            self.stop_local_ev.clear()
                            break

                    except Exception as err:
                        [imu.close() for imu in imu_array]
                        self.logger.error(f"Error: {err}")
                        break

                self.logger.info("Recording is terminated.")
            
            self.local_recording_thread = threading.Thread(target=record_csv, args=(path,), daemon=True)
            self.local_recording_thread.start()
            self.local_recording_started = True
            return None

    def stop_local(self) -> Optional[Exception]:
        print('----------- stop_local ------------')
        if self.local_recording_started is False:
            return Exception("Local recording is not started")
        elif self.start_fifo_ev.is_set():
            return Exception("FIFO is already started")
        else:
            # Do something
            self.stop_local_ev.set()
            if self.local_recording_thread is not None:
                self.local_recording_thread.join(timeout=3)
                if not self.local_recording_thread.is_alive():
                
                    self.local_recording_started = False
                    self.local_recording_thread = None
                    return None
                else:
                    return Exception("Failed to stop local recording")


if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./hipnuc_config.yaml")
    run_args = parser.parse_args(sys.argv[1:])

    logging.basicConfig(level=logging.INFO)

    app = Application(run_args)
    app.start_thread()

    app.start_fifo_ev.set()

    try:
        while True:
            print(app.get())

    except KeyboardInterrupt as e:
        app.shutdown()
