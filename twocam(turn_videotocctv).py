'''
import cv2
import time
import numpy as np
import requests

# 얼굴 인식을 위한 Haar Cascade 로드
face_cascade = cv2.CascadeClassifier(r'C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')

# 비디오 파일과 두 개의 웹캠 초기화
video = cv2.VideoCapture(r'C:\onecam\seoultech.mp4')
webcam1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 얼굴 인식을 위한 카메라1
webcam2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # CCTV 피드를 위한 카메라2

# 카메라가 제대로 열렸는지 확인
if not webcam1.isOpened():
    print("카메라1을 열 수 없습니다.")
    exit()
if not webcam2.isOpened():
    print("카메라2를 열 수 없습니다.")
    exit()
if not video.isOpened():
    print("비디오 파일을 열 수 없습니다.")
    exit()

# 윈도우 이름 정의
window_name1 = 'Monitor1'
window_name2 = 'Monitor2'

# 윈도우 생성 및 전체 화면 설정
cv2.namedWindow(window_name1, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)

# 전체 화면으로 설정
cv2.setWindowProperty(window_name1, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty(window_name2, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 윈도우 위치 설정 (모니터 해상도에 맞게 조정 필요)
# 예시: 두 모니터가 좌우로 배치되어 있고, 각 모니터의 해상도가 1920x1080인 경우
MONITOR_WIDTH = 1080
MONITOR_HEIGHT = 1920

cv2.moveWindow(window_name1, 0, 0)
cv2.moveWindow(window_name2, MONITOR_WIDTH, 0)

video_playing = False
last_detected_time = time.time()
face_count = 0
frame_count = 0
def get_center_rectangle(frame, width=480, height=320):
    """프레임의 중앙에서 지정된 너비와 높이의 사각형을 추출합니다."""
    center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
    half_width, half_height = width // 2, height // 2
    return frame[center_y - half_height:center_y + half_height, center_x - half_width:center_x + half_width]

def send_frames_to_server(frame1, frame2, face_count, video_playing):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            _, img_encoded1 = cv2.imencode('.jpg', frame1)
            _, img_encoded2 = cv2.imencode('.jpg', frame2)
            response = requests.post(
                'http://192.168.0.10:5000/update_frame',
                files={
                    'frame1': ('frame1.jpg', img_encoded1.tobytes(), 'image/jpeg'),
                    'frame2': ('frame2.jpg', img_encoded2.tobytes(), 'image/jpeg')
                },
                data={
                    'face_count': face_count,
                    'video_playing': video_playing
                },
                timeout=1  # 1초 타임아웃 설정
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"서버 연결 오류 (시도 {attempt+1}/{max_retries}): {e}")
            time.sleep(0.5)  # 재시도 전 잠시 대기
    return None

def split_frame(frame, monitor_width, monitor_height):
    """프레임을 좌우로 절반씩 분할하여 두 개의 프레임을 반환합니다."""
    height, width, _ = frame.shape
    # 원하는 모니터 해상도에 맞게 프레임을 리사이즈
    resized_frame = cv2.resize(frame, (monitor_width * 2, monitor_height))
    half_width = monitor_width
    left_half = resized_frame[:, :half_width]
    right_half = resized_frame[:, half_width:]
    return left_half, right_half

while True:
    # 카메라1에서 프레임 읽기 (얼굴 인식용)
    ret1, frame1 = webcam1.read()
    if not ret1:
        print("카메라1에서 프레임을 읽을 수 없습니다.")
        break

    # 얼굴 인식을 위한 중앙 사각형 추출
    center_rectangle = get_center_rectangle(frame1, width=480, height=320)
    frame_gray = cv2.cvtColor(center_rectangle, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=3)
    face_count = len(faces)

    if face_count > 0:
        video_playing = True
        last_detected_time = time.time()
    elif time.time() - last_detected_time > 2:
        video_playing = False

    # 표시할 프레임 결정
    if video_playing:
        ret_video, video_frame = video.read()
        if not ret_video:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret_video, video_frame = video.read()
        display_frame = video_frame
    else:
        # 카메라2에서 프레임 읽기 (CCTV 피드용)
        ret2, frame2 = webcam2.read()
        if not ret2:
            print("카메라2에서 프레임을 읽을 수 없습니다.")
            break
        display_frame = frame2

    # 프레임을 모니터 해상도에 맞게 분할
    left_half, right_half = split_frame(display_frame, MONITOR_WIDTH, MONITOR_HEIGHT)

    # 두 개의 윈도우에 분할된 프레임 표시
    cv2.imshow(window_name1, left_half)
    cv2.imshow(window_name2, right_half)

    # 10프레임마다 서버에 전송
    if frame_count % 10 == 0:
        #서버로 보낼 프레임은 카메라1과 카메라2의 최신 프레임을 사용
        # 비디오가 재생 중일 때는 비디오 프레임을, 아닐 때는 카메라2의 프레임을 전송
        if video_playing:
            server_frame2 = video_frame
        else:
            server_frame2 = frame2
        send_frames_to_server(frame1, server_frame2, face_count, video_playing)
    frame_count += 1

    # 종료 조건: 'q' 키 입력 시 종료
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# 자원 해제
video.release()
webcam1.release()
webcam2.release()
cv2.destroyAllWindows()
'''

