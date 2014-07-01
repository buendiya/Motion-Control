import os
from ctypes import *
from ctypes.wintypes import WORD, DWORD, LONG
import logging

logging.basicConfig(level=logging.DEBUG)

_cur_dir = os.path.dirname(os.path.abspath(__file__))
os.environ['PATH'] = os.path.pathsep.join([_cur_dir, os.environ['PATH']])
_dll_file = os.path.join(_cur_dir, 'ymcPCAPI.dll')
try:
    ymc = windll.LoadLibrary(_dll_file)
except Exception as e:
    logging.warning('Failed to load model ymcPCAPI.dll!')
    ymc = None
else:
    logging.info("LoadLibrary succeed")

MP_SUCCESS = 0x00000000


class COMMUNICATION_DEVICE(Structure):
    _fields_ = [
            ('ComDeviceType', WORD),
            ('PortNumber', WORD),
            ('CpuNumber', WORD),
            ('NetworkNumber', WORD),
            ('StationNumber', WORD),
            ('UnitNumber', WORD),
            ('IPAddress', c_char_p),
            ('Timeout', DWORD),
            ]

def processRc(rc, source):
    if rc == MP_SUCCESS:
        logging.debug('%s succeed', source)
    else:
        logging.debug('%s failed', source)
        raise Exception("Error number: %s" % hex(rc))


def YMC_OpenController(lpComDevice, phController):
    rc = ymc.ymcOpenController(lpComDevice, phController)
    processRc(rc, "ymcOpenController")

def YMC_CloseController(hController):
    rc = ymc.ymcCloseController(hController)
    processRc(rc, "ymcCloseController")
  
def YMC_GetRegisterDataHandle(pRegisterName, phRegisterData):
    rc = ymc.ymcGetRegisterDataHandle(pRegisterName, phRegisterData)
    processRc(rc, "ymcGetRegisterDataHandle")


def YMC_SetRegisterData(hRegisterData, RegisterDataNumber, pRegisterData):
    rc = ymc.ymcSetRegisterData(hRegisterData, RegisterDataNumber, pRegisterData)
    processRc(rc, "ymcSetRegisterData")
    
def YMC_GetRegisterData(hRegisterData, RegisterDataNumber, pRegisterData, pReadDataNumber):
    rc = ymc.ymcGetRegisterData(hRegisterData, RegisterDataNumber, pRegisterData, pReadDataNumber)
    processRc(rc, "ymcGetRegisterData")

def YMC_SetAPITimeoutValue(TimeoutValue):
    rc = ymc.ymcSetAPITimeoutValue(TimeoutValue)
    processRc(rc, "ymcSetAPITimeoutValue")

if __name__ == '__main__':
    ComDevice = COMMUNICATION_DEVICE(4, 1, 1, 0, 0, 0, None, 10000)
    Controller = DWORD()
    YMC_OpenController(byref(ComDevice), byref(Controller))
    logging.info("YMC_OpenController: %s", Controller)

    TimeoutValue = LONG(30000)
    YMC_SetAPITimeoutValue(TimeoutValue)
    
    RegisterName = "MW00010"
    hRegisterData = DWORD()
    YMC_GetRegisterDataHandle(c_char_p(RegisterName), byref(hRegisterData))
    logging.info("YMC_GetRegisterDataHandle: %s", hRegisterData)

    pReadDataNumber = DWORD()
    RegisterDataNumber = DWORD(3)
    pRegisterData1 = (WORD * 3)(1, 2, 3)     #for WORD type
    pRegisterData2 = (DWORD * 1)()    #for LONG type and FLOAT type
#     YMC_GetRegisterData(hRegisterData, 1, byref(pRegisterData1), byref(pReadDataNumber))
#     logging.info("YMC_GetRegisterData: %s, %s", pRegisterData1, pReadDataNumber)


    YMC_SetRegisterData(hRegisterData, RegisterDataNumber, cast(pRegisterData1, POINTER(WORD)))
    logging.info("YMC_SetRegisterData: %s", pRegisterData1)

    YMC_CloseController(Controller)
