# file: address/tests.py

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from netdevice.tests import create_router, create_interface
from .models import ipv6_address, ipv4_address

def create_v4_address(logical_interface, address):
    v4_address = ipv4_address.objects.create(interface=logical_interface,
                                             host=address,
                                             cidr=24,
                                            )

    return  v4_address

def create_v6_address(logical_interface, address):
    v6_address = ipv6_address.objects.create(interface=logical_interface,
                                             host=address,
                                             cidr=64,
                                            )

    return v6_address

class AddressViewTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_config_view_with_one_ios_address(self):
        """
        Create a test IOS router, with one ipv4 and one ipv6 address then check config view.
        """
        test_router     = create_router('ios')
        test_interface  = create_interface(test_router)
        test_v4_address = create_v4_address(test_interface, '1.1.1.1')
        test_v6_address = create_v6_address(test_interface, '2600::1')

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
        test_v4_address = create_v4_address(test_interface, '1.1.1.1')
        test_v6_address = create_v6_address(test_interface, '2600::1')

        response = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'address 1.1.1.1/24')
        self.assertContains(response, 'address 2600::1/64')

    def test_config_view_with_multiple_ios_address(self):
        """
        Create a test IOS router, then add 100 ipv4 and ipv6 addresses, confirm they are in the final template.
        """
        test_router     = create_router('ios')
        test_interface  = create_interface(test_router)
        address_count   = 100

        for i in range(1, address_count):
            create_v4_address(test_interface, '1.1.' + str(i) + '.1')
            create_v6_address(test_interface, '2600:' + str(i) + '::1')

        response = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

        for i in range(1, address_count):
            self.assertContains(response, 'ip address 1.1.' + str(i) + '.1 255.255.255.0')
            self.assertContains(response, 'ipv6 address 2600:' + str(i) + '::1/64')

    def test_config_view_with_multiple_junos_address(self):
        """
        Create a test IOS router, then add 100 ipv4 and ipv6 addresses, confirm they are in the final template.
        """
        test_router     = create_router('junos')
        test_interface  = create_interface(test_router)
        address_count   = 100

        for i in range(1, address_count):
            create_v4_address(test_interface, '1.1.' + str(i) + '.1')
            create_v6_address(test_interface, '2600:' + str(i) + '::1')

        response = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

        for i in range(1, address_count):
            self.assertContains(response, 'address 1.1.' + str(i) + '.1/24')
            self.assertContains(response, 'address 2600:' + str(i) + '::1/64')

    def test_ipv6_address_create_form_view(self):
        """
        Create a test router and interface, then test the form view of ipv6_address_create is displayed correctly.
        """
        test_router    = create_router('junos')
        test_interface = create_interface(test_router)

        response = self.client.get(reverse('op_webgui:ipv6_address_create', kwargs={'logical_interface_id': test_interface.id}))

        self.assertEqual(response.status_code, 200)

    def test_ipv4_address_create_form_view(self):
        """
        Create a test router and interface, then test the form view of ipv4_address_create is displayed correctly.
        """
        test_router    = create_router('junos')
        test_interface = create_interface(test_router)

        response = self.client.get(reverse('op_webgui:ipv4_address_create', kwargs={'logical_interface_id': test_interface.id}))

        self.assertEqual(response.status_code, 200)

    def test_ipv6_address_edit_form_view(self):
        """
        Create a test router, interface and address, then test the form view of ipv6_address_edit is displayed correctly.
        """
        test_router    = create_router('junos')
        test_interface = create_interface(test_router)
        test_address   = create_v6_address(test_interface, '2001:db8:1::1')

        response = self.client.get(reverse('op_webgui:ipv6_address_edit', kwargs={'ipv6_address_id': test_address.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="text" name="host" value="2001:db8:1::1" required id="id_host" />')

    def test_ipv4_address_edit_form_view(self):
        """
        Create a test router, interface and address, then test the form view of ipv4_address_edit is displayed correctly.
        """
        test_router    = create_router('junos')
        test_interface = create_interface(test_router)
        test_address   = create_v4_address(test_interface, '192.0.2.1')

        response = self.client.get(reverse('op_webgui:ipv4_address_edit', kwargs={'ipv4_address_id': test_address.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="text" name="host" value="192.0.2.1" required id="id_host" />')
