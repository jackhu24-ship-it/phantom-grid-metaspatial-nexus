import sys
import os

# Ensure current directory is first in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import MetaSpatialOrchestrator, SpatialGesturePacket, ASILDMemorySentry, ZDRPurger

def test_sentry_headroom():
    sentry = ASILDMemorySentry(ceiling_gb=50.0)
    assert sentry.verify_headroom() is True
    sentry.current_usage_gb = 50.1
    assert sentry.verify_headroom() is False
    print("PASS: test_sentry_headroom")

def test_zdr_purger():
    purger = ZDRPurger()
    residue = purger.scrub("test_buffer")
    assert residue == 0.000000
    print("PASS: test_zdr_purger")

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
    assert res["latency_ms"] < 16.66
    print("PASS: test_orchestrator_nominal_cycle")

def test_multi_agent_dag_dispatch():
    orchestrator = MetaSpatialOrchestrator()
    nodes = ["Strategic Planner", "Tactical Executor", "Safety Sentry", "ZDR Scrubber"]
    for node in nodes:
        packet = SpatialGesturePacket(
            gesture_type="depth_poke",
            joint_coordinates=[0.1, 0.2, 0.3],
            target_node_id=node,
            confidence_score=0.99
        )
        res = orchestrator.process_gesture(packet)
        assert res["status"] == "SUCCESS"
        assert res["target_node"] == node
    print("PASS: test_multi_agent_dag_dispatch (4 Nodes)")

def test_vram_meltdown_breaker():
    orchestrator = MetaSpatialOrchestrator()
    orchestrator.sentry.current_usage_gb = 50.5
    packet = SpatialGesturePacket(
        gesture_type="air_pinch",
        joint_coordinates=[0.0, 0.0, 0.0],
        target_node_id="Strategic Planner",
        confidence_score=0.95
    )
    try:
        orchestrator.process_gesture(packet)
        assert False, "Should have tripped ESTOP"
    except RuntimeError:
        print("PASS: test_vram_meltdown_breaker (ESTOP tripped)")

if __name__ == "__main__":
    test_sentry_headroom()
    test_zdr_purger()
    test_orchestrator_nominal_cycle()
    test_multi_agent_dag_dispatch()
    test_vram_meltdown_breaker()
    print("\n[SUCCESS] ALL 5 RIGID INDUSTRIAL GATES 100% PASSED!")
