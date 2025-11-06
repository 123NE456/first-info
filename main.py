# pip install fastapi uvicorn jinja2 python-multipart

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
from pydantic import BaseModel
from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Serve templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Fichier JSON
JSON_FILE = BASE_DIR / "annonces.json"

# ✅ Si le fichier n'existe pas, on le crée
if not JSON_FILE.exists():
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

# ✅ Fonction pour lire les annonces
def lire_annonces():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
        return []

# ✅ Fonction pour sauvegarder les annonces
def sauvegarder_annonces(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Home
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Récupérer toutes les annonces
@app.get("/annonces")
async def get_annonces():
    return JSONResponse(content=lire_annonces())

# ✅ Model pour API JSON
class Annonce(BaseModel):
    titre: str
    description: str
    lien: str
    contact: str

# ✅ Validation contact côté serveur
def is_valid_contact(contact: str) -> bool:
    # Email simple ou numéro
    pattern = re.compile(r"^([+]?[\d]{7,15}|[\w.-]+@[\w.-]+\.\w{2,})$")
    return bool(pattern.match(contact))

# ✅ API pour recevoir annonce JSON
@app.post("/api/publier-annonce")
async def publier_annonce(data: Annonce):
    # Validation minimale côté serveur
    if not data.titre.strip() or not data.description.strip():
        raise HTTPException(status_code=400, detail="Titre et description obligatoires")

    if not data.lien.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Lien invalide : doit commencer par http:// ou https://")

    if not is_valid_contact(data.contact):
        raise HTTPException(status_code=400, detail="Contact invalide : doit être un email ou un numéro valide")

    annonces = lire_annonces()

    nouvelle_annonce = {
        "titre": data.titre.strip(),
        "description": data.description.strip(),
        "lien": data.lien.strip(),
        "contact": data.contact.strip(),
        "date_publication": datetime.now().strftime("%Y-%m-%d")
    }

    annonces.append(nouvelle_annonce)
    sauvegarder_annonces(annonces)

    print(f"✅ Nouvelle annonce enregistrée : {nouvelle_annonce['titre']}")

    return {"message": "Annonce ajoutée avec succès", "annonce": nouvelle_annonce}
