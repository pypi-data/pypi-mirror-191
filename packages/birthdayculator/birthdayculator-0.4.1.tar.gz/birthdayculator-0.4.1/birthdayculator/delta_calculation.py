from arrow import Arrow
from dateutil.relativedelta import relativedelta


def calculate_delta(first: Arrow, second: Arrow) -> relativedelta:
    return relativedelta(second.date(), first.date())
