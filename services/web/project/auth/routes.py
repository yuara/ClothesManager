from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from flask_babel import _
from project import db
from project.auth import bp
from project.auth.forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
from project.models import User, Location
from project.auth.email import send_password_reset_email

# Get area_id from parent dropdown and show perf in child dropdown.
@bp.route("/_get_locations/")
def _get_locations():
    area = request.args.get("area", 1, type=int)
    locations = [
        (x.id, x.pref_name) for x in Location.query.filter_by(area_id=area).all()
    ]
    return jsonify(locations)


@bp.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for("auth.login"))

        # You login here
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", title=_("Sign Up"), form=form)


@bp.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm(form_name="RegistrationForm")
    if request.method == "GET":
        return render_template("auth/register.html", title=_("Register"), form=form)
    if form.validate_on_submit() and request.form["form_name"] == "RegistrationForm":
        user = User(
            username=form.username.data,
            email=form.email.data,
            location_id=form.location_pref.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_("Registered the new user successfully!"))
        return redirect(url_for("auth.login"))


@bp.route("/reset_password_request/", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # send a email to reset password if the user is correct.
        if user:
            send_password_reset_email(user)
        flash(_("Check your email for the instructions to reset your password"))
        return redirect(url_for("auth.login"))
    return render_template(
        "auth/reset_password_request.html", title=_("Reset Password"), form=form
    )


@bp.route("/reset_passowrd/<token>/", methods=["GET", "POST"])
def reset_passowrd(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    # reset passowrd
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_("Your password has been reset."))
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_passowrd.html", form=form)
