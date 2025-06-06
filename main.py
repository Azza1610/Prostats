# SlabStats
from flask import Flask, session, redirect, render_template, request
import logging
import bcrypt
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
from flask_session import Session

import userManagement as dbHandler
import driverManagement as driverHandler

# Logging config
app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

app = Flask(__name__)
app.secret_key = b"_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Redirect legacy index URLs to "/"


@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["POST", "GET"])
@csp_header({
    "base-uri": "'self'",
    "default-src": "'self'",
    "style-src": "'self'",
    "script-src": "'self'",
    "img-src": "'self' data:",
    "media-src": "'self'",
    "font-src": "'self'",
    "object-src": "'self'",
    "child-src": "'self'",
    "connect-src": "'self'",
    "worker-src": "'self'",
    "report-uri": "/csp_report",
    "frame-ancestors": "'none'",
    "form-action": "'self'",
    "frame-src": "'none'",
})
def index():
    # isLoggedin = session.get("isLoggedin")
    # user_name = session.get("user_name")
    drivers = []
    races = []
    if request.method == "POST":
        query = request.form["query"]
        print(query)
        drivers = driverHandler.search_drivers(query)
        races = driverHandler.search_races(query)
    return render_template("/index.html", drivers = drivers, races = races)


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")



@app.route("/delete_driver.html", methods=["POST"])
def delete_driver():
    if not session.get("isLoggedin"):
        return redirect("/login.html", code = 302)
    driver_id = request.form["driver_id"]
    driverHandler.delete_driver(driver_id)
    return redirect("/list_drivers.html", code=302)

@app.route("/signup.html", methods=["POST", "GET"])
def signup():
    error = ""
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        invite_code = request.form["invite_code"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if invite_code == "code":
            if password != confirm_password:
                return render_template("/signup.html", error="Passwords do not match")
            else:
                encoded_password = password.encode()
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(
                    password=encoded_password, salt=salt)
                dbHandler.insert_user(email, name, hashed_password)
            return redirect("/", code=302)
        else:
             error="Invaild invite code"
    return render_template("/signup.html", error = error)


@app.route("/login.html", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = dbHandler.login(email, password)
        if user:
            session["isLoggedin"] = True
            session["user_name"] = user['name']
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect("/", code=302)
        else:
            return render_template("/login.html", error="Login failed")
    return render_template("/login.html")


@app.route("/logout.html", methods=["GET"])
def logout():
    session["isLoggedin"] = False
    session["user_name"] = None
    session["role"] = None
    session["user_id"] = None
    return redirect("/", code=302)


@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


@app.route("/add_driver.html", methods=["POST", "GET"])
def add_driver():
    if not session.get("isLoggedin"):
        return redirect("/login.html", code = 302)
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        team_id = request.form["team_id"]
        driverHandler.insert_driver(name, age, team_id)
        return redirect("/", code=302)
    else:
        teams = driverHandler.list_teams()
        return render_template("/drivers/add.html", teams=teams)


@app.route("/list_teams.html")
def list_teams():
    teams = driverHandler.list_teams()
    return render_template("teams/index.html", teams=teams)


@app.route("/list_drivers.html", methods=["GET"])
def list_drivers():
    drivers = driverHandler.list_drivers()
    return render_template("drivers/index.html", drivers=drivers)


@app.route("/view_driver.html", methods=["GET"])
def view_driver():
    driver_id = request.args.get("driver_id")
    driver = driverHandler.get_driver(driver_id)  # returns dict with points
    # returns list of dicts for races
    races = driverHandler.get_races(driver_id)
    return render_template("drivers/view.html", driver=driver, races=races)


@app.route("/list_races.html", methods=["GET"])
def list_races():
    races = driverHandler.list_races()
    return render_template("races/index.html", races=races)


@app.route("/race_result.html", methods=["GET"])
def race_result():
    race_id = request.args.get("race_id")
    result = driverHandler.get_result(race_id)
    return render_template("races/result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
