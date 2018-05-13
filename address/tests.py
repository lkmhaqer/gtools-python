# file: address/tests.py

from django.test import TestCase
from django.urls import reverse

from netdevice.tests import create_router, create_interface
from .models import ipv6_address, ipv4_address

def create_v4_address(logical_interface):
    v4_address = ipv4_address.objects.create(interface=logical_interface,
                                             host='1.1.1.1',
                                             cidr=24,
                                            )

    return  v4_address

def create_v6_address(logical_interface):
    v6_address = ipv6_address.objects.create(interface=logical_interface,
                                             host='2600::1',
                                             cidr=64,
                                            )

    return v6_address

class AddressViewTests(TestCase):
     def test_config_view_with_one_ios_address(self):
         """
         Create a test IOS router, with one ipv4 and one ipv6 address then check config view.
         """
         test_router     = create_router('ios')
         test_interface  = create_interface(test_router)
         test_v4_address = create_v4_address(test_interface)
         test_v6_address = create_v6_address(test_interface)

         response = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

         self.assertEqual(response.status_code, 200)
         self.assertContains(response, 'ip address 1.1.1.1 255.255.255.0')
         self.assertContains(response, 'ipv6 address 2600::1/64')

     def test_config_view_with_one_junos_address(self):
         """
         Create a test JunOS router, with one ipv4 and one ipv6 address then check config view.
         """
         test_router     = create_router('junos')
         test_interface  = create_interface(test_router)
         test_v4_address = create_v4_address(test_interface)
         test_v6_address = create_v6_address(test_interface)

         response = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

         self.assertEqual(response.status_code, 200)
         self.assertContains(response, 'address 1.1.1.1/24')
         self.assertContains(response, 'address 2600::1/64')
