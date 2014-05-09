# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import httpretty

from novaclient.openstack.common import jsonutils
from novaclient.tests.fixture_data import base


class FloatingFixture(base.Fixture):

    base_url = 'os-floating-ips'

    def setUp(self):
        super(FloatingFixture, self).setUp()

        floating_ips = [{'id': 1, 'fixed_ip': '10.0.0.1', 'ip': '11.0.0.1'},
                        {'id': 2, 'fixed_ip': '10.0.0.2', 'ip': '11.0.0.2'}]

        get_os_floating_ips = {'floating_ips': floating_ips}
        httpretty.register_uri(httpretty.GET, self.url(),
                               body=jsonutils.dumps(get_os_floating_ips),
                               content_type='application/json')

        for ip in floating_ips:
            get_os_floating_ip = {'floating_ip': ip}
            httpretty.register_uri(httpretty.GET, self.url(ip['id']),
                                   body=jsonutils.dumps(get_os_floating_ip),
                                   content_type='application/json')

            httpretty.register_uri(httpretty.DELETE, self.url(ip['id']),
                                   content_type='application/json',
                                   status=204)

        def post_os_floating_ips(request, url, headers):
            ip = floating_ips[0].copy()
            ip['pool'] = request.parsed_body.get('pool')
            ip = jsonutils.dumps({'floating_ip': ip})
            return 200, headers, ip
        httpretty.register_uri(httpretty.POST, self.url(),
                               body=post_os_floating_ips,
                               content_type='application/json')
