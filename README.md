# 🔭 Handcrafted Google Lens

Une application web minimaliste qui utilise un modèle de vision IA pour décrire le contenu d'une photo. Prenez ou uploadez une image — le modèle vous dit ce qu'il voit.

> Propulsé par [Groq](https://groq.com) · Llama 4 Scout · FastAPI · HTMX

---

## Fonctionnalités

- 📷 Prise de photo directe depuis l'appareil mobile
- 🖼️ Upload d'image par clic ou glisser-déposer
- ⚡ Analyse rapide via Groq (inférence ultra-rapide)
- 📱 Interface mobile-first, fonctionne sur smartphone et desktop
- 🌑 Design dark mode

---

## Prérequis

- Python 3.10+
- Un compte [Groq](https://console.groq.com) avec une clé API

---

## Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/<votre-username>/handcrafted-google-lens.git
cd handcrafted-google-lens

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env et renseigner GROQ_API_KEY
```

Créer un fichier `.env` à la racine :
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

```bash
# 5. Lancer le serveur
uvicorn app:app --reload
```

Ouvrir [http://localhost:8000](http://localhost:8000).

Pour accéder depuis un smartphone sur le même réseau Wi-Fi :
```bash
uvicorn app:app --host 0.0.0.0 --reload
# puis ouvrir http://<IP-locale>:8000 sur le téléphone
```

---

## Structure du projet

```
handcrafted-google-lens/
├── app.py          # Serveur FastAPI (endpoints web)
├── backend.py      # ImageAgent — appel au modèle vision Groq
├── context.txt     # Prompt envoyé au modèle
├── static/
│   └── index.html  # Interface utilisateur (HTMX + CSS + JS)
├── Procfile        # Déploiement Railway
├── requirements.txt
└── .env            # Variables d'environnement (non commité)
```

---

## Personnaliser le prompt

Éditez `context.txt` pour modifier la consigne donnée au modèle. Exemples :

```
# Description générale
Analyse cette image et dis moi ce que tu vois.

# Mode expert
Tu es un expert en botanique. Identifie la plante sur cette image et donne ses caractéristiques.

# Mode accessibilité
Décris cette image de façon détaillée pour une personne malvoyante.
```

---

## Déploiement sur Railway

### 1. Préparer le dépôt

Assurez-vous que `.env` est dans `.gitignore` :
```bash
echo ".env" >> .gitignore
git add .
git commit -m "chore: add Railway deployment files"
git push
```

### 2. Créer le projet sur Railway

1. Aller sur [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
2. Sélectionner ce dépôt
3. Railway détecte automatiquement le `Procfile`

### 3. Ajouter la variable d'environnement

Dans Railway → Settings → Variables :
```
GROQ_API_KEY = gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

Railway injecte `PORT` automatiquement — l'application s'y connecte via `$PORT`.

### 4. Déployer

Cliquer **Deploy** ou pousser un commit — Railway redéploie automatiquement.

---

## Variables d'environnement

| Variable | Obligatoire | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Clé API Groq |
| `PORT` | Auto (Railway) | Port HTTP — injecté par la plateforme |

---

## Modèle utilisé

`meta-llama/llama-4-scout-17b-16e-instruct` via l'API Groq.  
Peut être changé dans `backend.py` → `ask_vision_model` → paramètre `model`.

---

## Licence

MIT
