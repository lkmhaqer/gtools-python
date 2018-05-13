# file: bgp/tests.py

from django.test import TestCase
from django.urls import reverse

from netdevice.tests import create_router, create_interface
from .models import aut_num, neighbor

def create_aut_num(asn):
    test_asn      = aut_num.objects.create(asn=asn,
                                           name='Test ASN',
                                           contact='test@test.com',
                                          )

    return test_asn

def create_neighbor(test_router, aut_num, peer_ip):
    test_neighbor = neighbor.objects.create(router=test_router,
                                            aut_num=aut_num,
                                            peer_ip=peer_ip,
                                            soft_inbound=True,
                                           )

    return test_neighbor

class AddressViewTests(TestCase):
     def test_config_view_with_one_ios_neighbor(self):
         """
         Create a test IOS router, with one ipv4 and one ipv6 address then check config view.
         """
         test_router      = create_router('ios')
         test_asn         = create_aut_num('65001')
         test_v4_neighbor = create_neighbor(test_router, test_asn, '1.1.1.1')
         test_v6_neighbor = create_neighbor(test_router, test_asn, '2001:db8::1')

         response = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

         self.assertEqual(response.status_code, 200)
         self.assertContains(response, 'neighbor 1.1.1.1 remote-as 65001')
         self.assertContains(response, 'neighbor 2001:db8::1 remote-as 65001')

     def test_config_view_with_one_junos_neighbor(self):
         """
         Create a test JunOS router, with one ipv4 and one ipv6 address then check config view.
         """
         test_router     = create_router('junos')
         test_asn         = create_aut_num('65001')
         test_v4_neighbor = create_neighbor(test_router, test_asn, '1.1.1.1')
         test_v6_neighbor = create_neighbor(test_router, test_asn, '2001:db8::1')

         response = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

         self.assertEqual(response.status_code, 200)
         self.assertContains(response, 'peer-as 65001;\n            neighbor 1.1.1.1;')
         self.assertContains(response, 'peer-as 65001;\n            neighbor 2001:db8::1;')
