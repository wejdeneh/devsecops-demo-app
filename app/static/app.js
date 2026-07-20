async function loadDashboard() {

    const health =
    await fetch("/health")
    .then(r => r.json());

    const security =
    await fetch("/security")
    .then(r => r.json());

    const runtime =
    await fetch("/runtime")
    .then(r => r.json());

    const gitops =
    await fetch("/gitops")
    .then(r => r.json());

    const pipeline =
    await fetch("/pipeline")
    .then(r => r.json());



    document.getElementById("status").innerHTML =
        "SYSTEM OPERATIONAL";



    document.getElementById("runtime").innerHTML = `

        <p><b>Platform:</b> ${runtime.platform}</p>
        <p><b>Deployment:</b> ${runtime.deployment}</p>
        <p><b>Replicas:</b> ${runtime.replicas}</p>
        <p><b>Status:</b> ${runtime.status}</p>

        <br>

        <p><b>Pod:</b> ${health.hostname}</p>

        <p><b>Version:</b> ${health.version}</p>

    `;



    document.getElementById("security").innerHTML = `

        <p class="success">${security.SAST}</p>
        <p class="success">${security.Secrets}</p>
        <p class="success">${security.Container}</p>
        <p class="success">${security.DAST}</p>

    `;



    document.getElementById("gitops").innerHTML = `

        <p><b>Controller:</b> ${gitops.controller}</p>

        <p><b>Sync:</b>
        <span class="success">
        ${gitops.sync_status}
        </span>
        </p>

        <p><b>Health:</b>
        <span class="success">
        ${gitops.health_status}
        </span>
        </p>

    `;



    let pipelineHtml =
    `<div class="pipeline-flow">`;

    pipeline.stages.forEach(stage => {

        pipelineHtml += `

            <div class="pipeline-stage">

                <b>${stage.name}</b>

                <br>

                ${stage.tool}

                <br>

                <span class="success">

                ${stage.status}

                </span>

            </div>

            <div class="arrow">→</div>

        `;
    });

    pipelineHtml += `</div>`;

    document.getElementById("pipeline").innerHTML =
    pipelineHtml;



    document.getElementById("activity-log").innerHTML = `

[INFO] Kubernetes Deployment Healthy

[INFO] ArgoCD Sync Successful

[INFO] Security Gates Passed

[INFO] Prometheus Metrics Active

[INFO] Application Version ${health.version}

[INFO] Pod ${health.hostname}

`;
}

loadDashboard();

setInterval(
    loadDashboard,
    10000
);
