import os

from setuptools import setup

requires = open("requirements.txt", "r").readlines() if os.path.exists("requirements.txt") else open("./hipnuc_usb_apiserver.egg-info/requires.txt", "r").readlines()
print("#-------------------    ", str(os.listdir("./")))
setup(
    name="hipnuc-usb-apiserver",
    version="0.3.0",
    author="davidliyutong",
    author_email="davidliyutong@sjtu.edu.cn",
    description="Driver for Arizona USB Pressure Sensor",
    packages=[
        "hipnuc_usb_apiserver",
        "hipnuc_usb_apiserver.apiserver",
        "hipnuc_usb_apiserver.client",
        "hipnuc_usb_apiserver.cmd",
        "hipnuc_usb_apiserver.grpc",
        "hipnuc_usb_apiserver.hipnuc"
    ],
    python_requires=">=3.7",
    install_requires=requires,
    test_requires=[
        "requests",
        "tqdm",
    ],
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown"
)