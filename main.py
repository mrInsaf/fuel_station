import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from time import time

app = FastAPI()

last_request_time = {}

REQUEST_LIMIT_SECONDS = 1

EXTERNAL_SERVICE_URL = "https://external-service.com/api/get_fuel"

class TankRequest(BaseModel):
    tank_id: int
    count: int

class Fuel(BaseModel):
    fuel_id: int
    quantity: int

class TankResponse(BaseModel):
    fuel: List[Fuel]

@app.post("/get_fuel", response_model=TankResponse)
async def get_fuel(request: TankRequest):
    current_time = time()
    if request.tank_id in last_request_time:
        time_since_last_request = current_time - last_request_time[request.tank_id]
        if time_since_last_request < REQUEST_LIMIT_SECONDS:
            raise HTTPException(
                status_code=429,
                detail=f"Too many requests. Please wait {REQUEST_LIMIT_SECONDS - time_since_last_request:.2f} seconds."
            )

    last_request_time[request.tank_id] = current_time

    if request.count <= 0:
        raise HTTPException(status_code=400, detail="Count must be greater than 0")

    fuel_to_request = min(request.count, 10)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                EXTERNAL_SERVICE_URL,
                json={"tank_id": request.tank_id, "count": fuel_to_request}
            )
            response.raise_for_status()

            fuel_data = response.json()

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error while fetching fuel from external service")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    fuel_tokens = [Fuel(fuel_id=i + 1, quantity=fuel_data.get("quantity", 1)) for i in range(fuel_to_request)]

    return {"fuel": fuel_tokens}
