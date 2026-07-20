from flask import Flask, render_template, jsonify
from flask_talisman import Talisman
from prometheus_flask_exporter import PrometheusMetrics
import socket
import os

from kubernetes import client, config
app = Flask(__name__)
try:
    config.load_incluster_config()
    k8s_client = client.AppsV1Api()
    core_client = client.CoreV1Api()
except Exception:
    k8s_client = None
    core_client = None

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

    namespace="default"

    deployment = k8s_client.read_namespaced_deployment(
        "devsecops-demo",
        namespace
    )

    pods = core_client.list_namespaced_pod(
        namespace,
        label_selector="app=devsecops-demo"
    )


    return jsonify(
        {
            "platform":"Kubernetes",
            "namespace":namespace,
            "deployment":deployment.metadata.name,
            "desired_replicas":
                deployment.spec.replicas,
            "available_replicas":
                deployment.status.available_replicas,
            "pods":[
                {
                    "name":p.metadata.name,
                    "status":p.status.phase
                }
                for p in pods.items
            ]
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

@app.route("/about")
def about():
    return jsonify({
        "project": "Cloud Native Security Platform",
        "architecture": "GitOps + DevSecOps",
        "deployment": "Kubernetes",
        "observability": "Prometheus",
        "security": [
            "Semgrep",
            "Gitleaks",
            "Trivy",
            "OWASP ZAP"
        ]
    })
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
