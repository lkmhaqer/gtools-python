# file: op_webgui/tests.py

from django.test import TestCase
from django.urls import reverse

from netdevice.models import router, network_os
from bgp.models import aut_num

class InterfacesViewTests(TestCase):
    def test_router_with_no_intefaces(self):
        """
        Show no results if there are no interfaces.
        """
        nos              = network_os.objects.create(name='test-os')
        local_aut_num    = aut_num.objects.create(asn=65000, name='Test ASN')
        one_router       = router.objects.create(routing_id='1.1.1.1',
                                                 hostname='test-router',
                                                 ibgp=True,
                                                 network_os=nos,
                                                 local_aut_num=local_aut_num
                                                )

        response         = self.client.get(reverse('op_webgui:router_detail',
                                           kwargs={'router_id': one_router.id})
                                          )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['router'].interface_set.all(), [])


