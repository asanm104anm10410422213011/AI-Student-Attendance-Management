from flask import Flask, render_template, request, redirect

app = Flask(__name__)

students = []

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        name = request.form["name"]
        roll_no = request.form["roll_no"]
        date = request.form["date"]
        status = request.form["status"]

        students.append({
            "name": name,
            "roll_no": roll_no,
            "date": date,
            "status": status
        })

        return redirect("/")

    return render_template("index.html", students=students)


if __name__ == "__main__":
    app.run(debug=True)
