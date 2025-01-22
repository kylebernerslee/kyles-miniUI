document.getElementById('queryForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the form from reloading the page
    
    const userInput = document.getElementById('userInput').value;
    const queryDiv = document.getElementById('query');
    const responseDiv = document.getElementById('response');
    
    queryDiv.textContent = userInput;

    console.log(userInput);

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
    }
    catch (error)
    {
      responseDiv.textContent = `Error: ${error.message}`;
    }
  });