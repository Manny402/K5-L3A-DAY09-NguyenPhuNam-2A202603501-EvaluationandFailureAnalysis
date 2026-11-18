"""Regression proof for the first incorrect step in C-002@11."""

import pytest

from lab9.trace_case import investigate


@pytest.mark.student
def test_ticket_delay_cannot_override_order_delay():
    broken = investigate("seeded_regression", "C-002", 11)["trial"]
    fixed = investigate("fixed", "C-002", 11)["trial"]
    assert not broken["lab8_pass"]
    assert broken["events"][2]["kind"] == "model_override"
    assert broken["events"][2]["payload"]["delay_days"] == 5
    assert broken["snapshot"]["refund_vnd"] == 20000
    assert fixed["lab8_pass"]
    assert not any(e["kind"] == "model_override" for e in fixed["events"])
    assert fixed["snapshot"]["refund_vnd"] == 0
