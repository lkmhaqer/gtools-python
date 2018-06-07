# -*- coding: utf-8 -*-
# file api/tests.py

from __future__ import unicode_literals

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from netdevice.models import router, network_os, interface, logical_interface
from bgp.models import aut_num, neighbor

from netdevice.tests import create_router

class APITests(APITestCase):
    def test_create_aut_num(self):
        """
        Create an aut_num object, and check if it exists.
        """
        data = {"asn": '65000', "name": 'My Test ASN', "contact": ''}

        response = self.client.post(reverse('api:aut_num'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(aut_num.objects.count(), 1)
        self.assertEqual(str(aut_num.objects.get().asn), '65000')

    def test_create_aut_num_and_view_detail(self):
        """
        Create an aut_num object, then check the aut_num_detail api view.
        """
        local_aut_num = aut_num.objects.create(asn=65000, name='test asn')
        url           = reverse('api:aut_num_detail', kwargs={'pk': local_aut_num.pk})

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
        url          = reverse('api:routers_detail', kwargs={'pk': test_router.pk})

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
        Create a network_os object, then view it in the api.
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
        Create a network_os object, then view it in the api.
        """
        test_router  = create_router('junos')
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
        test_router     = create_router('junos')
        test_interface  = interface.objects.create(router=test_router,
                                                   name='ge-0/0/0',
                                                   description='test-interface')
        test_logical_interface = logical_interface.objects.create(
                                                   interface=test_interface,
                                                   name='0',
                                                   description='test-description',
                                                   )
        url             = reverse(
                                  'api:logical_interfaces_detail',
                                  kwargs={'pk': test_logical_interface.pk}
                                 )

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(logical_interface.objects.count(), 1)
        self.assertEqual(logical_interface.objects.get(name='0'), test_logical_interface)
