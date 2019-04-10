# file: netdevice/models.py

from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
    vrf                   = models.ForeignKey(
                                              'netdevice.vrf',
                                              on_delete=models.CASCADE,
                                              null=True,
                                              blank=True
                                             )
    name                  = models.CharField(max_length=255)
    description           = models.CharField(max_length=1024, blank=True)
    mtu                   = models.BigIntegerField(default=1500)
    vlan                  = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1),MaxValueValidator(4096)])
    physical_interface    = models.BooleanField(default=False)
    ldp                   = models.BooleanField(default=False)
    inet_dhcp_client      = models.BooleanField(default=False)
    inet6_dhcp_client     = models.BooleanField(default=False)
    disabled              = models.BooleanField(default=False)

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
    disabled      = models.BooleanField(default=False)

    def __str__(self):
        return self.router.hostname + " " + self.name + " (" + self.description + ")"




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
    local_aut_num      = models.ForeignKey('bgp.aut_num', on_delete=models.CASCADE)

    def ldp_exists(self):
        return self.interface_set.filter(logical_interface__ldp=True).exists()

    def __str__(self):
        return self.hostname


class vrf(models.Model):
    """
    Virtual Routing and Forwarding - multiple co-existing routing instances in
                                     a single physical router.

    vrf_name:    The name of this VRF instance.
    vrf_target:  String of what the target identifier for the VRF is.
                 [target:65000:65000]

    Example string: VRF_Name (target:65000:65000)
    """

    name    = models.CharField(max_length=255)
    target  = models.CharField(max_length=255)

    def __str__(self):
        return self.name + " (" + self.target + ")"


class network_os(models.Model):
    """
    Network Operating Systems - The software platform which runs networking focused hardware.
    name:                  The name of the NOS, and the template file to build the configuration with.    [junos]
    mgmt_interface_name:   Name prefix for platform management interfaces.                                [fxp]
    Example string: junos
                    ios-12
                    ios-xe
    """

    name                = models.CharField(max_length=255)
    mgmt_interface_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


