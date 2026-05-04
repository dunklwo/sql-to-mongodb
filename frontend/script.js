async function convertQuery() {
    const query = document.getElementById("sqlInput").value;

    const response = await fetch('/convert', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
    });

    const data = await response.json();

    document.getElementById("output").innerText = data.mongo_query;
}