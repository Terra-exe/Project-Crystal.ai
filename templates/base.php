<?php
    include 'navbar.php';
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Terrable Apps</title>
  </head>

  {% include "navbar.php" %}
  {% include "pagetitle.php" %}
 
  <body>
      <!--<form action="{{ context.form_action }}" method="post"> -->
      <form method="post">
        <table style="width: 100%">
          <tbody id="textInputContainer">
            <tr>
              <td>
                <label for="textInputs">{{ context.form_label }}</label>
              </td>
              <td>
                <textarea class="form-control" id="textInputs" name="textInputs" rows="1" maxlength="1000" oninput="auto_grow(this)"></textarea>
              </td>
            </tr>
          </tbody>
        </table>
        <button type="button" id="addTextInputBtn" class="btn btn-primary">+</button>
        <button type="stop" class="btn btn-primary">Stop</button>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
    <script>
      document.getElementById("addTextInputBtn").addEventListener("click", function() {
        var textInputContainer = document.getElementById("textInputContainer");
        var newRow = document.createElement("tr");
        newRow.innerHTML = `
          <td>
            <label for="textInputs">{{ context.form_label }}</label>
          </td>
          <td>
            <textarea class="form-control" id="textInputs" name="textInputs" rows="1" maxlength="1000" oninput="auto_grow(this)"></textarea>
          </td>
        `;
        textInputContainer.appendChild(newRow);
      });
      function auto_grow(element) {
        element.style.height = "5px";
        element.style.height = (element.scrollHeight)+"px";
      }
    </script>

    {% block content %}{% endblock %}

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF
    

