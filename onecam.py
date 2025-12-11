import cv2
import time
import ctypes

face_cascade = cv2.CascadeClassifier(r'C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')

# Load the videos
video1 = cv2.VideoCapture(r'C:\onecam\black.mp4')
video2 = cv2.VideoCapture(r'C:\onecam\seoultech.mp4')

# Connect to the external camera
cap = cv2.VideoCapture(0)  # 0 is the default c amera index, adjust if needed

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Create a fullscreen window for displaying the videos
cv2.namedWindow('Screen', cv2.WINDOW_GUI_EXPANDED)
cv2.setWindowProperty('Screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


# Flag to track video playback
video1_playing = True
video2_playing = False

# Track video2 playback position
video2_position = 0

face_detceted = False
last_face_detection_time = 0
Face_detection_interval = 2
while True:
    current_time = time.time()

    # Capture frame from external camera
    _, cam_frame = cap.read()

    # Convert camera frame to grayscale for face detection
    gray = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    if current_time - last_face_detection_time >= Face_detection_interval:
       faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
       face_detceted = len(faces) > 0
       last_face_detection_time = current_time

    # Read frame from video based on face detection result
    if video1_playing:
        ret, frame = video1.read()
        if not ret:
            video1 = cv2.VideoCapture(r'C:\onecam\black.mp4')
            ret, frame = video1.read()

    elif video2_playing:
        ret, frame = video2.read()
        if not ret:
            video2.set(cv2.CAP_PROP_POS_FRAMES, video2_position)
            continue

    # Check if faces are detected in the cam frame
    if len(faces) > 0 and video1_playing:
        video1_playing = False
        video2_playing = True
        video2 = cv2.VideoCapture(r'C:\onecam\seoultech.mp4')
        video2.set(cv2.CAP_PROP_POS_FRAMES, video2_position)
        time.sleep(0.1)

    elif len(faces) == 0 and video2_playing:
        video2_playing = False
        video1_playing = True
        video2_position = video2.get(cv2.CAP_PROP_POS_FRAMES)  # Store the playback position before switching
        video1 = cv2.VideoCapture(r'C:\onecam\black.mp4')
        time.sleep(0.1)

    # Resize the frame to the screen's resolution
    frame = cv2.resize(frame, (screen_width, screen_height))

    # Display the video
    cv2.imshow('Screen', frame)

    # Check for key press
    key = cv2.waitKey(1)
    if key != -1:
        break

# Release video capture objects and close windows
video1.release()
video2.release()
cap.release()
cv2.destroyAllWindows()