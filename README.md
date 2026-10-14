# MovieMind AI

A student AIML mini project: movie discovery website with a content-based recommendation demo.

## Run locally (Windows)

1. Install Python 3.10+ from https://www.python.org/downloads/ and enable "Add Python to PATH".
2. Open this folder in VS Code.
3. In Terminal run:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python app.py
   ```

4. Open http://127.0.0.1:5000 in your browser. Keep the terminal running while using the site.

If PowerShell blocks activation, skip activation and run:
`python -m pip install -r requirements.txt` then `python app.py`.

## Deploy free on Render (availability/pricing can change)

1. Create a GitHub account if you do not already have one.
2. Create a new GitHub repository named `moviemind-ai-movie-recommender`.
3. Upload/push all files and folders from this project. Make sure `app.py`, `requirements.txt`, and `Procfile` are in the repository root.
4. Sign in to https://render.com with GitHub.
5. Choose **New + → Web Service**, connect the `moviemind-ai-movie-recommender` repository.
6. Set:
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
7. Select the free plan if it is offered to your account/region and click **Deploy Web Service**.
8. Wait for the deploy to finish, then open the `https://...onrender.com` URL Render provides.

Notes:
- Free services may sleep when inactive and can take a little time to wake up. Render's free plan and availability can change.
- Movie catalogue and recommendation logic are built into `app.py`; no API key or database is needed.
- Posters load from remote image URLs, so internet access is needed for posters. If a poster URL stops working, the page shows a placeholder.
- This is a demo content-based recommender, not a production-trained AI model. Its match percentage is a simple similarity score, not a verified probability that you will like a movie.
- The project is a student demo and is not affiliated with TMDB or any streaming platform.
