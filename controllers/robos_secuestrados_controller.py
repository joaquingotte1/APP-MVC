from models.robos_secuestrados_model import get_all, get_by_field, get_by_date_range

def fetch_all_robos_secuestrados():
    return get_all()

def fetch_robos_secuestrados_by_field(field, value):
    return get_by_field(field, value)

def fetch_robos_secuestrados_by_date_range(start_date, end_date):
    return get_by_date_range(start_date, end_date)