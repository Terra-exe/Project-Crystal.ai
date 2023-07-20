<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Transcribe Youtube to Summary Audio</title>
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
            </td>
          </tr>
        </tbody>
      </table>
      <button type="submit" class="btn btn-primary">Submit</button>
      <button type="button" class="btn btn-secondary" id="replayButton">Replay</button>
</form>

<div id="summaryList"></div>

<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
      function displaySummaryList() {
        const listDiv = document.getElementById('summaryList');
        fetch('/list_summary_files')
            .then(response => response.json())
            .then(files => {
                listDiv.innerHTML = '<ul>';
                files.forEach(file => {
                    listDiv.innerHTML += '<li>' + file + '</li>';
                });
                listDiv.innerHTML += '</ul>';
            })
            .catch(error => console.error('Error:', error));
      }





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
              displaySummaryList(JSON.parse(xhr.responseText)); // display the list of summaries
            } else {
              // handle the error
              console.error('Error:', xhr.statusText);
            }
          }
        };
        xhr.send(data);
      });


  const replayButton = document.getElementById('replayButton');
  replayButton.addEventListener('click', function(event) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/app1/replay-summary', true);
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
    xhr.send();
  });


    </script>
</html>