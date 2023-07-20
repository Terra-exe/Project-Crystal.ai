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

<form method="post" enctype="multipart/form-data" action="{{ form_action }}">
  <table style="width: 100%">
    <tbody>
      <tr>
        <td>
          <label for="audioFile">{{ form_label }}</label>
        </td>
        <td>
          <input type="file" class="form-control-file" id="audioFile" name="audioFile" accept="audio/*" required>
        </td>
      </tr>
    </tbody>
  </table>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>