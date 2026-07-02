/**
 * =========================================================
 * PASSWORD TOGGLE
 * =========================================================
 */

window.togglePass = function(inputId, btn) {

    const input = document.getElementById(inputId);

    if (!input) return;

    if (input.type === "password") {

        input.type = "text";
        btn.innerText = "👁️";

    } else {

        input.type = "password";
        btn.innerText = "🙈";
    }
};


/**
 * =========================================================
 * TOAST NOTIFICATION
 * =========================================================
 */

window.showToast = function(msg, callback) {

    const toast = document.createElement('div');

    toast.className =
        "fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-[#f1b40e] text-black px-8 py-4 rounded-xl font-black z-[9999] shadow-2xl border-2 border-black text-center";

    toast.style.minWidth = "280px";

    toast.innerText = msg;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.remove();

        if (callback) callback();

    }, 2000);
};


/**
 * =========================================================
 * REGISTER
 * =========================================================
 */

window.submitRegister = async function() {

    const first =
        document.getElementById('reg-first').value.trim();

    const last =
        document.getElementById('reg-last').value.trim();

    const email =
        document.getElementById('reg-email').value.trim();

    const pass =
        document.getElementById('reg-pass').value;

    const confirm =
        document.getElementById('reg-confirm').value;


    // =====================================================
    // VALIDATION
    // =====================================================

    const passRegex =
        /^(?=.*[A-Z])(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{6,}$/;

    if (!first || !email) {

        alert("First Name and Email are required.");
        return;
    }

    if (pass !== confirm) {

        alert("Passwords do not match!");
        return;
    }

    if (!passRegex.test(pass)) {

        alert(
            "Password must contain 1 Capital letter and 1 Special character."
        );

        return;
    }


    // =====================================================
    // CSRF TOKEN
    // =====================================================

    const csrfToken =
        document.querySelector('[name=csrfmiddlewaretoken]')
            ? document.querySelector('[name=csrfmiddlewaretoken]').value
            : getCookie('csrftoken');


    // =====================================================
    // DATA
    // =====================================================

    const data = {

        first: first,
        last: last,
        email: email,
        pass: pass,
        confirm: confirm
    };


    // =====================================================
    // API CALL
    // =====================================================

    try {

        const response = await fetch('/register/', {

            method: 'POST',

            headers: {

                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },

            body: JSON.stringify(data)
        });

        const result = await response.json();

        // =================================================
        // SUCCESS
        // =================================================

        if (result.status === 'success') {

            window.showToast(
                "USER REGISTERED SUCCESSFULLY!",
                () => {

                   window.location.reload();
                }
            );

        } else {

           if (result.message && result.message.toLowerCase().includes("email")) {
    showInputError("reg-email", "Email already registered");
} else {
    window.showToast(result.message || "Registration failed.");
}
        }

    } catch (err) {

        console.error("Register Error:", err);

        alert("An error occurred during registration.");
    }
};


/**
 * =========================================================
 * LOGIN
 * =========================================================
 */

window.submitLogin = async function() {

    const username =
        document.getElementById('login-user').value;

    const password =
        document.getElementById('login-pass').value;

    try {

        const response = await fetch('/login/', {

            method: 'POST',

            headers: {

                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },

            body: JSON.stringify({
                username,
                password
            })
        });

        const result = await response.json();

        if (result.status === 'success') {

            window.showToast(
                "LOGIN SUCCESSFUL!",
                () => {

                   window.location.reload();
                }
            );

        } else {

            showInputError("login-user", "Wrong username or email");
showInputError("login-pass", "Wrong password");
window.showToast("Wrong Password / Username");
        }

    } catch (err) {

        console.error("Login Error:", err);

        alert("Login failed.");
    }
};


/**
 * =========================================================
 * GUEST LOGIN
 * =========================================================
 */

window.submitGuest = async function() {

    try {

        const response = await fetch('/guest-login/', {

            method: 'POST',

            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const result = await response.json();

        if (result.status === 'success') {

            window.showToast(
                "GUEST LOGIN SUCCESSFUL!",
                () => {

                  window.location.reload();
                }
            );
        }

    } catch (err) {

        console.error("Guest Error:", err);

        alert("Guest login failed.");
    }
};


/**
 * =========================================================
 * FORGOT PASSWORD
 * =========================================================
 */

window.showForgot = function() {

    const container =
        document.getElementById('login-container');

    if (!container) return;

    container.innerHTML = `

        <div class="animate-in fade-in duration-500">

            <h2 class="text-white font-black text-xs mb-4 uppercase tracking-widest">
                Reset Password
            </h2>

            <input
                type="text"
                id="forgot-id"
                placeholder="Enter Registered Email / Username"
                class="w-full bg-slate-800 border-none rounded-xl p-3.5 text-xs text-white outline-none mb-4"
            >

            <button
                onclick="submitForgot()"
                class="w-full bg-[#f1b40e] text-black font-black py-3 rounded-xl text-[10px] uppercase"
            >
                Submit Request
            </button>

            <button
                onclick="location.reload()"
                class="w-full text-slate-500 text-[9px] mt-4 uppercase font-bold text-center"
            >
                Back to Login
            </button>

        </div>
    `;
};


window.submitForgot = function() {

    window.showToast(
        "Password reset link sent to your registered email."
    );
};




/**
 * =========================================================
 * CSRF COOKIE HELPER
 * =========================================================
 */

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (
                cookie.substring(0, name.length + 1)
                === (name + '=')
            ) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }
        }
    }

    return cookieValue;
}



