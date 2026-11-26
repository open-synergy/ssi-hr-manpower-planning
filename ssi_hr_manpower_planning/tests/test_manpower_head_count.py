# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestManpowerHeadCount(YamlTransactionCase):
    """Cover the head count snapshot computation and workflow."""

    def test_manpower_head_count(self):
        """Run the head count snapshot scenarios."""
        self.run_yaml_scenario("test_data_manpower_head_count.yaml")
