"""raspberry/camera_sources.py의 Picamera2 픽셀 형식이 OpenCV(BGR) 순서와 맞는지 검사한다 (실기기 없이)."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_picamera_requests_opencv_bgr_layout(monkeypatch):
    # Picamera2 매뉴얼의 형식 표: "RGB888"은 [B, G, R] 순서(OpenCV BGR), "BGR888"은 [R, G, B] 순서
    import types

    formats = []

    class FakePicamera2:
        def __init__(self, index):
            pass

        def create_preview_configuration(self, **kwargs):
            formats.append(kwargs["main"]["format"])
            return kwargs

        def configure(self, config):
            pass

        def start(self):
            pass

    monkeypatch.setitem(sys.modules, "picamera2", types.SimpleNamespace(Picamera2=FakePicamera2))
    spec = importlib.util.spec_from_file_location("camera_sources_format", ROOT / "raspberry" / "camera_sources.py")
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module.time, "sleep", lambda s: None)
    module.PiCamera(index=0)
    assert formats == ["RGB888"]
