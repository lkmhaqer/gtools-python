# file: bgp/models.py

from __future__ import unicode_literals
from django.db import models

class neighbor(models.Model):
    """
    BGP Neighbor - Peering sesssions with our neighbors over BGP.

    router:          Router that the peer session is tied to.
    aut_num:         ASN that the peer session is tied to.
    peer_ip:         IP Address of BGP neighbor.
                     [203.0.113.1]
    soft_inbound:    Boolean value for if soft-reconfiguration inbound is
                     enabled on the peer session.
                     [True]

    Example string: PeeringBuddy - Router1 203.0.113.1
    """

    router        = models.ForeignKey(
                                      'netdevice.router',
                                      on_delete=models.CASCADE
                                     )
    vrf           = models.ForeignKey(
                                      'netdevice.vrf',
                                      on_delete=models.CASCADE,
                                      null=True,
                                      blank=True
                                     )
    aut_num       = models.ForeignKey('aut_num', on_delete=models.CASCADE)
    peer_ip       = models.GenericIPAddressField(unpack_ipv4=True)
    soft_inbound  = models.BooleanField(default=True)

    def __str__(self):
        asn_router = self.aut_num.name + " - " + self.router.hostname + " "
        return asn_router + self.peer_ip



class aut_num(models.Model):
    """
    Autonomous System Number - Used in BGPv4 to represent an
                               administrative domain where internet prefixes
                               are exchanged.

    asn:        The actual autonomous system number of someone we neighbor.
                [65000]
    name:       A specific company or personal name for the peer.
                [123 ISP Inc.]
    contact:    An email address to go along with the name.
                [john.smith@example.com]

    Example string: 65000: 123 ISP Inc. (john.smith@example.com)
    """

    asn        = models.BigIntegerField(unique=True)
    name       = models.CharField(max_length=255)
    contact    = models.EmailField(blank=True)
    vrf        = models.ForeignKey(
                                   'netdevice.vrf',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True
                                  )

    def __str__(self):
        return str(self.asn) + ": " + self.name + " (" + self.contact + ")"
