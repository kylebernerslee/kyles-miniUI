// Check if the unique ID already exists in localStorage
let kyles_miniUI_uniqueId = localStorage.getItem('kyles_miniUI_uniqueId');

// If the unique ID doesn't exist, create a new one and store it in localStorage
if (!kyles_miniUI_uniqueId) {
  kyles_miniUI_uniqueId = `id-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
    localStorage.setItem('kyles_miniUI_uniqueId', kyles_miniUI_uniqueId);
}

document.getElementById('queryForm').addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent the form from reloading the page
  
  const userInput = document.querySelector('#userInput');
  const mainDiv = document.querySelector('#main');

  const queryDiv = document.createElement("div");
  const responseDiv = document.createElement("div");

  queryDiv.classList.add("query");
  responseDiv.classList.add("response");

  queryDiv.textContent = userInput.value;
  mainDiv.appendChild(queryDiv);

  try {
      const serverUrl = window.location.origin; 
      const response = await fetch(`${serverUrl}/query`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              query: userInput.value,
              uniqueId: kyles_miniUI_uniqueId // Send the unique ID with the query
          }),
      });

      if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      responseDiv.textContent = data.response; // Display the API response
      mainDiv.appendChild(responseDiv);
    }    
  catch (error) {
      responseDiv.textContent = `Error: ${error.message}`;
  }
});
