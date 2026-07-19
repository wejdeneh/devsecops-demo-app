from flask import Flask, render_template, jsonify
from flask_talisman import Talisman
from prometheus_flask_exporter import PrometheusMetrics
import socket
import os


app = Flask(__name__)


# Disable HTTPS redirect inside Kubernetes playground
Talisman(app, force_https=False)


# Prometheus metrics
metrics = PrometheusMetrics(app)


APP_VERSION = os.getenv(
    "APP_VERSION",
    "development"
)


metrics.info(
    "devsecops_app_info",
    "DevSecOps application information",
    version=APP_VERSION
)



@app.route("/")
def home():

    return render_template(
        "index.html"
    )



@app.route("/health")
def health():

    return jsonify(
        {
            "status": "healthy",
            "application": "cloud-native-security-platform",
            "environment": "kubernetes",
            "deployment": "argocd",
            "hostname": socket.gethostname(),
            "version": APP_VERSION
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
