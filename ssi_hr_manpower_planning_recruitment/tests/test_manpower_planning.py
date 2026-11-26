# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestManpowerPlanningRecruitment(YamlTransactionCase):
    """Cover the recruitment button of the manpower planning."""

    def test_action_create_recruitment_vacancy_returns_wizard(self):
        """Assert the action dict returned by the vacancy request button.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards the
        return value, so YAML cannot assert it at all). The wizard must
        open as a dialog with the planning as its default.
        """
        department = self.env["hr.department"].create({"name": "MPPR Dept PY"})
        planning = self.env["manpower_planning"].create(
            {
                "department_id": department.id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
            }
        )
        action = planning.action_create_recruitment_vacancy()
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(
            action["res_model"],
            "create_recruitment_vacancy_from_manpower_planning",
        )
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["context"]["default_planning_id"], planning.id)
