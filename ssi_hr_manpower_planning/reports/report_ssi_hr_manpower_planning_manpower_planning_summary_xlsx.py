# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models


class ReportSsiHrManpowerPlanningManpowerPlanningSummaryXlsx(models.AbstractModel):
    """
    Renders the Manpower Planning Summary as an ``.xlsx`` workbook. It
    reuses the helpers of the HTML report model and writes one worksheet
    per manpower planning: document header, formation table and contract
    review table.
    """

    _name = "report.ssi_hr_manpower_planning.manpower_planning_summary_xlsx"
    _description = "Manpower Planning Summary XLSX Report"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, plannings):
        """Write one summary worksheet per planning into the workbook.

        Override of the ``report.report_xlsx.abstract`` contract method.

        :param workbook: ``xlsxwriter.Workbook`` to write into
        :param data: unused, present for the abstract report contract
        :param plannings: ``manpower_planning`` recordset to render
        :return: nothing; the output is the side effect on ``workbook``
        """
        report_obj = self.env[
            "report.ssi_hr_manpower_planning.manpower_planning_summary"
        ]
        fmt_title = workbook.add_format({"bold": True, "font_size": 13})
        fmt_info = workbook.add_format({"font_size": 10})
        fmt_header = workbook.add_format(
            {"bold": True, "border": 1, "align": "center", "bg_color": "#C6EFCE"}
        )
        fmt_cell = workbook.add_format({"border": 1})
        fmt_number = workbook.add_format({"border": 1, "num_format": "#,##0"})
        fmt_total = workbook.add_format(
            {"bold": True, "border": 1, "bg_color": "#FFFFCC", "num_format": "#,##0"}
        )
        for planning in plannings:
            sheet_name = (planning.name or _("Manpower Planning"))[:31]
            sheet_name = sheet_name.replace("/", "-")
            sheet = workbook.add_worksheet(sheet_name)
            sheet.set_column(0, 0, 36)
            sheet.set_column(1, 5, 18)
            row = 0
            sheet.write(row, 0, _("MANPOWER PLANNING %s") % planning.name, fmt_title)
            row += 1
            sheet.write(
                row,
                0,
                _("Department: %s") % (planning.department_id.name or ""),
                fmt_info,
            )
            row += 1
            sheet.write(
                row,
                0,
                _("Period: %s - %s")
                % (
                    planning.date_start and planning.date_start.strftime("%d/%m/%Y"),
                    planning.date_end and planning.date_end.strftime("%d/%m/%Y"),
                ),
                fmt_info,
            )
            row += 2

            sheet.write(row, 0, _("Job Position"), fmt_header)
            sheet.write(row, 1, _("Needed"), fmt_header)
            sheet.write(row, 2, _("Filled"), fmt_header)
            sheet.write(row, 3, _("Vacant"), fmt_header)
            row += 1
            summary_lines = report_obj._get_summary_lines(planning)
            for line in summary_lines:
                sheet.write(row, 0, line["job"].name or "", fmt_cell)
                sheet.write_number(row, 1, line["quantity_needed"], fmt_number)
                sheet.write_number(row, 2, line["quantity_filled"], fmt_number)
                sheet.write_number(row, 3, line["quantity_vacant"], fmt_number)
                row += 1
            total = report_obj._get_summary_total(summary_lines)
            sheet.write(row, 0, _("Total"), fmt_total)
            sheet.write_number(row, 1, total["quantity_needed"], fmt_total)
            sheet.write_number(row, 2, total["quantity_filled"], fmt_total)
            sheet.write_number(row, 3, total["quantity_vacant"], fmt_total)
            row += 2

            sheet.write(row, 0, _("Employee"), fmt_header)
            sheet.write(row, 1, _("Job Position"), fmt_header)
            sheet.write(row, 2, _("Contract Start"), fmt_header)
            sheet.write(row, 3, _("Contract End"), fmt_header)
            sheet.write(row, 4, _("Recommendation"), fmt_header)
            sheet.write(row, 5, _("Notes"), fmt_header)
            row += 1
            for line in report_obj._get_contract_lines(planning):
                sheet.write(row, 0, line["employee"].name or "", fmt_cell)
                sheet.write(row, 1, line["job"].name or "", fmt_cell)
                sheet.write(
                    row,
                    2,
                    line["date_contract_start"]
                    and line["date_contract_start"].strftime("%d/%m/%Y")
                    or "",
                    fmt_cell,
                )
                sheet.write(
                    row,
                    3,
                    line["date_contract_end"]
                    and line["date_contract_end"].strftime("%d/%m/%Y")
                    or "",
                    fmt_cell,
                )
                sheet.write(row, 4, line["recommendation"].name or "", fmt_cell)
                sheet.write(row, 5, line["notes"], fmt_cell)
                row += 1
