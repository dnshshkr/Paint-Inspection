import pypylon.pylon as py
cam=py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
cam.DestroyDevice()
print(cam.DeviceInfo)
print('fak')