from pathlib import Path
import argparse
import time

import cv2

BASE_DIR = Path(__file__).resolve().parent
SEOULTECH_VIDEO = BASE_DIR / "seoultech.mp4"
CASCADE_PATH = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"


def get_center_rectangle(frame, width=480, height=320):
    """프레임 중앙에서 얼굴 감지용 영역을 잘라냅니다."""
    frame_h, frame_w = frame.shape[:2]
    width = min(width, frame_w)
    height = min(height, frame_h)
    center_x, center_y = frame_w // 2, frame_h // 2
    half_width, half_height = width // 2, height // 2
    return frame[
        center_y - half_height : center_y + half_height,
        center_x - half_width : center_x + half_width,
    ]


def split_frame(frame, monitor_width, monitor_height):
    """하나의 영상을 두 모니터에 표시할 수 있도록 좌우 절반으로 나눕니다."""
    resized = cv2.resize(frame, (monitor_width * 2, monitor_height))
    return resized[:, :monitor_width], resized[:, monitor_width:]


def open_camera(index):
    camera = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not camera.isOpened():
        raise RuntimeError(f"카메라 {index}를 열 수 없습니다.")
    return camera


def main():
    parser = argparse.ArgumentParser(
        description="얼굴 감지 여부에 따라 홍보영상/CCTV 화면을 전환해 듀얼 모니터에 출력합니다."
    )
    parser.add_argument("--detect-camera", type=int, default=1, help="얼굴 감지용 카메라 번호")
    parser.add_argument("--cctv-camera", type=int, default=0, help="CCTV 표시용 카메라 번호")
    parser.add_argument("--monitor-width", type=int, default=1080, help="모니터 한 대의 가로 픽셀")
    parser.add_argument("--monitor-height", type=int, default=1920, help="모니터 한 대의 세로 픽셀")
    parser.add_argument("--hold-seconds", type=float, default=1.0, help="얼굴이 사라진 뒤 영상 유지 시간")
    args = parser.parse_args()

    face_cascade = cv2.CascadeClassifier(str(CASCADE_PATH))
    if face_cascade.empty():
        raise RuntimeError(f"Haar Cascade를 불러오지 못했습니다: {CASCADE_PATH}")

    video = cv2.VideoCapture(str(SEOULTECH_VIDEO))
    if not video.isOpened():
        raise FileNotFoundError(f"영상 파일을 열 수 없습니다: {SEOULTECH_VIDEO}")

    webcam_detect = open_camera(args.detect_camera)
    webcam_cctv = open_camera(args.cctv_camera)

    window_name1 = "Monitor1"
    window_name2 = "Monitor2"
    cv2.namedWindow(window_name1, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name1, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty(window_name2, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow(window_name1, 0, 0)
    cv2.moveWindow(window_name2, args.monitor_width, 0)

    video_playing = False
    last_detected_time = 0.0

    try:
        while True:
            ok_detect, detect_frame = webcam_detect.read()
            if not ok_detect or detect_frame is None:
                print("얼굴 감지용 카메라 프레임을 읽을 수 없습니다.")
                break

            roi = get_center_rectangle(detect_frame)
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2)

            current_time = time.time()
            if len(faces) > 0:
                video_playing = True
                last_detected_time = current_time
            elif video_playing and current_time - last_detected_time > args.hold_seconds:
                video_playing = False

            if video_playing:
                ok_video, display_frame = video.read()
                if not ok_video or display_frame is None:
                    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ok_video, display_frame = video.read()
                    if not ok_video or display_frame is None:
                        print("홍보영상 프레임을 읽을 수 없습니다.")
                        break
            else:
                ok_cctv, display_frame = webcam_cctv.read()
                if not ok_cctv or display_frame is None:
                    print("CCTV 카메라 프레임을 읽을 수 없습니다.")
                    break

            left_half, right_half = split_frame(
                display_frame, args.monitor_width, args.monitor_height
            )
            cv2.imshow(window_name1, left_half)
            cv2.imshow(window_name2, right_half)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
    finally:
        video.release()
        webcam_detect.release()
        webcam_cctv.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
