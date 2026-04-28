import face_recognition
import numpy as np
from dotenv import load_dotenv
import os
import json


load_dotenv()

def get_face_embedding(image_path):
    print(image_path)
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return None
    
    return encodings[0]


def compare_faces(known_embedding, new_embedding):
    print(new_embedding)
    distance = np.linalg.norm(known_embedding - new_embedding)
    # threesold = os.getenv("EXACT_MATCH")
    return distance < 0.6   

def string_to_vector(s):
    return np.array(json.loads(s))