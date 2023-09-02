<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Audio / Merge S3 Genfiles</title>
  </head>

{% include "navbar.php" %}
{% include "pagetitle.php" %}
<h>Audio / Merge S3 Genfiles</h>
<body>
	<form id="my-form" method="POST" enctype="multipart/form-data">
        <input type="text" id="title" name="title" maxlength="128" placeholder="GenfileTitle">

		<br><br>
		<details>
			<summary>Instructions</summary>
                <ul>
                    <li>Merge S3 Genfiles</li>
                </ul>
		</details>
		<br><br>
		<div>
            <div class="d-flex">
                <div style="width: 80%;">
                   
                </div>
                <div id="custom-fields" style="display: none;">
                    
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
            const audioFileTitle = document.getElementById('title').value || 'GenfileTitle';
            const audioFileName = `${audioFileTitle}.mp3`;

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

            if (!formData.get("title")) {
                formData.set("title", "GenfileTitle");
            }

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/app51/merge_s3_genfiles', true); // adjust the URL if necessary
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