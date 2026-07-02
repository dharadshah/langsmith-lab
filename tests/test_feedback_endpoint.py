# tests/test_feedback_endpoint.py
def test_feedback_recorded(client, fake_feedback_service):
    response = client.post(
        "/qa/feedback",
        json={"run_id": "test-run-123", "helpful": True, "comment": "Good."},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Feedback recorded successfully."}
    assert len(fake_feedback_service.calls) == 1
    assert fake_feedback_service.calls[0]["run_id"] == "test-run-123"
    assert fake_feedback_service.calls[0]["helpful"] is True