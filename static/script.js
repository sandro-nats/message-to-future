// Relative API path (same server)
const API_BASE = "";

// Set min date to today
(function setMinDate() {
  const d = new Date();
  d.setHours(0,0,0,0);
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2,"0");
  const dd = String(d.getDate()).padStart(2,"0");
  document.getElementById("dateInput").setAttribute("min", `${yyyy}-${mm}-${dd}`);
})();

document.getElementById("futureForm").addEventListener("submit", async function(e){
  e.preventDefault();
  const resEl = document.getElementById("response");
  const submitBtn = document.getElementById("submitBtn");
  resEl.textContent = "";
  submitBtn.disabled = true;

  const formData = new FormData(this);

  try {
    const res = await fetch(`${API_BASE}/api/send-message`, {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    if(!res.ok) throw new Error(data.error || "Failed to schedule message.");
    resEl.textContent = data.message || "Scheduled!";
    this.reset();
  } catch(err){
    resEl.textContent = "Error: " + err.message;
  } finally {
    submitBtn.disabled = false;
  }
});
