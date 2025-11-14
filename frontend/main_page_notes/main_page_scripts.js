const form = document.querySelector(".note_form")
const titleInput = form.querySelector("input[name='title']");
const textInput = form.querySelector("textarea[name='text']");
const authorInput = form.querySelector("input[name='author_name']");
const error_p = document.querySelector(".note_error_p")

const createNoteButton = document.querySelector("#create_btn")
createNoteButton.addEventListener("click", async (e) => {
    e.preventDefault()

    const data = {
        title: titleInput.value,
        text: textInput.value,
        author_name: authorInput.value
    };

    const response = await fetch("http://127.0.0.1:8000/notes/create", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const result = await response.json();
        errorP.textContent = result.detail || "Ошибка при создании заметки";
        return;
    }

    const result = await response.json();
    alert(result.data);
});

const updateButton = document.querySelector("#update_btn")
updateButton.addEventListener("click", async (e) => {
    e.preventDefault();

    const data = {
        title: titleInput.value,
        text: textInput.value
    };

    const user = { login: authorInput.value };

    const response = await fetch("http://127.0.0.1:8000/notes/update_note", {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ note: data, user })
    });

    if (!response.ok) {
        const result = await response.json();
        errorP.textContent = result.detail || "Ошибка при обновлении заметки";
        return;
    }

    const result = await response.json();
    alert(result.data);
});

const commitButton = document.querySelector("#commit_btn")
commitButton.addEventListener("click", async (e) => {
    e.preventDefault()
    const author_name = authorInput.value;

    const response = await fetch("http://127.0.0.1:8000/dolt/commit", {
        method: "GET",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_name: author_name })
    });

    const result = await response.json();
    alert(result.data);
});

const showButton = document.querySelector("#show_btn")
showButton.addEventListener("click", async (e) => {
    e.preventDefault()
    const author_name = authorInput.value

    const response = await fetch(`http://127.0.0.1:8000/notes/show/${author_name}`);
    const result = await response.json();

    if (!response.ok) {
        errorP.textContent = result.detail || "Ошибка при получении заметки";
        return;
    }
    console.log(result)
    titleInput.value = result[0].title
    textInput.value = result[0].text
})