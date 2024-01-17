from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import timedelta
import pymongo
import hashlib
import uvicorn

app = FastAPI()

# Подключение к базе данных MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
database = client['secret_database']
collection = database['secrets']

class Secret(BaseModel):
    message: str
    passphrase: str
    expire_seconds: Optional[int] = 3600

@app.post("/generate")
def generate(secret: Secret):
    # Преобразование секрета и кодовой фразы в байтовые строки
    secret_bytes = secret.message.encode('utf-8')
    passphrase_bytes = secret.passphrase.encode('utf-8')
    # Соединение секрета и кодовой фразы
    concatenated = secret_bytes + passphrase_bytes

    # Вычисление хэша SHA-256 от объединенной строки
    hash_object = hashlib.sha256(concatenated)
    secret_key = hash_object.hexdigest()

    # Создание документа с секретом, парольной фразой и сгенерированным ключом
    document = {
        'secret': secret.message,
        'passphrase': secret.passphrase,
        'secret_key': secret_key
    }

    # Вставка документа в коллекцию
    collection.insert_one(document)

    return {"success": True, "secret_key": secret_key}



@app.get("/secrets/{secret_key}")
def get_secret(secret_key: str):
    secret_info = collection.find_one({"secret_key": secret_key})

    if secret_info:
        return {"secret": secret_info["secret"]}
    else:
        return {"error": "Неверная кодовая фраза!"}
    



if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)