# file: bgp/tests.py

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
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
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_config_view_with_one_ios_neighbor(self):
        """
        Create a test IOS router, with one ipv4 and one ipv6 neighbors then check config view.
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
        Create a test JunOS router, with one ipv4 and one ipv6 neighbors then check config view.
        """
        test_router      = create_router('junos')
        test_asn         = create_aut_num('65001')
        test_v4_neighbor = create_neighbor(test_router, test_asn, '1.1.1.1')
        test_v6_neighbor = create_neighbor(test_router, test_asn, '2001:db8::1')

        response = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'peer-as 65001;')
        self.assertContains(response, 'neighbor 1.1.1.1;')
        self.assertContains(response, 'neighbor 2001:db8::1;')

    def test_config_view_with_multiple_ios_neighbor(self):
        """
        Create a test IOS router, with 100 ipv4 and ipv6 neighbors then check the config view.
        """
        test_router      = create_router('ios')
        test_asn         = create_aut_num('65001')
        neighbor_count   = 100

        for i in range(1, neighbor_count):
            create_neighbor(test_router, test_asn, '1.1.' + str(i) + '.1')
            create_neighbor(test_router, test_asn, '2001:db8:' +  str(i) + '::1')

        response = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)

        for i in range(1, neighbor_count):
            self.assertContains(response, 'neighbor 1.1.' + str(i) + '.1 remote-as 65001')
            self.assertContains(response, 'neighbor 2001:db8:' +  str(i) + '::1 remote-as 65001')

    def test_config_view_with_multiple_junos_neighbor(self):
        """
        Create a test IOS router, with 100 ipv4 and ipv6 neighbors then check the config view.
        """
        test_router      = create_router('junos')
        test_asn_one     = create_aut_num('65001')
        test_asn_two     = create_aut_num('65002')
        neighbor_count   = 50 # Set this to half desired value, as we'll run two peer-groups.

        asn_one_config   = '        group test-asn {\n'
        asn_one_config  += '            type external;\n'

        asn_two_config   = asn_one_config
        asn_two_config  += '            peer-as 65002; \n'

        asn_one_config  += '            peer-as 65001; \n'

        for i in range(1, neighbor_count):
            create_neighbor(test_router, test_asn_one, '1.1.' + str(i) + '.1')
            asn_one_config += '            neighbor 1.1.' + str(i) + '.1; \n'

            create_neighbor(test_router, test_asn_two, '2.2.' + str(i) + '.1')
            asn_two_config += '            neighbor 2.2.' + str(i) + '.1; \n'

        for i in range(1, neighbor_count):
            create_neighbor(test_router, test_asn_one, '2001:db8:' +  str(i) + '::1')
            asn_one_config += '            neighbor 2001:db8:' +  str(i) + '::1; \n'

            create_neighbor(test_router, test_asn_two, '2001:db8:' +  str(i) + ':2::1')
            asn_two_config += '            neighbor 2001:db8:' +  str(i) + ':2::1; \n'

        asn_one_config += '        }'
        asn_two_config += '        }'

        response = self.client.get(reverse('op_webgui:router_config', kwargs={'router_id': test_router.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, asn_one_config)
        self.assertContains(response, asn_two_config)
