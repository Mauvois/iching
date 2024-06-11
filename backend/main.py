from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import duckdb
import os
from random import Random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, adjust as necessary for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/favicon.ico")
async def favicon():
    return {"message": "This is the favicon endpoint"}


# Construct the relative path to the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'iching.db')

class Question(BaseModel):
    text: str

@app.post("/initialize-toss")
async def initialize_toss(question: Question):
    if not question.text:
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide.")

    length = len(question.text)
    modified_length = length - 1
    random_state = modified_length % 9

    return {"random_state": random_state}

class TossResults(BaseModel):
    times: List[int]
    random_state: int

@app.post("/generate-line")
async def generate_line(results: TossResults):
    if len(results.times) != 3:
        raise HTTPException(status_code=400, detail="Exactly three stop times are required.")

    rng = Random(results.random_state)
    modified_times = [(time + rng.randint(0, 99)) % 100 for time in results.times]
    values = [2 if time % 2 == 0 else 3 for time in modified_times]
    line_sum = sum(values)
    line_mapping = {6: "Old Yin", 7: "Young Yang", 8: "Young Yin", 9: "Old Yang"}
    line_type = line_mapping.get(line_sum, "Invalid combination")

    return {"line_type": line_type, "line_sum": line_sum}

class HexagramRequest(BaseModel):
    line_values: List[int]

def get_hexagram_details(hexagram_id: int):
    con = None
    try:
        con = duckdb.connect(DATABASE_PATH)
        result = con.execute(f"SELECT * FROM iching WHERE Number = {hexagram_id}").fetchone()
        return result
    finally:
        if con:
            con.close()

def get_hexagram_id_by_combination(combination: str):
    con = None
    try:
        con = duckdb.connect(DATABASE_PATH)
        result = con.execute(f"SELECT hexagram_id FROM hexagram_mapping WHERE combination = '{combination}'").fetchone()
        return result[0] if result else None
    finally:
        if con:
            con.close()

@app.post("/get-hexagram")
async def get_hexagram(request: HexagramRequest):
    if not request.line_values or len(request.line_values) != 6:
        raise HTTPException(status_code=400, detail="Exactly six line values are required.")

    combination = ''.join(map(str, request.line_values))
    hexagram_id = get_hexagram_id_by_combination(combination)

    if not hexagram_id:
        raise HTTPException(status_code=404, detail="Hexagram not found.")

    hexagram_details = get_hexagram_details(hexagram_id)

    if not hexagram_details:
        raise HTTPException(status_code=404, detail="Hexagram details not found.")

    return {"hexagram": hexagram_details}
