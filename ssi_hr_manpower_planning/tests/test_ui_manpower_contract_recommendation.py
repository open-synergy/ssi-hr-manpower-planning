# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase, not HttpCase: this is the 14.0 base class.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiManpowerContractRecommendation(HttpSavepointCase):
    """Tour tests for the ``manpower_contract_recommendation`` model."""

    def test_create(self):
        """Run the create tour for contract recommendations.

        IK: docs/manpower_contract_recommendation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_manpower_contract_recommendation_create",
            login="admin",
        )
