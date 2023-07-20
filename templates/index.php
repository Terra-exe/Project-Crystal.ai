<?php
{% extends "base.php" %}

{% block content %}

{% set app_title = "App Title" %}
{% set app_header = "App Header" %}
{% set form_action = "/submit_app" %}
{% set form_label = "Enter text for app" %}

{{ super() }}
{% endblock %}
?>
