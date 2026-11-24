"""Synergy MTC: the settings page's button that resets the demo data."""

from sqlalchemy import select, update

from backend.database import claims, engine
from backend.tests.run_requests import create_dispatch
from backend.tests.sign_in import DANA, MARCUS, signed_in

RESET = "/api/demo/reset"


def switch_on(monkeypatch):
    monkeypatch.setenv("UNDERCOVER_DEMO_RESET", "on")


def first_claim_status():
    with engine().connect() as db:
        return db.execute(select(claims.c.status).limit(1)).scalar_one()


def test_a_senior_handler_resets_the_demo_data(client, monkeypatch):
    switch_on(monkeypatch)
    with engine().begin() as db:
        db.execute(update(claims).values(status="failed"))
    answer = client.post(RESET, headers=signed_in(DANA))
    assert answer.status_code == 200
    assert answer.json()["claims"] > 0
    assert first_claim_status() != "failed"


def test_the_reset_is_refused_when_switched_off(client, monkeypatch):
    monkeypatch.delenv("UNDERCOVER_DEMO_RESET", raising=False)
    answer = client.post(RESET, headers=signed_in(DANA))
    assert answer.status_code == 403
    assert "switched off" in answer.json()["detail"]


def test_only_a_senior_handler_may_reset(client, monkeypatch):
    switch_on(monkeypatch)
    assert client.post(RESET, headers=signed_in(MARCUS)).status_code == 403
    assert client.post(RESET).status_code == 401


def test_the_reset_waits_while_a_dispatch_runs(client, monkeypatch):
    switch_on(monkeypatch)
    create_dispatch(client)
    assert client.post(RESET, headers=signed_in(DANA)).status_code == 409
