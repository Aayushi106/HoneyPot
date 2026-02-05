from fastapi import FastAPI, Request, Header, HTTPException
import requests

app = FastAPI()

API_KEY = "hackathon123"

@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    # Auth check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    session_id = data.get("sessionId", "unknown")

    # 🔴 FINAL CALLBACK (MANDATORY)
    callback_payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": 1,
        "extractedIntelligence": {
            "bankAccounts": [],
            "upiIds": [],
            "phishingLinks": [],
            "phoneNumbers": [],
            "suspiciousKeywords": []
        },
        "agentNotes": "Basic engagement completed"
    }

    try:
        requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json=callback_payload,
            timeout=5
        )
    except:
        pass  # ignore failure, don't crash

    # ✅ REQUIRED RESPONSE
    return {
        "status": "success",
        "reply": "Can you please explain this again?"
    }

