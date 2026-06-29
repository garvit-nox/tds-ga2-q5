from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_wbb7b273qtd7dudwbb7vpt9n"

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class EventBatch(BaseModel):
    events: List[Event]

@app.post("/analytics")
async def analytics(
    body: EventBatch,
    x_api_key: str = Header(default=None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = body.events
    total_events = len(events)
    unique_users = len(set(e.user for e in events))

    revenue = sum(e.amount for e in events if e.amount > 0)

    user_totals: dict = {}
    for e in events:
        if e.amount > 0:
            user_totals[e.user] = user_totals.get(e.user, 0) + e.amount
    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": "24f1000625@ds.study.iitm.ac.in",
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": round(revenue, 4),
        "top_user": top_user,
    }
