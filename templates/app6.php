<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Audio / Bineural Merge</title>
  </head>

{% include "navbar.php" %}
{% include "pagetitle.php" %}
<h>Audio / Bineural Merge</h>
<body>
	<form id="my-form" method="POST" enctype="multipart/form-data">
        <input type="text" id="title" name="title" maxlength="128" placeholder="New Bineural Audio Title">
        <input type="file" id="audioFile" name="audioFile" accept="audio/*">

        </select>
		
		<br><br>
		<details>
			<summary>Instructions</summary>
                <ul>
                    <li>Add Bineural to your audio</li>
                </ul>
		</details>
		<br><br>
		<div>
            <div class="d-flex">
                <div style="width: 80%;">
                    <small>Select your presets: </small>
                    <br>
                    <label for="preset">Preset:</label>
                    <select id="preset" name="preset" onchange="checkCustom(this.value)">
                        <option value="delta">Delta</option>
                        <option value="theta">Theta</option>
                        <option value="alpha">Alpha</option>
                        <option value="beta">Beta</option>
                        <option value="gamma">Gamma</option>
                        <option value="pink">Pink</option>
                        <option value="custom">Custom</option>
                    </select>
                </div>
                <div id="custom-fields" style="display: none;">
                    <label for="base-frequency">Base Frequency:</label>
                    <input type="text" id="base-frequency" name="base_frequency" pattern="\d*\.?\d+" maxlength="5" size="3" oninput="this.value = this.value.replace(/[^\d\.]/g, '')" style="height: 20px;">
                    <label for="binarual-offset">Binarual Offset:</label>
                    <input type="text" id="binarual-offset" name="binarual_offset" pattern="\d*\.?\d+" maxlength="5" size="3" oninput="this.value = this.value.replace(/[^\d\.]/g, '')" style="height: 20px;">
                </div>
            
            </div>
		    <div style="clear: both;"></div>
            
		</div>
		<br><br>
        <div id="body-container" style="border: 1px solid black; padding: 10px;">
        </div>
        <hr>
        
		
		<br><br>
		<button type="submit" id="submit-button" class="btn btn-primary">Submit</button>
	</form>

    
    <div> <!--Download File-->
        <div id="wait-message" style="display: none;">Please wait while the audio file is being generated...</div>

        <div id="download-link" style="display: none;" class="btn btn-primary">
            <a href="#" id="download-button">Download Audio File</a>
        </div>
    </div>


    <script>

        function checkCustom(value) {
            if (value === 'custom') {
                document.getElementById('custom-fields').style.display = 'block';
            } else {
                document.getElementById('custom-fields').style.display = 'none';
            }
        }

        //////////////////////////
        //Download/Submit Button//
        //////////////////////////

        var form = document.getElementById('my-form');
        var waitMessage = document.getElementById('wait-message');
        var downloadLink = document.getElementById('download-link');
        var downloadButton = document.getElementById('download-button');
        var submitButton = document.getElementById('submit-button');

        
        function downloadButtonClickHandler(event) {
            event.preventDefault(); // prevent the default click action of the link

            // Get the audio file title
            const audioFileTitle = document.getElementById('title').value || 'NewFile';
            const audioFileName = `${audioFileTitle}_Binaural.wav`;

            // Construct the URL for the audio file
            const audioFileURL = `/audios/${audioFileName}`;

            // Download the audio file
            const link = document.createElement('a');
            link.href = downloadButton.href;
            link.download = audioFileName;
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }




        form.addEventListener('submit', function(event) {
            event.preventDefault(); // prevent the form from submitting normally

            waitMessage.style.display = 'block'; // show the wait message

            var formData = new FormData(); // change this to FormData to handle file upload
            formData.append("title", document.getElementById('title').value);
            formData.append("audio_file", document.getElementById('audioFile').files[0]); // append the uploaded file
            formData.append("preset", document.getElementById('preset').value); // add the preset parameter

            if (!formData.get("title")) {
                formData.set("title", "NewFile");
            }

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/app6/add_binaural_to_audio_file', true); // adjust the URL if necessary
            xhr.onreadystatechange = function() {
                console.log("boing boing");
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        // hide the wait message
                        waitMessage.style.display = 'none';
                        // show the download link
                        downloadLink.style.display = 'block';

                        // set the download URL to the response from the Python script
                        downloadButton.href = xhr.responseText;
                    } else {
                        // handle the error
                        console.error('Error:', xhr.statusText);
                        // show the error message
                        errorMessage.style.display = 'block';
                    }
                }
            };

            xhr.send(formData); // send the form data to the server
        });



    </script>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF">
</body>
</html>