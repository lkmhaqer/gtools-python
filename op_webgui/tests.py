# file: op_webgui/tests.py

from django.test import TestCase
from django.urls import reverse

from .models import aut_num, router, neighbor, network_os

# Create your tests here.

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
        nos = network_os.objects.create(name='test-os')
        router.objects.create(routing_id='1.1.1.1', hostname='test-router', ibgp=True, network_os=nos)
        response = self.client.get(reverse('op_webgui:index'))
        self.assertQuerysetEqual(
            response.context['router_list'], ['<router: test-router>']
        )

    def test_index_view_with_many_routers(self):
        """
        Create a bunch of routers, then verify the view.
        """
        nos = network_os.objects.create(name='many-test-os')
        new_router_list = []
        for i in range(0, 5):
            router.objects.create(
                hostname = 'test-router-' + str(i),
                routing_id = '1.1.1.' + str(i),
                ibgp = True,
                network_os = nos,
            )
            new_router_list.append('<router: test-router-' + str(i) + '>')

        response = self.client.get(reverse('op_webgui:index'))
        self.assertQuerysetEqual(
            response.context['router_list'], new_router_list
        )

