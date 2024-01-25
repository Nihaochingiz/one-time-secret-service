import secrets
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

class Secret(BaseModel):
    secret: str
    passphrase: str

class Database:
    def __init__(self, url: str):
        self.client = AsyncIOMotorClient(url)
        self.db = self.client["secrets_db"]
        self.collection = self.db["secrets"]

    async def save_secret(self, secret_data: Secret) -> str:
        secret_key = secrets.token_hex(16)
        await self.collection.insert_one({"_id": secret_key, "secret_data": secret_data.dict()})
        return secret_key

    async def get_secret(self, secret_key: str, passphrase: str) -> str:
        secret_doc = await self.collection.find_one({"_id": secret_key})
        if secret_doc:
            secret_data = secret_doc["secret_data"]
            if secret_data["passphrase"] == passphrase:
                await self.collection.delete_one({"_id": secret_key})
                return secret_data["secret"]
        raise HTTPException(status_code=404, detail="Secret not found")

db = Database("mongodb://localhost:27017")

@app.post("/generate")
async def generate(secret_data: Secret):
    secret_key = await db.save_secret(secret_data)
    return {"secret_key": secret_key}

@app.get("/secrets/{secret_key}")
async def get_secret(secret_key: str, passphrase: str):
    secret = await db.get_secret(secret_key, passphrase)
    return {"secret": secret}