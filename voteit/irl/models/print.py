# -*- coding: utf-8 -*-
from voteit.core.models.meeting import Meeting


def includeme(config):
    """ Add settings attribute to Meeting object"""
    Meeting.print_btn_enabled = ()
