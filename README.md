Реализация
 [avito-trainee-task](https://github.com/avito-tech/mi-trainee-task?tab=readme-ov-file)
 
 
HTTP сервис для одноразовых секретов наподобие https://onetimesecret.com/.

Он должен позволить создать секрет, задать кодовую фразу для его открытия и cгенерировать код, по которому можно прочитать секрет только один раз. UI не нужен, это должен быть JSON Api сервис.

Для написание сервиса можно использовать FastAPI или любой другой фреймворк.

Метод /generate должен принимать секрет и кодовую фразу и отдавать secret_key по которому этот секрет можно получить.

Метод /secrets/{secret_key} принимает на вход кодовую фразу и отдает секрет.

Запуск:
uvicorn main:app --host 0.0.0.0

## Documentation
This is a code implementation that utilizes the FastAPI framework to create an API for generating and retrieving secrets. The secrets are stored in a MongoDB database using the `motor` library for asynchronous database operations.

## Dependencies
- secrets
- fastapi
- pydantic
- motor (motor.motor_asyncio.AsyncIOMotorClient)

## Code Explanation

### Imports
- `secrets` is imported to generate secure and random secret keys.
- `FastAPI` is imported from the `fastapi` module which is used to build the API.
- `BaseModel` is imported from `pydantic` to define the structure of the secret data.
- `AsyncIOMotorClient` is imported from `motor.motor_asyncio` to establish a connection with the MongoDB database.

### FastAPI Application
- An instance of the `FastAPI` class is created and assigned to the `app` variable.

### Data Model
- The `Secret` class is defined as a Pydantic `BaseModel` with two fields: `secret` and `passphrase`.

### Database Class
- The `Database` class is defined to handle database operations.
- The class constructor takes a MongoDB connection URL and initializes the database connection using `AsyncIOMotorClient`.
- The `save_secret` method asynchronously saves a secret to the database.
  - It generates a unique secret key using `secrets.token_hex`.
  - Inserts the secret data into the `secrets` collection with the generated secret key as the document ID.
  - Returns the secret key.
- The `get_secret` method asynchronously retrieves a secret from the database using the provided secret key and passphrase.
  - It searches for the document with the given secret key.
  - If the document exists, it checks if the provided passphrase matches the stored passphrase.
  - If the passphrase matches, it deletes the document from the database and returns the secret.
  - If the secret key or passphrase is invalid, it raises an `HTTPException` with status code 404.

### Database Initialization
- An instance of the `Database` class is created with the MongoDB connection URL "mongodb://localhost:27017" and assigned to the `db` variable.

### API Endpoints
- `@app.post("/generate")` defines a POST endpoint where clients can generate a new secret.
  - It expects a JSON payload with the structure defined by the `Secret` model.
  - Calls the `save_secret` method to save the secret to the database and retrieves the generated secret key.
  - Returns a JSON response containing the generated secret key.

- `@app.get("/secrets/{secret_key}")` defines a GET endpoint for retrieving a secret.
  - It expects the `secret_key` and `passphrase` as path parameters.
  - Calls the `get_secret` method to retrieve the secret from the database.
  - Returns a JSON response containing the retrieved secret.

## Example Usage
1. To generate a new secret:
   - HTTP Method: POST
   - Endpoint: /generate
   - Request Body:
     ```json
     {
       "secret": "my_secret",
       "passphrase": "my_passphrase"
     }
     ```
     or
     ```json
     {
       "secret": "another_secret",
       "passphrase": "another_passphrase"
     }
     ```
   - Response:
     ```json
     {
       "secret_key": "7c20a8cbe33d78142d4e670665165b19"
     }
     ```

2. To retrieve a secret:
   - HTTP Method: GET
   - Endpoint: /secrets/{secret_key}
   - Path Parameters:
     - secret_key: The secret key returned from the generate endpoint.
     - passphrase: The passphrase used when generating the secret.
   - Response:
     ```json
     {
       "secret": "my_secret"
     }
     ```

   Note: If the secret key or passphrase is invalid, an HTTP 404 response will be returned with the error message "Secret not found".
