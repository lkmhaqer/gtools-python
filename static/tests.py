# file: static/tests.py

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from netdevice.tests import create_router
from static.models import ipv6_static, ipv4_static

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
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_config_view_with_a_single_ios_static_route(self):
        """
        Create an IOS router, interface, and IP addresses, then check the configuration template output.
        """
        test_router      = create_router('ios')
        test_v4_route    = create_v4_static(test_router, '10.0.0.0')
        test_v6_route    = create_v6_static(test_router, '2001:db8:100::')

        response         = self.client.get(reverse('netdevice:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ip route 10.0.0.0 255.255.0.0 172.16.0.1')
        self.assertContains(response, 'ipv6 route 2001:db8:100::/48 2001:db8::1')

    def test_config_view_with_junos_static_route(self):
        """
        Create a JunOS router, interface, and IP addresses, then check the configuration template output.
        """
        test_router      = create_router('junos')
        test_v4_route    = create_v4_static(test_router, '10.0.0.0')
        test_v6_route    = create_v6_static(test_router, '2001:db8:100::')

        response         = self.client.get(reverse('netdevice:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'route 10.0.0.0/16 next-hop 172.16.0.1')
        self.assertContains(response, 'route 2001:db8:100::/48 next-hop 2001:db8::1')

    def test_config_view_with_multiple_ios_static_route(self):
        """
        Create 100 static routes, and ensure they are templated properly.
        """
        test_router       = create_router('ios')
        route_count       = 100

        for i in range(1, route_count):
            create_v4_static(test_router, '10.' + str(i) + '.0.0')
            create_v6_static(test_router, '2001:db8:' + str(i) + '::')

        response         = self.client.get(reverse('netdevice:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

        for i in range(1, route_count):
            self.assertContains(response, 'ip route 10.' + str(i) + '.0.0 255.255.0.0 172.16.0.1')
            self.assertContains(response, 'ipv6 route 2001:db8:' + str(i) + '::/48 2001:db8::1')

    def test_config_view_with_multiple_junos_static_route(self):
        """
        Create 100 static routes, and ensure they are templated properly.
        """
        test_router       = create_router('junos')
        route_count       = 100

        for i in range(1, route_count):
            create_v4_static(test_router, '10.' + str(i) + '.0.0')
            create_v6_static(test_router, '2001:db8:' + str(i) + '::')

        response         = self.client.get(reverse('netdevice:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

        for i in range(1, route_count):
            self.assertContains(response, 'route 10.' + str(i) + '.0.0/16 next-hop 172.16.0.1')
            self.assertContains(response, 'route 2001:db8:' + str(i) + '::/48 next-hop 2001:db8::1')

    def test_create_ipv6_static_route_form_view(self):
        """
        Create a router, then test that the create a static route page view is displayed correctly.
        """
        test_router        = create_router('junos')
        response           = self.client.get(reverse('op_webgui:ipv6_static_create', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

    def test_create_ipv4_static_route_form_view(self):
        """
        Create a router, then test that the create a static route page view is displayed correctly.
        """
        test_router        = create_router('junos')
        response           = self.client.get(reverse('op_webgui:ipv4_static_create', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

    def test_edit_ipv6_static_route_form_view(self):
        """
        Create a router, and static route, then check that the edit form view is displayed correctly.
        """
        test_router        = create_router('junos')
        static_route       = create_v6_static(test_router, '2001:db8:1::')

        response           = self.client.get(reverse('op_webgui:ipv6_static_edit', kwargs={'ipv6_static_id': static_route.id}))

        self.assertEqual(response.status_code, 200)

    def test_edit_ipv4_static_route_form_view(self):
        """
        Create a router, and static route, then check that the edit form view is displayed correctly.
        """
        test_router        = create_router('junos')
        static_route       = create_v4_static(test_router, '192.0.2.0')

        response           = self.client.get(reverse('op_webgui:ipv4_static_edit', kwargs={'ipv4_static_id': static_route.id}))

        self.assertEqual(response.status_code, 200)
