# file: static/tests.py

from django.test import TestCase
from django.urls import reverse

from netdevice.tests import create_router
from .models import ipv6_static, ipv4_static

def create_v4_static(test_router, network):
    v4_route     = ipv4_static.objects.create(router=test_router,
                                              network=network,
                                              cidr=16,
                                              next_hop='172.16.0.1',
                                             )

    return v4_route

def create_v6_static(test_router, network):
    v6_route    = ipv6_static.objects.create(router=test_router,
                                              network=network,
                                              cidr=48,
                                              next_hop='2001:db8::1',
                                             )

    return v6_route



class StaticViewTest(TestCase):
    def test_config_view_with_a_single_ios_static_route(self):
        """
        Create an IOS router, interface, and IP addresses, then check the configuration template output.
        """
        test_router      = create_router('ios')
        test_v4_route    = create_v4_static(test_router, '10.0.0.0')
        test_v6_route    = create_v6_static(test_router, '2001:db8:100::')

        response         = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ip route 10.0.0.0 255.255.0.0 172.16.0.1")
        self.assertContains(response, "ipv6 route 2001:db8:100::/48 2001:db8::1")

    def test_config_view_with_junos_static_route(self):
        """
        Create a JunOS router, interface, and IP addresses, then check the configuration template output.
        """
        test_router      = create_router('junos')
        test_v4_route    = create_v4_static(test_router, '10.0.0.0')
        test_v6_route    = create_v6_static(test_router, '2001:db8:100::')

        response         = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "route 10.0.0.0/16 next-hop 172.16.0.1")
        self.assertContains(response, "route 2001:db8:100::/48 next-hop 2001:db8::1")


