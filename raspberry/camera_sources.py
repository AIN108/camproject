from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol

import cv2


class CameraSource(Protocol):
    def read(self): ...
    def close(self) -> None: ...


@dataclass
class UsbCamera:
    index: int = 0
    width: int = 640
    height: int = 480
    fps: int = 30

    def __post_init__(self) -> None:
        self._capture = cv2.VideoCapture(self.index, cv2.CAP_V4L2)
        if not self._capture.isOpened():
            self._capture.release()
            self._capture = cv2.VideoCapture(self.index)
        if not self._capture.isOpened():
            raise RuntimeError(
                f"USB 카메라 {self.index}을(를) 열 수 없습니다. /dev/video*와 카메라 권한을 확인하세요."
            )

        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self._capture.set(cv2.CAP_PROP_FPS, self.fps)

    def read(self):
        ok, frame = self._capture.read()
        if not ok or frame is None:
            raise RuntimeError(f"USB 카메라 {self.index}에서 프레임을 읽을 수 없습니다.")
        return frame

    def close(self) -> None:
        self._capture.release()


@dataclass
class PiCamera:
    index: int = 0
    width: int = 640
    height: int = 480
    fps: int = 30

    def __post_init__(self) -> None:
        try:
            from picamera2 import Picamera2
        except ImportError as exc:
            raise RuntimeError(
                "Picamera2가 없습니다. Raspberry Pi OS에서 'sudo apt install -y python3-picamera2'를 실행하세요."
            ) from exc

        self._camera = Picamera2(self.index)
        frame_duration_us = max(1, round(1_000_000 / max(1, self.fps)))
        try:
            # Picamera2(libcamera)의 "RGB888"은 메모리상 [B, G, R] 순서라 OpenCV(BGR)와 같다.
            # "BGR888"은 [R, G, B] 순서라 OpenCV에서 빨강·파랑이 뒤바뀐다. (실기기 확인 필요: PR 본문 참고)
            config = self._camera.create_preview_configuration(
                main={"size": (self.width, self.height), "format": "RGB888"},
                controls={"FrameDurationLimits": (frame_duration_us, frame_duration_us)},
            )
            self._camera.configure(config)
            self._camera.start()
        except Exception:
            # 설정·시작에 실패하면 카메라를 닫아 다음 실행에서 "장치 사용 중"이 되지 않게 한다
            self._camera.close()
            raise
        time.sleep(0.5)

    def read(self):
        frame = self._camera.capture_array("main")
        if frame is None:
            raise RuntimeError(f"Raspberry Pi Camera {self.index}에서 프레임을 읽을 수 없습니다.")
        return frame

    def close(self) -> None:
        self._camera.stop()
        self._camera.close()


def open_camera(source: str, index: int, width: int, height: int, fps: int) -> CameraSource:
    if source == "usb":
        return UsbCamera(index=index, width=width, height=height, fps=fps)
    if source == "picamera":
        return PiCamera(index=index, width=width, height=height, fps=fps)
    raise ValueError(f"지원하지 않는 카메라 종류입니다: {source}")
