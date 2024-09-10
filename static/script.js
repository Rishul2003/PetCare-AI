// static/script.js

document.getElementById('symptom-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const formData = new FormData(this); // Create a FormData object with form data

    fetch('/upload', { // Send data to the server
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display the results from the server
        console.log(data)
        document.getElementById('result').innerHTML = `
            <h3>Diagnosis Result:</h3>
            <p>${data}</p>
        `;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = `
            <p>An error occurred. Please try again later.</p>
        `;
    });
});
