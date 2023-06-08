from flask import Flask, render_template, session
from flask import Flask, render_template, Response
import cv2
import time
import os

import random
import string
import time

OTP_EXPIRATION_SECONDS = 60

cctv = cv2.VideoCapture('rtsp://admin:REEBullets007@192.168.254.141/live/ch1')
# Set camera resolution
cctv.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cctv.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
from flask import Flask, render_template,Response,jsonify,request,redirect,url_for
from Jojo_loRecognition.Face_Recognition import Face_Recognition as Jolo

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.debug = True  # Enable debug mode


#OTP
def generate_otp(length=6):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/otp')
def otp():
    current_time = time.time()

    if 'otp' not in session or 'otp_expiration' not in session or current_time > session['otp_expiration']:
        session['otp'] = generate_otp()
        session['otp_expiration'] = current_time + OTP_EXPIRATION_SECONDS
        session.modified = True


        remaining_time = session['otp_expiration'] - current_time
        return render_template('otp.html', otp=session['otp'], remaining_time=int(remaining_time))
        
# load a camera,face detection
camera = cv2.VideoCapture(1)
face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# homepage =========================================== #
@app.route('/')
def index():
    return render_template('index.html')

# facial Login =========================================== #
@app.route('/facial_login')
def facial_login():
    return render_template('face-login.html')

# ------------------- Load camera
@app.route('/video_feed')
def video_feed():
        return Response(facialDetection(camera=camera, face_detector=face_detection), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')

# ------------------- Facial recognition Function
Text = "Initializing"
def facialDetection(camera=None, face_detector=None):
    global Text
    
    Text=""
    B , G , R = (0,255,255)

    
    textResult = ""
    
    # Login Attempt
    success = 0
    fail = 0                                    
    
    # Initialize the timer and the start time
    timer = 0
    start_time = time.time()
    
    while True:
        
        # Capture a frame from the camera
        ret, frame = camera.read()
        
        if not ret:
            break

        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=20, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
   
        # # checking detecting face should be 1
        # if len(faces) == 1:
        #          = faces[0]
        for (x, y, w, h) in faces:
                            
            # Check if 2 seconds have elapsed since the last send
            if timer >= 2:
                       
                # facial comparison 
                response = Jolo().Face_Compare(face=frame)
                
                try:
                    textResult = response[0]

                    if "No match detected" == response[0]:
                        fail+=1
                        B, G, R = (0, 0, 255)
                        textResult = response[0]
                        if fail == 5:
                            Text = "Access Denied"
                    else:
                        B, G, R = (0, 255, 0)
                        textResult = response[0]
                        Text = "Access Granted"
                    
                except:
                    pass
                
                # Reset the timer and the start time
                timer = 0
                start_time = time.time()
            else:
                # Increment the timer by the elapsed time since the last send
                timer += time.time() - start_time
                start_time = time.time()
                
            # Get the coordinates of the face,draw rectangele and put text
            
        
            cv2.rectangle(frame, (x, y), (x+w, y+h), (B,G,R), 2)
            cv2.putText(frame,textResult,(x,y+h+30),cv2.FONT_HERSHEY_COMPLEX,1,(B,G,R),1)

        # elif len(faces) > 1:
            
        #     # If more than 1 faces 
        #     # B, G, R = (0, 0, 255)
        #     Text = "More than 1 face is detected"
        # else:
        #     # B, G, R = (0, 0, 0)
        #     Text = "No face is detected"    
            
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')
        
# ********************* API route Facial Recognition Result
@app.route("/GET_FacialResult", methods=["GET"])
def GET_FacialResult():
    return jsonify(Text) 

# # Finger or OTP Login ===========================================
# @app.route('/finger_otp')
# def finger_otp():
#     return render_template('fingeropt.html')

# Login as Admin =========================================== #
@app.route('/admin_login')
def admin_login():
    return render_template('login.html')

# Admin Page =========================================== #
# ------------------- Dashboard
@app.route('/admin')
def admin():
    return render_template('Admin/index.html')

# ------------------- Controls
@app.route('/admin/Controls')
def control():
    return render_template('Admin/controls.html')
#CCTV
def generate_frames():
    while True:
        success, frame = cctv.read()  # Read the video stream
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Generate frame bytes for streaming

@app.route('/cctv_feed')
def cctv_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # Stream the frames


# ------------------- Historic Data
@app.route('/admin/Historic')
def historic():
    return render_template('Admin/historic.html')

# ------------------- Register
@app.route('/admin/register')
def register():
    return render_template('Admin/register.html')

# ------------------- Family Name Register
@app.route('/admin/Name_Family')
def nameFamily():
    return render_template('Admin/family-name-reg.html')


# =====================  route for registered faces
path = f"Jojo_loRecognition/Known_Faces/"

# ********************* API for submit 
@app.route('/submit_family', methods=['POST'])
def submit_family():
    global path
    
    # print(str(request.form.get('fullname')))
    # return jsonify({ "message": "goods" })

    # Define the path to the folder you want to create
    path = f"Jojo_loRecognition/Registered-Faces/{str(request.form.get('fullname'))}"
    
    # Check if the folder already exists
    if os.path.exists(path):
        return jsonify({'error': f"Folder {path} already exists"}), 400
    else:
        os.makedirs(path)
        # route to facial registration
        return redirect(url_for('Finger_register'))

# ------------------- Guest Name Register
@app.route('/admin/Name_Guest')
def nameGuest():
    return render_template('Admin/guest-name-reg.html')
@app.route('/admin/cam')
def cam():
    return render_template('Admin/cam.html')

# ------------------- Finger Register
@app.route('/admin/Finger_register')
def Finger_register():
    return render_template('Admin/finger-register.html')

# ------------------- Facial Register
@app.route('/admin/Facial_Register')
def Facial_Register():
    return render_template('Admin/face-register.html')

# def facialDetection(camera=None, face_detector=None):
#     global Text
    
#     Text=""
#     B , G , R = (0,255,255)

    
#     textResult = ""
    
#     # Login Attempt
#     success = 0
#     fail = 0                                    
    
#     # Initialize the timer and the start time
#     timer = 0
#     start_time = time.time()
    
#     while True:
        
#         # Capture a frame from the camera
#         ret, frame = camera.read()
        
#         if not ret:
#             break

#         frame = cv2.flip(frame,1)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
#         # Detect faces in the frame
#         faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=20, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
   
#         # # checking detecting face should be 1
#         # if len(faces) == 1:
#         #          = faces[0]
#         for (x, y, w, h) in faces:
                            

#             # Get the coordinates of the face,draw rectangele and put text
            
        
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (B,G,R), 2)
#             cv2.putText(frame,textResult,(x,y+h+30),cv2.FONT_HERSHEY_COMPLEX,1,(B,G,R),1)

#         # elif len(faces) > 1:
            
#         #     # If more than 1 faces 
#         #     # B, G, R = (0, 0, 255)
#         #     Text = "More than 1 face is detected"
#         # else:
#         #     # B, G, R = (0, 0, 0)
#         #     Text = "No face is detected"    
            
#         _, frame_encoded  = cv2.imencode('.png', frame)
#         yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Database API


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5000)