from pathlib import Path
import ctypes
import sys
import time

import cv2

BASE_DIR = Path(__file__).resolve().parent
BLACK_VIDEO = BASE_DIR / "black.mp4"
SEOULTECH_VIDEO = BASE_DIR / "seoultech.mp4"
CASCADE_PATH = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
FACE_DETECTION_INTERVAL = 2.0


def open_video(path: Path) -> cv2.VideoCapture:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise FileNotFoundError(f"영상 파일을 열 수 없습니다: {path}")
    return capture


class VideoClock:
    """영상 파일의 fps에 맞춰 재생 속도를 맞춘다.

    루프가 영상보다 빠르면 waitKey로 기다리고, 느리면(웹캠 읽기·얼굴 검출이 오래 걸리면) 밀린 프레임을
    grab()으로 건너뛰어 원래 속도를 유지한다. 영상이 바뀌거나 처음으로 되감기면 기준 시각을 다시 잡는다.
    """

    MAX_SKIP = 10  # 한 번에 건너뛸 최대 프레임 수

    def __init__(self):
        self.video = None
        self.start_time = 0.0
        self.start_pos = 0.0
        self.last_pos = 0.0

    def pause(self):
        """영상을 잠시 보여 주지 않을 때 호출한다. 다시 재생하면 그 시점부터 기준을 잡는다."""
        self.video = None

    def wait_ms(self, video, now):
        """방금 읽은 프레임을 화면에 둔 채 기다릴 시간(ms). 늦었으면 밀린 프레임을 건너뛴다."""
        pos = video.get(cv2.CAP_PROP_POS_FRAMES)  # 다음에 읽을 프레임 번호
        fps = video.get(cv2.CAP_PROP_FPS) or 30.0
        if video is not self.video or pos < self.last_pos:
            self.video, self.start_time, self.start_pos = video, now, pos
        ahead = pos - (self.start_pos + (now - self.start_time) * fps)
        if ahead < -1:
            for _ in range(min(int(-ahead), self.MAX_SKIP)):
                if not video.grab():
                    break
            pos = video.get(cv2.CAP_PROP_POS_FRAMES)
        self.last_pos = pos
        return max(1, int(ahead * 1000 / fps)) if ahead > 0 else 1


def main() -> None:
    # 화면 크기를 Windows API(ctypes.windll)로 구하므로 Windows 전용이다.
    if sys.platform != "win32":
        raise SystemExit(
            "onecam.py는 Windows 전용입니다. Raspberry Pi·Linux에서는 "
            "`python3 raspberry/onecam_raspberry.py --camera usb`를 사용하세요."
        )

    face_cascade = cv2.CascadeClassifier(str(CASCADE_PATH))
    if face_cascade.empty():
        raise RuntimeError(f"Haar Cascade를 불러오지 못했습니다: {CASCADE_PATH}")

    black_video = open_video(BLACK_VIDEO)
    seoultech_video = open_video(SEOULTECH_VIDEO)
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("기본 웹캠(0)을 열 수 없습니다.")

    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    cv2.namedWindow("Screen", cv2.WINDOW_GUI_EXPANDED)
    cv2.setWindowProperty("Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    clock = VideoClock()

    showing_black = True
    face_detected = False
    last_detection_time = 0.0

    try:
        while True:
            current_time = time.time()
            ok, camera_frame = camera.read()
            if not ok or camera_frame is None:
                print("웹캠 프레임을 읽을 수 없습니다.")
                break

            if current_time - last_detection_time >= FACE_DETECTION_INTERVAL:
                gray = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
                face_detected = len(faces) > 0
                last_detection_time = current_time

            # 영상 파일은 한 번만 열고, 전환할 때 다시 열지 않는다.
            # 홍보영상은 검은 화면을 보여 주는 동안 읽지 않으므로 같은 캡처가 멈춘 위치에서 이어서 재생된다.
            if face_detected and showing_black:
                showing_black = False
            elif not face_detected and not showing_black:
                showing_black = True
                black_video.set(cv2.CAP_PROP_POS_FRAMES, 0)

            active_video = black_video if showing_black else seoultech_video
            ok, frame = active_video.read()

            if not ok or frame is None:
                # 영상 끝: 처음으로 되감아 반복 재생
                active_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ok, frame = active_video.read()

            if not ok or frame is None:
                print("표시할 영상 프레임을 읽을 수 없습니다.")
                break

            frame = cv2.resize(frame, (screen_width, screen_height))
            cv2.imshow("Screen", frame)

            key = cv2.waitKey(clock.wait_ms(active_video, time.time())) & 0xFF
            if key in (ord("q"), 27):
                break
    finally:
        black_video.release()
        seoultech_video.release()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
