import os
from typing import Annotated

import httpx
from fastapi import FastAPI, HTTPException, Path

app = FastAPI()

LTA_BUS_ARRIVAL_URL = "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival"


@app.get("/api/arrivals/{stop_code}")
def get_arrivals(stop_code: Annotated[str, Path(pattern=r"^[0-9]{5}$")]):
    account_key = os.getenv("LTA_ACCOUNT_KEY")
    if not account_key:
        raise HTTPException(status_code=500, detail="LTA API key is not configured.")

    try:
        response = httpx.get(
            LTA_BUS_ARRIVAL_URL,
            headers={"AccountKey": account_key},
            params={"BusStopCode": stop_code},
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"LTA returned HTTP {exc.response.status_code}.",
        ) from exc
    except (httpx.RequestError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Could not get a valid response from LTA.",
        ) from exc