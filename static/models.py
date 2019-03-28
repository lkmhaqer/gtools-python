# file: static/models.py

from __future__ import unicode_literals
from django.db import models
import socket, struct

class ipv6_static(models.Model):
    """
    IPv6 Static Routes - Routes set by the user in a given router.

    router:       The router to place this static route.
    network:      The network address of the route.                                    [2001:db8::]
    cidr:         The CIDR length of this static route.                                [64]
    next-hop:     Next-hop device of this static route.                                [2001:db8:1:1::1]

    Example string: Router1 2001:db8:: next-hop 2001:db8:1:1::1
    """

    router      = models.ForeignKey('netdevice.router', on_delete=models.CASCADE, null=True, blank=True)
    vrf         = models.ForeignKey(
                                    'netdevice.vrf',
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True
                                   )
    network     = models.GenericIPAddressField(unpack_ipv4=False)
    cidr        = models.PositiveSmallIntegerField(default=64)
    next_hop    = models.GenericIPAddressField(unpack_ipv4=True)

    def __str__(self):
        return self.router.hostname + " " + str(self.network) + "/" + str(self.cidr) + " next-hop " + str(self.next_hop)




class ipv4_static(models.Model):
    """
    IPv4 Static Routes - Routes set by the user in a given router

    router:       The router to place this static route.
    network:      The network address of the route.                                    [198.51.100.0]
    cidr:         The CIDR length of this static route.                                [24]
    next-hop:     Next-hop device of this static route.                                [198.51.100.1]

    Example string: Router1 198.51.100.0/24 next-hop 198.51.100.1
    """

    router      = models.ForeignKey('netdevice.router', on_delete=models.CASCADE, null=True, blank=True)
    vrf         = models.ForeignKey(
                                    'netdevice.vrf',
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True
                                   )
    network     = models.GenericIPAddressField(unpack_ipv4=True)
    cidr        = models.PositiveSmallIntegerField(default=24)
    next_hop    = models.GenericIPAddressField(unpack_ipv4=True)

    def subnet_mask(self):
        host_bits = 32 - int(self.cidr)
        netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
        return netmask

    def __str__(self):
        return self.router.hostname + " " + str(self.network) + "/" + str(self.cidr) + " next-hop " + str(self.next_hop)
