# -*- coding: utf-8 -*-
# file api/tests.py

from __future__ import unicode_literals

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from address.models import ipv6_address, ipv4_address
from bgp.models import aut_num, neighbor
from netdevice.models import router, network_os, interface, logical_interface
from static.models import ipv6_static, ipv4_static

from netdevice.tests import create_router, create_interface

class APITests(APITestCase):
    def test_create_aut_num(self):
        """
        Create an aut_num object, and check if it exists.
        """
        data = {"asn": '65000', "name": 'My Test ASN', "contact": ''}

        response = self.client.post(
                                    reverse('api:aut_num'),
                                    data,
                                    format='json'
                                   )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(aut_num.objects.count(), 1)
        self.assertEqual(str(aut_num.objects.get().asn), '65000')

    def test_create_aut_num_and_view_detail(self):
        """
        Create an aut_num object, then check the aut_num_detail api view.
        """
        local_aut_num = aut_num.objects.create(asn=65000, name='test asn')
        url           = reverse(
                                'api:aut_num_detail',
                                kwargs={'pk': local_aut_num.pk}
                               )

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(aut_num.objects.count(), 1)
        self.assertEqual(aut_num.objects.get().asn, local_aut_num.asn)

    def test_create_router(self):
        """
        Create an ASN, then create a router and check that it exists.
        """
        local_aut_num = aut_num.objects.create(asn=65000, name='test asn')
        data = {
                "routing_id": '1.1.1.1',
                "hostname": 'test-router',
                "ibgp": 'true',
                "service_ssh": 'true',
                "service_netconf": 'true',
                "network_os": 2,
                "local_aut_num": local_aut_num.pk,
               }

        response = self.client.post(reverse('api:routers'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(router.objects.count(), 1)
        self.assertEqual(router.objects.get().hostname, 'test-router')

    def test_create_router_and_view_detail(self):
        test_router  = create_router('junos')
        url          = reverse(
                               'api:routers_detail',
                               kwargs={'pk': test_router.pk}
                              )

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(router.objects.count(), 1)
        self.assertEqual(router.objects.get().hostname, 'test-router')

    def test_create_network_os(self):
        """
        Create a network_os object, then view it in the api.
        """
        data  = {"name": 'test-os'}
        url   = reverse('api:network_os')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(network_os.objects.count(), 6)
        self.assertEqual(str(network_os.objects.get(name='test-os')), 'test-os')

    def test_create_network_os_and_view_detail(self):
        test_os  = network_os.objects.create(name='test-os')
        url      = reverse('api:network_os_detail',  kwargs={'pk': test_os.pk})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(network_os.objects.count(), 6)
        self.assertEqual(network_os.objects.get(name='test-os'), test_os)

    def test_create_interface(self):
        """
        Create an interface object, then view it in the api.
        """
        test_router  = create_router('junos')
        data         = {
                        "router": test_router.pk,
                        "name": 'ge-0/0/0',
                        "description": 'test-interface',
                       }
        url          = reverse('api:interfaces')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(interface.objects.count(), 1)
        self.assertEqual(str(interface.objects.get().name), 'ge-0/0/0')

    def test_create_interface_and_view_detail(self):
        """
        Create an interface object, then view the detailed api call.
        """
        test_router     = create_router('junos')
        test_interface  = interface.objects.create(router=test_router,
                                                   name='ge-0/0/0',
                                                   description='test-interface')
        url             = reverse(
                                  'api:interfaces_detail',
                                  kwargs={'pk': test_interface.pk}
                                 )

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(interface.objects.count(), 1)
        self.assertEqual(interface.objects.get(name='ge-0/0/0'), test_interface)

    def test_create_logical_interface(self):
        """
        Create a logical_interface object, then view it in the api.
        """
        test_router     = create_router('junos')
        test_interface  = interface.objects.create(router=test_router,
                                                   name='ge-0/0/0',
                                                   description='test-interface')
        data         = {
                        "interface": test_interface.pk,
                        "name": '0',
                        "description": 'test-logical-interface',
                       }
        url          = reverse('api:logical_interfaces')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(logical_interface.objects.count(), 1)
        self.assertEqual(str(logical_interface.objects.get().name), '0')

    def test_create_logical_interface_and_view_detail(self):
        """
        Create a logical_interface object, then view the detailed api call.
        """
        test_router     = create_router('junos')
        test_interface  = create_interface(test_router)
        url             = reverse(
                                  'api:logical_interfaces_detail',
                                  kwargs={'pk': test_interface.pk},
                                 )

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(logical_interface.objects.count(), 1)
        self.assertEqual(
                         logical_interface.objects.get(name='10'),
                         test_interface
                        )

    def test_create_ipv6_address(self):
        """
        Create an ipv6_address object, then view it in the api.
        """
        test_router     = create_router('junos')
        test_interface  = create_interface(test_router)
        data         = {
                        "interface": test_interface.pk,
                        "host": '2001:db8::1',
                        "cidr": '64',
                       }
        url          = reverse('api:ipv6_address')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ipv6_address.objects.count(), 1)
        self.assertEqual(str(ipv6_address.objects.get().host), '2001:db8::1')

    def test_create_ipv6_address_and_view_detail(self):
        """
        Create an ipv6_address object, then view the detailed api call.
        """
        test_router     = create_router('junos')
        test_interface  = create_interface(test_router)
        test_address    = ipv6_address.objects.create(
                                                      interface=test_interface,
                                                      host='2001:db8::1',
                                                      cidr=64,
                                                     )
        url             = reverse(
                                  'api:ipv6_address_detail',
                                  kwargs={'pk': test_address.pk},
                                 )

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ipv6_address.objects.count(), 1)
        self.assertEqual(
                         ipv6_address.objects.get(host='2001:db8::1'),
                         test_address
                        )

    def test_create_ipv4_address(self):
        """
        Create an ipv4_address object, then view it in the api.
        """
        test_router     = create_router('junos')
        test_interface  = create_interface(test_router)
        data            = {
                           "interface": test_interface.pk,
                           "host": '192.0.2.1',
                           "cidr": '24',
                          }
        url             = reverse('api:ipv4_address')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ipv4_address.objects.count(), 1)
        self.assertEqual(str(ipv4_address.objects.get().host), '192.0.2.1')

    def test_create_ipv4_address_and_view_detail(self):
        """
        Create an ipv4_address object, then view the detailed api call.
        """
        test_router     = create_router('junos')
        test_interface  = create_interface(test_router)
        test_address    = ipv4_address.objects.create(
                                                      interface=test_interface,
                                                      host='192.0.2.1',
                                                      cidr=24,
                                                     )
        url             = reverse(
                                  'api:ipv4_address_detail',
                                  kwargs={'pk': test_address.pk},
                                 )

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ipv4_address.objects.count(), 1)
        self.assertEqual(
                         ipv4_address.objects.get(host='192.0.2.1'),
                         test_address
                        )

    def test_create_ipv6_static(self):
        """
        Create an ipv6_static object, with an api call.
        """
        test_router     = create_router('junos')
        data            = {
                           "router": test_router.pk,
                           "network": '2001:db8::',
                           "next_hop": '2001:db8:1::1',
                          }
        url             = reverse('api:ipv6_static')

        response  = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ipv6_static.objects.count(), 1)
        self.assertEqual(str(ipv6_static.objects.get().network), '2001:db8::')

    def test_create_ipv6_static_and_view_detail(self):
        """
        Create an ipv6 static object, then check the detailed api view.
        """
        test_router     = create_router('junos')
        test_route      = ipv6_static.objects.create(
                                                     router=test_router,
                                                     network='2001:db8::',
                                                     next_hop='2001:db8:1::1',
                                                    )
        url             = reverse(
                                  'api:ipv6_static_detail',
                                  kwargs={'pk': test_route.pk},
                                 )

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ipv6_static.objects.count(), 1)
        self.assertEqual(
                         ipv6_static.objects.get(network='2001:db8::'),
                         test_route,
                        )

    def test_create_ipv4_static(self):
        """
        Create an ipv4_static object, with an api call.
        """
        test_router     = create_router('junos')
        data            = {
                           "router": test_router.pk,
                           "network": '192.0.2.0',
                           "next_hop": '192.0.2.1',
                          }
        url             = reverse('api:ipv4_static')

        response  = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ipv4_static.objects.count(), 1)
        self.assertEqual(str(ipv4_static.objects.get().network), '192.0.2.0')

    def test_create_ipv4_static_and_view_detail(self):
        """
        Create an ipv4 static object, then check the detailed api view.
        """
        test_router     = create_router('junos')
        test_route      = ipv4_static.objects.create(
                                                     router=test_router,
                                                     network='192.0.2.0',
                                                     next_hop='192.0.2.1',
                                                    )
        url             = reverse(
                                  'api:ipv4_static_detail',
                                  kwargs={'pk': test_route.pk},
                                 )

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ipv4_static.objects.count(), 1)
        self.assertEqual(
                         ipv4_static.objects.get(network='192.0.2.0'),
                         test_route,
                        )