import cv2
import time
import numpy as np

# 얼굴 인식을 위한 Haar Cascade 로드
face_cascade = cv2.CascadeClassifier(r'C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')

# 비디오 파일과 두 개의 웹캠 초기화
video = cv2.VideoCapture(r'C:\onecam\seoultech.mp4')
webcam1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # 얼굴 인식을 위한 카메라1
webcam2 = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CCTV 피드를 위한 카메라2

# 카메라가 제대로 열렸는지 확인
if not webcam1.isOpened():
    print("카메라1을 열 수 없습니다.")
    exit()
if not webcam2.isOpened():
    print("카메라2를 열 수 없습니다.")
    exit()
if not video.isOpened():
    print("비디오 파일을 열 수 없습니다.")
    exit()

# 윈도우 이름 정의
window_name1 = 'Monitor1'
window_name2 = 'Monitor2'

# 윈도우 생성 및 전체 화면 설정
cv2.namedWindow(window_name1, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)

# 전체 화면으로 설정
cv2.setWindowProperty(window_name1, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty(window_name2, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 윈도우 위치 설정 (모니터 해상도에 맞게 조정 필요)
MONITOR_WIDTH = 1080
MONITOR_HEIGHT = 1920

cv2.moveWindow(window_name1, 0, 0)
cv2.moveWindow(window_name2, MONITOR_WIDTH, 0)

video_playing = False
last_detected_time = time.time()
face_count = 0
frame_count = 0

def get_center_rectangle(frame, width=720, height=640):
    """프레임의 중앙에서 지정된 너비와 높이의 사각형을 추출합니다."""
    center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
    half_width, half_height = width // 2, height // 2
    return frame[center_y - half_height:center_y + half_height, center_x - half_width:center_x + half_width]

def split_frame(frame, monitor_width, monitor_height):
    resized_frame = cv2.resize(frame, (monitor_width * 2, monitor_height))
    half_width = monitor_width
    left_half = resized_frame[:, :half_width]
    right_half = resized_frame[:, half_width:]
    return left_half, right_half

while True:
    # 카메라1에서 프레임 읽기 (얼굴 인식용)
    ret1, frame1 = webcam1.read()
    if not ret1:
        print("카메라1에서 프레임을 읽을 수 없습니다.")
        break

    # 얼굴 인식을 위한 중앙 사각형 추출
    center_rectangle = get_center_rectangle(frame1, width=480, height=320)
    frame_gray = cv2.cvtColor(center_rectangle, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=2)
    face_count = len(faces)

    # 사람 감지 여부에 따른 전환 속도 개선
    current_time = time.time()
    if face_count > 0:
        if not video_playing or current_time - last_detected_time > 0.5:
            video_playing = True
            last_detected_time = current_time
    elif current_time - last_detected_time > 1:
        if video_playing:
            video_playing = False

    # 표시할 프레임 결정
    if video_playing:
        ret_video, video_frame = video.read()
        if not ret_video:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret_video, video_frame = video.read()
        display_frame = video_frame
    else:
        # 카메라2에서 프레임 읽기 (CCTV 피드용)
        ret2, frame2 = webcam2.read()
        if not ret2:
            print("카메라2에서 프레임을 읽을 수 없습니다.")
            break
        display_frame = frame2

    # 프레임을 모니터 해상도에 맞게 분할
    left_half, right_half = split_frame(display_frame, MONITOR_WIDTH, MONITOR_HEIGHT)

    # 두 개의 윈도우에 분할된 프레임 표시
    cv2.imshow(window_name1, left_half)
    cv2.imshow(window_name2, right_half)

    frame_count += 1

    # 종료 조건: 'q' 키 입력 시 종료
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# 자원 해제
video.release()
webcam1.release()
webcam2.release()
cv2.destroyAllWindows()




