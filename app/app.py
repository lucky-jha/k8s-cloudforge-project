import json
import logging
import os
import sys
import time
from flask import Flask, jsonify , render_template

# Structured JSON logging so every log line is machine-parsable.
logging.basicConfig(
    stream=sys.stdout,
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',
)
logger = logging.getLogger("cloudforge")

app = Flask(__name__)

START_TIME = time.time()
VERSION = os.getenv("APP_VERSION", "dev")


@app.route("/health")
def health():
    """Readiness/liveness probe target. Returns 200 when the app is up."""
    return jsonify(status="ok", version=VERSION), 200


@app.route("/")
def index():
    logger.info("index page serve")
    return render_template(
        "index.html",
        version=VERSION,
        uptime_seconds=round(time.time() - START_TIME, 2),
    ), 200

@app.route("/api/info")
def info():
    """Machine-readable info used by test , curl , and rollback demo."""
    logger.info("info endpoint hit")
    return jsonify(
        service="cloudforge-app",
        version=VERSION,
        uptime_seconds=round(time.time() - START_TIME, 2),
    ), 200

@app.route("/api/work")
def work():
    """A trivial 'real' endpoint that produces a log line and a JSON body."""
    logger.info("work endpoint hit")
    return jsonify(task="done", result=42), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)