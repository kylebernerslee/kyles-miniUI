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
  let responseText = "";  // To accumulate the streamed response

  const queryDiv = document.createElement("div");
  queryDiv.classList.add("query");
  queryDiv.textContent = userInput.value;
  mainDiv.appendChild(queryDiv);

  const responseDiv = document.createElement("div");
  responseDiv.classList.add("response");

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

    // Create a reader from the streamed response
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let done, value;

    // Read the stream chunk-by-chunk
    while (true) {
      ({ done, value } = await reader.read());
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      responseText += chunk;

      // Update the DOM incrementally with the new content
      responseDiv.textContent = responseText;
      mainDiv.appendChild(responseDiv);
    }
  } catch (error) {
    responseDiv.textContent = `Error: ${error.message}`;
  }
});
