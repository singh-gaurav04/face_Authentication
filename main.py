from fastapi import FastAPI, Depends,UploadFile,Form,File,status,HTTPException
from multipart import multipart
from db.database import get_db,Base,engine,init_db
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_face_embedding,compare_faces,string_to_vector
from apis.user_apis import create_user , get_user
import os,shutil
from rich import print
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Face_Authentication")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await init_db()


UPLOAD_PIC = "Demo_pic"
os.makedirs(UPLOAD_PIC,exist_ok=True)


@app.get("/",status_code=status.HTTP_200_OK)
async def greet():
    return {"message": "Hello world"}

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    return {"status": "DB connected"}

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    path = None

    try:
        path = f"{UPLOAD_PIC}/{file.filename}"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        embedding = get_face_embedding(path)

        if embedding is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No face detected"
            )

        await create_user(db, email, embedding, name)

        return {"message": "User registered successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    finally:
        if path and os.path.exists(path):
            os.remove(path)


@app.post("/verify",status_code=status.HTTP_200_OK)
async def verify(
    email: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    path = None
    try:
        path = f"{UPLOAD_PIC}/{file.filename}"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        user = await get_user(db, email)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        new_embedding = get_face_embedding(path)

        if new_embedding is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No face detected")
        
        match = compare_faces(np.array(user.embedding), new_embedding)
        return {"message":bool(match)}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    finally:
        if path and os.path.exists(path):
            os.remove(path)


