from __future__ import annotations

import argparse
import time
from pathlib import Path

import cv2

from camera_sources import open_camera

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ACTIVE_VIDEO = ROOT_DIR / "seoultech.mp4"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Raspberry Pi용 CamProject 2카메라/CCTV 전환 버전"
    )
    parser.add_argument("--detector-source", choices=("usb", "picamera"), default="usb")
    parser.add_argument("--detector-index", type=int, default=0)
    parser.add_argument("--cctv-source", choices=("usb", "picamera"), default="usb")
    parser.add_argument("--cctv-index", type=int, default=1)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--active-video", type=Path, default=DEFAULT_ACTIVE_VIDEO)
    parser.add_argument("--hold-seconds", type=float, default=1.0,
                        help="마지막 얼굴 검출 후 광고를 유지하는 시간")
    parser.add_argument("--roi-width", type=int, default=480)
    parser.add_argument("--roi-height", type=int, default=320)
    parser.add_argument("--windowed", action="store_true", help="전체화면 대신 일반 창으로 표시")
    parser.add_argument("--dual-output", action="store_true",
                        help="출력을 좌우 절반으로 나눠 두 OpenCV 창에 표시")
    parser.add_argument("--monitor-width", type=int, default=1920)
    parser.add_argument("--monitor-height", type=int, default=1080)
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


def center_roi(frame, width: int, height: int):
    frame_height, frame_width = frame.shape[:2]
    width = min(max(1, width), frame_width)
    height = min(max(1, height), frame_height)
    x1 = (frame_width - width) // 2
    y1 = (frame_height - height) // 2
    return frame[y1:y1 + height, x1:x1 + width]


def show_single(window_name: str, frame) -> None:
    cv2.imshow(window_name, frame)


def show_dual(frame, monitor_width: int, monitor_height: int) -> None:
    resized = cv2.resize(frame, (monitor_width * 2, monitor_height))
    left = resized[:, :monitor_width]
    right = resized[:, monitor_width:]
    cv2.imshow("Monitor1", left)
    cv2.imshow("Monitor2", right)


def main() -> int:
    args = parse_args()
    if args.width <= 0 or args.height <= 0 or args.fps <= 0:
        raise ValueError("width, height, fps는 1보다 큰 값이어야 합니다.")
    if args.hold_seconds < 0:
        raise ValueError("hold-seconds는 0 이상이어야 합니다.")

    if (
        args.detector_source == args.cctv_source
        and args.detector_index == args.cctv_index
    ):
        raise ValueError("얼굴 검출용 카메라와 CCTV용 카메라는 서로 다른 장치를 지정하세요.")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    if face_cascade.empty():
        raise RuntimeError("OpenCV Haar Cascade를 불러오지 못했습니다.")

    detector_camera = open_camera(
        args.detector_source, args.detector_index, args.width, args.height, args.fps
    )
    cctv_camera = open_camera(
        args.cctv_source, args.cctv_index, args.width, args.height, args.fps
    )
    active_video = open_video(args.active_video)

    if args.dual_output:
        if args.monitor_width <= 0 or args.monitor_height <= 0:
            raise ValueError("monitor-width와 monitor-height는 1보다 큰 값이어야 합니다.")
        for name in ("Monitor1", "Monitor2"):
            cv2.namedWindow(name, cv2.WINDOW_NORMAL)
            if not args.windowed:
                cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.moveWindow("Monitor1", 0, 0)
        cv2.moveWindow("Monitor2", args.monitor_width, 0)
    else:
        cv2.namedWindow("Screen", cv2.WINDOW_NORMAL)
        if not args.windowed:
            cv2.setWindowProperty("Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    video_playing = False
    last_face_time = 0.0

    try:
        while True:
            detector_frame = detector_camera.read()
            roi = center_roi(detector_frame, args.roi_width, args.roi_height)
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.2, minNeighbors=2
            )

            now = time.monotonic()
            if len(faces) > 0:
                video_playing = True
                last_face_time = now
            elif video_playing and now - last_face_time > args.hold_seconds:
                video_playing = False

            if video_playing:
                display_frame = read_looping(active_video, args.active_video)
            else:
                display_frame = cctv_camera.read()

            if args.dual_output:
                show_dual(display_frame, args.monitor_width, args.monitor_height)
            else:
                show_single("Screen", display_frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
    finally:
        active_video.release()
        detector_camera.close()
        cctv_camera.close()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
