async function loadDashboard(){


const health =
await fetch("/health")
.then(r=>r.json());


document.getElementById(
"health-status"
).innerHTML =
"ONLINE ✅";


document.getElementById(
"hostname"
).innerHTML =
health.hostname;


document.getElementById(
"version"
).innerHTML =
health.version;



const pipeline =
await fetch("/pipeline")
.then(r=>r.json());



let pipelineHTML="";


pipeline.stages.forEach(stage=>{


pipelineHTML += `

<div class="pipeline-item">

${stage.name}

<br>

<strong>
${stage.tool}
</strong>

<span class="success">
✓ ${stage.status}
</span>


</div>

`;

});


document.getElementById(
"pipeline"
).innerHTML=pipelineHTML;



}



loadDashboard();
