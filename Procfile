# Gunicorn production server
# -w 4      → 4 worker processes (Render free tier has 0.1 vCPU; 2-4 workers is fine)
# --timeout → worker timeout in seconds (important for slow DB cold-starts)
# --log-level → all logs go to stdout for Render to capture
web: gunicorn -w 4 --timeout 120 --log-level info -b 0.0.0.0:$PORT app:app
