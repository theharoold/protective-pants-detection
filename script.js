let tbody = document.getElementById("incident-tbody");

fetch('http://localhost:5000/incident')
.then(data => data.json())
.then(data => {
    let final_html = "";
    data.forEach(element => {
        final_html += "<tr " + ((element.worn != 1) ? "style='background-color:red'" : "") + "><td " + ((element.worn != 1) ? "style='color:white'" : "") + ">" + element.id + "</td><td " + ((element.worn != 1) ? "style='color:white'" : "") + ">" + element.time + "</td><td>" + ((element.worn == 1) ? "Protective pants were worn!" : "<span style='color:white;'> Protective pants were not worn!</span>") + "</td></tr>";
        console.log(final_html);
    })  
    tbody.innerHTML = final_html;
});