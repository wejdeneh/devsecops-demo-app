async function fetchJSON(url){

    const response = await fetch(url);

    return await response.json();

}



async function loadRuntime(){


    try {


        const health =
            await fetchJSON("/health");


        document
        .getElementById("hostname")
        .innerText =
        health.hostname;



        document
        .getElementById("version")
        .innerText =
        health.version;



        document
        .getElementById("environment")
        .innerText =
        health.environment;



        const runtime =
            await fetchJSON("/runtime");



        document
        .getElementById("platform")
        .innerText =
        runtime.platform;



        document
        .getElementById("replicas")
        .innerText =
        runtime.replicas;



    }


    catch(error){

        console.error(
            "Runtime loading failed",
            error
        );

    }


}





async function loadGitOps(){


    try {


        const data =
        await fetchJSON("/gitops");



        document
        .getElementById("sync")
        .innerText =
        data.sync_status;



        document
        .getElementById("health")
        .innerText =
        data.health_status;



    }


    catch(error){

        console.error(
            "GitOps loading failed",
            error
        );

    }


}





async function loadPipeline(){


    try {


        const data =
        await fetchJSON("/pipeline");



        const container =
        document.getElementById(
            "pipeline"
        );



        container.innerHTML="";



        data.stages.forEach(stage=>{


            container.innerHTML += `


            <div class="pipeline-item">


                <div>


                    <strong>
                    ${stage.name}
                    </strong>


                    <br>


                    <small>
                    ${stage.tool}
                    </small>


                </div>



                <span class="badge">

                ${stage.status}

                </span>


            </div>


            `;


        });



    }


    catch(error){


        console.error(
            "Pipeline loading failed",
            error
        );


    }


}






async function refreshDashboard(){


    await loadRuntime();

    await loadGitOps();

    await loadPipeline();


}





refreshDashboard();


// refresh every 30 seconds

setInterval(
    refreshDashboard,
    30000
);
