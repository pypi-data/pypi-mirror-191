#!/usr/bin/env python

# SPDX-FileCopyrightText: 2017-2023 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2017-2023 GNU Solidario <health@gnusolidario.org>

# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#             GNUHEALTH HOSPITAL MANAGEMENT - GTK CLIENT                #
#                     https://www.gnuhealth.org                         #
#########################################################################
#                  activity.py: Activity log window                     #
#########################################################################
# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from gnuhealth.config import GNUHEALTH_ICON
from gi.repository import Gtk


class Activity():
    "GNU Health client Activity Logger"
    activity_window = Gtk.Window()
    activity_window.set_default_size(500, 500)
    activity_window.set_title("Activity log - GNU Health ")
    activity_window.set_icon(GNUHEALTH_ICON)

    sw = Gtk.ScrolledWindow()
    sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

    # TextView
    activity = Gtk.TextView()
    sw.add(activity)

    # Make it read-only
    activity.set_editable(False)
    textbuffer = activity.get_buffer()

    activity_window.add(sw)
