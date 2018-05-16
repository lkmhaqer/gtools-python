# file: op_webgui/tests.py

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from netdevice.models import router, network_os
from netdevice.tests import create_router
from bgp.models import aut_num

#user = User.objects.create_user('test', 'test', 'test')
#user.save()


class WebGUIViewTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_index_view_with_no_routers(self):
        """
        We want to see an error if there are no routers.
        """
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('op_webgui:index'), follow=True)
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

    def test_router_with_no_intefaces(self):
        """
        Show no results if there are no interfaces.
        """
        one_router       = create_router('junos')

        response         = self.client.get(reverse('op_webgui:router_detail',
                                           kwargs={'router_id': one_router.id})
                                          )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['router'].interface_set.all(), [])


