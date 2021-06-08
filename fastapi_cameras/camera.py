from vidgear.gears import CamGear
import cv2

class WebcamCamera(object):
    def __init__(self, camera_source):
        self.camera_source = camera_source
        self.options = {
            "CAP_PROP_FRAME_WIDTH": 320,
            "CAP_PROP_FRAME_HEIGHT": 240,
            "CAP_PROP_FPS": 60,
        }
        self.stream = CamGear(source=self.camera_source, logging=True, **self.options).start()

    def __del__(self):
        self.stream.stop()

    
    def getFrames(self):
        frame = self.stream.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

