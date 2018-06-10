# file: address/models.py

from __future__ import unicode_literals
from django.db import models
import socket, struct

class ipv6_address(models.Model):
    """
    IPv6 Addresses - 128 bit Internet Protocol Addresses
    interface:    The logical interface the IP is tied to. (optional)
    host:         IP Address itself
                  [2001:db8:1:1::1]
    cidr:         The CIDR (Classless Inter-Domain Routing)
                  notation of mask length
                  [64]
    Example string: 2001:db8:1:1::1/64
    """

    interface    = models.ForeignKey(
                                     'netdevice.logical_interface',
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True
                                    )
    host         = models.GenericIPAddressField(unpack_ipv4=False)
    cidr         = models.PositiveSmallIntegerField(default=64)

    def __str__(self):
        return str(self.host) + "/" + str(self.cidr)




class ipv4_address(models.Model):
    """
    IPv4 Addresses - 32 bit Internet Protocol Addresses
    interface:      The logical interface the IP is tied to. (optional)
    host:           IP Address itself
                    [198.51.100.0]
    cidr:           The CIDR (Classless Inter-Domain Routing)
                    notation of mask length
                    [24]
    Example string: 198.51.100.0/24
    """

    interface    = models.ForeignKey(
                                     'netdevice.logical_interface',
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True
                                    )
    host         = models.GenericIPAddressField(unpack_ipv4=True)
    cidr         = models.PositiveSmallIntegerField(default=24)

    def subnet_mask(self):
        host_bits = 32 - int(self.cidr)
        bitmask = struct.pack('!I', (1 << 32) - (1 << host_bits))
        netmask = socket.inet_ntoa(bitmask)
        return netmask

    def __str__(self):
        return str(self.host) + "/" + str(self.cidr)

