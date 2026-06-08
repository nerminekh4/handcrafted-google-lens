# CLAUDE.md — Mémoire du projet handcrafted-google-lens

## Vue d'ensemble
Application web de type "Google Lens artisanal" : l'utilisateur prend ou uploade une photo, et un LLM vision décrit ce qu'il voit. Interface mobile-first.

## Stack technique
| Couche | Technologie |
|---|---|
| LLM | Groq API — `meta-llama/llama-4-scout-17b-16e-instruct` |
| Backend | Python · FastAPI · Uvicorn |
| Frontend | HTML · HTMX 1.9 · Vanilla JS · CSS (aucun framework) |
| Dépendances | `groq`, `python-dotenv`, `fastapi`, `uvicorn[standard]`, `python-multipart` |
| Déploiement | Railway (Procfile) |

## Structure du projet
```
handcrafted-google-lens/
├── app.py              # Serveur FastAPI — point d'entrée web
├── backend.py          # ImageAgent — logique LLM vision
├── context.txt         # Prompt principal (system + fallback user text)
├── prompt.txt          # (optionnel) user text alternatif — si absent, context.txt est utilisé
├── static/
│   └── index.html      # Interface utilisateur complète (HTMX + CSS + JS)
├── Procfile            # Déploiement Railway
├── requirements.txt    # Dépendances pip
├── CLAUDE.md           # Ce fichier
└── README.md
```

## Décisions d'architecture

### backend.py — ImageAgent
- `read_file(path, default="")` : lecture fichier avec fallback silencieux (FileNotFoundError).
- `prompt.txt` est **optionnel** : si absent, le contenu de `context.txt` est utilisé comme user text.
- L'image est encodée en base64 et envoyée directement à Groq (pas de stockage serveur).

### app.py — FastAPI
- `GET /` → sert `static/index.html` via `FileResponse`.
- `POST /analyze` → reçoit un `UploadFile`, écrit dans un fichier temporaire, appelle `ImageAgent.ask_vision_model`, supprime le temp, renvoie un **fragment HTML** (pas du JSON).
- Le fragment HTML retourné est swappé par HTMX dans `#result`.
- L'agent est instancié **une seule fois** au démarrage du serveur (singleton).

### Frontend (static/index.html)
- HTMX gère la soumission du formulaire (`hx-post`, `hx-target="#result"`, `hx-encoding="multipart/form-data"`).
- `hx-indicator="#spinner"` affiche un spinner pendant la requête.
- JS natif gère : aperçu de l'image avant envoi, synchronisation `cameraInput → fileInput` via `DataTransfer`, drag & drop, bouton clear.
- Le bouton caméra (`capture="environment"`) déclenche directement l'appareil photo sur mobile.
- Design : dark mode, palette violet (`#7c3aed`), mobile-first (max-width 480px).

## Variables d'environnement
| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Clé API Groq (obligatoire) |
| `PORT` | Port HTTP — injecté automatiquement par Railway |

Fichier `.env` local (non commité) :
```
GROQ_API_KEY=gsk_...
```

## Commandes utiles
```bash
# Installation
pip install -r requirements.txt

# Développement local
uvicorn app:app --reload

# Production (Railway le fait via Procfile)
uvicorn app:app --host 0.0.0.0 --port $PORT
```

## Prochaines étapes possibles
- [ ] Historique des analyses (BDD légère type SQLite ou TinyDB)
- [ ] Support multi-images
- [ ] Choix de la langue de la réponse (FR / EN / AR…)
- [ ] Authentification utilisateur
- [ ] Streaming de la réponse (SSE / HTMX SSE extension)
- [ ] Tests unitaires sur `ImageAgent`
