"""Synergy MTC: a button on the settings page that puts the demo data back as
npm run seed leaves it, for a demo in front of a customer. It works only where
UNDERCOVER_DEMO_RESET is on, as on the demo server, and only for a handler who
can sign off payouts over the limit, while none of the agent's work is going."""

import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.agent_work import refuse_while_work_goes_on
from backend.database import engine, seed
from backend.dependencies import Database, senior
from backend.models import Handler

SWITCH = "UNDERCOVER_DEMO_RESET"
SWITCHED_OFF = "Resetting the demo data is switched off on this server"

router = APIRouter()

ResetsTheDemo = Annotated[Handler, Depends(senior("reset the demo data"))]


class DemoReset(BaseModel):
    """What the demo data holds after a reset."""

    claims: int
    customers: int
    policies: int


def switched_on() -> bool:
    """Say whether this server lets a handler reset the demo data, read now."""
    return os.getenv(SWITCH, "").lower() == "on"


@router.post("/api/demo/reset", operation_id="reset_demo")
def reset_demo(handler: ResetsTheDemo, db: Database) -> DemoReset:
    """Put the demo data back as it was seeded, when no work is going."""
    if not switched_on():
        raise HTTPException(403, SWITCHED_OFF)
    refuse_while_work_goes_on(db)
    db.commit()  # end this request's reads, so the reset can drop the tables
    counts = seed(engine())
    return DemoReset(
        claims=counts["claims"],
        customers=counts["customers"],
        policies=counts["policies"],
    )
