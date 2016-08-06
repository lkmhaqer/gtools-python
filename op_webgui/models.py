from __future__ import unicode_literals

from django.db import models

class neighbor(models.Model):
    router = models.ForeignKey('router', on_delete=models.CASCADE)
    aut_num = models.ForeignKey('aut_num', on_delete=models.CASCADE)
    peer_ip = models.GenericIPAddressField(unpack_ipv4=True)
    soft_inbound = models.BooleanField(default=1)

    def __str__(self):
        return self.aut_num.name + " - " + self.router.hostname + " " + self.peer_ip

class router(models.Model):
    routing_id = models.GenericIPAddressField(unpack_ipv4=True)
    hostname = models.CharField(max_length=255)
    ibgp = models.BooleanField()
    network_os = models.ForeignKey('network_os', on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname

class network_os(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class aut_num(models.Model):
    asn = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    contact = models.EmailField(blank=True)

    def __str__(self):
        return str(self.asn) + " - " + self.name
