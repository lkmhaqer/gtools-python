# file: netdevice/tests.py

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from netdevice.models import router, network_os, interface, logical_interface, vrf
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

    def test_vrf_list_view_with_one_vrf(self):
        """
        Create one VRF, then check the vrf_list view and template.
        """
        test_vrf  = vrf.objects.create(name='Test VRF', target='target:65000:65000')
        response  = self.client.get(reverse('netdevice:vrf_list'))

        self.assertEqual(response.status_code, 200)

    def test_vrf_list_view_with_100_vrf(self):
        """
        Create 100 VRF, then check the vrf_list view.
        """
        test_vrfs = []
        for i in range(00, 99):
            target_str = 'target:650' + str(i) + ':65000'
            test_vrfs.append(vrf.objects.create(name='Test VRF #' + str(i), target=target_str))
        response  = self.client.get(reverse('netdevice:vrf_list'))

        self.assertEqual(response.status_code, 200)

    def test_vrf_detail_view(self):
        """
        Create one VRF, then check the detail view.
        """
        test_vrf  = vrf.objects.create(name='Test VRF', target='target:65000:65000')
        response  = self.client.get(reverse('netdevice:vrf_detail', kwargs={'vrf_id': test_vrf.id}))

        self.assertEqual(response.status_code, 200)

    def test_vrf_edit_view(self):
        """
        Create one VRF, then check the edit view.
        """
        test_vrf  = vrf.objects.create(name='Test VRF', target='target:65000:65000')
        response  = self.client.get(reverse('netdevice:vrf_edit', kwargs={'vrf_id': test_vrf.id}))

        self.assertEqual(response.status_code, 200)

    def test_config_view_with_ios_router(self):
        """
        Create an IOS router, interface, and IP addresses, then check the configuration template output.
        """
        test_router      = create_router('ios')
        response         = self.client.get(reverse('netdevice:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

    def test_config_view_with_junos_router(self):
        """
        Create a JunOS router, interface, and IP addresses, then check the configuration template output.
        """
        test_router      = create_router('junos')
        response         = self.client.get(reverse('netdevice:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

    def test_create_interface_form_view(self):
        """
        Create a router, then check the create interface form view is displayed correctly.
        """
        test_router             = create_router('junos')
        response                = self.client.get(reverse('netdevice:interface_create', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

    def test_edit_interface_form_view(self):
        """
        Create a router, create an interface, then check the edit interface form view is displayed correctly.
        """
        test_router             = create_router('junos')
        test_logical_interface  = create_interface(test_router)

        response                = self.client.get(reverse('netdevice:interface_edit', kwargs={'interface_id': test_logical_interface.interface.id}))

        self.assertEqual(response.status_code, 200)

    def test_create_logical_interface_form_view(self):
        """
        Create a router, then check the create interface form view is displayed correctly.
        """
        test_router             = create_router('junos')
        test_logical_interface  = create_interface(test_router)

        response                = self.client.get(reverse('netdevice:logical_interface_create', kwargs={'interface_id': test_logical_interface.interface.id}))

        self.assertEqual(response.status_code, 200)

    def test_edit_logical_interface_form_view(self):
        """
        Create a router, create an interface, then check the edit interface form view is displayed correctly.
        """
        test_router             = create_router('junos')
        test_logical_interface  = create_interface(test_router)

        response                = self.client.get(reverse('netdevice:logical_interface_edit', kwargs={'logical_interface_id': test_logical_interface.id}))

        self.assertEqual(response.status_code, 200)
