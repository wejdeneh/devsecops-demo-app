async function loadData(){


const health =
await fetch("/health")
.then(r=>r.json());


document.getElementById("status")
.innerHTML =
`
🟢 SYSTEM OPERATIONAL
<br>
Version:
${health.version}
`;



const runtime =
await fetch("/runtime")
.then(r=>r.json());


document.getElementById("runtime")
.innerHTML =
`
<p>Platform:
<b>${runtime.platform}</b>
</p>

<p>
Container:
<b>${runtime.container}</b>
</p>

<p>
Replicas:
<b>${runtime.replicas}</b>
</p>

`;



const gitops =
await fetch("/gitops")
.then(r=>r.json());


document.getElementById("gitops")
.innerHTML =
`
<p>
Controller:
<b>${gitops.controller}</b>
</p>

<p class="success">
${gitops.sync_status}
</p>

<p class="success">
${gitops.health_status}
</p>
`;




const pipeline =
await fetch("/pipeline")
.then(r=>r.json());



document.getElementById("pipeline")
.innerHTML =
pipeline.stages.map(stage=>


`
<div class="pipeline-item">

${stage.name}

<br>

<span class="success">
${stage.tool}
✓ ${stage.status}
</span>


</div>

`

).join("");




const security =
await fetch("/security")
.then(r=>r.json());


document.getElementById("security")
.innerHTML =


Object.entries(security)
.map(
item =>

`
<div class="pipeline-item">

${item[0]}

<br>

<span class="success">
${item[1]}
</span>


</div>
`

)
.join("");



}


loadData();
