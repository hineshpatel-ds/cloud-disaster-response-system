// const API_URL = "https://fe221mvva7.execute-api.ca-central-1.amazonaws.com/prod";

// async function submitIncident() {
//     const typeInput = document.getElementById("type");
//     const locationInput = document.getElementById("location");
//     const descriptionInput = document.getElementById("description");
//     const fileInput = document.getElementById("imageFile");

//     const type = typeInput.value;
//     const location = locationInput.value;
//     const description = descriptionInput.value;

//     if (!type || !location || !description) {
//         alert("Please fill all required fields.");
//         return;
//     }

//     let fileKey = null;

//     try {
//         if (fileInput.files.length > 0) {
//             const file = fileInput.files[0];

//             if (!file.type.startsWith("image/")) {
//                 alert("Only image files are allowed.");
//                 return;
//             }

//             if (file.size > 5 * 1024 * 1024) {
//                 alert("Image must be smaller than 5MB.");
//                 return;
//             }

//             // Step 1: Get upload URL
//             const uploadResponse = await fetch(`${API_URL}/upload-url`);
//             const uploadData = await uploadResponse.json();
//             fileKey = uploadData.fileKey;

//             // Step 2: Upload file directly to S3
//             await fetch(uploadData.uploadUrl, {
//                 method: "PUT",
//                 body: file
//             });
//         }

//         // Step 3: Create incident
//         await fetch(`${API_URL}/incidents`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ type, location, description, fileKey })
//         });

//         alert("Incident reported successfully!");

//         // ✅ Clear form fields
//         typeInput.value = "";
//         locationInput.value = "";
//         descriptionInput.value = "";
//         fileInput.value = "";

//         // ✅ Refresh the list once
//         loadIncidents();

//     } catch (error) {
//         console.error("Error submitting incident:", error);
//         alert("Failed to submit incident. Check console for details.");
//     }
// }

// async function loadIncidents() {
//     try {
//         const response = await fetch(`${API_URL}/incidents`);
//         const incidents = await response.json();

//         const list = document.getElementById("incidentList");
//         list.innerHTML = "";

//         incidents.forEach(i => {
//             const div = document.createElement("div");
//             div.className = "incident";

//             div.innerHTML = `
//                 <strong>${i.type}</strong><br/>
//                 Location: ${i.location}<br/>
//                 Status: ${i.status}<br/>
//                 ${i.imageUrl ? `<img src="${i.imageUrl}" width="200" alt="Incident Image"/>` : ""}
//             `;
//             list.appendChild(div);
//         });
//     } catch (error) {
//         console.error("Error loading incidents:", error);
//     }
// }

// window.onload = loadIncidents;