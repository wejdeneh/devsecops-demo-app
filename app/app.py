from flask import Flask, render_template, jsonify
from flask_talisman import Talisman
from prometheus_flask_exporter import PrometheusMetrics
import socket


app = Flask(__name__)


# Security headers
Talisman(app)


# Prometheus metrics
metrics = PrometheusMetrics(app)

metrics.info(
    "devsecops_app_info",
    "DevSecOps application information",
    version="1.0"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():

    return jsonify(
        {
            "status": "healthy",
            "application": "devsecops-demo",
            "environment": "kubernetes",
            "deployment": "argocd",
            "hostname": socket.gethostname()
        }
    )


@app.route("/security")
def security():

    return jsonify(
        {
            "SAST": "Semgrep PASSED",
            "Secrets": "Gitleaks PASSED",
            "Container": "Trivy PASSED",
            "DAST": "OWASP ZAP PASSED"
        }
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
