const API_URL = "https://fe221mvva7.execute-api.ca-central-1.amazonaws.com/prod";

async function submitIncident() {
    const type = document.getElementById("type").value;
    const location = document.getElementById("location").value;
    const description = document.getElementById("description").value;
    const fileInput = document.getElementById("imageFile");

    let fileKey = null;

    if (fileInput.files.length > 0) {
        // Step 1: Get upload URL
        const uploadResponse = await fetch(`${API_URL}/upload-url`);
        const uploadData = await uploadResponse.json();

        fileKey = uploadData.fileKey;

        // Step 2: Upload file directly to S3
        await fetch(uploadData.uploadUrl, {
            method: "PUT",
            body: fileInput.files[0]
        });
    }

    // Step 3: Create incident
    await fetch(`${API_URL}/incidents`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            type,
            location,
            description,
            fileKey
        })
    });

    loadIncidents();
}

async function loadIncidents() {
    const response = await fetch(`${API_URL}/incidents`);
    const incidents = await response.json();

    const list = document.getElementById("incidentList");
    list.innerHTML = "";

    incidents.forEach(i => {
        const div = document.createElement("div");
        div.className = "incident";

        div.innerHTML = `
            <strong>${i.type}</strong><br/>
            Location: ${i.location}<br/>
            Status: ${i.status}<br/>
            ${i.imageUrl ? `<img src="${i.imageUrl}" width="200"/>` : ""}
        `;

        list.appendChild(div);
    });
}

window.onload = loadIncidents;