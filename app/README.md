# Frontend (FastAPI + Tailwind demo)

This folder contains a minimal FastAPI app that demonstrates a simple doctor/patient register & login flow and a session page. It's intentionally minimal and uses an in-memory store (no DB) for quick prototyping.

Run locally:

```bash
cd raspberry/app/frontend
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/

Notes:
- Uses Tailwind via CDN for quick styling.
- This is a demo; do not use the in-memory store in production.