window.setTheme = function(mode) {
    localStorage.setItem("themeMode", mode);

    document.body.classList.remove(
        "theme-light",
        "theme-dark",
        "theme-reader",
        "theme-pink"
    );

    document.body.classList.add("theme-" + mode);

    showToast("Theme Updated");
};

window.autoSyncLibrary = function() {
    showToast("Library synced successfully!");
};

function showInputError(inputId, message) {
    const input = document.getElementById(inputId);

    if (!input) return;

    input.classList.add("border-2", "border-red-500");
    input.value = "";
    input.placeholder = message;
}

document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("themeMode");
    if (savedTheme) {
        document.body.classList.add("theme-" + savedTheme);
    }
});

window.addToLibrary = function(id, title, imageUrl) {
    let library = JSON.parse(localStorage.getItem("my_library") || "[]");

    if (!library.find(book => book.id === id)) {
        library.push({ id, title, imageUrl });
    }

    localStorage.setItem("my_library", JSON.stringify(library));
    showToast("Added to My Library ❤️");
};

window.showMyLibrary = function() {
    const library = JSON.parse(localStorage.getItem("my_library") || "[]");

    let html = `
        <div class="fixed inset-0 bg-black/70 z-[9999] flex items-center justify-center">
            <div class="bg-white w-[90%] max-w-lg rounded-2xl p-6 relative">
                <button onclick="this.closest('.fixed').remove()" class="absolute right-4 top-4 text-xl">✕</button>
                <h2 class="text-2xl font-black mb-4">📚 My Library</h2>
                <p class="text-sm mb-4">Like books to add it to library.</p>
    `;

    if (library.length === 0) {
        html += `<p class="text-slate-500">No books added yet.</p>`;
    } else {
        library.forEach(book => {
            html += `
                <div class="flex justify-between items-center border-b py-2">
                    <span class="font-bold text-sm">${book.title}</span>
                    <button onclick="removeFromLibrary('${book.id}')" class="text-red-500 font-black">Remove</button>
                </div>
            `;
        });
    }

    html += `
                <button onclick="clearMyLibrary()" class="mt-5 bg-red-500 text-white px-4 py-2 rounded-xl font-black text-xs">
                    Delete All Books
                </button>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML("beforeend", html);
};

window.removeFromLibrary = function(id) {
    let library = JSON.parse(localStorage.getItem("my_library") || "[]");
    library = library.filter(book => book.id !== id);
    localStorage.setItem("my_library", JSON.stringify(library));
    location.reload();
};

window.clearMyLibrary = function() {
    localStorage.removeItem("my_library");
    location.reload();
};

window.scrollRow = function(id, direction) {

    const row = document.getElementById(id);

    if (!row) return;

    row.scrollBy({
        left: direction * 400,
        behavior: 'smooth'
    });
};

window.showCategoryBooks = function(category) {

    showToast(
        `Top rated ${category} books coming soon 📚`
    );
};