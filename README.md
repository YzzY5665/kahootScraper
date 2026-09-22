# Kahoot Scraper

Small Flask API that proxies Kahoot's internal quiz endpoint so it can be
called from a browser (Godot Web Export) without hitting CORS/mixed-content
issues.

Live at https://kahootscraper.onrender.com — access is restricted to
browser requests from `yzzy.online` and its subdomains via CORS.

## Endpoints

- `GET /scrape?quiz_id=<alphanumeric id>` — fetches
  `https://kahoot.it/rest/kahoots/<quiz_id>` and returns the JSON, or a JSON
  `{"error": "..."}` with a 4xx/5xx status on failure.
- `GET /` — health check, returns a plain-text string.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

Serves on `http://localhost:10000`.

## Frontend

[docs/index.html](docs/index.html) is a plain HTML/JS page that calls
`/scrape` and dumps the raw JSON response. It's served via GitHub Pages
(Settings → Pages → Deploy from branch `main`, folder `/docs`), and should
be mapped to a `yzzy.online` subdomain to satisfy the API's CORS rule.

## Deployment

Deployed to [Render](https://render.com) via [render.yaml](render.yaml),
using `gunicorn` in production.
