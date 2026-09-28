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

    # Attendance Percentage
    student_summary = []

    for student in students:

        roll_no = student["roll_no"]

        total_days = 0
        present_days = 0

        for date_data in attendance.values():

            if roll_no in date_data:

                total_days += 1

                if date_data[roll_no] == "Present":
                    present_days += 1

        if total_days > 0:
            percentage = round(
                (present_days / total_days) * 100, 2
            )
        else:
            percentage = 0

        student_summary.append({
            "name": student["name"],
            "roll_no": roll_no,
            "percentage": percentage
        })

    return render_template(
        "index.html",
        students=students,
        student_summary=student_summary
    )


if __name__ == "__main__":
    app.run(debug=True)
