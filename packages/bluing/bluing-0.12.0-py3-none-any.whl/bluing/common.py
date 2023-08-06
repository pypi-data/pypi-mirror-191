#!/usr/bin/env python

import io
import pkg_resources

from dbus.exceptions import DBusException

from xpycommon.log import Logger
from xpycommon.ui import blue, red

from . import LOG_LEVEL


logger = Logger(__name__, LOG_LEVEL)

oui_file = pkg_resources.resource_stream(__name__, "res/oui.txt")
oui_file = io.TextIOWrapper(oui_file)
oui_company_names = {}
for line in oui_file:
    items = line.strip().split('\t\t')
    if len(items) == 2 and '   (hex)' in items[0]:
        company_id = items[0].removesuffix('   (hex)')
        oui_company_names[company_id] = items[1]
        
# logger.debug("oui_company_names: {}".format(oui_company_names))


class InvalidArgsException(DBusException):
    _dbus_error_name = 'org.freedesktop.DBus.Error.InvalidArgs'

class NotSupportedException(DBusException):
    _dbus_error_name = 'org.bluez.Error.NotSupported'

class NotPermittedException(DBusException):
    _dbus_error_name = 'org.bluez.Error.NotPermitted'

class InvalidValueLengthException(DBusException):
    _dbus_error_name = 'org.bluez.Error.InvalidValueLength'

class FailedException(DBusException):
    _dbus_error_name = 'org.bluez.Error.Failed'

class Rejected(DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"


def bdaddr_to_company_name(addr: str):
    company_id = addr.replace(':', '-').upper()[0:8]
    
    logger.debug("bdaddr_to_company_name(), addr: " + addr)
    logger.debug(company_id)

    try:
        return blue(oui_company_names[company_id])
    except KeyError:
        return red('Unknown')
