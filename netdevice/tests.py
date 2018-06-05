# file: netdevice/tests.py

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from netdevice.models import router, network_os, interface, logical_interface
from bgp.models import aut_num

def create_router(network_os_name):
    nos               = network_os.objects.get(name=network_os_name)
    local_aut_num     = aut_num.objects.create(asn=65000, name='Test ASN')
    test_router       = router.objects.create(routing_id='1.1.1.1',
                                              hostname='test-router',
                                              ibgp=True,
                                              network_os=nos,
                                              local_aut_num=local_aut_num,
                                             )

    return test_router

def create_interface(test_router):
    test_interface          = interface.objects.create(router=test_router,
                                                       name='ge-0/0/0',
                                                       description="A test description.",
                                                       mtu=9000,
                                                       dot1q=True,
                                                      )

    test_logical_interface  = logical_interface.objects.create(interface=test_interface,
                                                               name='10',
                                                               description="A logical test description.",
                                                               mtu=4170,
                                                               vlan=10,
                                                               physical_interface=False,
                                                               ldp=True,
                                                               inet_dhcp_client=False,
                                                               inet6_dhcp_client=False,
                                                              )

    return test_logical_interface

class NetdeviceViewTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_config_view_with_ios_router(self):
        """
        Create an IOS router, interface, and IP addresses, then check the configuration template output.
        """
        test_router      = create_router('ios')
        response         = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

    def test_config_view_with_junos_router(self):
        """
        Create a JunOS router, interface, and IP addresses, then check the configuration template output.
        """
        test_router      = create_router('junos')
        response         = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

    def test_create_interface_form_view(self):
        """
        Create a router, then check the create interface form view is displayed correctly.
        """
        test_router             = create_router('junos')
        response                = self.client.get(reverse('op_webgui:interface_create', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

    def test_edit_interface_form_view(self):
        """
        Create a router, create an interface, then check the edit interface form view is displayed correctly.
        """
        test_router             = create_router('junos')
        test_logical_interface  = create_interface(test_router)

        response                = self.client.get(reverse('op_webgui:interface_edit', kwargs={'interface_id': test_logical_interface.interface.id}))

        self.assertEqual(response.status_code, 200)

    def test_create_logical_interface_form_view(self):
        """
        Create a router, then check the create interface form view is displayed correctly.
        """
        test_router             = create_router('junos')
        test_logical_interface  = create_interface(test_router)

        response                = self.client.get(reverse('op_webgui:logical_interface_create', kwargs={'interface_id': test_logical_interface.interface.id}))

        self.assertEqual(response.status_code, 200)

    def test_edit_logical_interface_form_view(self):
        """
        Create a router, create an interface, then check the edit interface form view is displayed correctly.
        """
        test_router             = create_router('junos')
        test_logical_interface  = create_interface(test_router)

        response                = self.client.get(reverse('op_webgui:logical_interface_edit', kwargs={'logical_interface_id': test_logical_interface.id}))

        self.assertEqual(response.status_code, 200)
