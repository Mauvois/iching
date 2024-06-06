from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import duckdb
import os
from random import Random

app = FastAPI()

# Chemin absolu vers la base de données dans le répertoire 'data'
DATABASE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'data', 'iching.db'))

@app.get("/")
async def read_root():
    return {"message": "Welcome to the I Ching Digital Project API"}

class Question(BaseModel):
    text: str

@app.post("/initialize-toss")
async def initialize_toss(question: Question):
    if not question.text:
        raise HTTPException(
            status_code=400, detail="La question ne peut pas être vide.")

    # Calculer la longueur de la question
    length = len(question.text)

    # Appliquer la logique du principe cosmique de l'unité
    modified_length = length - 1

    # Calculer le random state avec modulo 9
    random_state = modified_length % 9

    # Renvoyer le random state
    return {"random_state": random_state}

class TossResults(BaseModel):
    times: List[int]
    random_state: int

@app.post("/generate-line")
async def generate_line(results: TossResults):
    if len(results.times) != 3:
        raise HTTPException(
            status_code=400, detail="Exactly three stop times are required.")

    # Utiliser le random_state pour initialiser le générateur aléatoire
    rng = Random(results.random_state)

    # Combiner les temps d'arrêt avec une valeur générée
    modified_times = [(time + rng.randint(0, 99)) % 100 for time in results.times]

    # Calculate yin (2) or yang (3) based on even or odd values
    values = [2 if time % 2 == 0 else 3 for time in modified_times]
    line_sum = sum(values)

    # Map sum to I Ching line
    line_mapping = {6: "Old Yin", 7: "Young Yang",
                    8: "Young Yin", 9: "Old Yang"}
    line_type = line_mapping.get(line_sum, "Invalid combination")

    return {"line_type": line_type, "line_sum": line_sum}

class HexagramRequest(BaseModel):
    line_values: List[int]

def get_hexagram_details(hexagram_id: int):
    con = duckdb.connect(DATABASE_PATH)
    result = con.execute(
        f"SELECT * FROM iching WHERE Number = {hexagram_id}").fetchone()
    con.close()
    return result

def get_hexagram_id_by_combination(combination: str):
    con = duckdb.connect(DATABASE_PATH)
    result = con.execute(
        f"SELECT hexagram_id FROM hexagram_mapping WHERE combination = '{combination}'").fetchone()
    con.close()
    return result[0] if result else None

@app.post("/get-hexagram")
async def get_hexagram(request: HexagramRequest):
    if not request.line_values or len(request.line_values) != 6:
        raise HTTPException(
            status_code=400, detail="Exactly six line values are required.")

    # Convertir les valeurs de lignes en une chaîne de caractères pour la recherche
    combination = ''.join(map(str, request.line_values))

    # Récupérer l'ID de l'hexagramme correspondant
    hexagram_id = get_hexagram_id_by_combination(combination)

    if not hexagram_id:
        raise HTTPException(status_code=404, detail="Hexagram not found.")

    # Récupérer les détails de l'hexagramme
    hexagram_details = get_hexagram_details(hexagram_id)

    if not hexagram_details:
        raise HTTPException(
            status_code=404, detail="Hexagram details not found.")

    return {"hexagram": hexagram_details}
