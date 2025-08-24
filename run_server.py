import os
from app import app, start_scheduler

if __name__ == "__main__":
    start_scheduler()  # Start scheduler
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
