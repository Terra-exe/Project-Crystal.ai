<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Transcribe Youtube to Summary Audio</title>

    <style>
      .file-list-item {
        display: flex;
        justify-content: space-between;
        align-items: left;
      }
    </style>

  </head>



{% include "navbar.php" %}
{% include "pagetitle.php" %}

<h>Transcribe Youtube to Summary Audio</h>

<form id="transcriptionForm">
      <table style="width: 100%">
        <tbody>
          <tr>
            <td>
              <label for="youtubeurl">YouTube URL:</label>
            </td>
            <td>
              <input type="text" class="form-control" id="youtubeurl" name="youtubeurl" placeholder="Enter YouTube URL" required>
              <p id="summarytext"></p>
            </td>
          </tr>
        </tbody>
      </table>
      <button type="submit" class="btn btn-primary">Submit</button>
</form>

<br>
<br>
<h1>List of Summary Files</h1>
    <ul id="file-list"></ul>


<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>

      // send a GET request to retrieve the summary file list
  fetch("/app1/list_summary_files")
    .then(response => response.json())
    .then(data => {
      // get the file-list element
      const fileList = document.getElementById("file-list");

      // loop through each file and create a list item with a link
      data.forEach(file => {
        const li = document.createElement("li");
        li.className = "file-list-item";


        // create a delete button with a red X
        const deleteButton = document.createElement("button");
          deleteButton.innerHTML = "❌";
          deleteButton.style.color = "red";
          // add a click listener to the delete button
          deleteButton.addEventListener("click", function(event) {
            event.preventDefault();
            const data = JSON.stringify({ "filename": file });
            
            // send an AJAX POST request to call the Python function
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/app1/delete-summary', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function() {
              if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                  console.log('Delete successful');
                  const jsonResponse = JSON.parse(xhr.responseText);
                  console.log("Response from delete_summary:", jsonResponse);
                  li.remove();
                } else {
                  // handle the error
                  console.error('Error:', xhr.statusText);
                }
              }
            };
            xhr.send(data);
            
            // handle the delete action here
            console.log("Delete button clicked for:", file);
        });



        const link = document.createElement("a");
        //link.href = `/app1/view_summary_file?filename=${file}`;
        link.href = "#";
        link.innerText = file;

        // add a click listener to the link
        link.addEventListener('click', function(event) {
          event.preventDefault(); // prevent the link from navigating to a new page

          const filename = link.innerText;
          const data = JSON.stringify({ "filename": filename });

          // send an AJAX request to call the Python function
          const xhr = new XMLHttpRequest();
          xhr.open('POST', '/app1/replay-summary', true);
          xhr.setRequestHeader('Content-Type', 'application/json');
          xhr.onreadystatechange = function() {
              if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                  console.log('pass');
                } else {
                  // handle the error
                  console.error('Error:', xhr.statusText);
                }
              }
            };
            xhr.send(data);
          });


          // create a GPT button
          const gptButton = document.createElement("button");
          gptButton.innerText = "GPT";
          // add a click listener to the GPT button
          gptButton.addEventListener("click", function(event) {
            event.preventDefault();

            // send an AJAX GET request to call the Python function
            const xhr = new XMLHttpRequest();
            xhr.open('GET', `/app1/read-gpt-summary?filename=${encodeURIComponent(file)}`, true);
            xhr.onreadystatechange = function() {
              if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                  console.log('GPT Read successful');
                  const jsonResponse = JSON.parse(xhr.responseText);
                  const summaryText = jsonResponse.message;
                  document.getElementById("summarytext").innerText = summaryText;
                  
                  console.log("Response from read GPT summary:", jsonResponse.message);
                } else {
                  // handle the error
                  console.error('Error:', xhr.statusText);
                }
              }
            };
            xhr.send(null);
            console.log("GPT button clicked for:", file);
          });



          // create a read button
          const readButton = document.createElement("button");
          readButton.innerHTML = "&#x1F4DD;";
          // add a click listener to the play button
          readButton.addEventListener("click", function(event) {
            event.preventDefault();
            // handle the play action here
            // send an AJAX GET request to call the Python function
            const xhr = new XMLHttpRequest();
            xhr.open('GET', `/app1/read-summary?filename=${encodeURIComponent(file)}`, true);
            xhr.onreadystatechange = function() {
              if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                  console.log('Read successful');
                  // update the summarytext element with the received data
                  const jsonResponse = JSON.parse(xhr.responseText);
                  const summaryText = jsonResponse.message;
                  document.getElementById("summarytext").innerText = summaryText;
                  
                  console.log("Response from read summary:", jsonResponse.message);


                } else {
                  // handle the error
                  console.error('Error:', xhr.statusText);
                }
              }
            };
            xhr.send(null);
            console.log("Read button clicked for:", file);
          });
        
        li.appendChild(deleteButton);
        li.appendChild(link);
        li.appendChild(gptButton);
        li.appendChild(readButton);
        fileList.appendChild(li);
      });
    });


      const form = document.getElementById('transcriptionForm');
      form.addEventListener('submit', function(event) {
        event.preventDefault(); // prevent the form from submitting normally

        const youtubeurl = document.getElementById('youtubeurl').value;
        const data = JSON.stringify({ "youtubeurl": youtubeurl });

        // send an AJAX request to call the Python function
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/app1/transcribe-summarize', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
          if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
              console.log('pass');
              
            } else {
              // handle the error
              console.error('Error:', xhr.statusText);
            }
          }
        };
        xhr.send(data);
      });



    </script>
</html>