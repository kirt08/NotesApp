const form = document.querySelector(".registration_form")
const button_sign_up = document.querySelector(".registration_form_button_sign_up")
const button_login = document.querySelector(".registration_form_button_login")

button_sign_up.addEventListener("click", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form))

    const response = await fetch("http://127.0.0.1:8000/users/create", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if (response.ok === false) {
        const p_error = document.querySelector(".registration_form_error_p")
        p_error.textContent = "User with this login already exists."
        return;
    }
    
    window.location.href = "http://127.0.0.1:5500/frontend/main_page_notes/main_page.html";  
});

button_login.addEventListener("click", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form))

    const response = await fetch("http://127.0.0.1:8000/users/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if (response.ok == false) {
        const p_error = document.querySelector(".registration_form_error_p")
        p_error.textContent = "Incorrect login or password"
        return;
    }
    window.location.href = "http://127.0.0.1:5500/frontend/main_page_notes/main_page.html";
});