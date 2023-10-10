
from flask import Flask, render_template, session, redirect, url_for, flash, request
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

# Define a custom validator function for the email field
def validate_uoft_email(form, field):
    if "@" not in field.data:
        raise ValidationError('Please include an "@" in the email.')

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    
    # Add the custom validator to the email field
    email = StringField('What is your UofT Email address', validators=[DataRequired(), Email(), validate_uoft_email])
    
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if request.method == 'POST' and form.validate():
        session.permanent = False
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        
        # Check if "@" is missing in the email field
        if old_email is not None and old_email != form.email.data:
            if "@" not in form.email.data:
                flash('Please include an "@" in the email.')
        elif old_email is not None and old_email != form.email.data:
            if "utoronto" not in form.email.data:
                flash('Please include an "utoronto" in the email.')

        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

@app.route('/user/<name>')
def user(name):
    print(datetime.utcnow())
    return render_template('user.html', name=name, current_time=datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True)