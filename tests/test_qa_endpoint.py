# tests/test_qa_endpoint.py
import uuid


def test_ask_returns_answer_and_run_id(client, fake_service):
    response = client.post("/qa/ask", json={"question": "What is 6 times 7?"})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "Mocked answer: 42."
    # run_id must be a valid UUID string
    uuid.UUID(body["run_id"])
    # the service received the question we sent
    assert fake_service.received_question == "What is 6 times 7?"


def test_ask_rejects_empty_question(client):
    response = client.post("/qa/ask", json={"question": ""})
    assert response.status_code == 422  # schema min_length


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}