import dateutil
import six
import datetime


class TimezoneError(Exception):
    pass


def mktz(zone=None):
    """
    Return a new timezone (datetime.tzinfo object) based on the zone using the datetime
    package.

    The concise name 'mktz' is for convenient when using it on the
    console.

    Parameters
    ----------
    zone : `String`
           The zone for the timezone. This defaults to local, returning:
           datetime.datetime.now().astimezone().tzinfo

    Returns
    -------
    An instance of a timezone which implements the tzinfo interface.

    Raises
    - - - - - -
    TimezoneError : Raised if a user inputs a bad timezone name.
    """
    if zone is None:
        tz = datetime.datetime.now().astimezone().tzinfo
        zone = tz.tzname(None)
    elif zone=='UTC' or zone == 'utc':
        tz = datetime.timezone.utc
    else:
        zone = six.u(zone)
        tz = dateutil.tz.gettz(zone)
        if not tz:
            raise TimezoneError('Timezone "%s" can not be read' % (zone))
        # Stash the zone name as an attribute (as pytz does)
        if not hasattr(tz, 'zone'):
            tz.zone = zone
            for p in dateutil.tz.TZPATHS:
                if zone.startswith(p):
                    tz.zone = zone[len(p) + 1:]
                    break
    return tz
