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
        <input type="text" id="title" name="title" maxlength="128" placeholder="ttsFileTitle">

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
                        <option value="variable_frequency">Variable Frequency</option>
                        <option value="crown">crown 480Hz</option>
                        <option value="3rdeye">third eye 426.7Hz</option>
                        <option value="throat">throat 384Hz</option>
                        <option value="heart">heart 341.3Hz</option>
                        <option value="solar">solar plexus 320Hz</option>
                        <option value="sacral">sacral 288Hz</option>
                        <option value="root">root 256Hz</option>

                    </select>

                    <!-- Variable Frequency Specific Dropdowns (hidden initially) -->
                    <div id="variable-frequency-fields" style="display: none;">
                        <label for="start_freq">Start Frequency:</label>
                        <select id="start_freq" name="start_freq">
                            <option value="delta">Delta</option>
                            <option value="theta">Theta</option>
                            <option value="alpha">Alpha</option>
                            <option value="beta">Beta</option>
                            <option value="gamma">Gamma</option>            
                            <option value="custom">Custom</option>
                            <option value="crown">crown 480Hz</option>
                            <option value="3rdeye">third eye 426.7Hz</option>
                            <option value="throat">throat 384Hz</option>
                            <option value="heart">heart 341.3Hz</option>
                            <option value="solar">solar plexus 320Hz</option>
                            <option value="sacral">sacral 288Hz</option>
                            <option value="root">root 256Hz</option>
                            <!-- Other frequency options -->
                        </select>

                        <label for="mid_freq">Mid Frequency:</label>
                        <select id="mid_freq" name="mid_freq">
                            <option value="delta">Delta</option>
                            <option value="theta">Theta</option>
                            <option value="alpha">Alpha</option>
                            <option value="beta">Beta</option>
                            <option value="gamma">Gamma</option>            
                            <option value="custom">Custom</option>
                            <option value="crown">crown 480Hz</option>
                            <option value="3rdeye">third eye 426.7Hz</option>
                            <option value="throat">throat 384Hz</option>
                            <option value="heart">heart 341.3Hz</option>
                            <option value="solar">solar plexus 320Hz</option>
                            <option value="sacral">sacral 288Hz</option>
                            <option value="root">root 256Hz</option>
                        </select>

                        <label for="end_freq">End Frequency:</label>
                        <select id="end_freq" name="end_freq">
                            <option value="delta">Delta</option>
                            <option value="theta">Theta</option>
                            <option value="alpha">Alpha</option>
                            <option value="beta">Beta</option>
                            <option value="gamma">Gamma</option>            
                            <option value="custom">Custom</option>
                            <option value="crown">crown 480Hz</option>
                            <option value="3rdeye">third eye 426.7Hz</option>
                            <option value="throat">throat 384Hz</option>
                            <option value="heart">heart 341.3Hz</option>
                            <option value="solar">solar plexus 320Hz</option>
                            <option value="sacral">sacral 288Hz</option>
                            <option value="root">root 256Hz</option>
                        </select>
                    </div>

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
            var customFields = document.getElementById('custom-fields');
            var variableFrequencyFields = document.getElementById('variable-frequency-fields');
            customFields.style.display = 'none';
            variableFrequencyFields.style.display = 'none';

            if (value === 'custom') {
                customFields.style.display = 'block';
                variableFrequencyFields.style.display = 'none';
            } else if (value === 'variable_frequency') {
                variableFrequencyFields.style.display = 'block';
                customFields.style.display = 'none';
            } else {
                customFields.style.display = 'none';
                variableFrequencyFields.style.display = 'none';
            }

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
            const audioFileTitle = document.getElementById('title').value || 'ttsFileTitle';
            const audioFileName = `${audioFileTitle}_Binaural.wav`;
            

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
            formData.append("preset", document.getElementById('preset').value); // add the preset parameter
           
            // Append start, mid, and end frequency values to formData
            if (document.getElementById('preset').value === 'variable_frequency') {
                formData.append("start_freq", document.getElementById('start_freq').value);
                formData.append("mid_freq", document.getElementById('mid_freq').value);
                formData.append("end_freq", document.getElementById('end_freq').value);
            }
            
            if (!formData.get("title")) {
                formData.set("title", "ttsFileTitle");
            }

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/app6/add_binaural_to_audio_file', true); // adjust the URL if necessary
            xhr.onreadystatechange = function() {
                console.log("boing boing");
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        // Parse the JSON response from the server
                        var response = JSON.parse(xhr.responseText);

                        // Extract the S3 URL from the response
                        var s3URL = response.message;

                        // hide the wait message
                        waitMessage.style.display = 'none';
                        // show the download link
                        downloadLink.style.display = 'block';


                        // set the download URL to the S3 URL
                        downloadButton.href = s3URL;
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





