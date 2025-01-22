document.getElementById('queryForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the form from reloading the page
    
    const userInput = document.querySelector('#userInput').value;
    const mainDiv = document.querySelector('#main');
    
    const queryDiv = document.createElement("div");
    const responseDiv = document.createElement("div");

    queryDiv.classList.add("query");
    responseDiv.classList.add("response");

    queryDiv.textContent = userInput;
    mainDiv.appendChild(queryDiv);

    try {
      const response = await fetch('http://localhost:5000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      responseDiv.textContent = data.response; // Display the API response
      mainDiv.appendChild(responseDiv);
    }
    catch (error)
    {
      responseDiv.textContent = `Error: ${error.message}`;
    }
  });