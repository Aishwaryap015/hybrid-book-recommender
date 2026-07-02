// 1. Define the App Object to fix the "Undefined" error in image_1e169a.png
window.DoodleApp = {
    setView: (viewName) => {
        const container = document.getElementById('vault-content'); // Ensure this ID exists in your modal
        if (views[viewName]) {
            container.innerHTML = views[viewName]();
        }
    }
};

// 2. 2-Second Center Pop-up (The "Small pop-up")
window.showPopup = (message, callback) => {
    const el = document.createElement('div');
    el.className = "fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-[#f1b40e] text-black px-10 py-5 rounded-2xl font-black z-[10002] shadow-2xl animate-pulse";
    el.innerText = message;
    document.body.appendChild(el);
    setTimeout(() => {
        el.remove();
        if (callback) callback();
    }, 2000);
};

// 3. Register Function with Alphanumeric Check
window.submitRegister = async () => {
    const p1 = document.getElementById('reg-pass').value;
    const p2 = document.getElementById('reg-confirm').value;
    const regex = /^(?=.*[A-Z])(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{6,}$/;

    if (p1 !== p2) { alert("password doesn't matched"); return; }
    if (!regex.test(p1)) { alert("Use format: Abcd@5 (6+ chars, 1 Cap, 1 Special)"); return; }

    // This sends data to your Django view to save in MongoDB
    const res = await fetch('/api/register/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
       body: JSON.stringify({
    first: document.getElementById('reg-first').value,
    last: document.getElementById('reg-last').value,
    email: document.getElementById('reg-email').value,
    pass: p1,
    confirm: p2
})
    });

  const data = await res.json();

console.log(data);

if (res.ok) {

    showPopup("USER REGISTERED!", () => {
        document.getElementById('vaultModal').classList.add('hidden');
        document.getElementById('prefModal').classList.remove('hidden');
    });

} else {

    alert(data.message || "Registration failed");

}
};

// 4. Preference Logic (Pick 3)
let selectedInterests = [];
window.toggleInterest = (btn, genre) => {
    btn.classList.toggle('bg-yellow-500');
    btn.classList.toggle('text-black');
    if (selectedInterests.includes(genre)) {
        selectedInterests = selectedInterests.filter(i => i !== genre);
    } else {
        selectedInterests.push(genre);
    }
    const saveBtn = document.getElementById('savePrefBtn');
    saveBtn.disabled = selectedInterests.length < 3;
    saveBtn.style.opacity = selectedInterests.length >= 3 ? "1" : "0.5";
    saveBtn.style.cursor = selectedInterests.length >= 3 ? "pointer" : "not-allowed";
};