import os, sys, json
from epkernel import epcam, BASE

def init(path:str): 
    epcam.init(path)
    BASE.set_config_path(path)
    v = epcam.getVersion()
    version = v['ep_version'] + v['sub_version']
    if not version == '1.01':
        print("Epkernel与bin包版本不匹配，请谨慎使用")

def set_sysattr_path(path:str):
    try:
        BASE.set_sysAttr_path(path)
    except Exception as e:
        print(e)
    return 

def set_userattr_path(path:str):
    try:
        BASE.set_userAttr_path(path)
    except Exception as e:
        print(e)
    return  
