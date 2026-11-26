# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase, not HttpCase: this is the 14.0 base class.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiManpowerPlanningCurriculum(HttpSavepointCase):
    """Tour tests for the ``manpower_planning_curriculum`` model."""

    def test_create(self):
        """Run the create tour for the curriculum master data.

        IK: docs/manpower_planning_curriculum/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_school_manpower_planning_curriculum_create",
            login="admin",
        )
