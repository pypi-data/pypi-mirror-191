"""
forms for :mod:`django_notifications.admin` application.

:creationdate:  07/01/2022 10:33
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.admin.forms
"""
import logging

from django import forms

from django_notifications import models

__author__ = "fguerin"
logger = logging.getLogger(__name__)


class NotificationAdminForm(forms.ModelForm):
    """Admin form for :class:`django_notifications.models.Notification` model."""

    class Meta:
        """Meta class for :class:`django_notifications.admin.NotificationAdminForm`."""

        model = models.Notification
        fields = "__all__"
