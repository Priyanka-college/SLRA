from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="riskmanagement"
)
cursor = db.cursor(dictionary=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        activity = request.form["activity"]
        hazard = request.form["hazard"]
        description = request.form["description"]
        likelihood = int(request.form["likelihood"])
        consequence = int(request.form["consequence"])
        control = float(request.form["control"])
        control_desc = request.form["control_desc"]

        rpn_before = likelihood * consequence
        rpn_after = likelihood * consequence * control

        if rpn_after >= 10:
            risk_level = "High"
        elif rpn_after >= 5:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        cursor.execute("""
            INSERT INTO risks 
            (activity, hazard, description, likelihood, consequence, control, control_desc, rpn_before, rpn_after, risk_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (activity, hazard, description, likelihood, consequence, control, control_desc, rpn_before, rpn_after, risk_level))
        db.commit()

        return redirect("/")

    cursor.execute("SELECT * FROM risks ORDER BY id DESC")
    risks = cursor.fetchall()
    return render_template("index.html", risks=risks)

if __name__ == "__main__":
    app.run(debug=True)
