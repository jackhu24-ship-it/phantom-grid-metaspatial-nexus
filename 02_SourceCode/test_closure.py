import pytest
import time
from main import MetaSpatialOrchestrator, SpatialGesturePacket, ASILDMemorySentry, ZDRPurger

def test_sentry_headroom():
    sentry = ASILDMemorySentry(ceiling_gb=50.0)
    assert sentry.verify_headroom() is True
    sentry.current_usage_gb = 50.1
    assert sentry.verify_headroom() is False

def test_zdr_purger():
    purger = ZDRPurger()
    residue = purger.scrub("test_buffer")
    assert residue == 0.000000

def test_orchestrator_nominal_cycle():
    orchestrator = MetaSpatialOrchestrator()
    packet = SpatialGesturePacket(
        gesture_type="air_pinch",
        joint_coordinates=[0.0, 1.2, -0.5],
        target_node_id="Tactical Executor",
        confidence_score=0.985
    )
    res = orchestrator.process_gesture(packet)
    assert res["status"] == "SUCCESS"
    assert res["residual_mb"] == 0.000000
    assert res["safety_cert"] == "ASIL-D PASS"
    assert res["latency_ms"] < 16.66  # Must satisfy 60 FPS VR frame budget
