from model import Donation

def create_donation(donor, amount):
    """Creates a donation in the Donation model"""
    Donation.create(donor=donor, value=amount)
    return True

def get_donations_by_donor(donor):
    """Gets all donations for a user by donor"""
    Donation.select(donor=donor)