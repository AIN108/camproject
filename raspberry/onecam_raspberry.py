from __future__ import annotations

import argparse
import time
from pathlib import Path

import cv2

from camera_sources import open_camera

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_IDLE_VIDEO = ROOT_DIR / "black.mp4"
DEFAULT_ACTIVE_VIDEO = ROOT_DIR / "seoultech.mp4"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Raspberry Pi용 CamProject 단일 카메라 버전"
    )
    parser.add_argument("--camera", choices=("usb", "picamera"), default="usb")
    parser.add_argument("--camera-index", type=int, default=0)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--detect-interval", type=float, default=0.25)
    parser.add_argument("--idle-video", type=Path, default=DEFAULT_IDLE_VIDEO)
    parser.add_argument("--active-video", type=Path, default=DEFAULT_ACTIVE_VIDEO)
    parser.add_argument("--windowed", action="store_true", help="전체화면 대신 일반 창으로 표시")
    return parser.parse_args()


def open_video(path: Path) -> cv2.VideoCapture:
    path = path.expanduser().resolve()
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        capture.release()
        raise RuntimeError(f"동영상 파일을 열 수 없습니다: {path}")
    return capture


def read_looping(capture: cv2.VideoCapture, path: Path):
    ok, frame = capture.read()
    if ok and frame is not None:
        return frame

    capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ok, frame = capture.read()
    if not ok or frame is None:
        raise RuntimeError(f"동영상 프레임을 읽을 수 없습니다: {path}")
    return frame


def main() -> int:
    args = parse_args()
    if args.width <= 0 or args.height <= 0 or args.fps <= 0:
        raise ValueError("width, height, fps는 1보다 큰 값이어야 합니다.")
    if args.detect_interval < 0:
        raise ValueError("detect-interval은 0 이상이어야 합니다.")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    if face_cascade.empty():
        raise RuntimeError("OpenCV Haar Cascade를 불러오지 못했습니다.")

    camera = open_camera(args.camera, args.camera_index, args.width, args.height, args.fps)
    idle_video = open_video(args.idle_video)
    active_video = open_video(args.active_video)

    window_name = "CamProject Raspberry"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    if not args.windowed:
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    active_position = 0.0
    face_detected = False
    last_detection_time = 0.0

    try:
        while True:
            now = time.monotonic()
            camera_frame = camera.read()

            if now - last_detection_time >= args.detect_interval:
                gray = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=4
                )
                new_face_detected = len(faces) > 0

                if new_face_detected and not face_detected:
                    active_video.set(cv2.CAP_PROP_POS_FRAMES, active_position)
                elif not new_face_detected and face_detected:
                    active_position = active_video.get(cv2.CAP_PROP_POS_FRAMES)
                    idle_video.set(cv2.CAP_PROP_POS_FRAMES, 0)

                face_detected = new_face_detected
                last_detection_time = now

            if face_detected:
                frame = read_looping(active_video, args.active_video)
            else:
                frame = read_looping(idle_video, args.idle_video)

            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
    finally:
        idle_video.release()
        active_video.release()
        camera.close()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
