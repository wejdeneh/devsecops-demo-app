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


@app.route("/pipeline")
def pipeline():

    return jsonify(
        {
            "stages": [
                {
                    "name": "SAST",
                    "tool": "Semgrep",
                    "status": "PASSED"
                },
                {
                    "name": "Secrets Detection",
                    "tool": "Gitleaks",
                    "status": "PASSED"
                },
                {
                    "name": "Container Security",
                    "tool": "Trivy",
                    "status": "PASSED"
                },
                {
                    "name": "DAST",
                    "tool": "OWASP ZAP",
                    "status": "PASSED"
                }
            ]
        }
    )

@app.route("/runtime")
def runtime():

    return jsonify(
        {
            "platform": "Kubernetes",
            "namespace": "default",
            "deployment": "devsecops-demo",
            "replicas": 2,
            "status": "Running",
            "container": "wejdenehm/devsecops-demo"
        }
    )


@app.route("/gitops")
def gitops():

    return jsonify(
        {
            "controller": "ArgoCD",
            "sync_status": "Synced",
            "health_status": "Healthy",
            "deployment": "devsecops-demo"
        }
    )


@app.route("/metrics-summary")
def metrics_summary():

    return jsonify(
        {
            "requests": "active",
            "monitoring": "Prometheus",
            "metrics_endpoint": "/metrics"
        }
    )    
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
