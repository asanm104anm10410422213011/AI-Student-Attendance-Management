from flask import Flask, render_template, request, redirect

app = Flask(__name__)

students = [
    {"name": "Gayathri", "roll_no": "101"},
    {"name": "Student 2", "roll_no": "102"},
    {"name": "Student 3", "roll_no": "103"}
]

attendance = {}


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        date = request.form["date"]

        attendance[date] = {}

        for student in students:
            roll_no = student["roll_no"]
            status = request.form.get(roll_no, "Absent")

            attendance[date][roll_no] = status

        return redirect("/")

    return render_template(
        "index.html",
        students=students
    )


if __name__ == "__main__":
    app.run(debug=True)
