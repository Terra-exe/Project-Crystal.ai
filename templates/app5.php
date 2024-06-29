<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Text/JSON to Audio</title>
  </head>

{% include "navbar.php" %}
{% include "pagetitle.php" %}
<h>Text/JSON to Audio</h>
<body>
	<form id="my-form" method="POST">
        <input type="text" id="title" name="title" maxlength="128" placeholder="New Audio File">

        <label for="voice">Voice:</label>
        <select id="voice" name="voice">
            <option value="crystal" selected>Crystal</option>
            <option value="GLADOS">GLADOS</option>
            <option value="Terra">Terra</option>
        </select>
		<button id="play-demo" type="button" class="btn btn-primary">Demo</button>
		<br><br>
        <!-- Voice Selection Dropdown -->
        <select id="voiceSelection" name="voiceSelection" onchange="voiceChanged()">
            <option value="USE_AWS_POLLY">USE_AWS_POLLY</option>
            <option value="ELEVENLABS_VOICE_ID_FREYA">ELEVENLABS_VOICE_ID_FREYA</option>
            <option value="ELEVENLABS_VOICE_ID_ADAM">ELEVENLABS_VOICE_ID_ADAM</option>
            <option value="ELEVENLABS_VOICE_ID_GIGI">ELEVENLABS_VOICE_ID_GIGI</option>
        </select>

        <!-- API Key Selection Dropdown (initially hidden) -->
        <select id="apiKeySelection" name="apiKeySelection" style="display:none;">
            <option value="ELEVENLABS_API_KEY_1">ELEVENLABS_API_KEY_1</option>
            <option value="ELEVENLABS_API_KEY_2">ELEVENLABS_API_KEY_2</option>
            <option value="ELEVENLABS_API_KEY_3">ELEVENLABS_API_KEY_3</option>
            <option value="ELEVENLABS_API_KEY_4">ELEVENLABS_API_KEY_4</option>
            <option value="ELEVENLABS_API_KEY_5">ELEVENLABS_API_KEY_5</option>
            <option value="ELEVENLABS_API_KEY_6">ELEVENLABS_API_KEY_6</option>
            <option value="ELEVENLABS_API_KEY_7">ELEVENLABS_API_KEY_7</option>
            <option value="ELEVENLABS_API_KEY_8">ELEVENLABS_API_KEY_8</option>
        </select>

		<details>
			<summary>Instructions</summary>
                <ul>
                    <li>The intention of this program is to allow you to copy paste yoga, meditation, and kriya instructions, to create a custom text-to-speech guided experience.</li>
                    <li>You can select the voice of your choice, and you can even add an audio file to acompany newly generated file.</li>
                    <li>In each step you can begin filling out sentences and paragraphs which will transform into speech.</li>
                    <li>The program will detect commas, periods, and new-lines, automatically. It will apply pauses/delays/wait-times to them, which you can predefine.</li>                    
                    <li>Typically exercises are divided into major steps/stages/sections. You can add a additional step by pressing the "+" button at the bottom.</li>
                    <li>You can define a default wait time between sections, and you can also override the default. These wait times are perfect when you need to continue and exercise for X minutes.</li>                   
                    <li>You can also add custom sound effects to the beginning and ending of the wait period.</li>
                    <li>When complete, You can press the submit button to download the wav.</li>
                </ul>
		</details>
		<br><br>
		<div>
            <div class="d-flex">
                <div style="width: 80%;">
                    <small>Default speech delays/pauses in seconds: </small>
                    <br>
                    <label for="comma-pause"><strong>Comma (,):</strong></label>
                    <input type="text" id="comma-pause" name="comma_pause" pattern="\d*\.?\d+" placeholder="0.2"  maxlength="4" size="4" oninput="this.value = this.value.replace(/[^\d\.]/g, '')" style="height: 20px;">

                    <label for="period-pause"><strong>Period (.):</strong></label>
                    <input type="text" id="period-pause" name="period_pause" pattern="\d*\.?\d+" placeholder="0.2" maxlength="4" size="4" oninput="this.value = this.value.replace(/[^\d\.]/g, '')" style="height: 20px;">

                    <label for="newline-pause"><strong>New Line:</strong></label>
                    <input type="text" id="newline-pause" name="newline_pause" pattern="\d*\.?\d+" placeholder="0.5" maxlength="4" size="4" oninput="this.value = this.value.replace(/[^\d\.]/g, '')" style="height: 20px;">

                    <label for="newsection-pause"><strong>New Section:</strong></label>
                    <input type="text" id="newsection-pause" name="newsection_pause" pattern="\d*\.?\d+" placeholder="2" maxlength="5" size="4" oninput="this.value = this.value.replace(/[^\d\.]/g, '')" style="height: 20px;">
                </div>

                <div class="ml-auto" style="width: 20%;">
                    <label for="audio-file">Upload Audio File:</label>
                    <div class="custom-file">
                        <input type="file" class="custom-file-input btn btn-primary" id="audio-file" name="audio_file">
                        <label class="custom-file-label" for="audio-file">Choose file</label>
                        <input type="checkbox" id="crossfade" name="crossfade">
                        <br>
                        <label for="crossfade">crossfade?</label>
                    </div>
                    <br><br>
                    <p>Upload a background audio file to loop</p>
                    <div class="custom-file">
                        <label for="file-upload">Upload Text File:</label>
                        <input type="file" id="file-upload" name="file-upload" accept=".json">
                    </div>

                </div>
            </div>
		    <div style="clear: both;"></div>
		</div>
		<br><br>
        <div id="steps-container" style="border: 1px solid black; padding: 10px;">
            <label for="step1" class="col-form-label">Step 1:</label>
            <br><br>
            <textarea class="form-control" id="step1" name="step1" rows="1" oninput="auto_grow(this)"></textarea>
            <br><br>
            <details>
            <summary>Overrides</summary>
            
            <table style="border: 1px solid black;">
                <tr>
                    <td style="border-right: 1px solid black; padding: 10px;">
                        <label><small>New Section Pause:</small></label>
                    </td>
                    <td style="border-right: 1px solid black; padding: 10px;">
                        <label><small>Sound effect to play at the beginning of the pause</small></label>
                    </td>
                    <td style="border-right: 1px solid black; padding: 10px;">
                        <label><small>Sound effect to play at the end of the pause</small></label>
                    </td>
                </tr>
                <tr>
                    <td style="border-right: 1px solid black; padding: 10px; text-align: center;">
                        <input type="text" id="pause1" name="pause1" pattern="\d*\.?\d+" maxlength="5" size="3" oninput="this.value = this.value.replace(/[^\d\.]/g, '')" style="height: 20px;">
                    </td>

                    <td style="border-right: 1px solid black; padding: 10px;">
                        <div class="custom-file">
                            <input type="file" class="custom-file-input btn btn-primary" id="start-audio-file-step1" name="start_audio_file_step1">
                            <label class="custom-file-label" for="start-audio-file-step1">Start</label>
                        </div>
                    </td>
                    <td style="border-right: 1px solid black; padding: 10px;">
                        <div class="custom-file">
                            <input type="file" class="custom-file-input btn btn-primary" id="end-audio-file-step1" name="end_audio_file_step1">
                            <label class="custom-file-label" for="end-audio-file-step1">End</label>
                        </div>
                    </td>
                </tr>
            </table>


            </details>  
            <br><br>
        </div>
        <hr>
        <label for="newsection"><strong>Add Step:</strong></label>
		<button id="add-step" type="button" class="btn btn-primary">+</button>
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


        ////////////////////
        //Play Demo Button//
        ////////////////////
        // Get the playDemoButton button
        var audio = new Audio('/app5/audio/crystal_demo')
        const playDemoButton = document.getElementById('play-demo');
        playDemoButton.addEventListener('click', function() {
            event.preventDefault();
            audio.play();
        });

        function voiceChanged() {
            var voice = document.getElementById("voiceSelection").value;
            var apiKeySelect = document.getElementById("apiKeySelection");
            if (voice == "USE_AWS_POLLY") {
                apiKeySelect.style.display = "none";
            } else {
                apiKeySelect.style.display = "block";
            }
        }

        ///////////////////
        //Add Step Button//
        ///////////////////

        // Get the container element
        const stepsContainer = document.getElementById('steps-container');
        // Get the "+"" button
        const addStepButton = document.getElementById('add-step');

        // Initialize the step counter
        let stepCounter = 1;

        function addStepWithData(stepText, newSectionPause, startAudioFile, endAudioFile) {
            event.preventDefault();
            
            stepCounter++;
            console.log("Step added [" + stepCounter + "]");
            
            // Create a new label element for the step
            const stepLabel = document.createElement('label');
            stepLabel.setAttribute('for', 'step' + stepCounter);
            stepLabel.textContent = 'Step ' + stepCounter + ': ';
            stepLabel.setAttribute('class', 'col-form-label');


            //---------

            // Create a new textarea element for the step
            const stepTextarea = document.createElement('textarea');
            stepTextarea.setAttribute('class', 'form-control');
            stepTextarea.setAttribute('id', 'step' + stepCounter);
            stepTextarea.setAttribute('name', 'step' + stepCounter);
            stepTextarea.setAttribute('rows', '1');
            stepTextarea.setAttribute('oninput', 'auto_grow(this)');


            /////////overrides start////////

            // Create a new details element for the overrides
            const overridesDetails = document.createElement('details');
            const overridesSummary = document.createElement('summary');
            overridesSummary.textContent = "Overrides";
            overridesDetails.appendChild(overridesSummary);

            // Create a table to hold the override information
            const overridesTable = document.createElement('table');
            overridesTable.style.border = '1px solid black';
            
            const row1 = overridesTable.insertRow();
            const cell1_1 = row1.insertCell();
            cell1_1.style.borderRight = '1px solid black';
            cell1_1.style.padding = '10px';
            const label1_1 = document.createElement('label');
            label1_1.innerHTML = '<small>New Section Pause:</small>';
            cell1_1.appendChild(label1_1);

            const cell1_2 = row1.insertCell();
            cell1_2.style.borderRight = '1px solid black';
            cell1_2.style.padding = '10px';
            const label1_2 = document.createElement('label');
            label1_2.innerHTML = '<small>Sound effect to play at the beginning of the pause</small>';
            cell1_2.appendChild(label1_2);

            const cell1_3 = row1.insertCell();
            cell1_3.style.borderRight = '1px solid black';
            cell1_3.style.padding = '10px';
            const label1_3 = document.createElement('label');
            label1_3.innerHTML = '<small>Sound effect to play at the end of the pause</small>';
            cell1_3.appendChild(label1_3);

            // Create the second row with input fields and labels
            const row2 = overridesTable.insertRow();
            const cell2_1 = row2.insertCell();
            cell2_1.style.borderRight = '1px solid black';
            cell2_1.style.padding = '10px';
            cell2_1.style.textAlign = 'center';
            const input2_1 = document.createElement('input');
            input2_1.type = 'text';
            input2_1.id = 'pause' + stepCounter;
            input2_1.name = 'pause' + stepCounter;
            input2_1.pattern = '\\d*\\.?\\d+';
            input2_1.maxlength = '5';
            input2_1.size = '3';
            input2_1.oninput = function() { this.value = this.value.replace(/[^\d\.]/g, ''); };
            input2_1.style.height = '20px';
            cell2_1.appendChild(input2_1);

            const cell2_2 = row2.insertCell();
            cell2_2.style.borderRight = '1px solid black';
            cell2_2.style.padding = '10px';
            const div2_2 = document.createElement('div');
            div2_2.className = 'custom-file';
            const input2_2 = document.createElement('input');
            input2_2.type = 'file';
            input2_2.className = 'custom-file-input btn btn-primary';
            input2_2.id = 'start-audio-file-step' + stepCounter;
            input2_2.name = 'start_audio_file_step' + stepCounter;
            const label2_2 = document.createElement('label');
            label2_2.className = 'custom-file-label';
            label2_2.htmlFor = 'start-audio-file-step' + stepCounter;
            label2_2.innerHTML = 'Start';
            div2_2.appendChild(input2_2);
            div2_2.appendChild(label2_2);
            cell2_2.appendChild(div2_2);

            const cell2_3 = row2.insertCell();
            cell2_3.style.borderRight = '1px solid black';
            cell2_3.style.padding = '10px';
            const div2_3 = document.createElement('div');
            div2_3.className = 'custom-file';
            const input2_3 = document.createElement('input');
            input2_3.type = 'file';
            input2_3.className = 'custom-file-input btn btn-primary';
            input2_3.id = 'end-audio-file-step' + stepCounter;
            input2_3.name = 'end_audio_file_step' + stepCounter;
            const label2_3 = document.createElement('label');
            label2_3.className = 'custom-file-label';
            label2_3.htmlFor = 'end-audio-file-step' + stepCounter;
            label2_3.innerHTML = 'End';
            div2_3.appendChild(input2_3);
            div2_3.appendChild(label2_3);
            cell2_3.appendChild(div2_3);



            /////////overrides end////////

            // Create a new label element for the pause
            const overridesLabel = document.createElement('label');
            overridesLabel.innerHTML = 'Overrides';

            // Create a new label element for the pause
            const pauseLabel = document.createElement('label');
            pauseLabel.setAttribute('for', 'pause' + stepCounter);
            pauseLabel.innerHTML = '<small>Default Section Pause:</small>\u00A0';


            // Create a new input element for the pause
            const pauseInput = document.createElement('input');
            pauseInput.setAttribute('type', 'text');
            pauseInput.setAttribute('id', 'pause' + stepCounter);
            pauseInput.setAttribute('name', 'pause' + stepCounter);
            pauseInput.setAttribute('pattern', '\\d*\\.?\\d+');
            pauseInput.setAttribute('maxlength', '5');
            pauseInput.setAttribute('size', '3');
            pauseInput.setAttribute('style', 'height: 20px;');
            pauseInput.setAttribute('oninput', `this.value = this.value.replace(/[^\\d.]/g, ''); if (this.value > 10) this.value = 10;`);


            // Append the table to the overrides details element
            overridesDetails.appendChild(overridesTable);


            // Append the new elements to the container
            stepsContainer.appendChild(stepLabel);
            stepsContainer.appendChild(stepTextarea);
            stepsContainer.appendChild(document.createElement('br'));
            stepsContainer.appendChild(overridesDetails)
            stepsContainer.appendChild(document.createElement('br'));
            stepsContainer.appendChild(document.createElement('br'));
            stepsContainer.appendChild(document.createElement('br'));
            
            // Set the values of the fields
            stepTextarea.value = stepText;
            input2_1.value = newSectionPause;


            console.log("Step add COMPLETE [" + stepCounter + "]");
            console.log("Added : [" + stepText + "] to " + stepTextarea.id);

        }

        addStepButton.addEventListener('click', function() {
            event.preventDefault();
            addStepWithData('', '', '', '');
        });


        ////////////////////////
        //Auto Grow Text Field//
        ////////////////////////

        function auto_grow(element) {
            element.style.height = "5px";
            element.style.height = (element.scrollHeight)+"px";
        }


        function downloadTextFile(content, fileName, contentType) {
            console.log("download json run")
            var a = document.createElement("a");
            var file = new Blob([content], { type: contentType }); 
            a.href = URL.createObjectURL(file);
            a.download = fileName;

                // Adding console logs to show the URL
            console.log("URL:", a.href);
            console.log("Download file name:", a.download);


            a.click();
        }


        //////////////////////////
        ////////Upload JSON///////
        //////////////////////////
        document.getElementById('file-upload').addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const content = e.target.result;
                    autofillFormData(content);
                    // Hide the download button when a new file is uploaded
                    document.getElementById('download-button').style.display = 'none';
                };
                reader.readAsText(file);
            }
        });


        ////////////////////////////
        ////////Autofill data///////
        ////////////////////////////
        function autofillFormData(content) {
            stepCounter = 0;
            console.log('Autofill data 1');
            // Parse the JSON content
            const jsonData = JSON.parse(content);

            // Fill in the form fields
            document.getElementById('title').value = jsonData.title || '';
            document.getElementById('voice').value = jsonData.voice || '';
            document.getElementById('comma-pause').value = jsonData.comma_pause || '';
            document.getElementById('period-pause').value = jsonData.period_pause || '';
            document.getElementById('newline-pause').value = jsonData.newline_pause || '';
            document.getElementById('newsection-pause').value = jsonData.newsection_pause || '';
            document.getElementById('crossfade').checked = jsonData.crossfade || false;

            // Clear existing steps
            stepsContainer.innerHTML = '';
            
            console.log('Autofill data 2');
            // Loop through the steps and add them to the form
            for (let i = 1; i <= jsonData.stepcount; i++) {
                const stepText = jsonData[`step${i}`] || '';
                console.log("Step text [" + i +"]" + stepText);
                const newSectionPause = jsonData[`pause${i}`] || '';
                console.log("Step pause [" + i +"]" + newSectionPause);
                
                // Add a step to the form with the parsed data
                addStepWithData(stepText, newSectionPause, '', '');
                console.log("done step [" + i + "]")
                
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
            const audioFileName = `${audioFileTitle}_combined.wav`;

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


            var formData = {
                title: document.getElementById('title').value,
                // Assuming 'voiceSelection' is the ID for the dropdown for voice choice
                voiceSelection: document.getElementById('voiceSelection').value,
                // Assuming 'apiKeySelection' is the ID for the dropdown for the API key, which may not be present for all choices
                apiKeySelection: document.getElementById('apiKeySelection') ? document.getElementById('apiKeySelection').value : '',            
                voice: document.getElementById('voice').value,
                comma_pause: document.getElementById('comma-pause').value,
                period_pause: document.getElementById('period-pause').value,
                newline_pause: document.getElementById('newline-pause').value,
                newsection_pause: document.getElementById('newsection-pause').value,
                crossfade: document.getElementById('crossfade').checked,
                stepcount: stepCounter
            };
            

            if (!formData["title"]){
              formData["title"] = "NewFile";
            }
            
            if (!formData["comma_pause"] || parseFloat(formData["comma_pause"]) < 0.1 || parseFloat(formData["comma_pause"]) > 999) {
                formData["comma_pause"] = "0.2";
            }
            
            if (!formData["period_pause"] || parseFloat(formData["period_pause"]) < 0.1 || parseFloat(formData["period_pause"]) > 999) {
               formData["period_pause"] = "0.5";
            }
            
            if (!formData["newline_pause"] || parseFloat(formData["newline_pause"]) < 0.1 || parseFloat(formData["newline_pause"]) > 999) {
                formData["newline_pause"] = "0.5";
            }
            if (!formData["newsection_pause"] || parseFloat(formData["newsection_pause"]) < 0.1 || parseFloat(formData["newsection_pause"]) > 9999) {
                formData["newsection_pause"] = "2";
            }


            // add any dynamic elements to the formData object
            var i = 0;
            var stepInput, pauseInput;
            while (i < stepCounter) {
                i++;
                stepInput = document.getElementById('step' + i)
                pauseInput = document.getElementById('pause' + i);
                formData['step' + i] = stepInput.value;
                formData['pause' + i] = pauseInput.value;
                console.log('steps 1');
            }

            console.log('count 1');
            // send an AJAX request to the call the Python function
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/app5/create-audio-file', true);
           // xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.setRequestHeader('Content-Type', 'application/json');
            console.log('count 2');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        // hide the wait message
                        waitMessage.style.display = 'none';
                        console.log('count 3');
                        // show the download link
                        downloadLink.style.display = 'block';

                        // set the download URL to the response from the python script
                        downloadButton.href = xhr.responseText;
                        
                        

                    } else {
                        // handle the error
                        console.log('count 5');
                        console.error('Error:', xhr.statusText);
                        // show the error message
                        errorMessage.style.display = 'block';
                    }
                }
            };
            console.log('count 5');
            console.log(formData["title"])
            console.log(formData["comma_pause"])
            console.log(formData["period_pause"])
            console.log(formData["newline_pause"])
            console.log(formData["newsection_pause"])

            jsonString = JSON.stringify(formData)
            
            /* Disable the download text file it's not necessary at the moment */
            // downloadTextFile(jsonString, formData["title"] + ".json", "text/plain"); // This line triggers the download
                        /*submitButton.addEventListener('click', function(event) {
                            console.log('submit pressed');
                            event.preventDefault();
                            console.log('submit default ignored');
                            window.open(submitButton.href, '_blank');
                            console.log('window open');
                        });*/

        
            console.log(jsonString);
      

            xhr.send(jsonString); // send the form data to the Python as JSON
            console.log('Sent');

    
        
            // Remove the old event listener
            downloadButton.removeEventListener('click', downloadButtonClickHandler);

            // Add the new event listener
            downloadButton.addEventListener('click', downloadButtonClickHandler);
            document.getElementById('download-button').style.display = 'block';
      });


    </script>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF">
</body>
</html>