# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestManpowerPlanningReport(YamlTransactionCase):
    """Test the helpers of the manpower planning summary report."""

    def setUp(self):
        """Create the department, jobs, employee and planning fixtures.

        ``YamlTransactionCase`` only provides ``self.env`` per test in
        ``setUp``, so the fixtures are built here and recreated for every
        test method.
        """
        super().setUp()
        self.department = self.env["hr.department"].create(
            {"name": "MPP Report Department"}
        )
        self.job_a = self.env["hr.job"].create({"name": "MPP Report Job A"})
        self.job_b = self.env["hr.job"].create({"name": "MPP Report Job B"})
        self.recommendation = self.env["manpower_contract_recommendation"].create(
            {"name": "MPP Report Recommendation", "code": "MPP-RPT-REC"}
        )
        self.employee = self.env["hr.employee"].create(
            {
                "name": "MPP Report Employee",
                "department_id": self.department.id,
                "job_id": self.job_a.id,
            }
        )
        self.planning = self.env["manpower_planning"].create(
            {
                "department_id": self.department.id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
                "formation_ids": [
                    (
                        0,
                        0,
                        {
                            "job_id": self.job_a.id,
                            "employee_id": self.employee.id,
                            "quantity": 1,
                        },
                    ),
                    (0, 0, {"job_id": self.job_b.id, "quantity": 2}),
                    (0, 0, {"job_id": self.job_b.id, "quantity": 1}),
                ],
                "contract_ids": [
                    (
                        0,
                        0,
                        {
                            "employee_id": self.employee.id,
                            "recommendation_id": self.recommendation.id,
                            "notes": "Extend one year",
                        },
                    ),
                ],
            }
        )
        self.report_obj = self.env[
            "report.ssi_hr_manpower_planning.manpower_planning_summary"
        ]

    def test_get_summary_lines_and_total(self):
        """Assert the summary lines and their total of a planning.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare list return value).
        """
        lines = self.report_obj._get_summary_lines(self.planning)
        self.assertEqual(len(lines), 2)
        total = self.report_obj._get_summary_total(lines)
        self.assertEqual(total["quantity_needed"], 4)
        self.assertEqual(total["quantity_filled"], 1)
        self.assertEqual(total["quantity_vacant"], 3)

    def test_get_summary_lines_empty_planning(self):
        """Assert a planning without formation has no summary line.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare list return value).
        """
        empty = self.env["manpower_planning"].create(
            {
                "department_id": self.department.id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
            }
        )
        lines = self.report_obj._get_summary_lines(empty)
        self.assertEqual(lines, [])
        total = self.report_obj._get_summary_total(lines)
        self.assertEqual(total["quantity_needed"], 0)

    def test_get_contract_lines(self):
        """Assert the contract review lines carry their recommendation.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value; L-02: YAML asserts only target a dotted
        ``getattr`` on a record, not a bare list return value).
        """
        lines = self.report_obj._get_contract_lines(self.planning)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["employee"], self.employee)
        self.assertEqual(lines[0]["recommendation"], self.recommendation)
        self.assertEqual(lines[0]["notes"], "Extend one year")

    def test_xlsx_report_generates_file(self):
        """Assert ``create_xlsx_report`` produces a non-empty XLSX file.

        Pure Python — trigger P8 (L-01: ``call`` discards the method
        return value, so the rendered bytes can't be asserted from
        YAML; L-19: the base class is locked to ``TransactionCase``,
        so report rendering can't reach an ``HttpCase``-only helper).
        """
        report_xlsx = self.env[
            "report.ssi_hr_manpower_planning.manpower_planning_summary_xlsx"
        ].with_context(active_model="manpower_planning")
        content, content_type = report_xlsx.create_xlsx_report([self.planning.id], {})
        self.assertEqual(content_type, "xlsx")
        self.assertTrue(content)
