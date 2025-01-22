document.getElementById('queryForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the form from reloading the page
    
    const userInput = document.querySelector('#userInput');
    const mainDiv = document.querySelector('#main');

    const queryDiv = document.createElement("div");
    const responseDiv = document.createElement("div");

    queryDiv.classList.add("query");
    responseDiv.classList.add("response");

    queryDiv.textContent = userInput.value;
    mainDiv.appendChild(queryDiv);

    try {
      const serverUrl = window.location.origin; 
      const response = await fetch(`${serverUrl}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput.value }),
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