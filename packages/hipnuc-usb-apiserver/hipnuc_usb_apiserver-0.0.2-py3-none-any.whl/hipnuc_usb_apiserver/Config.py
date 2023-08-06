
import yaml
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class Config:
    path: str = './hipnuc_config.yaml'
    
    serial: Dict[str, Any] = None
    api_port: str = 8080
    api_interface: str = '0.0.0.0'
    debug: bool = False
    
    valid: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        err = self.load()
        if err is None:
            self.valid = True
        else:
            self.valid = False

    def load(self) -> Optional[Exception]:
        if self.path is not None:
            try:
                cfg_dict = yaml.load(open(self.path, "r"),
                                     Loader=yaml.SafeLoader)
            except Exception as e:
                return e

            try:
                cfg = cfg_dict['hipnuc_usb_apiserver']
                
                self.serial = cfg['serial']
                self.api_port = cfg['api']['port']
                self.api_interface = cfg['api']['interface'] if 'interface' in cfg['api'] else '0.0.0.0'
                self.debug = cfg['debug']
                
                return None

            except Exception as e:
                return e

        else:
            return Exception("Config path is not set")

    def dump(self) -> Optional[Exception]:
        if self.path is not None:
            try:
                with open(self.path, 'w') as f:
                    yaml.dump({
                        "serial": self.serial,
                        "api": {
                            "port": self.api_port,
                            "interface": self.api_interface
                        },
                        "debug": self.debug,
                    }, f)
                    return None
            except:
                return Exception("Failed to dump config")
        else:
            return Exception("Config path is not set")