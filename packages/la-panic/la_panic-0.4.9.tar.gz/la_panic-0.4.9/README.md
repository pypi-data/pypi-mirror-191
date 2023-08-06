# iOS Panic Parser

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
  - [Example](#example)
- [Contributing](#contribution)

# Description

`la_panic` is a tool for working with iPhone crash reports.

# Installation
```shell
python3 -m pip install --user -U la_panic
```

Or install the latest version from sources:

```shell
git clone git@gitlab.com:yanivhasbanidev/la_panic.git
cd la_panic
python3 -m pip install --user -U -e .
```

# Usage
```shell
la_panic parser parse <IPS_FILE>
```
## Example
```
la_panic parser parse "forceReset-full.ips"

35F77863-C28D-42BA-B633-9732EA1F342A 2022-12-24 11:43:00.470000
<full_path>/forceReset-full.ips

Exception: Panic

Metadata:
	Bug Type: BugType.FORCE_RESET
	Timestamp: 2022-12-24 11:43:00.470000
	iPhone Model: iPhone XR
	XNU Version: xnu-8792.62.2~1/RELEASE_ARM64_T8020


Crashed Core Registers:None

Backtrace:
	LR = 0xfffffff02cfc6ba8,  FP = 0xffffffecfb44f820
	LR = 0xfffffff02cfc697c,  FP = 0xffffffecfb44f890
	LR = 0xfffffff02d10bdd4,  FP = 0xffffffecfb44f8b0
	LR = 0xfffffff02d0ff258,  FP = 0xffffffecfb44f920
	LR = 0xfffffff02d0fddf0,  FP = 0xffffffecfb44f9b0
	LR = 0xfffffff02cf837b8,  FP = 0xffffffecfb44f9c0
	LR = 0xfffffff02cfc6390,  FP = 0xffffffecfb44fd70
	LR = 0xfffffff02d6df108,  FP = 0xffffffecfb44fd90
	LR = 0xfffffff02e156784,  FP = 0xffffffecfb44fdd0
	LR = 0xfffffff02e1430a4,  FP = 0xffffffecfb44fe00
	LR = 0xfffffff02d60ba00,  FP = 0xffffffecfb44fe30
	LR = 0xfffffff02d01ef68,  FP = 0xffffffecfb44ff20
	LR = 0xfffffff02cf8c7c0,  FP = 0x0


Sliders:
	Kernel Slide = 0x0000000025ec0000
	Kernel Text Base = 0xfffffff02cec4000
	Kernel Text Exec Base: 0xfffffff02cf7c000
	Kernel Text Exec Slide: 0x0000000025f78000
	Kernel Cache Base: 0xfffffff02c2dc000
	Kernel Cache Slide: 0x00000000252d8000


Loaded kexts:
	Last selected kext:
		name = com.apple.driver.ApplePearlSEPDriver

	Kexts:
		com.apple.driver.AppleUSBDeviceMux, 1.0.0d1
		com.apple.nke.l2tp, 1.9
		com.apple.filesystems.tmpfs, 1
		com.apple.driver.ApplePMP, 1
		com.apple.filesystems.lifs, 1
		com.apple.filesystems.apfs, 2142.62.1
		com.apple.IOTextEncryptionFamily, 1.0.0
		com.apple.filesystems.hfs.kext, 627.40.1
		com.apple.AppleFSCompression.AppleFSCompressionTypeZlib, 1.0.0
		com.apple.driver.AppleT8020PMPFirmware, 1
		com.apple.driver.AppleAD5860, 600.99
		com.apple.driver.AppleFAN53740, 1
		com.apple.driver.AppleIDV, 5.207
		com.apple.driver.AppleEmbeddedGPS, 1.0.0d1
		com.apple.driver.AppleBasebandPCIICEPDP, 1
		com.apple.driver.AppleBluetooth, 1.0.0d1
		com.apple.driver.ApplePinotLCD, 1.0.0
		com.apple.driver.AppleCS35L27Amp, 600.99
		com.apple.driver.AppleCS42L75Audio, 600.99
		com.apple.driver.AppleChestnutDisplayPMU, 1
		com.apple.driver.AppleSamsungSPI, 1
		com.apple.driver.AppleSynopsysMIPIDSI, 1.0.0
		com.apple.driver.AppleSPMIPMU, 1.0.1
		com.apple.driver.AppleLMBacklight, 1
		com.apple.driver.AppleHapticsSupportCallan, 7.20
		com.apple.driver.AppleSerialShim, 1
		com.apple.driver.AppleJPEGDriver, 5.1.3
		com.apple.driver.AppleSmartIO2, 1
		com.apple.driver.AppleSmartBatteryManagerEmbedded, 1
		com.apple.driver.AppleSMCWirelessCharger, 1.0.1
		com.apple.driver.AppleAVE2, 640.4.1
		com.apple.driver.AppleAVD, 617.5
		com.apple.AGXG11P, 227.2.43
		com.apple.driver.AppleS5L8940XI2C, 1.0.0d2
		com.apple.driver.AppleMobileDispH11P, 140.0
		com.apple.driver.AppleS8000DWI, 1.0.0d1
		com.apple.driver.AppleBCMWLANBusInterfacePCIe, 1
		com.apple.driver.AppleS8000AES, 1
		com.apple.driver.AppleEmbeddedAudioResourceManager, 600.99
		com.apple.driver.AppleSamsungSerial, 1.0.0d1
		com.apple.driver.AppleT8020DART, 1
		com.apple.driver.AppleDAPF, 1
		com.apple.driver.AppleT8020CLPCv3, 1
		com.apple.driver.AppleT8020SOCTuner, 1
		com.apple.driver.AppleS5L8920XPWM, 1.0.0d1
		com.apple.driver.AppleS5L8960XNCO, 1
		com.apple.driver.AppleT8020PMGR, 1
		com.apple.driver.AppleInterruptController, 1.0.0d1
		com.apple.driver.AppleT8020, 1
		com.apple.driver.AppleM68Buttons, 1.0.0d1
		com.apple.iokit.IOUserEthernet, 1.0.1
		com.apple.driver.IOAudioCodecs, 1.0.0
		com.apple.driver.AppleTemperatureSensor, 1.0.0d1
		com.apple.driver.AppleDiskImages2, 198.40.3
		com.apple.driver.ASIOKit, 10.32
		com.apple.security.sandbox, 300.0
		com.apple.kec.Compression, 1
		com.apple.driver.ApplePearlSEPDriver, 1
		com.apple.iokit.IOBiometricFamily, 1
		com.apple.iokit.AppleSEPGenericTransfer, 1
		com.apple.driver.AppleEffaceableBlockDevice, 1.0
		com.apple.driver.AppleSynopsysOTGDevice, 1.0.0d1
		com.apple.iokit.IOUSBDeviceFamily, 2.0.0
		com.apple.nke.ppp, 1.9
		com.apple.driver.AppleBSDKextStarter, 3
		com.apple.driver.AppleBasebandPCIICEControl, 1
		com.apple.driver.AppleBasebandPCI, 1
		com.apple.driver.AppleBluetoothDebug, 1
		com.apple.driver.AppleHIDTransportSPI, 6110.3
		com.apple.driver.AppleHIDTransport, 6110.3
		com.apple.driver.AppleInputDeviceSupport, 6110.3
		com.apple.driver.AppleTriStar, 1.0.0
		com.apple.iokit.IOMikeyBusFamily, 1.0.0
		com.apple.driver.AppleCSEmbeddedAudio, 600.99
		com.apple.driver.AppleEmbeddedAudio, 600.99
		com.apple.iokit.AppleARMIISAudio, 200.8
		com.apple.driver.AppleStockholmControl, 1.0.0
		com.apple.AGXFirmwareKextG11PRTBuddy, 227.2.43
		com.apple.AGXFirmwareKextRTBuddy64, 227.2.43
		com.apple.driver.AppleDiagnosticDataAccessReadOnly, 1.0.0
		com.apple.driver.AppleDialogPMU, 1.0.1
		com.apple.driver.AppleT8020USB, 1
		com.apple.driver.AppleAstrisGpioProbe, 1.0.1
		com.apple.driver.AppleAuthCP, 1.0.0
		com.apple.driver.AppleC26Charger, 1.0.1
		com.apple.driver.AppleH11ANEInterface, 6.201.0
		com.apple.driver.AppleH10CameraInterface, 19.202.0
		com.apple.driver.AppleH10PearlCameraInterface, 19.202.0
		com.apple.iokit.IOGPUFamily, 65.0.22
		com.apple.driver.AppleT8011USB, 1
		com.apple.driver.AppleS5L8960XUSB, 1
		com.apple.driver.AppleEmbeddedUSB, 1
		com.apple.iokit.IONVMeFamily, 2.1.0
		com.apple.driver.AppleNANDConfigAccess, 1.0.0
		com.apple.driver.AppleSPMI, 1.0.1
		com.apple.iokit.IOMobileGraphicsFamily, 343.0.0
		com.apple.driver.AppleSPU, 1
		com.apple.driver.AppleT8020PCIe, 1
		com.apple.driver.AppleBluetoothDebugService, 1
		com.apple.driver.AppleBCMWLANCore, 1.0.0
		com.apple.iokit.IO80211Family, 1200.13.0
		com.apple.driver.IOImageLoader, 1.0.0
		com.apple.driver.AppleOLYHAL, 1
		com.apple.driver.corecapture, 1.0.4
		com.apple.driver.AppleMCA2-T8020, 701.14
		com.apple.driver.AppleSART, 1
		com.apple.driver.AppleEmbeddedAudioLibs, 200.5
		com.apple.driver.AppleFirmwareUpdateKext, 1
		com.apple.driver.AppleT8020PPM, 3.0
		com.apple.driver.AppleGPIOICController, 1.0.2
		com.apple.driver.AppleARMWatchdogTimer, 1
		com.apple.driver.AppleVortexErrorHandler, 1
		com.apple.driver.AppleBasebandD101, 1.0.0d1
		com.apple.driver.AppleEmbeddedPCIE, 1
		com.apple.driver.AppleMobileApNonce, 1
		com.apple.driver.usb.AppleUSBHostPacketFilter, 1.0
		com.apple.iokit.IOUSBMassStorageDriver, 232
		com.apple.iokit.IOSCSIArchitectureModelFamily, 476
		com.apple.iokit.IOPCIFamily, 2.9
		com.apple.iokit.IOUSBHostFamily, 1.2
		com.apple.driver.AppleUSBHostMergeProperties, 1.2
		com.apple.driver.usb.AppleUSBCommon, 1.0
		com.apple.iokit.IOTimeSyncFamily, 1110.14
		com.apple.driver.DiskImages, 493.0.0
		com.apple.driver.AppleSMC, 1
		com.apple.driver.RTBuddy, 1.0.0
		com.apple.driver.AppleEmbeddedTempSensor, 1.0.0
		com.apple.driver.AppleARMPMU, 1.0
		com.apple.iokit.IOAccessoryManager, 1.0.0
		com.apple.iokit.IOHIDFamily, 2.0.0
		com.apple.driver.AppleOnboardSerial, 1.0
		com.apple.iokit.IOSerialFamily, 11
		com.apple.driver.AppleSEPKeyStore, 2
		com.apple.driver.AppleEffaceableStorage, 1.0
		com.apple.driver.AppleSEPCredentialManager, 1.0
		com.apple.driver.AppleIPAppender, 1.0
		com.apple.iokit.IOSkywalkFamily, 1.0
		com.apple.driver.mDNSOffloadUserClient-Embedded, 1.0.1b8
		com.apple.iokit.IONetworkingFamily, 3.4
		com.apple.AUC, 1.0
		com.apple.iokit.IOAVFamily, 1.0.0
		com.apple.iokit.IOHDCPFamily, 1.0.0
		com.apple.iokit.IOCECFamily, 1
		com.apple.iokit.IOAudio2Family, 1.0
		com.apple.driver.AppleIISController, 200.2
		com.apple.driver.AppleAudioClockLibs, 200.5
		com.apple.driver.AppleM2ScalerCSCDriver, 265.0.0
		com.apple.iokit.IOSurface, 334.0.1
		com.apple.driver.IODARTFamily, 1
		com.apple.driver.AppleSSE, 1.0
		com.apple.driver.AppleSEPManager, 1.0.1
		com.apple.driver.AppleA7IOP, 1.0.2
		com.apple.driver.IOSlaveProcessor, 1
		com.apple.driver.LSKDIOKit, 19.10.0
		com.apple.driver.FairPlayIOKit, 70.35.0
		com.apple.kext.AppleMatch, 1.0.0d1
		com.apple.driver.AppleMobileFileIntegrity, 1.0.5
		com.apple.iokit.CoreAnalyticsFamily, 1
		com.apple.driver.ApplePMGR, 1
		com.apple.driver.AppleARMPlatform, 1.0.2
		com.apple.iokit.IOStorageFamily, 2.1
		com.apple.iokit.IOSlowAdaptiveClockingFamily, 1.0.0
		com.apple.iokit.IOReportFamily, 47
		com.apple.security.AppleImage4, 5.0.0
		com.apple.kext.CoreTrust, 1
		com.apple.iokit.IOCryptoAcceleratorFamily, 1.0.1
		com.apple.kec.pthread, 1
		com.apple.kec.Libm, 1
		com.apple.kec.corecrypto, 12.0
```

## Tested Panic Types
* Force Reset (151)
* Panic Full (210)

# Contribution
See [CONTRIBUTING](CONTRIBUTING.md).
