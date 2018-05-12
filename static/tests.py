# file: static/tests.py

from django.test import TestCase
from django.urls import reverse

from netdevice.tests import create_router

class StaticViewTest(TestCase):
    def test_config_view_with_ios_static_route(self):
        """
        Create an IOS router, interface, and IP addresses, then check the configuration template output.
        """
        test_router      = create_router('ios')
        response         = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ip route 10.0.0.0 255.255.0.0 172.16.0.1")
        self.assertContains(response, "ipv6 route 2001:db8:100::/48 2001:db8::1")

    def test_config_view_with_junos_static_route(self):
        """
        Create a JunOS router, interface, and IP addresses, then check the configuration template output.
        """
        test_router      = create_router('junos')
        response         = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "route 10.0.0.0/16 next-hop 172.16.0.1")
        self.assertContains(response, "route 2001:db8:100::/48 next-hop 2001:db8::1")


