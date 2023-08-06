import unittest
import sys
import os
import shutil

import m1com
import ctypes
import time
import pandas as pd
from datetime import datetime
from numpy import datetime64, timedelta64

def assertNotBytes(test, methodReturn):

    test.assertNotEqual(type(methodReturn), bytes)

    if hasattr(methodReturn, '_fields_'):
        for attribute in methodReturn._fields_:
            assertType = type(getattr(methodReturn, attribute[0]))
            test.assertNotEqual(assertType, bytes)
    elif type(methodReturn) != int:
        if type(methodReturn) == list:
            for listItem in methodReturn:
                assertNotBytes(test, listItem)
        elif type(methodReturn) == dict:
            for key in methodReturn.keys():
                assertNotBytes(test, methodReturn[key])
        elif type(methodReturn) == str:
            pass
        elif type(methodReturn) == bool:
            pass
        else:
            for attribute in list(dir(methodReturn)):
                if not attribute.startswith('__'):
                    assertType = type(getattr(methodReturn, attribute))
                    test.assertNotEqual(assertType, bytes)

def sviAppInstall():

    # Connect to controller
    mh = m1com.M1Controller(ip=ipAddress)
    mh.connect(timeout=3000)

    # First check if the test application is still running
    application = m1com.M1Application('SVIWRITE', mh)
    error = None
    try:
        application.getState()
    except Exception as e:
        error = e.value

    # Expects that the application.getState() function caused this error since it shouldn't be installed on the target
    if error != 'pyCom Error: Could not get information about application from target Controller['+ipAddress+']!':
        raise RuntimeError("Error when installing test applications, if they are still running, uninstall them!")

    # Determine current directory
    curDir = os.path.dirname(os.path.abspath(__file__))

    # Copy test application to bachmann
    mh.copyToTarget(curDir + '/unittestFiles/sviwrite.m', '/cfc0/app/sviwrite.m')

    # Make a copy of the mconfig.ini
    mh.copyFromTarget('/cfc0/mconfig.ini', curDir + '/unittestFiles/mconfigBackup.ini')
    shutil.copyfile(curDir + '/unittestFiles/mconfigBackup.ini', curDir + '/unittestFiles/mconfigSVIWrite.ini')

    # Add application to mconfig.ini
    f = open(curDir + '/unittestFiles/mconfigSVIWrite.ini', 'a')
    f.write("[SVIWRITE]\n")
    f.write("(BaseParms)\n")
    f.write("  Partition = 2\n")
    f.write("  DebugMode = 0x0\n")
    f.write("  Priority = 130\n")
    f.write("  ModuleIndex = 0\n")
    f.write("  ModulePath = app/\n")
    f.write("  ModuleName = sviwrite.m\n")
    f.write("(ControlTask)\n")
    f.write("  CycleTime = 1000.000000\n")
    f.write("  Priority = 90\n")
    f.write("  WatchdogRatio = 0\n")
    f.write("  TimeBase = Tick\n")
    f.close()

    # Remove old mconfig.ini from target, copy the new mconfig.ini and reboot
    mh.remove('/cfc0/mconfig.ini')
    mh.copyToTarget(curDir + '/unittestFiles/mconfigSVIWrite.ini', '/cfc0/mconfig.ini')
    mh.reboot()
    mh.disconnect()
    time.sleep(30)

def sviAppReset():

    # Connect to controller
    mh = m1com.M1Controller(ip=ipAddress)
    mh.connect(timeout=3000)

    # Reset and restart the test application
    application = m1com.M1Application('SVIWRITE', mh)

    application.reset()
    if(application.getState() != 'RES_S_RUN'):
        print(application.getState())
        raise RuntimeError("Error when resetting test application!")

    # Disconnect from the controller
    mh.disconnect()

def sviAppRemove():

    # Connect to controller
    mh = m1com.M1Controller(ip=ipAddress)
    mh.connect(timeout=3000)

    # Determine current directory
    curDir = os.path.dirname(os.path.abspath(__file__))

    # Remove application and mconfig.ini from target, copy back the original mconfig.ini and reboot
    mh.remove('/cfc0/app/sviwrite.m')
    mh.remove('/cfc0/mconfig.ini')
    mh.copyToTarget(curDir + '/unittestFiles/mconfigBackup.ini', '/cfc0/mconfig.ini')
    mh.reboot()
    mh.disconnect()
    os.remove(curDir + '/unittestFiles/mconfigBackup.ini')
    os.remove(curDir + '/unittestFiles/mconfigSVIWrite.ini')
    time.sleep(20)

class Test_PyComException(unittest.TestCase):
    def test_with_traceback(self):
        exception = m1com.PyComException('PyComException Test')

        self.assertEqual(exception.value, 'PyComException Test')
        assertNotBytes(self, exception)

        tb = sys.exc_info()[2]
        exception = m1com.PyComException('PyComException Test').with_traceback(tb)

        self.assertEqual(exception.value, 'PyComException Test')
        assertNotBytes(self, exception)

        try:
            raise m1com.PyComException('PyComException Test')
        except:
            tb = sys.exc_info()[2]
            exception = m1com.PyComException('PyComException Test').with_traceback(tb)

        self.assertEqual(exception.value, 'PyComException Test')
        assertNotBytes(self, exception)

        testedMethods.append('PyComException.with_traceback')

class Test_PyComTypeException(unittest.TestCase):
    def test_with_traceback(self):
        exception = m1com.PyComTypeException('PyComTypeException Test')

        self.assertEqual(exception.value, 'PyComTypeException Test')
        assertNotBytes(self, exception)

        tb = sys.exc_info()[2]
        exception = m1com.PyComTypeException('PyComTypeException Test').with_traceback(tb)

        self.assertEqual(exception.value, 'PyComTypeException Test')
        assertNotBytes(self, exception)

        try:
            raise m1com.PyComTypeException('PyComTypeException Test')
        except:
            tb = sys.exc_info()[2]
            exception = m1com.PyComTypeException('PyComTypeException Test').with_traceback(tb)

        self.assertEqual(exception.value, 'PyComTypeException Test')
        assertNotBytes(self, exception)

        testedMethods.append('PyComTypeException.with_traceback')

class Test_PyCom(unittest.TestCase):
    def test_getDllVersion(self):
        dll = m1com.PyCom()
        dllVersion = dll.getDllVersion()

        version = ctypes.create_string_buffer(40)
        dll.M1C_GetVersion(version, 40)

        self.assertEqual(dllVersion, version.value.decode())
        assertNotBytes(self, dllVersion)

        testedMethods.append('PyCom.getDllVersion')

    def test_getDllBits(self):
        dll = m1com.PyCom()
        dllBits = dll.getDllBits()

        if sys.maxsize > 2**32: # 64bit
            self.assertEqual(dllBits, '64bit')
        else:
            self.assertEqual(dllBits, '32bit')
        assertNotBytes(self, dllBits)

        testedMethods.append('PyCom.getDllBits')

