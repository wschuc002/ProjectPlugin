# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CBSmapper
                                 A QGIS plugin
 Can map CBS demographic data
                             -------------------
        begin                : 2016-01-25
        copyright            : (C) 2016 by Geodetic engeneers
        email                : saxoriko@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CBSmapper class from file CBSmapper.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .CBS_mapper import CBSmapper
    return CBSmapper(iface)
