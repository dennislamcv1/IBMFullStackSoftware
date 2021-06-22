<!DOCTYPE html>
<html lang="en">
<head>
     {% load static %}
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <meta charset="UTF-8">
</head>

<body>
    <!-- Navigation bar -->
    <nav class="navbar navbar-light bg-light">
        <div class="container-fluid">
            <div class="navbar-header">
                  <a class="navbar-brand" href="{% url 'onlinecourse:index' %}">Home</a>
            </div>
            <ul class="nav navbar-nav navbar-right">
                {% if user.is_authenticated %}
                <li>
                    <a class="btn btn-link" href="#">{{ user.first_name }}({{ user.username }})</a>
                    <a class="btn btn-link" href="{% url 'onlinecourse:logout' %}">Logout</a>
                </li>
                {% else %}
                <li>
                    <form class="form-inline" action="{% url 'onlinecourse:login' %}" method="post">
                        {% csrf_token %}
                        <div class="input-group">
                            <input type="text" class="form-control" placeholder="Username" name="username" >
                            <input type="password" class="form-control" placeholder="Username" name="psw" >
                            <button class="btn btn-primary" type="submit">Login</button>
                            <a class="btn btn-link" href="{% url 'onlinecourse:registration' %}">Sign Up</a>
                        </div>
                    </form>
                </li>
                {% endif %}
            </ul>
        </div>
    </nav>

    <!-- Page content -->
    <div class="container-fluid">
            <h2>{{ course.name }}</h2>
            <div class="card-columns-vertical">
                {% for lesson in course.lesson_set.all %}
                    <div class="card mt-1">
                        <div class="card-header"><h5>Lesson {{lesson.order|add:1}}: {{lesson.title}}</h5></div>
                        <div class="card-body">{{lesson.content}}</div>
                    </div>
                {% endfor %}
            </div>
            <!-- Task: show questions and choices -->
            <!-- <HINT> Use Bootstrap Collapse to hide exam first, more details could be found here
            https://www.w3schools.com/bootstrap4/bootstrap_collapse.asp-->

            <!--

            A collapse example here:
            <div id="exam" class="collapse">
                Click to expand elements within the collapse div
                </div>

            -->

            <!-- <HINT> If user is authenticated, show course exam with a list of question -->

            <!-- <HINT> Each example will have many questions -->

            <!-- <HINT> Each question will have many choices -->


            <!-- <HINT> Create a form to collect the selected choices for all questions -->
            <!-- <HINT> For each question choice, you may create a checkbox input like
            <input type="check" name="choice_{{choice.id}}" id="{{choice.id}}" ...>
            -->

            <!-- A choice submission form example
            <form id="questionform" action="point to a submit view" method="post">
                        ... for each question in the course ...
                        <div class="card mt-1">
                            <div class="card-header"><h5>{{ question.question_text}}</h5></div>
                            {% csrf_token %}
                            <div class="form-group">
                               ... for each choice in the question ...
                                <div class="form-check">
                                    <label class="form-check-label">
                                        <input type="checkbox" name="choice_{{choice.id}}"
                                               class="form-check-input" id="{{choice.id}}"
                                               value="{{choice.id}}">{{ choice.choice_text }}
                                    </label>
                                </div>
                            </div>
                        </div>
                    <input class="btn btn-success btn-block" type="submit" value="Submit">
            </form> -->

            <!--Check here to see more details Bootstrap checkbox
             https://www.w3schools.com/bootstrap4/bootstrap_forms_inputs.asp-->
    </div>
</body>
</html>