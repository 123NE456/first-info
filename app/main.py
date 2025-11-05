# pip install fastapi uvicorn jinja2 python-multipart

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
from pydantic import BaseModel
import csv
import os

app = FastAPI()

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve HTML templates
templates = Jinja2Templates(directory="app/templates")

# Temporary storage for annonces
annonces = []

# Path du fichier CSV
CSV_FILE = "annonces.csv"

# Créer le fichier CSV avec les en-têtes si il n'existe pas
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["titre", "description", "contact", "lieu", "date"])

# Route pour la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Get all annonces (temporary storage)
@app.get("/annonces")
async def get_annonces():
    return JSONResponse(content=annonces)

# Publish a new annonce via form (HTML form submission)
@app.post("/annonces")
async def post_annonce(
    titre: str = Form(...),
    description: str = Form(...)
):
    annonce = {
        "titre": titre,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "contact": "non spécifié",
        "lieu": "non spécifié"
    }
    
    annonces.append(annonce)

    # Sauvegarde dans CSV
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([annonce["titre"], annonce["description"], annonce["contact"], annonce["lieu"], annonce["date"]])

    return {"message": "Annonce ajoutée avec succès 👍", "annonce": annonce}

# Data model pour API JSON
class Annonce(BaseModel):
    titre: str
    description: str
    contact: str
    lieu: str
    date: str = datetime.now().strftime("%Y-%m-%d")  # date par défaut

# Publish a new annonce via API (JSON)
@app.post("/api/publier-annonce")
async def publier_annonce(data: Annonce):
    print(f"📩 Nouvelle annonce reçue : titre='{data.titre}' description='{data.description}' contact='{data.contact}' lieu='{data.lieu}' date='{data.date}'")

    # Sauvegarde dans CSV
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([data.titre, data.description, data.contact, data.lieu, data.date])

    return {"message": "Annonce ajoutée avec succès 👍", "annonce": data}
