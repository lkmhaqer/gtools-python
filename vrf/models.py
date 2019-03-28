# file: vrf/models.py

from __future__ import unicode_literals
from django.db import models


class vrf(models.Model):
    """
    Virtual Routing and Forwarding - multiple co-existing routing instances in
                                     a single physical router.

    vrf_name:    The name of this VRF instance.
    vrf_target:  String of what the target identifier for the VRF is.
                 [target:65000:65000]

    Example string: VRF_Name (target:65000:65000)
    """

    vrf_name    = models.CharField(max_length=255)
    vrf_target  = models.CharField(max_length=255)

    def __str__(self):
        return self.vrf_name + " (" + self.vrf_target + ")"
