from flask import Flask, render_template, request, redirect

app = Flask(__name__)

students = []

attendance = {}


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        action = request.form.get("action")

        # Add Student
        if action == "add_student":
            name = request.form["name"]
            roll_no = request.form["roll_no"]

            students.append({
                "name": name,
                "roll_no": roll_no
            })

            return redirect("/")

        # Delete Student
        if action == "delete_student":
            roll_no = request.form["roll_no"]

            students[:] = [
                student for student in students
                if student["roll_no"] != roll_no
            ]

            return redirect("/")

        # Save Attendance
        if action == "attendance":
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
