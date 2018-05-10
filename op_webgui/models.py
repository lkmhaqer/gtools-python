# file: op_webgui/models.py

from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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

    router      = models.ForeignKey('router', on_delete=models.CASCADE, null=True, blank=True)
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

    router      = models.ForeignKey('router', on_delete=models.CASCADE, null=True, blank=True)
    network     = models.GenericIPAddressField(unpack_ipv4=True)
    cidr        = models.PositiveSmallIntegerField(default=24)
    next_hop    = models.GenericIPAddressField(unpack_ipv4=True)

    def subnet_mask(self):
        host_bits = 32 - int(self.cidr)
        netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
        return netmask

    def __str__(self):
        return self.router.hostname + " " + str(self.network) + "/" + str(self.cidr) + " next-hop " + str(self.next_hop)




class ipv6_address(models.Model):
    """
    IPv6 Addresses - 128 bit Internet Protocol Addresses

    interface:    The logical interface the IP is tied to. (optional)
    host:         IP Address itself                                                    [2001:db8:1:1::1]
    cidr:         The CIDR (Classless Inter-Domain Routing) notation of mask length    [64]

    Example string: 2001:db8:1:1::1/64
    """

    interface    = models.ForeignKey('logical_interface', on_delete=models.CASCADE, null=True, blank=True)
    host         = models.GenericIPAddressField(unpack_ipv4=False)
    cidr         = models.PositiveSmallIntegerField(default=64)

    def __str__(self):
        return str(self.host) + "/" + str(self.cidr)




class ipv4_address(models.Model):
    """
    IPv4 Addresses - 32 bit Internet Protocol Addresses

    interface:    The logical interface the IP is tied to. (optional)
    host:         IP Address itself                                                    [198.51.100.0]
    cidr:         The CIDR (Classless Inter-Domain Routing) notation of mask length    [24]

    Example string: 198.51.100.0/24
    """

    interface    = models.ForeignKey('logical_interface', on_delete=models.CASCADE, null=True, blank=True)
    host         = models.GenericIPAddressField(unpack_ipv4=True)
    cidr         = models.PositiveSmallIntegerField(default=24)

    def subnet_mask(self):
        host_bits = 32 - int(self.cidr)
        netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
        return netmask

    def __str__(self):
        return str(self.host) + "/" + str(self.cidr)




class logical_interface(models.Model):
    """
    Logical Interface - An abstract instance of a physical interface, usually seperated layer2 protocols (VLANs, DLCIs, etc.)

    interface:             The physical interface that this logical interface is tied to.
    name:                  Actual name of the interface, usually an integer.                                    [1]
    description:           A quick sentence or details on what this interface holds. (optional)                 [An ethernet interface]
    mtu:                   Maximum Transmission Unit, used when needed.                                         [1500]
    vlan:                  A VLAN tag ID, used when needed. (optional)                                          [1]
    physical_interface:    A boolean value if this logical interface takes up the entire physical interface.    [False]
    ldp:                   A boolean value to set LDP transmit and recieve on the interface.                    [False]
    inet_dhcp_client:      A boolean value for using the interface as a dhcp-client.                            [False]
    inet6_dhcp_client:     A boolean value for using the interface as a dhcpv6-client.                          [False]

    Example string: Router1 FastEthernet1/0
                    Router2 et-1/0/0.100
    """

    interface             = models.ForeignKey('interface', on_delete=models.CASCADE)
    name                  = models.CharField(max_length=255)
    description           = models.CharField(max_length=1024, blank=True)
    mtu                   = models.BigIntegerField(default=1500)
    vlan                  = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1),MaxValueValidator(4096)])
    physical_interface    = models.BooleanField(default=False)
    ldp                   = models.BooleanField(default=False)
    inet_dhcp_client      = models.BooleanField(default=False)
    inet6_dhcp_client     = models.BooleanField(default=False)

    def __str__(self):
        if self.physical_interface:
            return self.interface.router.hostname + " " + self.interface.name + " (" + self.description + ")"
        else:
            return self.interface.router.hostname + " " + self.interface.name + "." + self.name + " (" + self.description + ")"




