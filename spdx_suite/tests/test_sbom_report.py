import os
import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from spdx_suite import sbom_report


class SbomReportTest(TestCase):
    def setUp(self) -> None:
        sbom_report.parse_args = MagicMock()
        sbom_report.parse_args.return_value.ws_user_key = os.environ['WS_USER_KEY']
        sbom_report.parse_args.return_value.ws_token = os.environ['WS_SCOPE_ORG']
        sbom_report.parse_args.return_value.scope_token = os.environ['WS_SCOPE']
        sbom_report.parse_args.return_value.ws_url = 'saas'
        sbom_report.parse_args.return_value.extra_file = os.path.join(os.getcwd(), 'spdx-suite/sbom_extra.json')
        sbom_report.parse_args.return_value.out_dir = '.'

    def test_full_tv_report(self):
        sbom_report.parse_args.return_value.type = 'tv'
        file_content = get_file(sbom_report.main())

        self.assertIsNotNone(file_content)

    def test_full_tv_report(self):
        sbom_report.parse_args.return_value.type = 'json'
        file_content = get_file(sbom_report.main())

        self.assertIsNotNone(file_content)

    def test_full_tv_report(self):
        sbom_report.parse_args.return_value.type = 'xml'
        file_content = get_file(sbom_report.main())

        self.assertIsNotNone(file_content)

    def test_full_tv_report(self):
        sbom_report.parse_args.return_value.type = 'rdf'
        file_content = get_file(sbom_report.main())

        self.assertIsNotNone(file_content)


def get_file(file_path):
    with open(file_path, 'r') as fp:
        return fp.read()


if __name__ == '__main__':
    unittest.main()
