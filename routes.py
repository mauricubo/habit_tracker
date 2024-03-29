import datetime
import uuid
import socket
from flask import Blueprint, current_app, render_template, redirect, request, url_for

pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")

# Allows Jinja to access to this function in all context
@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {'date_range': date_range}

# Just a simple function
def today_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)

def get_hostname():
    return socket.gethostname()

# Index of the page, shows the calendar and the list of habits
@pages.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = today_at_midnight()

    habits_on_date = current_app.db.habits.find({"added": {"$lte": selected_date}})
    completions = [
        habit["habit"]
        for habit in current_app.db.completions.find({"date": selected_date})
    ]

    return render_template("index.html", 
                           habits=habits_on_date, 
                           title="Habit Tracker - Home", 
                           # date_range=date_range, removed from here because was added to the context 
                           completions=completions,
                           selected_date=selected_date,
                           hostname=get_hostname()
                           )

# Add a new habit to the daily list
@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    today = today_at_midnight()

    if request.method == "POST":
        current_app.db.habits.insert_one(
            {"_id": uuid.uuid4().hex, "added": today, "name": request.form.get("habit")}
        )
    
    return render_template(
            "add_habit.html", 
            title="Habit Tracker - Add Habit",
            selected_date=today, # because we want to add habits for today  
            hostname=get_hostname()
        )

# Check the habit as complete on the day
@pages.route("/complete", methods=["POST"])
def complete():
    date_string = request.form.get("date")
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_string)
    current_app.db.completions.insert_one({"date": date, "habit": habit})

    return redirect(url_for("habits.index", date=date_string))
