# Audito: Crowdsourced Music Critics

#### GROUP-2-CSC

Audito is a music review platform where users rate and review songs, and get recommendations based on what they like.

## Features
- Song recommendations from the Kaggle Spotify Tracks dataset
- Search songs, albums, and artists
- Rate songs and albums
- Write reviews
- Follow friends and influencers to see their opinions
- Trending music and recent reviews
- Lists and collections of favorite songs
- Connect to a music streaming platform


## Tech Stack
- **Frontend:** React + Vite (styling: CSS)
- **Backend:** Flask (Python), with pandas and scikit-learn for recommendations
- **Database:** MongoDB (setup: see [backend/database/README.md](backend/database/README.md))


## Project Structure
- `frontend/`: React app
- `backend/`: Flask API (`api.py`), recommendation logic (`recommend.py`), and database code (`database/`)
- `backend/data/`: dataset (`songs.csv`)



## Running the website locally
### Prerequisites
- Node.js (LTS): https://nodejs.org/
- Python 3.10+
- `songs.csv` (Kaggle Spotify Tracks dataset) placed at `backend/data/songs.csv`

Check that everything is installed with `node -v`, `npm -v`, and `python3 --version`.

### One-time setup
**Backend** (run from the `backend/` folder):
1. `python3 -m venv .venv`
2. `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
3. `pip install -r requirements.txt`

**Frontend** (run from the `frontend/` folder):
1. `npm install`

Re-run `pip install -r requirements.txt` when `requirements.txt` changes, and `npm install` when `package.json` changes.

### Running the app
You need **two terminals**, one for the backend and one for the frontend. 
Run both from the **project root**.

**Terminal 1: backend**
- Mac & Linux: `backend/.venv/bin/python backend/api.py`
- Windows: `backend\.venv\Scripts\python.exe backend\api.py`

The API runs at http://127.0.0.1:5000. The "development server" warning is normal.

**Terminal 2: frontend**
- All systems: `npm --prefix frontend run dev`

Open the link it prints (usually http://localhost:5173/) in your browser.

To stop either server, press `Ctrl + C` in its terminal.