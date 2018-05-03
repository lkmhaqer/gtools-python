# file: op_webgui/models.py

from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

"""
IPv6 Addresses - 128 bit Internet Protocol Addresses

interface:    The logical interface the IP is tied to. (optional)
host:         IP Address itself                                                    [2001:db8:1:1::1]
cidr:         The CIDR (Classless Inter-Domain Routing) notation of mask length    [64]

Example string: 2001:db8:1:1::1/64
"""
class ipv6_address(models.Model):
    interface    = models.ForeignKey('logical_interface', on_delete=models.CASCADE, null=True, blank=True)
    host         = models.GenericIPAddressField(unpack_ipv4=False)
    cidr         = models.PositiveSmallIntegerField(default=64)

    def __str__(self):
        return str(self.host) + "/" + str(self.cidr)

"""
IPv4 Addresses - 32 bit Internet Protocol Addresses

interface:    The logical interface the IP is tied to. (optional)
host:         IP Address itself                                                    [198.51.100.0]
cidr:         The CIDR (Classless Inter-Domain Routing) notation of mask length    [24]

Example string: 198.51.100.0/24
"""
class ipv4_address(models.Model):
    interface    = models.ForeignKey('logical_interface', on_delete=models.CASCADE, null=True, blank=True)
    host         = models.GenericIPAddressField(unpack_ipv4=True)
    cidr         = models.PositiveSmallIntegerField(default=24)

    def __str__(self):
        return str(self.host) + "/" + str(self.cidr)

"""
Logical Interface - An abstract instance of a physical interface, usually seperated layer2 protocols (VLANs, DLCIs, etc.)

interface:             The physical interface that this logical interface is tied to.
name:                  Actual name of the interface, usually an integer.                                    [1]
description:           A quick sentence or details on what this interface holds. (optional)                 [An ethernet interface]
mtu:                   Maximum Transmission Unit, used when needed.                                         [1500]
vlan:                  A VLAN tag ID, used when needed. (optional)                                          [1]
physical_interface:    A boolean value if this logical interface takes up the entire physical interface.    [False]

Example string: Router1 FastEthernet1/0
                Router2 et-1/0/0.100
"""
class logical_interface(models.Model):
    interface             = models.ForeignKey('interface', on_delete=models.CASCADE)
    name                  = models.CharField(max_length=255)
    description           = models.CharField(max_length=1024, blank=True)
    mtu                   = models.BigIntegerField(default=1500)
    vlan                  = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1),MaxValueValidator(4096)])
    physical_interface    = models.BooleanField(default=0)

    def __str__(self):
        if self.physical_interface:
            return self.interface.router.hostname + " " + self.interface.name + " (" + self.description + ")"
        else:
            return self.interface.router.hostname + " " + self.interface.name + "." + self.name + " (" + self.description + ")"

"""
Interface - Physical network interface, may contain multiple logical interfaces.

router:         Router that the interface is tied to.
name:           Name of the actual interface, on the target platform.                   [et-1/0/0]
description:    A quick sentence or details on what this interface holds. (optional)    [An ethernet interface]
mtu:            Maximum Transmission Unit, used when needed.                            [1514]

Example string: Router1 et-1/0/0
"""
class interface(models.Model):
    router        = models.ForeignKey('router', on_delete=models.CASCADE)
    name          = models.CharField(max_length=255)
    description   = models.CharField(max_length=1024, blank=True)
    mtu           = models.BigIntegerField(default=1514)

    def __str__(self):
        return self.router.hostname + " " + self.name + " (" + self.description + ")"

"""
BGP Neighbor - Peering sesssions with our neighbors over BGP.

router:          Router that the peer session is tied to.
aut_num:         ASN that the peer session is tied to.
peer_ip:         IP Address of BGP neighbor.                                                          [203.0.113.1]
soft_inbound:    Boolean value for if soft-reconfiguration inbound is enabled on the peer session.    [True]

Example string: PeeringBuddy - Router1 203.0.113.1
"""
class neighbor(models.Model):
    router        = models.ForeignKey('router', on_delete=models.CASCADE)
    aut_num       = models.ForeignKey('aut_num', on_delete=models.CASCADE)
    peer_ip       = models.GenericIPAddressField(unpack_ipv4=True)
    soft_inbound  = models.BooleanField(default=1)

    def __str__(self):
        return self.aut_num.name + " - " + self.router.hostname + " " + self.peer_ip

"""
Router - A network device that moves packets around.

routing_id:    An IP address the router will use as identification and routing decisions.    [203.0.113.1]
hostname:      The (DNS) hostname of the router, domain included.                            [Router1.isp]
ibgp:          Boolean value to build an iBGP mesh with every router in the database.        [True]
network_os:    The network operating system and subsequent template this router is tied too.

Example string: Router1
"""
class router(models.Model):
    routing_id    = models.GenericIPAddressField(unpack_ipv4=True)
    hostname      = models.CharField(max_length=255)
    ibgp          = models.BooleanField()
    network_os    = models.ForeignKey('network_os', on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname

"""
Network Operating Systems - The software platform which runs networking focused hardware.

name:    The name of the NOS, and the template file to build the configuration with.

Example string: junos
                ios-12
                ios-xe
"""
class network_os(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

"""
Autonomous System Number - Used in BGPv4 to represent an administrative domain where internet prefixes are exchanged.

asn:        The actual autonomous system number of someone we neighbor.    [65000]
name:       A specific company or personal name for the peer.              [NTT Communications]
contact:    An email address to go along with the name.                    [john.smith@example.com]

Example string: 65000: NTT Communications (john.smith@example.com)
"""
class aut_num(models.Model):
    asn        = models.BigIntegerField(unique=True)
    name       = models.CharField(max_length=255)
    contact    = models.EmailField(blank=True)

    def __str__(self):
        return str(self.asn) + ": " + self.name + " (" + self.contact + ")"