class interface(models.Model):
    """
    Interface - Physical network interface, may contain multiple logical interfaces.

    router:         Router that the interface is tied to.
    name:           Name of the actual interface, on the target platform.                   [et-1/0/0]
    description:    A quick sentence or details on what this interface holds. (optional)    [An ethernet interface]
    mtu:            Maximum Transmission Unit, used when needed.                            [1514]
    dot1q:          Enable 802.1Q VLAN Tags on the interface                                [True]

    Example string: Router1 et-1/0/0
    """

    router        = models.ForeignKey('router', on_delete=models.CASCADE)
    name          = models.CharField(max_length=255)
    description   = models.CharField(max_length=1024, blank=True)
    mtu           = models.BigIntegerField(default=1514)
    dot1q         = models.BooleanField(default=False)

    def __str__(self):
        return self.router.hostname + " " + self.name + " (" + self.description + ")"




class neighbor(models.Model):
    """
    BGP Neighbor - Peering sesssions with our neighbors over BGP.

    router:          Router that the peer session is tied to.
    aut_num:         ASN that the peer session is tied to.
    peer_ip:         IP Address of BGP neighbor.                                                          [203.0.113.1]
    soft_inbound:    Boolean value for if soft-reconfiguration inbound is enabled on the peer session.    [True]

    Example string: PeeringBuddy - Router1 203.0.113.1
    """

    router        = models.ForeignKey('router', on_delete=models.CASCADE)
    aut_num       = models.ForeignKey('aut_num', on_delete=models.CASCADE)
    peer_ip       = models.GenericIPAddressField(unpack_ipv4=True)
    soft_inbound  = models.BooleanField(default=True)

    def __str__(self):
        return self.aut_num.name + " - " + self.router.hostname + " " + self.peer_ip




class router(models.Model):
    """
    Router - A network device that moves packets around.

    routing_id:         An IP address the router will use as identification and routing decisions.    [203.0.113.1]
    hostname:           The (DNS) hostname of the router, domain included.                            [Router1.isp]
    ibgp:               Boolean value to build an iBGP mesh with every router in the database.        [True]
    network_os:         The network operating system and subsequent template this router is tied too.
    service_ssh:        Boolean value to enable SSHv2 on the router.                                  [True]
    service_netconf:    Boolean value to enable NETCONF on the router.                                [True]
    local_aut_num:      Local autonomous system number for the router.

    Example string: Router1
    """

    routing_id         = models.GenericIPAddressField(unpack_ipv4=True)
    hostname           = models.CharField(max_length=255)
    ibgp               = models.BooleanField()
    network_os         = models.ForeignKey('network_os', on_delete=models.CASCADE)
    service_ssh        = models.BooleanField(default=True)
    service_netconf    = models.BooleanField(default=True)
    local_aut_num      = models.ForeignKey('aut_num', on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname



class network_os(models.Model):
    """
    Network Operating Systems - The software platform which runs networking focused hardware.

    name:    The name of the NOS, and the template file to build the configuration with.    [junos]

    Example string: junos
                    ios-12
                    ios-xe
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name




class aut_num(models.Model):
    """
    Autonomous System Number - Used in BGPv4 to represent an administrative domain where internet prefixes are exchanged.

    asn:        The actual autonomous system number of someone we neighbor.    [65000]
    name:       A specific company or personal name for the peer.              [NTT Communications]
    contact:    An email address to go along with the name.                    [john.smith@example.com]

    Example string: 65000: NTT Communications (john.smith@example.com)
    """

    asn        = models.BigIntegerField(unique=True)
    name       = models.CharField(max_length=255)
    contact    = models.EmailField(blank=True)

    def __str__(self):
        return str(self.asn) + ": " + self.name + " (" + self.contact + ")"
