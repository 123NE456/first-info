first info


pour le main.py simple 


# pip install fastapi uvicorn jinja2 python-multipart

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve HTML templates
templates = Jinja2Templates(directory="app/templates")

# Route pour la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})










			<!-- Formulaire de publication d'annonce -->

			<form method="post" action="/annonces"> <!-- L'action devra être configurée pour envoyer les données -->
				<div class="row gtr-uniform gtr-50">
					<div class="col-12">
						<input type="text" name="titre" id="titre" value=""
							placeholder="Titre de la publication" required />
					</div>
					<div class="col-12">
						<textarea name="description" id="description"
							placeholder="Description de l'opportunité ou contenu de la publication" rows="6"
							required></textarea>
					</div>

					<div class="col-12">
						<ul class="actions special">
							<li><input type="submit" value="Envoyer la publication" class="primary" /></li>
							<li><input type="reset" value="Réinitialiser" /></li>
						</ul>
					</div>
				</div>
			</form>
