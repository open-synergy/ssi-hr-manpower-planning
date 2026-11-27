# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models


class ReportSsiHrManpowerPlanningManpowerPlanningSummaryXlsx(models.AbstractModel):
    """
    Renders the Manpower Planning Summary as an ``.xlsx`` workbook. It
    reuses the helpers of the HTML report model and writes one worksheet
    per manpower planning. A worksheet is built from sections: document
    header, formation table, category recap and contract review table.
    Other modules add or reorder sections by extending
    :meth:`_get_xlsx_sections`.
    """

    _name = "report.ssi_hr_manpower_planning.manpower_planning_summary_xlsx"
    _description = "Manpower Planning Summary XLSX Report"
    _inherit = "report.report_xlsx.abstract"

    @api.model
    def _get_xlsx_sections(self):
        """Return the worksheet sections in the order they are written.

        Every name must be a method with the signature
        ``(self, sheet, row, planning, formats)`` that writes its part
        starting at ``row`` and returns the next free row. Other
        modules add a section by extending the returned list through
        ``super()``.

        :return: list of method names, one per worksheet section
        :rtype: list
        """
        return [
            "_write_xlsx_header",
            "_write_xlsx_summary",
            "_write_xlsx_category_recap",
            "_write_xlsx_contract",
        ]

    @api.model
    def _get_xlsx_formats(self, workbook):
        """Build the cell formats shared by all sections, once.

        :param workbook: ``xlsxwriter.Workbook`` the formats belong to
        :return: dict of ``xlsxwriter`` formats keyed ``title``,
            ``info``, ``header``, ``cell``, ``number``, ``percent``,
            ``total`` and ``total_percent``
        :rtype: dict
        """
        return {
            "title": workbook.add_format({"bold": True, "font_size": 13}),
            "info": workbook.add_format({"font_size": 10}),
            "header": workbook.add_format(
                {
                    "bold": True,
                    "border": 1,
                    "align": "center",
                    "bg_color": "#C6EFCE",
                }
            ),
            "cell": workbook.add_format({"border": 1}),
            "number": workbook.add_format({"border": 1, "num_format": "#,##0"}),
            "percent": workbook.add_format({"border": 1, "num_format": "0.00"}),
            "total": workbook.add_format(
                {
                    "bold": True,
                    "border": 1,
                    "bg_color": "#FFFFCC",
                    "num_format": "#,##0",
                }
            ),
            "total_percent": workbook.add_format(
                {
                    "bold": True,
                    "border": 1,
                    "bg_color": "#FFFFCC",
                    "num_format": "0.00",
                }
            ),
        }

    def generate_xlsx_report(self, workbook, data, plannings):
        """Write one summary worksheet per planning into the workbook.

        Override of the ``report.report_xlsx.abstract`` contract method.
        Each worksheet is filled by calling the section methods named by
        :meth:`_get_xlsx_sections`, passing the next free row along.

        :param workbook: ``xlsxwriter.Workbook`` to write into
        :param data: unused, present for the abstract report contract
        :param plannings: ``manpower_planning`` recordset to render
        :return: nothing; the output is the side effect on ``workbook``
        """
        formats = self._get_xlsx_formats(workbook)
        for planning in plannings:
            sheet_name = (planning.name or _("Manpower Planning"))[:31]
            sheet_name = sheet_name.replace("/", "-")
            sheet = workbook.add_worksheet(sheet_name)
            sheet.set_column(0, 0, 36)
            sheet.set_column(1, 6, 18)
            row = 0
            for section in self._get_xlsx_sections():
                row = getattr(self, section)(sheet, row, planning, formats)

    def _write_xlsx_header(self, sheet, row, planning, formats):
        """Write the document header: title, department and period.

        :param sheet: worksheet of the planning
        :param row: first row to write
        :param planning: a single ``manpower_planning`` record
        :param formats: cell formats from :meth:`_get_xlsx_formats`
        :return: the next free row
        :rtype: int
        """
        sheet.write(row, 0, _("MANPOWER PLANNING %s") % planning.name, formats["title"])
        row += 1
        sheet.write(
            row,
            0,
            _("Department: %s") % (planning.department_id.name or ""),
            formats["info"],
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
            formats["info"],
        )
        return row + 2

    def _write_xlsx_summary(self, sheet, row, planning, formats):
        """Write the manpower summary table per job position.

        :param sheet: worksheet of the planning
        :param row: first row to write
        :param planning: a single ``manpower_planning`` record
        :param formats: cell formats from :meth:`_get_xlsx_formats`
        :return: the next free row
        :rtype: int
        """
        report_obj = self.env[
            "report.ssi_hr_manpower_planning.manpower_planning_summary"
        ]
        headers = [
            _("Job Position"),
            _("Needed"),
            _("Filled"),
            _("Vacant"),
            _("Filled (%)"),
            _("Vacant (%)"),
            _("Category"),
        ]
        for column, header in enumerate(headers):
            sheet.write(row, column, header, formats["header"])
        row += 1
        summary_lines = report_obj._get_summary_lines(planning)
        for line in summary_lines:
            sheet.write(row, 0, line["job"].name or "", formats["cell"])
            sheet.write_number(row, 1, line["quantity_needed"], formats["number"])
            sheet.write_number(row, 2, line["quantity_filled"], formats["number"])
            sheet.write_number(row, 3, line["quantity_vacant"], formats["number"])
            sheet.write_number(row, 4, line["percent_filled"], formats["percent"])
            sheet.write_number(row, 5, line["percent_vacant"], formats["percent"])
            sheet.write(row, 6, line["category"], formats["cell"])
            row += 1
        total = report_obj._get_summary_total(summary_lines)
        sheet.write(row, 0, _("Total"), formats["total"])
        sheet.write_number(row, 1, total["quantity_needed"], formats["total"])
        sheet.write_number(row, 2, total["quantity_filled"], formats["total"])
        sheet.write_number(row, 3, total["quantity_vacant"], formats["total"])
        sheet.write_number(
            row,
            4,
            report_obj._get_percent(total["quantity_filled"], total["quantity_needed"]),
            formats["total_percent"],
        )
        sheet.write_number(
            row,
            5,
            report_obj._get_percent(total["quantity_vacant"], total["quantity_needed"]),
            formats["total_percent"],
        )
        return row + 2

    def _write_xlsx_category_recap(self, sheet, row, planning, formats):
        """Write the manpower recap table per category.

        :param sheet: worksheet of the planning
        :param row: first row to write
        :param planning: a single ``manpower_planning`` record
        :param formats: cell formats from :meth:`_get_xlsx_formats`
        :return: the next free row
        :rtype: int
        """
        report_obj = self.env[
            "report.ssi_hr_manpower_planning.manpower_planning_summary"
        ]
        headers = [
            _("Category"),
            _("Needed"),
            _("Filled"),
            _("Vacant"),
            _("Filled (%)"),
            _("Vacant (%)"),
        ]
        for column, header in enumerate(headers):
            sheet.write(row, column, header, formats["header"])
        row += 1
        for line in report_obj._get_category_recap(planning):
            sheet.write(row, 0, line["category"], formats["cell"])
            sheet.write_number(row, 1, line["quantity_needed"], formats["number"])
            sheet.write_number(row, 2, line["quantity_filled"], formats["number"])
            sheet.write_number(row, 3, line["quantity_vacant"], formats["number"])
            sheet.write_number(row, 4, line["percent_filled"], formats["percent"])
            sheet.write_number(row, 5, line["percent_vacant"], formats["percent"])
            row += 1
        return row + 1

    def _write_xlsx_contract(self, sheet, row, planning, formats):
        """Write the contract review table and its continued percentage.

        :param sheet: worksheet of the planning
        :param row: first row to write
        :param planning: a single ``manpower_planning`` record
        :param formats: cell formats from :meth:`_get_xlsx_formats`
        :return: the next free row
        :rtype: int
        """
        report_obj = self.env[
            "report.ssi_hr_manpower_planning.manpower_planning_summary"
        ]
        headers = [
            _("Employee"),
            _("Job Position"),
            _("Contract Start"),
            _("Contract End"),
            _("Recommendation"),
            _("Notes"),
        ]
        for column, header in enumerate(headers):
            sheet.write(row, column, header, formats["header"])
        row += 1
        for line in report_obj._get_contract_lines(planning):
            sheet.write(row, 0, line["employee"].name or "", formats["cell"])
            sheet.write(row, 1, line["job"].name or "", formats["cell"])
            sheet.write(
                row,
                2,
                line["date_contract_start"]
                and line["date_contract_start"].strftime("%d/%m/%Y")
                or "",
                formats["cell"],
            )
            sheet.write(
                row,
                3,
                line["date_contract_end"]
                and line["date_contract_end"].strftime("%d/%m/%Y")
                or "",
                formats["cell"],
            )
            sheet.write(row, 4, line["recommendation"].name or "", formats["cell"])
            sheet.write(row, 5, line["notes"], formats["cell"])
            row += 1
        sheet.write(row, 0, _("Continued Contracts (%)"), formats["total"])
        sheet.write_number(
            row, 1, planning.contract_continue_percent, formats["total_percent"]
        )
        return row + 1
