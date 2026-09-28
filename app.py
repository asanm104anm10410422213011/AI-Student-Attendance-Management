from flask import Flask, render_template, request, redirect
from model import predict_attendance
import sqlite3

app = Flask(__name__)


# Database connection
def get_db():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create database tables
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def home():

    conn = get_db()

    # Add Student
    if request.method == "POST":

        action = request.form.get("action")

        if action == "add_student":

            name = request.form["name"]
            roll_no = request.form["roll_no"]

            try:
                conn.execute(
                    "INSERT INTO students (name, roll_no) VALUES (?, ?)",
                    (name, roll_no)
                )

                conn.commit()

            except sqlite3.IntegrityError:
                pass

            conn.close()

            return redirect("/")


        # Delete Student
        if action == "delete_student":

            roll_no = request.form["roll_no"]

            conn.execute(
                "DELETE FROM students WHERE roll_no = ?",
                (roll_no,)
            )

            conn.execute(
                "DELETE FROM attendance WHERE roll_no = ?",
                (roll_no,)
            )

            conn.commit()
            conn.close()

            return redirect("/")


        # Save Attendance
        if action == "attendance":

            date = request.form["date"]

            students = conn.execute(
                "SELECT * FROM students"
            ).fetchall()

            # Remove existing attendance for same date
            conn.execute(
                "DELETE FROM attendance WHERE date = ?",
                (date,)
            )

            for student in students:

                roll_no = student["roll_no"]

                status = request.form.get(
                    roll_no,
                    "Absent"
                )

                conn.execute(
                    """
                    INSERT INTO attendance
                    (date, roll_no, status)
                    VALUES (?, ?, ?)
                    """,
                    (date, roll_no, status)
                )

            conn.commit()
            conn.close()

            return redirect("/")


    # Get Students
    students = conn.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()


    # Attendance Summary
    student_summary = []

    for student in students:

        roll_no = student["roll_no"]

        records = conn.execute(
            """
            SELECT status
            FROM attendance
            WHERE roll_no = ?
            ORDER BY date
            """,
            (roll_no,)
        ).fetchall()

        total_days = len(records)

        present_days = sum(
            1 for record in records
            if record["status"] == "Present"
        )

        if total_days > 0:

            percentage = round(
                (present_days / total_days) * 100,
                2
            )

        else:

            percentage = 0


        # AI prediction data
        attendance_values = []

        for record in records:

            if record["status"] == "Present":
                attendance_values.append(1)
            else:
                attendance_values.append(0)


        prediction = predict_attendance(
            attendance_values
        )


        student_summary.append({
            "name": student["name"],
            "roll_no": roll_no,
            "percentage": percentage,
            "prediction": prediction
        })


    # Attendance History
    attendance_history = conn.execute(
        """
        SELECT
            attendance.date,
            students.name,
            attendance.roll_no,
            attendance.status
        FROM attendance
        JOIN students
        ON attendance.roll_no = students.roll_no
        ORDER BY attendance.date DESC
        """
    ).fetchall()


    conn.close()


    return render_template(
        "index.html",
        students=students,
        student_summary=student_summary,
        attendance_history=attendance_history
    )


if __name__ == "__main__":
    app.run(debug=True)
