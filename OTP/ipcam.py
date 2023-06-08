from flask import Flask, render_template, Response
import cv2 

app = Flask(__name__)
camera = cv2.VideoCapture('rtsp://admin:REEBullets007@192.168.254.141/live/ch1')

# Set camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

def generate_frames():
    while True:
        success, frame = camera.read()  # Read the video stream
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Generate frame bytes for streaming

@app.route('/')
def index():
    return render_template('cam.html')  # Render the updated HTML template for video streaming

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # Stream the frames

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)  # Enable threading for better performance
