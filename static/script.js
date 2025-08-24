const API_BASE = "https://message-to-future.onrender.com";


const form = document.getElementById("messageForm");
const statusDiv = document.getElementById("status");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        email: form.email.value,
        subject: form.subject.value,
        message: form.message.value,
        delivery_date: form.delivery_date.value
    };

    try {
        const res = await fetch(`${API_BASE}/api/send-message`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        if (result.success) {
            statusDiv.textContent = "Message scheduled successfully!";
            statusDiv.style.color = "green";
            form.reset();
        } else {
            statusDiv.textContent = "Error: " + (result.error || "Unknown error");
            statusDiv.style.color = "red";
        }
    } catch (err) {
        statusDiv.textContent = "Network error!";
        statusDiv.style.color = "red";
        console.error(err);
    }
});
