from __future__ import unicode_literals

from django.db import models

class ipv6_address(models.Model):
    interface = models.ForeignKey('logical_interface', on_delete=models.CASCADE)
    host      = models.GenericIPAddressField(unpack_ipv4=False)
    cidr      = models.PositiveSmallIntegerField(default=64)

    def __str__(self):
        return str(self.host) + "/" + str(self.cidr)

class ipv4_address(models.Model):
    interface = models.ForeignKey('logical_interface', on_delete=models.CASCADE)
    host      = models.GenericIPAddressField(unpack_ipv4=True)
    cidr      = models.PositiveSmallIntegerField(default=24)

    def __str__(self):
        return str(self.host) + "/" + str(self.cidr)

class logical_interface(models.Model):
    interface     = models.ForeignKey('interface', on_delete=models.CASCADE)
    name          = models.CharField(max_length=255)
    description   = models.CharField(max_length=1024, blank=True)
    mtu           = models.BigIntegerField(default=1500)
    vlan          = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.interface.router.hostname + " " + self.interface.name + "." + self.name + " (" + self.description + ")"

class interface(models.Model):
    router        = models.ForeignKey('router', on_delete=models.CASCADE)
    name          = models.CharField(max_length=255)
    description   = models.CharField(max_length=1024, blank=True)
    mtu           = models.BigIntegerField(default=1514)

    def __str__(self):
        return self.router.hostname + " " + self.name + " (" + self.description + ")"

class neighbor(models.Model):
    router        = models.ForeignKey('router', on_delete=models.CASCADE)
    aut_num       = models.ForeignKey('aut_num', on_delete=models.CASCADE)
    peer_ip       = models.GenericIPAddressField(unpack_ipv4=True)
    soft_inbound  = models.BooleanField(default=1)

    def __str__(self):
        return self.aut_num.name + " - " + self.router.hostname + " " + self.peer_ip

class router(models.Model):
    routing_id    = models.GenericIPAddressField(unpack_ipv4=True)
    hostname      = models.CharField(max_length=255)
    ibgp          = models.BooleanField()
    network_os    = models.ForeignKey('network_os', on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname

class network_os(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class aut_num(models.Model):
    asn        = models.BigIntegerField(unique=True)
    name       = models.CharField(max_length=255)
    contact    = models.EmailField(blank=True)

    def __str__(self):
        return str(self.asn) + ": " + self.name + " (" + self.contact + ")"
