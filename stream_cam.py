from flask import Flask,Response
import cv2
import pypylon.pylon as py
from gevent.pywsgi import WSGIServer
import socket
app=Flask(__name__)
try:
    camera=py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
    camera.StartGrabbing(py.GrabStrategy_LatestImageOnly)
except:
    print('failed to access camera')
    exit(0)
converter=py.ImageFormatConverter()
converter.OutputPixelFormat=py.PixelType_BGR8packed
converter.OutputBitAlignment=py.OutputBitAlignment_MsbAligned
@app.route('/')
def index():
    return 'Basler'
def gen():
    while camera.IsGrabbing():
        grabResult=camera.RetrieveResult(4000,py.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            image=cv2.GaussianBlur(cv2.resize(converter.Convert(grabResult).GetArray(),(1920,1080)),(3,3),0)
            ret,jpeg=cv2.imencode('.jpg',image)
            frame=jpeg.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type:image/jpeg\r\n'
                  b'Content-Length: '+f"{len(frame)}".encode()+b'\r\n'
                  b'\r\n'+frame+b'\r\n')
            grabResult.Release()
    camera.StopGrabbing()
@app.route('/stream')
def stream():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    #http_server=WSGIServer(('192.168.137.1',2608),app)
    http_server=WSGIServer((socket.gethostbyname(socket.gethostname()),2608),app)
    print(http_server.address)
    http_server.serve_forever()

    #app.run(host='0.0.0.0',port=2608,threaded=True)