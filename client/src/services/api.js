export function submitNote (note) {
    return fetch("http://localhost:1337/api/notes-simples", {
        method: "POST",
        body: JSON.stringify({data: note}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json())
    .then(db_entry => {
        return fetch("http://localhost:1337/api/comentaris", {
            method: "POST",
            body: JSON.stringify({
                data: {
                    text: note.comentari,
                    nota_simple: db_entry.data.id
                }
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
    });
}