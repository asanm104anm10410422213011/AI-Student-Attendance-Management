from flask import Flask, render_template, request, redirect
from model import predict_attendance
import sqlite3
from datetime import date

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn


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

    if request.method == "POST":

        action = request.form.get("action")

        # Add Student
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

            attendance_date = request.form["date"]

            students = conn.execute(
                "SELECT * FROM students"
            ).fetchall()

            conn.execute(
                "DELETE FROM attendance WHERE date = ?",
                (attendance_date,)
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
                    (attendance_date, roll_no, status)
                )

            conn.commit()
            conn.close()

            return redirect("/")


    # Students
    students = conn.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()


    # Dashboard
    total_students = len(students)

    today = date.today().isoformat()

    today_present = conn.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE date = ?
        AND status = 'Present'
        """,
        (today,)
    ).fetchone()[0]


    today_absent = conn.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE date = ?
        AND status = 'Absent'
        """,
        (today,)
    ).fetchone()[0]


    total_days = conn.execute(
        """
        SELECT COUNT(DISTINCT date)
        FROM attendance
        """
    ).fetchone()[0]


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

        total = len(records)

        present = sum(
            1
            for record in records
            if record["status"] == "Present"
        )

        if total > 0:
            percentage = round(
                (present / total) * 100,
                2
            )
        else:
            percentage = 0


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
        attendance_history=attendance_history,
        total_students=total_students,
        today_present=today_present,
        today_absent=today_absent,
        total_days=total_days
    )


if __name__ == "__main__":
    app.run(debug=True)
