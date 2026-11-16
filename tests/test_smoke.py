"""카메라·디스플레이 없이 실행할 수 있는 스모크 테스트."""
import importlib.util
import py_compile
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = sorted(ROOT.glob("*.py")) + sorted((ROOT / "raspberry").glob("*.py"))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("path", SCRIPTS, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_scripts_compile(path, tmp_path):
    py_compile.compile(str(path), cfile=str(tmp_path / "out.pyc"), doraise=True)


@pytest.mark.parametrize("name", ["black.mp4", "seoultech.mp4"])
def test_bundled_videos_open_and_decode(name):
    capture = cv2.VideoCapture(str(ROOT / name))
    try:
        assert capture.isOpened()
        assert capture.get(cv2.CAP_PROP_FRAME_COUNT) > 0
        assert capture.get(cv2.CAP_PROP_FPS) > 0
        ok, frame = capture.read()
        assert ok and frame is not None and frame.ndim == 3
    finally:
        capture.release()


@pytest.mark.parametrize("script", ["onecam_raspberry.py", "twocam_raspberry.py"])
def test_raspberry_scripts_show_help(script):
    result = subprocess.run([sys.executable, str(ROOT / "raspberry" / script), "--help"],
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    assert "usage" in result.stdout.lower()


def test_twocam_frame_helpers():
    twocam = load(ROOT / "twocam(turn_videotocctv).py", "twocam")
    frame = np.zeros((720, 1280, 3), np.uint8)
    assert twocam.get_center_rectangle(frame).shape == (320, 480, 3)
    left, right = twocam.split_frame(frame, 1080, 1920)
    assert left.shape == right.shape == (1920, 1080, 3)


def test_raspberry_center_roi_is_clamped():
    sys.path.insert(0, str(ROOT / "raspberry"))
    try:
        twocam = load(ROOT / "raspberry" / "twocam_raspberry.py", "twocam_raspberry")
    finally:
        sys.path.pop(0)
    frame = np.zeros((240, 320, 3), np.uint8)
    assert twocam.center_roi(frame, 480, 320).shape == (240, 320, 3)  # 프레임보다 크면 프레임 크기로
    assert twocam.center_roi(frame, 100, 50).shape == (50, 100, 3)
