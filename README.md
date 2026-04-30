# Face Authentication API

This project is a FastAPI service for face-based user registration and verification.

## Features

- Register a user with `name`, `email`, and a face image.
- Store face embeddings in PostgreSQL.
- Verify a user by comparing a new face image against the stored embedding.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- `face_recognition` + NumPy

## Project Structure

```text
face_authentication/
├── apis/
│   └── user_apis.py
├── db/
│   └── database.py
├── models/
│   └── user_model.py
├── main.py
├── utils.py
└── .gitignore
```

## Prerequisites

Install these before running:

- Python 3.10+ (recommended)
- PostgreSQL (running locally or remotely)
- pip

`face_recognition` also requires native dependencies.  
On Windows, if installation fails, install Visual C++ Build Tools and CMake first.

## Setup

### 1) Clone and open project

```bash
git clone <your-repo-url>
cd face_authentication
```

### 2) Create virtual environment

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3) Install dependencies

If you have a `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

Otherwise install manually:

```bash
pip install fastapi uvicorn sqlalchemy asyncpg python-dotenv face-recognition numpy python-multipart rich
```

### 4) Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<database_name>
```

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/face_auth
```

## Run the Program

Start the API server:

```bash
uvicorn main:app --reload
```

Server will run at:

- API: `http://127.0.0.1:8000`
- Swagger Docs: `http://127.0.0.1:8000/docs`

## API Endpoints

### `GET /`

Health check endpoint.

### `GET /test-db`

Checks database session connectivity.

### `POST /register`

Registers a user with face image.

Form fields:

- `name` (string)
- `email` (string)
- `file` (image file)

### `POST /verify`

Verifies a face image against stored user embedding.

Form fields:

- `email` (string)
- `file` (image file)

Response:

- `{ "message": true }` for match
- `{ "message": false }` for no match

## Quick Test Using cURL

Register:

```bash
curl -X POST "http://127.0.0.1:8000/register" \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "file=@/path/to/john.jpg"
```

Verify:

```bash
curl -X POST "http://127.0.0.1:8000/verify" \
  -F "email=john@example.com" \
  -F "file=@/path/to/john_verify.jpg"
```

## Notes

- Images are temporarily saved to `Demo_pic/` and deleted after processing.
- The face match threshold is currently set to `0.6` in `utils.py`.
- Ensure your PostgreSQL database exists before starting the server.
