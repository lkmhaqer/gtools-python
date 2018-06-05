# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from netdevice.models import router, network_os
from bgp.models import aut_num, neighbor

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