class Test_M1Controller(unittest.TestCase):
    def test_getCtrlHandle(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.getCtrlHandle(), mh._ctrlHandle)
        assertNotBytes(self, mh.getCtrlHandle())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getCtrlHandle')

    def test_connect(self):
        mh = m1com.M1Controller(ip=ipAddress)

        mh.connect(timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        mh.connect(protocol='TCP', timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None, msg="Connect with protocol TCP failed!")
        self.assertEqual(mh.disconnect(), 0)

        mh.connect(protocol='QSOAP', timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None, msg="Connect with protocol QSOAP failed!")
        self.assertEqual(mh.disconnect(), 0)

        mh.connect(protocol='UDP', timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None, msg="Connect with protocol UDP failed!")
        self.assertEqual(mh.disconnect(), 0)

        #mh.connect(protocol='SSL', timeout=3000)
        #self.assertNotEqual(mh._ctrlHandle, None, msg="Connect with protocol SSL failed!")
        #self.assertEqual(mh.disconnect(), 0)

        crtFile = 'C:/Users/COEK/Documents/XCA Database/coek.p12'
        mh.connect(protocol='SSL', clientCert=crtFile, clientCertPassword='bachmann', timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None, msg="Connect with protocol SSL and client certificate failed!")
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.connect')

    def test_getSessionLiveTime(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertGreaterEqual(mh.getSessionLiveTime(), 0)
        assertNotBytes(self, mh.getSessionLiveTime())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getSessionLiveTime')

    def test_getLoginInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        loginInfo = mh.getLoginInfo()

        self.assertEqual(type(loginInfo), dict)
        assertNotBytes(self, loginInfo)
        self.assertGreaterEqual(loginInfo['SecurityLevel'], 0)
        self.assertLessEqual(loginInfo['SecurityLevel'], 4)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getLoginInfo')

    def test_renewConnection(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.renewConnection(), None)
        assertNotBytes(self, mh.renewConnection())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.renewConnection')

    def test_getNumberofSwModules(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertGreaterEqual(mh.getNumberofSwModules(), 8)
        assertNotBytes(self, mh.getNumberofSwModules())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getNumberofSwModules')

    def test_getSwModuleByName(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = mh.getSwModuleByName('RES')

        self.assertEqual(str(type(swModule)), "<class 'm1com._M1SwModule'>")
        self.assertEqual(swModule.name, 'RES')
        assertNotBytes(self, swModule)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getSwModuleByName')

    def test_getListofSwModules(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        listSWmodules = mh.getListofSwModules()

        self.assertEqual(type(listSWmodules), dict)
        self.assertEqual(len(listSWmodules), mh.getNumberofSwModules())
        assertNotBytes(self, listSWmodules)
        self.assertEqual(str(type(listSWmodules['RES'])), "<class 'm1com._M1SwModule'>")
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getListofSwModules')

    def test_getListofHwModules(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        listHWModules = mh.getListofHwModules()
        lastHwModuleNb = listHWModules[-1]['CardNb']

        self.assertEqual(type(listHWModules), list)
        self.assertGreater(lastHwModuleNb, 0)
        assertNotBytes(self, mh.getListofHwModules())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getListofHwModules')

    def test_getDrvId(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']

        self.assertGreater(mh.getDrvId(lastHwModuleNb), 0)
        assertNotBytes(self, mh.getDrvId(lastHwModuleNb))
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getDrvId')

    def test_getCardInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']
        cardInfo = mh.getCardInfo(lastHwModuleNb)

        self.assertEqual(type(cardInfo), dict)
        self.assertEqual(cardInfo['CardNb'], lastHwModuleNb)
        assertNotBytes(self, cardInfo)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getCardInfo')

    def test_getCardInfoExt(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']

        self.assertEqual(mh.getCardInfoExt(lastHwModuleNb)['CardNb'], lastHwModuleNb)
        assertNotBytes(self, mh.getCardInfoExt(lastHwModuleNb))
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getCardInfoExt')

    def test_copyFromTarget(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.copyFromTarget('/cfc0/mconfig.ini', 'localCopyMconfig.ini'), None)
        self.assertEqual(mh.disconnect(), 0)
        self.assertTrue(os.path.isfile('localCopyMconfig.ini'))
        os.remove('localCopyMconfig.ini')

        testedMethods.append('M1Controller.copyFromTarget')

    def test_copyToTarget(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        f = open('test_copyToTarget.txt', 'w')
        f.write("Test for mh.copyToTarget('test_copyToTarget.txt', '/cfc0/test_copyToTarget.txt')")
        f.close()

        self.assertEqual(mh.copyToTarget('test_copyToTarget.txt', '/cfc0/test_copyToTarget.txt'), None)
        self.assertEqual(mh.disconnect(), 0)

        os.remove('test_copyToTarget.txt')

        testedMethods.append('M1Controller.copyToTarget')

    def test_copyRemote(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.copyRemote('/cfc0/mconfig.ini', '/cfc0/test_copyRemoteOfMconfig.txt'), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.copyRemote')

    def test_remove(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.remove('/cfc0/test_copyRemoteOfMconfig.txt'), None)
        self.assertEqual(mh.remove('/cfc0/test_copyToTarget.txt'), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.remove')

    def test_listDirectory(self):

        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        dirContent = mh.listDirectory("/cfc0/")

        foundMconfigIni = False
        for item in dirContent:
            if "mconfig" in dirContent:
                foundMconfigIni = True

        # Currently fails....
        self.assertTrue(foundMconfigIni, msg="mconfig.ini not found using listDirectory function")

        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.listDirectory')

    def test_resetAll(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            self.assertEqual(mh.resetAll(), None)
            self.assertEqual(mh.reboot(), None)
            self.assertEqual(mh.disconnect(), 0)
            time.sleep(20)

            testedMethods.append('M1Controller.resetAll')

    def test_reboot(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            self.assertEqual(mh.reboot(), None)
            self.assertEqual(mh.disconnect(), 0)
            time.sleep(20)

            testedMethods.append('M1Controller.reboot')

    def test_disconnect(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.disconnect(), 0)
        self.assertEqual(mh._ctrlHandle, None)

        testedMethods.append('M1Controller.disconnect')

    def test_getConnectionState(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.getConnectionState(), 'ONLINE')
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getConnectionState')

    def test_getTargetState(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.getTargetState()['appState'], 'RES_S_RUN')
        self.assertGreater(mh.getTargetState()['rebootCount'], 0)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getTargetState')

    def test_sendCall(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            self.assertEqual(str(mh.sendCall('MOD', 134, ctypes.c_int32(0), ctypes.c_int32(0), timeout=3000, version=2)), 'c_long(0)')
            self.assertEqual(mh.disconnect(), 0)
            time.sleep(20)

            testedMethods.append('M1Controller.sendCall')

    def test_getsetUintParam(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        keys = ['M1C_PROXY_USED', 'M1C_PROXY_PORT', 'M1C_QSOAP_PORT', 'M1C_IGNORE_SERVER_CERT', 'M1C_COUNT_SOCKETS',
                'M1C_IGNORE_SERVER_CERT_CN', 'M1C_LOGIN2_USER_PARAM']
        for key in keys:
            original = mh.getUintParam(key)
            mh.setUintParam(key=key, value=1)
            self.assertEqual(1, mh.getUintParam(key))
            mh.setUintParam(key=key, value=original)
            self.assertEqual(original, mh.getUintParam(key))

        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.setUintParam')
        testedMethods.append('M1Controller.getUintParam')

    def test_getsetStringParam(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        keys = ['M1C_PROXY_HOST', 'M1C_PROXY_USERNAME', 'M1C_PROXY_PASSWD', 'M1C_QSOAP_PATH', 'M1C_VHD_SESSIONNAME']
        for key in keys:
            original = mh.getStringParam(key)
            mh.setStringParam(key=key, value='test')
            self.assertEqual('test', mh.getStringParam(key))
            mh.setStringParam(key=key, value=original)
            self.assertEqual(original, mh.getStringParam(key))

        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.setStringParam')
        testedMethods.append('M1Controller.getStringParam')

    def test_getMaxCallSize(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(type(mh.getMaxCallSize()), int)
        self.assertIn(mh.getMaxCallSize(), [2004, 4052, 8148, 16340])
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getMaxCallSize')

    def test_getErrorInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        errorCodes = [  m1com.M1C_E_MEM_ALLOC, m1com.M1C_E_INVALID_PARTNER, m1com.M1C_E_WSA_INIT, m1com.M1C_E_ENET_DOWN,
                        m1com.M1C_E_ADDRESS_SUPPORT, m1com.M1C_E_SOCKET_PROGRESS, m1com.M1C_E_NOMORE_SOCKETS, m1com.M1C_E_PROTOCOL,
                        m1com.M1C_E_SOCKET, m1com.M1C_E_SOCKET_ACCESS ]

        for errorCode in errorCodes:
            ret = mh.getErrorInfo(errorCode)
            self.assertEqual(type(ret), dict)
            self.assertNotEqual(ret['errorSrc'], '')
            self.assertNotEqual(ret['errorMsg'], '')

        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getErrorInfo')

    def test_getNetworkInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Get controller network information
        networkInfo = mh.getNetworkInfo("eth0")
        self.assertEqual(type(networkInfo), dict)
        assertNotBytes(self, networkInfo)

        # Check whether disconnect was successful
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getNetworkInfo')
    
    def test_setIP(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Set controller IP
        mh.setIP("eth0", "192.168.1.164", "255.255.255.0")

        # Get new controller IP

        # Reset controller IP

        # Get new controller IP

        # Check whether disconnect was successful
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.setIP')

    def test_setDateTime(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Read RES/Time/TimeLocal variable
        swModule = m1com._M1SwModule('RES', mh)
        sviTimeLocal = m1com._SVIVariable('RES/Time/TimeLocal', swModule)
        timeLocalOld = sviTimeLocal.read()

        # Remove location from timestamp
        stringFormat = "YYYY-MM-DD HH:MM:SS"
        stringFormatLen = len(stringFormat)
        timeLocalOld = timeLocalOld[0:stringFormatLen]

        # Convert to datetime string
        timeLocalOld = pd.to_datetime(pd.Timestamp(timeLocalOld)).strftime('%Y-%m-%d_%H-%M-%S')

        # Time to set
        timeLocalSet = "2022-01-01_12-00-00"

        # Set controller time
        mh.setDateTime(timeLocalSet)

        # Get new controller time
        timeLocalNew = sviTimeLocal.read()

        # Remove location from timestamp
        timeLocalNew = timeLocalNew[0:stringFormatLen]

        # Convert to datetime
        timeLocalSet = datetime64(datetime.strptime(timeLocalSet, '%Y-%m-%d_%H-%M-%S'))
        timeLocalNew = datetime64(pd.to_datetime(pd.Timestamp(timeLocalNew)))

        # Check whether time is within a diff of 3 seconds
        timeLocalDiff = timeLocalSet - timeLocalNew
        self.assertLessEqual(timeLocalDiff, timedelta64(3, 's'))

        # Set back to original time
        mh.setDateTime(timeLocalOld)

        # Get new controller time
        timeLocalNew = sviTimeLocal.read()

        # Remove location from timestamp
        timeLocalNew = timeLocalNew[0:stringFormatLen]

        # Convert to datetime
        timeLocalOld = datetime64(datetime.strptime(timeLocalOld, '%Y-%m-%d_%H-%M-%S'))
        timeLocalNew = datetime64(pd.to_datetime(pd.Timestamp(timeLocalNew)))

        # Check whether time is within a diff of 3 seconds
        timeLocalDiff = timeLocalOld - timeLocalNew
        self.assertLessEqual(timeLocalDiff, timedelta64(3, 's'))

        # Check whether disconnect was successful
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.setDateTime')

    def test_syncDateTime(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Read RES/Time/TimeLocal variable
        swModule = m1com._M1SwModule('RES', mh)
        sviTimeLocal = m1com._SVIVariable('RES/Time/TimeLocal', swModule)

        # Time to set
        timeLocalSet = "2022-01-01_12-00-00"

        # Set controller time
        mh.setDateTime(timeLocalSet)

        # Get new controller time
        timeLocalNew = sviTimeLocal.read()

        # Remove location from timestamp
        stringFormat = "YYYY-MM-DD HH:MM:SS"
        stringFormatLen = len(stringFormat)
        timeLocalNew = timeLocalNew[0:stringFormatLen]

        # Convert to datetime
        timeLocalSet = datetime64(datetime.strptime(timeLocalSet, '%Y-%m-%d_%H-%M-%S'))
        timeLocalNew = datetime64(pd.to_datetime(pd.Timestamp(timeLocalNew)))

        # Check whether time is within a diff of 3 seconds
        timeLocalDiff = timeLocalSet - timeLocalNew
        self.assertLessEqual(timeLocalDiff, timedelta64(3, 's'))

        # Sync with PC time
        mh.syncDateTime()

        # Get new controller time
        timeLocalNew = sviTimeLocal.read()

        # Get PC time
        timeLocalPC = datetime.now()

        # Remove location from timestamp
        timeLocalNew = timeLocalNew[0:stringFormatLen]

        # Convert to datetime
        timeLocalPC = datetime64(timeLocalPC)
        timeLocalNew = datetime64(pd.to_datetime(pd.Timestamp(timeLocalNew)))

        # Check whether time is within a diff of 3 seconds
        timeLocalDiff = timeLocalPC - timeLocalNew
        self.assertLessEqual(timeLocalDiff, timedelta64(3, 's'))

        # Check whether disconnect was successful
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.syncDateTime')

class Test_M1Application(unittest.TestCase):
    def test_deinit(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            application = m1com.M1Application('SVIWRITE', mh)
            self.assertEqual(application.getState(), 'RES_S_RUN')
            self.assertEqual(application.deinit(), None)
            time.sleep(3)

            error = None
            try:
                application.getState()
            except Exception as e:
                error = e.value

            # Expects that the application.getState() function caused this error since it shouldn't be installed on the target
            self.assertEqual(error, 'pyCom Error: Could not get information about application from target Controller['+ipAddress+']!')
            self.assertEqual(mh.reboot(), None)
            self.assertEqual(mh.disconnect(), 0)
            time.sleep(20)

            testedMethods.append('M1Application.deinit')

    def test_reset(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('SVIWRITE', mh)
        sviVariable = m1com._SVIVariable('SVIWRITE/boolVar', swModule)

        self.assertEqual(sviVariable.read(), False)
        self.assertEqual(sviVariable.write(True), None)
        self.assertEqual(sviVariable.read(), True)

        application = m1com.M1Application('SVIWRITE', mh)

        self.assertEqual(application.reset(), None)
        self.assertEqual(application.getState(), 'RES_S_RUN')

        swModule = m1com._M1SwModule('SVIWRITE', mh)
        sviVariable = m1com._SVIVariable('SVIWRITE/boolVar', swModule)

        self.assertEqual(sviVariable.read(), False)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Application.reset')

    def test_stopstart(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        application = m1com.M1Application('SVIWRITE', mh)
        self.assertEqual(application.getState(), 'RES_S_RUN')
        self.assertEqual(application.stop(), None)
        self.assertEqual(application.getState(), 'RES_S_STOP')
        self.assertEqual(application.start(), None)
        self.assertEqual(application.getState(), 'RES_S_RUN')

        testedMethods.append('M1Application.stop')
        testedMethods.append('M1Application.start')

    def test_getInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        application = m1com.M1Application('SVIWRITE', mh)
        appInfo = application.getInfo()
        self.assertEqual(type(appInfo), dict)
        assertNotBytes(self, appInfo)

        testedMethods.append('M1Application.getInfo')

    def test_getState(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        application = m1com.M1Application('SVIWRITE', mh)
        appState = application.getState()
        self.assertEqual(type(appState), str)
        self.assertEqual(appState, 'RES_S_RUN')

        testedMethods.append('M1Application.getState')

class Test_M1SVIObserver(unittest.TestCase):
    def test_detach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        self.assertNotEqual(sviObserver._obsHandle, None)
        self.assertEqual(sviObserver.detach(), None)

        self.assertEqual(sviObserver._obsHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1SVIObserver.detach')

    def test_getObsHandle(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)

        self.assertEqual(sviObserver.getObsHandle(), sviObserver._obsHandle)
        self.assertNotEqual(sviObserver._obsHandle, None)
        self.assertEqual(sviObserver.detach(), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1SVIObserver.getObsHandle')

    def test_attach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        self.assertEqual(sviObserver.getObsHandle(), sviObserver._obsHandle)
        self.assertNotEqual(sviObserver._obsHandle, None)
        self.assertEqual(len(sviObserver._sviHandles), 4)
        for i in range(4):
            self.assertEqual(type(sviObserver._sviHandles[i]), int)
        self.assertEqual(len(sviObserver._sviInfos), 4)
        for i in range(4):
            self.assertEqual(str(type(sviObserver._sviInfos[i])), "<class 'm1com.VARIABLE_INFO'>")
        self.assertEqual(len(sviObserver._sviValues), 4)
        self.assertEqual(str(type(sviObserver._sviValues[0])), "<class 'ctypes.c_ulong'>")
        self.assertEqual(str(type(sviObserver._sviValues[1])), "<class 'ctypes.c_ulong'>")
        self.assertEqual(str(type(sviObserver._sviValues[2])), "<class 'ctypes.c_ulong'>")
        self.assertEqual(str(type(sviObserver._sviValues[3])), "<class 'm1com.c_char_Array_20'>")
        self.assertNotEqual(sviObserver._indicesChanged, None)
        self.assertEqual(sviObserver.detach(), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1SVIObserver.attach')

    def test_update(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        self.assertEqual(sviObserver.update(), 4)
        time.sleep(1)
        self.assertEqual(sviObserver.update(), 2)
        self.assertEqual(sviObserver.detach(), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1SVIObserver.update')

    def test_getVariables(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        self.assertEqual(len(sviObserver.getVariables(updatedOnly=True)), 4)
        assertNotBytes(self, sviObserver.getVariables(updatedOnly=True))
        time.sleep(1)
        for i in range(5):
            self.assertEqual(len(sviObserver.getVariables(updatedOnly=True)), 2)
            assertNotBytes(self, sviObserver.getVariables(updatedOnly=True))
            time.sleep(1)
        self.assertEqual(sviObserver.detach(), None)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        self.assertEqual(len(sviObserver.getVariables(updatedOnly=False)), 4)
        assertNotBytes(self, sviObserver.getVariables(updatedOnly=False))
        time.sleep(1)
        for i in range(5):
            self.assertEqual(len(sviObserver.getVariables(updatedOnly=False)), 4)
            assertNotBytes(self, sviObserver.getVariables(updatedOnly=False))
            time.sleep(1)
        self.assertEqual(sviObserver.detach(), None)
        self.assertEqual(mh.disconnect(), 0)

        # Connect to the target
        mh.connect(timeout=3000)

        # Reset the svi test application
        sviAppReset()

        # Perform the read tests
        readVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                            'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                            'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                            'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                            'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                            'SVIWRITE/ustringVar': str,
                            'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                            'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                            'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                            'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                            'SVIWRITE/stringArray': [str], 'SVIWRITE/ustringArray': [str], 'SVIWRITE/mixedVar': [int]}

        readValues =     [False, False, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, "O", "O", "OOOO", "OOOO",
                         [False, False, False], [False, False, False], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                         [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                         ["OOOO", "OOOO", "OOOO"], ["OOOO", "OOOO", "OOOO"], [0]*52]

        Error = False
        ErrorMsg = ''
        try:
            # Setup the observer
            sviObserver = m1com.M1SVIObserver(list(readVariables.keys()), mh)
            obtainedVariables = sviObserver.getVariables(updatedOnly=False)

            j = 0
            for key in readVariables:
                sviValue = obtainedVariables[key]
                if type(readValues[j]) == list:
                    for i in range(len(readValues[j])):
                        self.assertEqual(type(sviValue[i]), readVariables[key][0], msg='for ' + key + '=' + str(readValues[j][i]))
                        if type(sviValue[i]) == float:
                            self.assertAlmostEqual(sviValue[i], readValues[j][i], msg='for ' + key + '=' + str(readValues[j][i]))
                        else:
                            self.assertEqual(sviValue[i], readValues[j][i], msg='for ' + key + '=' + str(readValues[j][i]))
                else:
                    self.assertEqual(type(sviValue), readVariables[key], msg='for ' + key + '=' + str(readValues[j]))
                    if type(sviValue) == float:
                        self.assertAlmostEqual(sviValue, readValues[j], msg='for ' + key + '=' + str(readValues[j]))
                    else:
                        self.assertEqual(sviValue, readValues[j], msg='for ' + key + '=' + str(readValues[j]))
                j = j + 1

            # Setup the observer
            sviObserver = m1com.M1SVIObserver(list(readVariables.keys()), mh)
            obtainedVariables = sviObserver.getVariables(updatedOnly=True)

            j = 0
            for key in readVariables:
                sviValue = obtainedVariables[key]
                if type(readValues[j]) == list:
                    for i in range(len(readValues[j])):
                        self.assertEqual(type(sviValue[i]), readVariables[key][0], msg='for ' + key + '=' + str(readValues[j][i]))
                        if type(sviValue[i]) == float:
                            self.assertAlmostEqual(sviValue[i], readValues[j][i], msg='for ' + key + '=' + str(readValues[j][i]))
                        else:
                            self.assertEqual(sviValue[i], readValues[j][i], msg='for ' + key + '=' + str(readValues[j][i]))
                else:
                    self.assertEqual(type(sviValue), readVariables[key], msg='for ' + key + '=' + str(readValues[j]))
                    if type(sviValue) == float:
                        self.assertAlmostEqual(sviValue, readValues[j], msg='for ' + key + '=' + str(readValues[j]))
                    else:
                        self.assertEqual(sviValue, readValues[j], msg='for ' + key + '=' + str(readValues[j]))
                j = j + 1

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('M1SVIObserver.getVariables')

    def test_reset(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        for i in range(5):
            self.assertEqual(len(sviObserver.getVariables(updatedOnly=True)), 4)
            assertNotBytes(self, sviObserver.getVariables(updatedOnly=True))
            self.assertEqual(sviObserver.reset(), None)
            time.sleep(1)
        self.assertEqual(sviObserver.detach(), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1SVIObserver.reset')

class Test_M1SVIReader(unittest.TestCase):
    def test_detach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Reset the svi test application
        sviAppReset()

        Error = False
        ErrorMsg = ''
        try:
            readVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                            'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                            'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                            'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                            'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                            'SVIWRITE/ustringVar': str,
                            'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                            'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                            'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                            'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                            'SVIWRITE/stringArray': [str], 'SVIWRITE/ustringArray': [str], 'SVIWRITE/mixedVar': [int]}

            # Setup the observer
            sviReader = m1com.M1SVIReader(list(readVariables.keys()), mh)

            self.assertNotEqual(sviReader._sviHandles, None)
            self.assertEqual(sviReader.detach(), None)

            self.assertEqual(sviReader._sviHandles, None)

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('M1SVIReader.detach')

    def test_getSVIHandles(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Reset the svi test application
        sviAppReset()

        Error = False
        ErrorMsg = ''
        try:
            readVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                            'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                            'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                            'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                            'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                            'SVIWRITE/ustringVar': str,
                            'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                            'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                            'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                            'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                            'SVIWRITE/stringArray': [str], 'SVIWRITE/ustringArray': [str], 'SVIWRITE/mixedVar': [int]}

            # Setup the observer
            sviReader = m1com.M1SVIReader(list(readVariables.keys()), mh)

            self.assertNotEqual(sviReader.getSVIHandles(), None)
            self.assertEqual(type(sviReader.getSVIHandles()), list)
            self.assertEqual(sviReader.getSVIHandles(), sviReader._sviHandles)
            for sviHandle in sviReader.getSVIHandles():
                self.assertGreater(sviHandle, 0)
            self.assertEqual(sviReader.detach(), None)
            self.assertEqual(sviReader._sviHandles, None)

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('M1SVIReader.getSVIHandles')

    def test_attach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Reset the svi test application
        sviAppReset()

        Error = False
        ErrorMsg = ''
        try:
            readVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                            'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                            'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                            'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                            'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                            'SVIWRITE/ustringVar': str,
                            'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                            'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                            'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                            'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                            'SVIWRITE/stringArray': [str], 'SVIWRITE/ustringArray': [str], 'SVIWRITE/mixedVar': [int]}

            # Setup the observer
            sviReader = m1com.M1SVIReader(list(readVariables.keys()), mh)

            self.assertEqual(sviReader.getSVIHandles(), sviReader._sviHandles)
            self.assertNotEqual(sviReader.getSVIHandles(), None)
            self.assertEqual(len(sviReader._sviHandles), len(list(readVariables.keys())))
            for i in range(len(list(readVariables.keys()))):
                self.assertEqual(type(sviReader._sviHandles[i]), int)
            self.assertEqual(len(sviReader._sviInfos), len(list(readVariables.keys())))
            for i in range(len(list(readVariables.keys()))):
                self.assertEqual(str(type(sviReader._sviInfos[i])), "<class 'm1com.VARIABLE_INFO'>")
            self.assertEqual(len(sviReader._sviValues), len(list(readVariables.keys())))
            self.assertEqual(sviReader.detach(), None)

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('M1SVIReader.attach')

    def test_getVariables(self):
        # Connect to the target
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Reset the svi test application
        sviAppReset()

        # Perform the read tests
        readVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                            'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                            'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                            'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                            'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                            'SVIWRITE/ustringVar': str,
                            'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                            'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                            'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                            'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                            'SVIWRITE/stringArray': [str], 'SVIWRITE/ustringArray': [str], 'SVIWRITE/mixedVar': [int]}

        readValues = [  [True,  True,  1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1.1, "A", "A", "ABCD", "ABCD",
                         [True, True, True], [True, True, True], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3],
                         [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1.1, 2.2, 3.3], [1.1, 2.2, 3.3],
                         ["ABCD", "EFGH", "IJKL"], ["ABCD", "EFGH", "IJKL"], [255]*52],

                        [False, False, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, "O", "O", "OOOO", "OOOO",
                         [False, False, False], [False, False, False], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                         [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                         ["OOOO", "OOOO", "OOOO"], ["OOOO", "OOOO", "OOOO"], [0]*52] ]

        # Setup the SVI writer and reader
        sviWriter = m1com.M1SVIWriter(list(readVariables.keys()), mh)
        sviReader = m1com.M1SVIReader(list(readVariables.keys()), mh)

        Error = False
        ErrorMsg = ''
        try:
            for i in range(len(readValues)):

                sviWriter.setVariables(readValues[i])
                obtainedVariables = sviReader.getVariables()

                j = 0
                for key in readVariables:
                    sviValue = obtainedVariables[j]
                    realValue = readValues[i][j]
                    if type(realValue) == list:
                        for k in range(len(realValue)):
                            self.assertEqual(type(sviValue[k]), readVariables[key][0], msg='for ' + key + '=' + str(realValue[k]))
                            if type(sviValue[k]) == float:
                                self.assertAlmostEqual(sviValue[k], realValue[k], msg='for ' + key + '=' + str(realValue[k]))
                            else:
                                self.assertEqual(sviValue[k], realValue[k], msg='for ' + key + '=' + str(realValue[k]))
                    else:
                        self.assertEqual(type(sviValue), readVariables[key], msg='for ' + key + '=' + str(realValue))
                        if type(sviValue) == float:
                            self.assertAlmostEqual(sviValue, realValue, msg='for ' + key + '=' + str(realValue))
                        else:
                            self.assertEqual(sviValue, realValue, msg='for ' + key + '=' + str(realValue))

                    j = j + 1

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('M1SVIReader.getVariables')

class Test_M1SVIWriter(unittest.TestCase):
    def test_detach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Reset the svi test application
        sviAppReset()

        Error = False
        ErrorMsg = ''
        try:
            writeVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                            'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                            'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                            'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                            'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                            'SVIWRITE/ustringVar': str,
                            'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                            'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                            'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                            'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                            'SVIWRITE/stringArray': [str], 'SVIWRITE/ustringArray': [str], 'SVIWRITE/mixedVar': [int]}

            # Setup the observer
            sviWriter = m1com.M1SVIWriter(list(writeVariables.keys()), mh)

            self.assertNotEqual(sviWriter._sviHandles, None)
            self.assertEqual(sviWriter.detach(), None)

            self.assertEqual(sviWriter._sviHandles, None)

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('M1SVIWriter.detach')

    def test_getSVIHandles(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Reset the svi test application
        sviAppReset()

        Error = False
        ErrorMsg = ''
        try:
            writeVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                            'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                            'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                            'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                            'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                            'SVIWRITE/ustringVar': str,
                            'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                            'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                            'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                            'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                            'SVIWRITE/stringArray': [str], 'SVIWRITE/ustringArray': [str], 'SVIWRITE/mixedVar': [int]}

            # Setup the observer
            sviWriter = m1com.M1SVIWriter(list(writeVariables.keys()), mh)

            self.assertNotEqual(sviWriter.getSVIHandles(), None)
            self.assertEqual(type(sviWriter.getSVIHandles()), list)
            self.assertEqual(sviWriter.getSVIHandles(), sviWriter._sviHandles)
            for sviHandle in sviWriter.getSVIHandles():
                self.assertGreater(sviHandle, 0)
            self.assertEqual(sviWriter.detach(), None)
            self.assertEqual(sviWriter._sviHandles, None)

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('M1SVIWriter.getSVIHandles')

    def test_attach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Reset the svi test application
        sviAppReset()

        Error = False
        ErrorMsg = ''
        try:
            writeVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                            'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                            'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                            'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                            'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                            'SVIWRITE/ustringVar': str,
                            'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                            'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                            'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                            'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                            'SVIWRITE/stringArray': [str], 'SVIWRITE/ustringArray': [str], 'SVIWRITE/mixedVar': [int]}

            # Setup the observer
            sviWriter = m1com.M1SVIWriter(list(writeVariables.keys()), mh)

            self.assertEqual(sviWriter.getSVIHandles(), sviWriter._sviHandles)
            self.assertNotEqual(sviWriter.getSVIHandles(), None)
            self.assertEqual(len(sviWriter._sviHandles), len(list(writeVariables.keys())))
            for i in range(len(list(writeVariables.keys()))):
                self.assertEqual(type(sviWriter._sviHandles[i]), int)
            self.assertEqual(len(sviWriter._sviInfos), len(list(writeVariables.keys())))
            for i in range(len(list(writeVariables.keys()))):
                self.assertEqual(str(type(sviWriter._sviInfos[i])), "<class 'm1com.VARIABLE_INFO'>")
            self.assertEqual(len(sviWriter._sviValues), len(list(writeVariables.keys())))
            self.assertEqual(sviWriter.detach(), None)

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('M1SVIWriter.attach')

    def test_setVariables(self):
        # Connect to the target
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Reset the svi test application
        sviAppReset()

        # Perform the read tests
        writeVariables = {  'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                            'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                            'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                            'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                            'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                            'SVIWRITE/ustringVar': str,
                            'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                            'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                            'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                            'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                            'SVIWRITE/stringArray': [str], 'SVIWRITE/ustringArray': [str], 'SVIWRITE/mixedVar': [int]}

        writeValues = [  [True,  True,  1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1.1, "A", "A", "ABCD", "ABCD",
                         [True, True, True], [True, True, True], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3],
                         [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1.1, 2.2, 3.3], [1.1, 2.2, 3.3],
                         ["ABCD", "EFGH", "IJKL"], ["ABCD", "EFGH", "IJKL"], [255]*52],

                         [False,  False,  255,
                          -128, 65535, -32768,
                          4294967295, -2147483648, 18446744073709551615,
                          -9223372036854775808, 0.0, 0.0,
                          "O", "O", "OOOO",
                          "OOOO",
                         [False, False, False], [False, False, False], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                         [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                         ["OOOO", "OOOO", "OOOO"], ["OOOO", "OOOO", "OOOO"], [0]*52],

                         [True,  True,  1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1.1, "A", "A", "ABCD", "ABCD",
                         [True, True, True], [True, True, True], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3],
                         [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1.1, 2.2, 3.3], [1.1, 2.2, 3.3],
                         ["ABCD", "EFGH", "IJKL"], ["ABCD", "EFGH", "IJKL"], [255]*52],

                        [False, False, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, "O", "O", "OOOO", "OOOO",
                         [False, False, False], [False, False, False], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                         [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                         ["OOOO", "OOOO", "OOOO"], ["OOOO", "OOOO", "OOOO"], [0]*52] ]

        # Setup the writer and observer
        sviWriter = m1com.M1SVIWriter(list(writeVariables.keys()), mh)
        sviObserver = m1com.M1SVIObserver(list(writeVariables.keys()), mh)

        Error = False
        ErrorMsg = ''
        try:
            for i in range(len(writeValues)):

                sviWriter.setVariables(writeValues[i])
                obtainedVariables = sviObserver.getVariables()

                j = 0
                for key in writeVariables:
                    sviValue = obtainedVariables[key]
                    realValue = writeValues[i][j]
                    if type(realValue) == list:
                        for k in range(len(realValue)):
                            self.assertEqual(type(sviValue[k]), writeVariables[key][0], msg='for ' + key + '=' + str(realValue[k]))
                            if type(sviValue[k]) == float:
                                self.assertAlmostEqual(sviValue[k], realValue[k], msg='for ' + key + '=' + str(realValue[k]))
                            else:
                                self.assertEqual(sviValue[k], realValue[k], msg='for ' + key + '=' + str(realValue[k]))
                    else:
                        self.assertEqual(type(sviValue), writeVariables[key], msg='for ' + key + '=' + str(realValue))
                        if type(sviValue) == float:
                            self.assertAlmostEqual(sviValue, realValue, msg='for ' + key + '=' + str(realValue))
                        else:
                            self.assertEqual(sviValue, realValue, msg='for ' + key + '=' + str(realValue))

                    j = j + 1

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('M1SVIWriter.setVariables')

class Test_M1TargetFinder(unittest.TestCase):
    def test_TargetBroadcastSmiPing(self):
        mt = m1com.M1TargetFinder()
        broadcastSmiPing = mt.TargetBroadcastSmiPing(timeout=3000)

        # Check if broadcastSmiPing returns something
        self.assertNotEqual(broadcastSmiPing, None)
        self.assertEqual(type(broadcastSmiPing), dict)

        # Check if broadcastSmiPing also finds the ip we are using
        ipFound = ''
        for target in broadcastSmiPing:
            if broadcastSmiPing[target]['hostAddr'] == ipAddress:
                ipFound = broadcastSmiPing[target]['hostAddr']

        self.assertEqual(ipFound, ipAddress)
        assertNotBytes(self, broadcastSmiPing)

        testedMethods.append('M1TargetFinder.TargetBroadcastSmiPing')

    def test_TargetSmiPing(self):
        mt = m1com.M1TargetFinder()
        smiPing = mt.TargetSmiPing(ip=ipAddress, timeout=3000)

        # Check if smiPing returns something
        self.assertNotEqual(smiPing, None)
        self.assertEqual(type(smiPing), dict)
        assertNotBytes(self, smiPing)

        testedMethods.append('M1TargetFinder.TargetSmiPing')

class Test_M1SwModule(unittest.TestCase):
    def test_attach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)

        self.assertEqual(swModule.attach(), None)
        self.assertNotEqual(swModule._modHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.attach')

    def test_detach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)

        self.assertEqual(swModule.detach(), None)
        self.assertEqual(swModule._modHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.detach')

    def test_getModHandle(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)

        self.assertEqual(swModule.getModHandle(), swModule._modHandle)
        self.assertNotEqual(swModule._modHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.getModHandle')

    def test_getNumberofSviVariables(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)

        self.assertGreater(swModule.getNumberofSviVariables(), 200)
        self.assertEqual(type(swModule.getNumberofSviVariables()), int)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.getNumberofSviVariables')

    def test_getListofSviVariables(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)

        listOfSviVariables = swModule.getListofSviVariables()

        self.assertEqual(type(listOfSviVariables), dict)
        assertNotBytes(self, listOfSviVariables)
        self.assertEqual(str(type(listOfSviVariables['RES/Time_s'])), "<class 'm1com._SVIVariable'>")
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.getListofSviVariables')

class Test_SVIVariable(unittest.TestCase):
    def test_attach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)

        self.assertEqual(sviVariable.attach(), None)
        self.assertNotEqual(sviVariable._varHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.attach')

    def test_detach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)

        self.assertEqual(sviVariable.detach(), None)
        self.assertEqual(sviVariable._varHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.detach')

    def test_getVarHandle(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)

        self.assertEqual(sviVariable.getVarHandle(), sviVariable._varHandle)
        self.assertNotEqual(sviVariable._varHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getVarHandle')

    def test_getVarInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        sviInfo = sviVariable.getVarInfo()

        self.assertEqual(sviInfo, m1com.ctypesInfo2dict(sviVariable._varInfo))
        self.assertEqual(type(sviInfo), dict)
        self.assertNotEqual(sviInfo, None)
        self.assertEqual(sviInfo['name'], 'RES/CPU/TempCelsius')
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getVarInfo')

    def test_updateVarInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        updateSviInfo = sviVariable.updateVarInfo()

        self.assertEqual(updateSviInfo, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.updateVarInfo')

    def test_read(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        sviValue = sviVariable.read()

        self.assertEqual(type(sviValue), int)
        self.assertGreaterEqual(sviValue, 20)
        self.assertLessEqual(sviValue, 100)

        swModule = m1com._M1SwModule('EHD', mh)
        sviVariable = m1com._SVIVariable('EHD/Type1/Entry1', swModule)
        sviValue = sviVariable.read()

        self.assertEqual(type(sviValue), list)
        self.assertEqual(min(sviValue), 0)
        self.assertGreaterEqual(max(sviValue), 0)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.read')

    def test_write(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)

        try:
            sviVariable.write(60)
        except m1com.PyComException as error:
            error = str(error.value)
            self.assertEqual(error, 'pyCom Error: Svi Variable[RES/CPU/TempCelsius] is not writable!')

        # Reset the svi test application
        sviAppReset()

        # Perform the write tests
        swModule = m1com._M1SwModule('SVIWRITE', mh)
        writeVariables = {  'boolVar': bool, 'bool8Var': bool, 'uInt8Var': int,
                            'sInt8Var': int, 'uInt16Var': int, 'sInt16Var': int,
                            'uInt32Var': int, 'sInt32Var': int, 'uInt64Var': int,
                            'sInt64Var': int, 'real32Var': float, 'real64Var': float,
                            'char8Var': str, 'char16Var': str, 'stringVar': str,
                            'ustringVar': str,
                            'boolArray': [bool], 'bool8Array': [bool], 'uInt8Array': [int],
                            'sInt8Array': [int], 'uInt16Array': [int], 'sInt16Array': [int],
                            'uInt32Array': [int], 'sInt32Array': [int], 'uInt64Array': [int],
                            'sInt64Array': [int], 'real32Array': [float], 'real64Array': [float],
                            'stringArray': [str], 'ustringArray': [str], 'mixedVar': ['mixed']}

        Error = False
        ErrorMsg = ''
        try:
            for key in writeVariables:
                sviVariable = m1com._SVIVariable('SVIWRITE/' + key, swModule)
                sviVariable2 = m1com._SVIVariable('SVIWRITE/' + key, swModule)
                if writeVariables[key] == bool:
                    value = [True, False]
                elif writeVariables[key] == int:
                    value = [1, 0]
                elif writeVariables[key] == float:
                    value = [1.1, 0.0]
                elif writeVariables[key] == str:
                    value = ['L', 'O']
                elif writeVariables[key] == [bool]:
                    value = [[True, True, True], [False, False, False]]
                elif writeVariables[key] == [int]:
                    value = [[1, 2, 3], [0, 0, 0]]
                elif writeVariables[key] == [float]:
                    value = [[1.1, 2.2, 3.3], [0.0, 0.0, 0.0]]
                elif writeVariables[key] == ['mixed']:
                    value = [[255]*52, [0]*52]
                elif writeVariables[key] == [str]:
                    value = [['ABCD', 'EFGH', 'IJKL'], ['OOOO', 'OOOO', 'OOOO']]
                else:
                    value = None
                    print('Unsupported type: ' + str(writeVariables[key]) + ' for ' + str(key))
                sviVariable.write(value[0])
                sviValue = sviVariable.read()
                sviValue2 = sviVariable2.read()
                if type(sviValue) == list:
                    for i in range(len(sviValue)):
                        if writeVariables[key][0] == 'mixed':
                            self.assertEqual(type(sviValue[i]), int, msg='for ' + key + '=' + str(value[0][i]))
                            self.assertEqual(type(sviValue2[i]), int, msg='for ' + key + '=' + str(value[0][i]))
                        else:
                            self.assertEqual(type(sviValue[i]), writeVariables[key][0], msg='for ' + key + '=' + str(value[0][i]))
                            self.assertEqual(type(sviValue2[i]), writeVariables[key][0], msg='for ' + key + '=' + str(value[0][i]))
                        if type(sviValue[i]) == float:
                            self.assertAlmostEqual(sviValue[i], value[0][i], msg='for ' + key + '=' + str(value[0][i]))
                            self.assertAlmostEqual(sviValue2[i], value[0][i], msg='for ' + key + '=' + str(value[0][i]))
                        else:
                            self.assertEqual(sviValue[i], value[0][i], msg='for ' + key + '=' + str(value[0][i]))
                            self.assertEqual(sviValue2[i], value[0][i], msg='for ' + key + '=' + str(value[0][i]))
                else:
                    self.assertEqual(type(sviValue), writeVariables[key], msg='for ' + key + '=' + str(value[0]))
                    self.assertEqual(type(sviValue2), writeVariables[key], msg='for ' + key + '=' + str(value[0]))
                    if type(sviValue) == float:
                        self.assertAlmostEqual(sviValue, value[0], msg='for ' + key + '=' + str(value[0]))
                        self.assertAlmostEqual(sviValue2, value[0], msg='for ' + key + '=' + str(value[0]))
                    else:
                        self.assertEqual(sviValue, value[0], msg='for ' + key + '=' + str(value[0]))
                        self.assertEqual(sviValue2, value[0], msg='for ' + key + '=' + str(value[0]))

                sviVariable.write(value[1])
                sviValue = sviVariable.read()
                sviValue2 = sviVariable2.read()
                if type(sviValue) == list:
                    for i in range(len(sviValue)):
                        if writeVariables[key][0] == 'mixed':
                            self.assertEqual(type(sviValue[i]), int, msg='for ' + key + '=' + str(value[1][i]))
                            self.assertEqual(type(sviValue2[i]), int, msg='for ' + key + '=' + str(value[1][i]))
                        else:
                            self.assertEqual(type(sviValue[i]), writeVariables[key][0], msg='for ' + key + '=' + str(value[1][i]))
                            self.assertEqual(type(sviValue2[i]), writeVariables[key][0], msg='for ' + key + '=' + str(value[1][i]))
                        self.assertEqual(sviValue[i], value[1][i], msg='for ' + key + '=' + str(value[1][i]))
                        self.assertEqual(sviValue2[i], value[1][i], msg='for ' + key + '=' + str(value[1][i]))
                else:
                    self.assertEqual(type(sviValue), writeVariables[key], msg='for ' + key + '=' + str(value[1]))
                    self.assertEqual(type(sviValue2), writeVariables[key], msg='for ' + key + '=' + str(value[1]))
                    self.assertEqual(sviValue, value[1], msg='for ' + key + '=' + str(value[1]))
                    self.assertEqual(sviValue2, value[1], msg='for ' + key + '=' + str(value[1]))

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('_SVIVariable.write')

    def test_getConnectionState(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        connectionState = sviVariable.getConnectionState()

        self.assertEqual(connectionState, 'ONLINE')
        self.assertEqual(type(connectionState), str)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getConnectionState')

    def test_getFullName(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        name = sviVariable.getFullName()

        self.assertEqual(type(name), str)
        self.assertEqual(name, 'RES/CPU/TempCelsius')
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getFullName')

    def test_getArrayLen(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        ret = sviVariable.getArrayLen()

        self.assertEqual(type(ret), int)
        self.assertEqual(ret, 1)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/Version', swModule)
        ret = sviVariable.getArrayLen()

        self.assertEqual(type(ret), int)
        self.assertEqual(ret, 20)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getArrayLen')

    def test_getBaseDataType(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        # Reset the svi test application
        sviAppReset()

        # Perform the write tests
        swModule = m1com._M1SwModule('SVIWRITE', mh)
        checkVariables = { 'boolVar': 'SVI_F_UINT1', 'bool8Var': 'SVI_F_BOOL8', 'uInt8Var': 'SVI_F_UINT8', 'sInt8Var': 'SVI_F_SINT8',
                           'uInt16Var': 'SVI_F_UINT16', 'sInt16Var': 'SVI_F_SINT16', 'uInt32Var': 'SVI_F_UINT32', 'sInt32Var': 'SVI_F_SINT32',
                           'uInt64Var': 'SVI_F_UINT64', 'sInt64Var': 'SVI_F_SINT64', 'real32Var': 'SVI_F_REAL32', 'real64Var': 'SVI_F_REAL64',
                           'char8Var': 'SVI_F_CHAR8', 'char16Var': 'SVI_F_CHAR16', 'stringVar': 'SVI_F_CHAR8', 'ustringVar': 'SVI_F_CHAR16',
                           'boolArray': 'SVI_F_UINT1', 'bool8Array': 'SVI_F_BOOL8', 'uInt8Array': 'SVI_F_UINT8', 'sInt8Array': 'SVI_F_SINT8',
                           'uInt16Array': 'SVI_F_UINT16', 'sInt16Array': 'SVI_F_SINT16', 'uInt32Array': 'SVI_F_UINT32', 'sInt32Array': 'SVI_F_SINT32',
                           'uInt64Array': 'SVI_F_UINT64', 'sInt64Array': 'SVI_F_SINT64', 'real32Array': 'SVI_F_REAL32', 'real64Array': 'SVI_F_REAL64',
                           'stringArray': 'SVI_F_STRINGLSTBASE', 'ustringArray': 'SVI_F_USTRINGLSTBASE', 'mixedVar': 'SVI_F_MIXED'
                           }

        Error = False
        ErrorMsg = ''
        try:
            for key in checkVariables:
                sviVariable = m1com._SVIVariable('SVIWRITE/' + key, swModule)

                obtainedDataType = sviVariable.getBaseDataType()
                realDataType = checkVariables[key]

                self.assertEqual(type(obtainedDataType), str)
                self.assertEqual(obtainedDataType, realDataType)

        except Exception as e:
            ErrorMsg = e
            Error = True
            print(str(e))

        # Reset the svi test application
        sviAppReset()

        if Error:
            raise ErrorMsg
        else:
            testedMethods.append('_SVIVariable.getBaseDataType')

    def test_checkReadable(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        ret = sviVariable.checkReadable()

        self.assertEqual(type(ret), bool)
        self.assertEqual(ret, True)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.checkReadable')

    def test_checkWritable(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        ret = sviVariable.checkWritable()

        self.assertEqual(type(ret), bool)
        self.assertEqual(ret, False)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.checkWritable')

if __name__ == "__main__":

    # Settings
    ipAddress  = '192.168.1.163'      # Set ip address of the Bachmann PLC used for testing
    fastTest   = False                # Skip tests that require a reboot

    # List where name of tested methods will be saved
    testedMethods = []

    test = Test_M1Controller()
    test.test_getNetworkInfo()
    test.test_setIP()

    # Find all classes and there callable methods in m1com
    M1comClasses = {}
    for Class in dir(m1com):

        # Check if the class is callable
        if callable(getattr(m1com, Class)):

            # Find all methods in the callable class
            M1comClassMethods = [Method for Method in dir(getattr(m1com, Class)) if callable(getattr(getattr(m1com, Class), Method)) and not Method.startswith('__')]

            # Add class and its methods to dictionary if it does have methods
            if len(M1comClassMethods) != 0:
                M1comClasses.update({Class:M1comClassMethods})

    # Install the test application
    sviAppInstall()

    # Perform the unit test
    unittest.main(verbosity=2, exit=False)

    # Remove the test application
    sviAppRemove()

    # Check if all methods in m1com where tested
    count = 0
    for Class in M1comClasses:
        for Method in M1comClasses[Class]:
            if (Class + '.' + Method) not in testedMethods:
                if count == 0:
                    print('\nThe following methods were not tested or failed the unittest:')
                print(Class + '.' + Method + '()')
                count = count + 1

    # Print number of not tested methods
    if count > 0:
        print('\n' + str(count) + ' methods were not tested or failed the unittest!')

