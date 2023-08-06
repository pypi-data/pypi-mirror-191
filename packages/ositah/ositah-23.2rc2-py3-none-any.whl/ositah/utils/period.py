# Module providing functions related to declaration period

from datetime import datetime
from typing import List

from .exceptions import ValidationPeriodAmbiguous, ValidationPeriodMissing


class OSITAHDeclarationPeriod:
    def __init__(self, name: str, start_date: str, end_date: str):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def get_name(self):
        return self.name

    def get_dates(self):
        return self.start_date, self.end_date

    def get_label(self):
        return f"{self.get_name()} ({' au '.join(self.get_dates())})"

    def get_start_date(self):
        return self.start_date


def get_validation_period_data(period_date: str):
    """
    Return the current declaration period object.

    :param period_date: a date that must be inside the declaration period
    :return: declaration period object (OSITAHValidationPeriod)
    """

    from .hito_db import OSITAHValidationPeriod

    selection_date = datetime.fromisoformat(period_date)
    period_id = OSITAHValidationPeriod.query.filter(
        OSITAHValidationPeriod.start_date <= selection_date,
        OSITAHValidationPeriod.end_date >= selection_date,
    ).all()
    if len(period_id) == 1:
        return period_id[0]
    elif len(period_id) > 1:
        raise ValidationPeriodAmbiguous(selection_date)
    else:
        raise ValidationPeriodMissing(selection_date)


def get_validation_period_dates(period_date: str):
    """
    Return the start and end date of the current declaration period.

    :param period_date: a date that must be inside the declaration period
    :return: UUID
    """

    validation_period = get_validation_period_data(period_date)
    return validation_period.start_date, validation_period.end_date


def get_validation_period_id(period_date: str):
    """
    Return the current declaration period ID.

    :param period_date: a date that must be inside the declaration period
    :return: UUID
    """

    return get_validation_period_data(period_date).id


def get_declaration_periods():
    """
    Return a list of declaration period name and dates, sorted by start date in descending order.
    Dates are strings, without the time information.

    :return: list of OSITAHDeclarationPeriod
    """

    from .hito_db import OSITAHValidationPeriod

    periods = []

    periods_data = OSITAHValidationPeriod.query.order_by(
        OSITAHValidationPeriod.start_date.desc()
    ).all()

    for row in periods_data:
        periods.append(
            OSITAHDeclarationPeriod(
                row.name,
                row.start_date.date().isoformat(),
                row.end_date.date().isoformat(),
            )
        )

    return periods


def get_default_period_date(periods: List[OSITAHDeclarationPeriod], date: datetime.date):
    """
    Return the start date of the default period. The default period is selected by passing a date
    that must be between period start and end dates (included).

    :param periods: period list
    :param date: date that must be inside the period (string)
    :return: period start date (string) or None if not found
    """

    period_date = date.isoformat()

    for p in periods:
        if period_date >= p.start_date and period_date <= p.end_date:
            return p.get_start_date()

    return None
