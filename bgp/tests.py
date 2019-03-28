# file: bgp/tests.py

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from netdevice.tests import create_router, create_interface
from bgp.models import aut_num, neighbor

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
        test_user = User.objects.get_or_create(username='testuser')[0]
        self.client.force_login(test_user)

    def test_config_view_with_one_ios_neighbor(self):
        """
        Create a test IOS router, with one ipv4 and one ipv6 neighbors
        then check config view.
        """
        test_router      = create_router('ios')
        test_asn         = create_aut_num('65001')
        test_v4_neighbor = create_neighbor(test_router, test_asn, '1.1.1.1')
        test_v6_neighbor = create_neighbor(
                                           test_router,
                                           test_asn,
                                           '2001:db8::1'
                                          )
        url              = reverse(
                                   'netdevice:router_config',
                                   kwargs={'router_id': test_router.id},
                                  )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'neighbor 1.1.1.1 remote-as 65001')
        self.assertContains(response, 'neighbor 2001:db8::1 remote-as 65001')

    def test_config_view_with_one_junos_neighbor(self):
        """
        Create a test JunOS router, with one ipv4 and one ipv6 neighbors
        then check config view.
        """
        test_router      = create_router('junos')
        test_asn         = create_aut_num('65001')
        test_v4_neighbor = create_neighbor(test_router, test_asn, '1.1.1.1')
        test_v6_neighbor = create_neighbor(test_router, test_asn, '2001:db8::1')
        url              = reverse(
                                   'netdevice:router_config',
                                   kwargs={'router_id': test_router.id},
                                  )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'peer-as 65001;')
        self.assertContains(response, 'neighbor 1.1.1.1;')
        self.assertContains(response, 'neighbor 2001:db8::1;')

    def test_config_view_with_multiple_ios_neighbor(self):
        """
        Create a test IOS router, with 100 ipv4 and ipv6 neighbors
        then check the config view.
        """
        test_router      = create_router('ios')
        test_asn         = create_aut_num('65001')
        neighbor_count   = 100

        for i in range(1, neighbor_count):
            create_neighbor(test_router, test_asn, '1.1.' + str(i) + '.1')
            create_neighbor(
                            test_router,
                            test_asn,
                            '2001:db8:' +  str(i) + '::1'
                           )

        url = reverse(
                      'netdevice:router_config',
                      kwargs={'router_id': test_router.id},
                     )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        for i in range(1, neighbor_count):
            v4_text = 'neighbor 1.1.' + str(i) + '.1 remote-as 65001'
            v6_text = 'neighbor 2001:db8:' +  str(i) + '::1 remote-as 65001'
            self.assertContains(response, v4_text)
            self.assertContains(response, v6_text)

    def test_config_view_with_multiple_junos_neighbor(self):
        """
        Create a test IOS router, with 100 ipv4 and ipv6 neighbors
        then check the config view.
        """
        test_router      = create_router('junos')
        test_asn_one     = create_aut_num('65001')
        test_asn_two     = create_aut_num('65002')
        neighbor_count   = 50

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
            create_neighbor(
                            test_router,
                            test_asn_one,
                            '2001:db8:' +  str(i) + '::1'
                           )
            asn_one_config += '            neighbor 2001:db8:'
            asn_one_config += str(i) + '::1; \n'

            create_neighbor(
                            test_router,
                            test_asn_two,
                            '2001:db8:' +  str(i) + ':2::1'
                           )
            asn_two_config += '            neighbor 2001:db8:'
            asn_two_config += str(i) + ':2::1; \n'

        asn_one_config += '        }'
        asn_two_config += '        }'
        url             = reverse(
                                  'netdevice:router_config',
                                  kwargs={'router_id': test_router.id},
                                 )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, asn_one_config)
        self.assertContains(response, asn_two_config)

    def test_create_neighbor_form_view(self):
        """
        Create a test router, and then test the form view of create display.
        """
        test_router  = create_router('junos')
        url          = reverse(
                               'bgp:neighbor_create',
                               kwargs={'router_id': test_router.id},
                              )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_edit_neighbor_form_view(self):
        """
        Create a test router, and neighbor, then test the form view of neighbor
        edit is displayed correctly.
        """
        test_router     = create_router('junos')
        test_asn_one    = create_aut_num('65001')
        test_neighbor   = create_neighbor(
                                          test_router,
                                          test_asn_one,
                                          '2001:db8:1::1'
                                         )
        url             = reverse(
                                  'bgp:neighbor_edit',
                                  kwargs={'neighbor_id': test_neighbor.id},
                                 )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_aut_num_form_view(self):
        """
        Test the form view of create ASN display.
        """
        response = self.client.get(reverse('bgp:aut_num_create'))

        self.assertEqual(response.status_code, 200)

    def test_edit_aut_num_form_view(self):
        """
        Create an ASN, then test the form view of the edit ASN display.
        """
        test_asn = create_aut_num('65001')
        url      = reverse(
                           'bgp:aut_num_edit',
                           kwargs={'aut_num_id': test_asn.id},
                          )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
