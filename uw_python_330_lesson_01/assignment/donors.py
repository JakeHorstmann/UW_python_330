from model import Donor
from peewee import DoesNotExist

def create_donor(name):
    """Creates a donor in the Donor model"""
    if get_donor_by_name(name):
        return False
    Donor.create(name=name)
    return True

def get_donor_by_name(name):
    """Finds a donor by name"""
    try:
        donor = Donor.get(Donor.name == name)
    except DoesNotExist:
        return None
    return donor