import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session, abort

from model import Donation 
import donors, donations

app = Flask(__name__)

@app.route('/')
def home():
    """Sets the home page for the app"""
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    """Displays all donators to the user"""
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route("/donations/<name>/")
def user_donations(name):
    """Displays all donations for a user"""
    donor = donors.get_donor_by_name(name)
    # handle if the donor does not exist
    if not donor:
        abort(404)
    # return user donation page
    donations = list(donor.donations.select())
    return render_template('donations.jinja2', donations=donations)


@app.route("/donate/", methods=["GET", "POST"])
def donate():
    """Adds a donation page to the web app"""
    # ensure it is a form
    if request.method == "POST":
        donor_name = request.form["donor_name"]
        donation_amount = request.form["donation_amount"]
        # check that the user inputted values
        if donor_name and donation_amount:
            donation_amount = int(donation_amount)
            # create donor if they DNE
            if not donors.get_donor_by_name(donor_name):
                donors.create_donor(donor_name)
            # add donation
            donor = donors.get_donor_by_name(donor_name)
            donations.create_donation(donor, donation_amount)
            return redirect(url_for("home"))
    return render_template("donate.jinja2")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

