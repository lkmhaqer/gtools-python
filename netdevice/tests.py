# file: netdevices/tests.py

from django.test import TestCase
from django.urls import reverse

from .models import router, network_os, interface, logical_interface
from bgp.models import aut_num

def create_router(network_os_name):
    nos               = network_os.objects.create(name=network_os_name)
    local_aut_num     = aut_num.objects.create(asn=65000, name='test asn')
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

class RouterViewTests(TestCase):
    def test_index_view_with_no_routers(self):
        """
        We want to see an error if there are no routers.
        """
        response = self.client.get(reverse('op_webgui:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No routers")
        self.assertQuerysetEqual(response.context['router_list'], [])

    def test_index_view_with_routers(self):
        """
        Create a router, then check that the view reflects this.
        """
        test_router      = create_router('ios')
        response         = self.client.get(reverse('op_webgui:index'))

        self.assertQuerysetEqual(
            response.context['router_list'], ['<router: test-router>']
        )

    def test_index_view_with_many_routers(self):
        """
        Create a bunch of routers, then verify the view.
        """
        nos              = network_os.objects.create(name='many-test-os')
        local_aut_num    = aut_num.objects.create(asn=65000, name='test asn')
        new_router_list  = []

        for i in range(0, 5):
            router.objects.create(
                hostname   = 'test-router-' + str(i),
                routing_id = '1.1.1.' + str(i),
                ibgp       = True,
                network_os = nos,
                local_aut_num=local_aut_num,
            )
            new_router_list.append('<router: test-router-' + str(i) + '>')

        response = self.client.get(reverse('op_webgui:index'))

        self.assertQuerysetEqual(
            response.context['router_list'], new_router_list
        )

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
