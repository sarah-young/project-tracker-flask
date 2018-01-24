"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def homepage():
    """A placeholder page."""

    return render_template("homepage.html")


@app.route("/student")
def search_by_student_github():
    """Shows student info that is linked to given github account."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    all_grades = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html", first=first, last=last,
                           github=github, all_grades=all_grades)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def add_student():
    """Shows form for adding a student."""

    return render_template("student_add.html")


@app.route("/student-confirmation", methods=["POST"])
def update_student_database():
    """Updates database with new student and displays a confirmation to user."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_confirmation.html", first_name=first_name,
                           last_name=last_name, github=github)


@app.route("/project/<title>")
def show_project(title):
    """Show project information."""

    project_name, description, max_grade = hackbright.get_project_by_title(title)
    # unpacking the tuple :)

    gh_name_dict = {}

    accounts_and_grades = hackbright.get_grades_by_title(title)

    for student_account in accounts_and_grades:
    # loop through accounts & grades list to parse students
        gh_account = student_account[0]
        grade = student_account[1]
        first_name, last_name, github = hackbright.get_student_by_github(gh_account)
        # unpacking elements from tuple
        gh_name_dict[github] = (first_name + " " + last_name, grade, gh_account)
        # assigning github UN as key and full name and grade as values

    student_grade_pair = gh_name_dict.values()
    # stripping off key to leave paired values (grade and full name)
    # passing to Jinja in template

    return render_template("project.html",
                           max_grade=max_grade,
                           project_name=project_name,
                           description=description,
                           students=student_grade_pair
                           )


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
