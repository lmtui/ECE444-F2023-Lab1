from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    name = "Lisa"  # Replace with your desired name
    current_time = datetime.now()
    event_time = current_time - timedelta(minutes=1)  # Set event time to 1 minute before current time
    elapsed_time = int((current_time - event_time).total_seconds() / 60)  # Calculate elapsed time in minutes and round to the nearest integer
    return render_template('user.html', name=name, current_time=current_time, elapsed_time=elapsed_time)

if __name__ == '__main__':
    app.run(debug=True)
