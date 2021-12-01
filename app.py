from flask import Flask, render_template, abort, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_mail import Message, Mail
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_admin.contrib.sqla import ModelView
import sqlalchemy
import os
from os import environ
from dotenv import load_dotenv


#######################################################################################################################
# CONFIG BLOCK
#######################################################################################################################


app = Flask(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')

app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')

app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')

db = SQLAlchemy(app)
admin = Admin(app)

ADMIN_USERNAME = environ.get('ADMIN_USERNAME')

ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD')

mail = Mail(app)


#######################################################################################################################
# MODELS BLOCK
#######################################################################################################################


class BioLang(db.Model):
    __tablename__ = "Biography"
    id = db.Column(db.Integer, primary_key=True)
    language_title = db.Column(db.String(50))
    content = db.Column(db.Text)
    slug_language_id = db.Column(db.String(10))


class RepertoireSolo(db.Model):
    __tablename__ = "Repertoire Solo"
    id = db.Column(db.Integer, primary_key=True)
    composer = db.Column(db.String(100))
    title = db.Column(db.Text)


class RepertoireWithPiano(db.Model):
    __tablename__ = "Repertoire With Piano"
    id = db.Column(db.Integer, primary_key=True)
    composer = db.Column(db.String(100))
    title = db.Column(db.Text)


class RepertoireWithOrchestra(db.Model):
    __tablename__ = "Repertoire With Orchestra"
    id = db.Column(db.Integer, primary_key=True)
    composer = db.Column(db.String(100))
    title = db.Column(db.Text)


class RepertoireChamber(db.Model):
    __tablename__ = "Repertoire Chamber Music"
    id = db.Column(db.Integer, primary_key=True)
    composer = db.Column(db.String(100))
    title = db.Column(db.Text)


class Event(db.Model):
    __tablename__ = "Events"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(400))
    description = db.Column(db.Text)
    ticket_link = db.Column(db.String(200))


class VideoLink(db.Model):
    __tablename__ = "Video Link"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    link = db.Column(db.Text)


class PhotoLink(db.Model):
    __tablename__ = "Photo Link"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    link = db.Column(db.Text)


class ContactData(db.Model):
    __tablename__ = "Contacts"
    id = db.Column(db.Integer, primary_key=True)
    contact_person = db.Column(db.String(200))
    phone_number = db.Column(db.String(50))
    phone_number_optional = db.Column(db.String(50), nullable=True)
    e_mail = db.Column(db.String(100))
    e_mail_optional = db.Column(db.String(100), nullable=True)
    whatsapp_number_optional = db.Column(db.String(30), nullable=True)


#######################################################################################################################
# MODEL VIEW BLOCK
#######################################################################################################################


class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)


admin.add_view(SecureModelView(BioLang, db.session))
admin.add_view(SecureModelView(RepertoireSolo, db.session))
admin.add_view(SecureModelView(RepertoireWithPiano, db.session))
admin.add_view(SecureModelView(RepertoireWithOrchestra, db.session))
admin.add_view(SecureModelView(RepertoireChamber, db.session))
admin.add_view(SecureModelView(Event, db.session))
admin.add_view(SecureModelView(VideoLink, db.session))
admin.add_view(SecureModelView(PhotoLink, db.session))
admin.add_view(SecureModelView(ContactData, db.session))


#######################################################################################################################
# FORMS BLOCK
#######################################################################################################################

class FeedbackForm(FlaskForm):
    email = EmailField(label='Enter your e-mail address', validators=[DataRequired()])
    subject = StringField(label='Enter your subject', validators=[DataRequired()])
    text = TextAreaField(label='Enter Your Message', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class LoginForm(FlaskForm):
    login = StringField(label="Enter the login", validators=[DataRequired()])
    password = PasswordField(label="Enter The Password", validators=[DataRequired()])
    submit = SubmitField(label='Submit')


#######################################################################################################################
# ROUTES BLOCK
#######################################################################################################################


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/bio')
def main_bio_page():
    bios = BioLang.query.all()
    bio = BioLang.query.get(1)
    return render_template('bio_page.html', bios=bios, sel_bio=bio)


@app.route('/bio/<string:slug_language_id>')
def other_bio_pages(slug_language_id):
    try:
        bios = BioLang.query.all()
        bio = BioLang.query.filter_by(slug_language_id=slug_language_id).one()
        return render_template('bio_page.html', bios=bios, sel_bio=bio)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)


@app.route('/repertoire')
def rep_page():
    solo = RepertoireSolo.query.order_by(RepertoireSolo.composer)
    with_piano = RepertoireWithPiano.query.order_by(RepertoireWithPiano.composer)
    with_orchestra = RepertoireWithOrchestra.query.order_by(RepertoireWithOrchestra.composer)
    chamber = RepertoireChamber.query.order_by(RepertoireChamber.composer)

    return render_template('rep_page.html', solo=solo, with_piano=with_piano,
                           with_orchestra=with_orchestra, chamber=chamber)


@app.route('/events')
def event_page():
    events = Event.query.order_by(Event.date.desc())  # ?????
    return render_template('event_page.html', events=events)


@app.route('/media')
def media_page():
    photos = PhotoLink.query.all()
    videos = VideoLink.query.all()
    return render_template('media_page.html', photos=photos, videos=videos)


@app.route('/contacts')
def contact_page():
    contacts = ContactData.query.all()
    return render_template('contact_page.html', contacts=contacts)


@app.route('/feedback', methods=["POST", "GET"])
def feedback_page():
    form = FeedbackForm()
    if form.validate_on_submit():
        email = form.email.data
        subject = form.subject.data
        text = form.text.data
        message = Message(subject, [app.config['MAIL_USERNAME']])
        message.html = render_template('mail.html', email=email, subject=subject, text=text)
        mail.send(message)
        notification = "The message was sent successfully"
        return render_template('feedback_page.html', form=form, notification=notification)
    return render_template('feedback_page.html', form=form)


@app.route('/login', methods=["POST", "GET"])
def admin_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.login.data == ADMIN_USERNAME and form.password.data == ADMIN_PASSWORD:
                session['logged_in'] = True
                return redirect('/admin')
            else:
                return render_template('login.html', form=form, notification="Incorrect Data")
        else:
            return render_template('login.html', form=form, notification="Incorrect Data")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")
