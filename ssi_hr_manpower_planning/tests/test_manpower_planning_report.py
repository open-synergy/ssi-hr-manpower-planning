# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest import mock

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

    def test_summary_lines_carry_percentages(self):
        """Assert a summary line holds unrounded filled/vacant percent.

        Pure Python — trigger P2 (L-04: the YAML ``equals`` assert is a
        bit-exact ``!=``, so a repeating fraction such as 100 / 3
        needs ``assertAlmostEqual``).
        """
        planning = self.env["manpower_planning"].create(
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
                    (0, 0, {"job_id": self.job_a.id, "quantity": 2}),
                ],
            }
        )
        lines = self.report_obj._get_summary_lines(planning)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["category"], "Formation")
        self.assertAlmostEqual(lines[0]["percent_filled"], 100.0 / 3, places=6)
        self.assertAlmostEqual(lines[0]["percent_vacant"], 200.0 / 3, places=6)

    def test_get_category_recap(self):
        """Assert the category recap sums the rows then derives percent.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value) and P2 (L-04: float equality is bit-exact in
        YAML, so the fractions use ``assertAlmostEqual``).
        """
        recap = self.report_obj._get_category_recap(self.planning)
        self.assertEqual(len(recap), 1)
        self.assertEqual(recap[0]["category"], "Formation")
        self.assertEqual(recap[0]["quantity_needed"], 4)
        self.assertEqual(recap[0]["quantity_filled"], 1)
        self.assertEqual(recap[0]["quantity_vacant"], 3)
        self.assertAlmostEqual(recap[0]["percent_filled"], 25.0, places=6)
        self.assertAlmostEqual(recap[0]["percent_vacant"], 75.0, places=6)

    def test_get_category_recap_empty_planning(self):
        """Assert a planning without formation has an empty recap.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value, so the returned list can't be asserted from
        YAML).
        """
        empty = self.env["manpower_planning"].create(
            {
                "department_id": self.department.id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
            }
        )
        self.assertEqual(self.report_obj._get_category_recap(empty), [])
        values = self.report_obj._get_report_values([empty.id])
        self.assertEqual(values["docs"][0]["category_recap"], [])
        self.assertEqual(values["docs"][0]["contract_continue_percent"], 0.0)

    def test_get_report_values_recap_and_contract_percent(self):
        """Assert the report values carry the recap and contract percent.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value) and P2 (L-04: the 2 / 3 fraction needs
        ``assertAlmostEqual``).
        """
        extend = self.env["manpower_contract_recommendation"].create(
            {"name": "MPP Report Extend", "code": "MPP-RPT-EXT"}
        )
        terminate = self.env["manpower_contract_recommendation"].create(
            {
                "name": "MPP Report Terminate",
                "code": "MPP-RPT-TRM",
                "is_terminate": True,
            }
        )
        planning = self.env["manpower_planning"].create(
            {
                "department_id": self.department.id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
            }
        )
        recommendations = [extend, extend, terminate]
        for index, recommendation in enumerate(recommendations):
            employee = self.env["hr.employee"].create(
                {
                    "name": "MPP Report Contract Employee %s" % index,
                    "department_id": self.department.id,
                }
            )
            self.env["manpower_planning_contract"].create(
                {
                    "planning_id": planning.id,
                    "employee_id": employee.id,
                    "recommendation_id": recommendation.id,
                }
            )
        self.assertAlmostEqual(planning.contract_continue_percent, 200.0 / 3, places=6)
        values = self.report_obj._get_report_values([planning.id])
        self.assertAlmostEqual(
            values["docs"][0]["contract_continue_percent"], 200.0 / 3, places=6
        )
        self.assertIn("category_recap", values["docs"][0])

    def test_xlsx_sections_default_order(self):
        """Assert the XLSX report lists its four default sections.

        Pure Python — trigger P1 (L-01: ``call`` discards the method
        return value, so the returned list of names can't be asserted
        from YAML).
        """
        report_xlsx = self.env[
            "report.ssi_hr_manpower_planning.manpower_planning_summary_xlsx"
        ]
        self.assertEqual(
            report_xlsx._get_xlsx_sections(),
            [
                "_write_xlsx_header",
                "_write_xlsx_summary",
                "_write_xlsx_category_recap",
                "_write_xlsx_contract",
            ],
        )

    def test_xlsx_sections_can_be_extended(self):
        """Assert a section added to the list is written by the report.

        Pure Python — trigger P6 (L-15: YAML has no mock/patch to
        replace the extension point on the model class) and P1 (L-01:
        ``call`` discards the rendered bytes).
        """
        report_xlsx = self.env[
            "report.ssi_hr_manpower_planning.manpower_planning_summary_xlsx"
        ].with_context(active_model="manpower_planning")
        model_class = type(report_xlsx)
        default_sections = report_xlsx._get_xlsx_sections()
        calls = []

        def extra_section(this, sheet, row, planning, formats):
            """Record the call and return the next free row."""
            calls.append((row, planning.id))
            sheet.write(row, 0, "extra section")
            return row + 1

        with mock.patch.object(
            model_class,
            "_get_xlsx_sections",
            return_value=default_sections + ["_write_xlsx_extra"],
        ), mock.patch.object(
            model_class, "_write_xlsx_extra", extra_section, create=True
        ):
            content, content_type = report_xlsx.create_xlsx_report(
                [self.planning.id], {}
            )
        self.assertEqual(content_type, "xlsx")
        self.assertTrue(content)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1], self.planning.id)
