import os
import unittest
from unittest.mock import MagicMock

from spdx_suite import spdx2ws


class SPDX2WS(unittest.TestCase):
    def setUp(self) -> None:
        spdx2ws.parse_args = MagicMock()
        spdx2ws.parse_args.return_value.ws_user_key = os.environ['WS_USER_KEY']
        spdx2ws.parse_args.return_value.ws_token = os.environ['WS_SCOPE_ORG']
        spdx2ws.parse_args.return_value.ws_url = 'saas'
        spdx2ws.parse_args.return_value.output_dir = os.getcwd()
        spdx2ws.parse_args.return_value.project_token = None
        spdx2ws.parse_args.return_value.product_token = None
        spdx2ws.parse_args.return_value.product_name = None
        spdx2ws.parse_args.return_value.target = None

    def test_generate_update_req_tv(self):
        spdx2ws.parse_args.return_value.spdx_file = 'examples/WhiteSource node-npm SBOM report-SPDX-2.2.tv'
        spdx2ws.main()

        self.assertTrue(True)

    def test_generate_update_req_json(self):
        spdx2ws.parse_args.return_value.spdx_file = 'examples/WhiteSource node-npm SBOM report-SPDX-2.2.json'
        spdx2ws.main()

        self.assertTrue(True)

    def test_generate_update_req_json(self):
        spdx2ws.parse_args.return_value.spdx_file = 'examples/WhiteSource node-npm SBOM report-SPDX-2.2.xml'
        spdx2ws.main()

        self.assertTrue(True)

    def test_generate_update_req_json(self):
        spdx2ws.parse_args.return_value.spdx_file = 'examples/WhiteSource node-npm SBOM report-SPDX-2.2-rdf.xml'
        spdx2ws.main()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
