import math

import pycountry


def get_data_dict(instance):
    """
    Get data dictionary from model instance.
    """
    return {
        field.name: getattr(instance, field.name)
        for field in instance._meta.fields
        if field.name not in ["id", "created_at", "updated_at"]
    }


def distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def get_currency_by_country(country):
    country = pycountry.countries.get(name=country)
    if not country:
        return None
    return pycountry.currencies.get(numeric=country.numeric).alpha_3


def get_country_by_currency(currency):
    currency = pycountry.currencies.get(alpha_3=currency)
    if not currency:
        return None
    return pycountry.countries.get(numeric=currency.numeric).alpha_2
