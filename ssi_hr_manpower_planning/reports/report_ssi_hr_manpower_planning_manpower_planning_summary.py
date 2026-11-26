# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ReportSsiHrManpowerPlanningManpowerPlanningSummary(models.AbstractModel):
    """
    Builds the values consumed by the Manpower Planning Summary QWeb report.
    The helpers return the needed, filled and vacant manpower per job
    position and the contract review lines of a planning, and are shared
    by the HTML/PDF report and the ``.xlsx`` export.
    """

    _name = "report.ssi_hr_manpower_planning.manpower_planning_summary"
    _description = "Manpower Planning Summary Report"

    def _get_summary_lines(self, planning):
        """Return the manpower summary of a planning per job position.

        The rows come from the ``manpower_planning_summary`` SQL view.

        :param planning: a single ``manpower_planning`` record
        :return: list of dicts with the keys ``job``,
            ``quantity_needed``, ``quantity_filled`` and
            ``quantity_vacant``; empty list when the planning has no
            formation line
        """
        self.env["manpower_planning_formation"].flush()
        summaries = self.env["manpower_planning_summary"].search(
            [("planning_id", "=", planning.id)],
            order="job_id",
        )
        result = []
        for summary in summaries:
            result.append(
                {
                    "job": summary.job_id,
                    "quantity_needed": summary.quantity_needed,
                    "quantity_filled": summary.quantity_filled,
                    "quantity_vacant": summary.quantity_vacant,
                }
            )
        return result

    def _get_summary_total(self, lines):
        """Sum the manpower figures of summary lines.

        :param lines: list returned by ``_get_summary_lines``
        :return: dict with the keys ``quantity_needed``,
            ``quantity_filled`` and ``quantity_vacant``
        """
        result = {
            "quantity_needed": 0,
            "quantity_filled": 0,
            "quantity_vacant": 0,
        }
        for line in lines:
            for key in result:
                result[key] += line[key]
        return result

    def _get_contract_lines(self, planning):
        """Return the contract review lines of a planning.

        :param planning: a single ``manpower_planning`` record
        :return: list of dicts with the keys ``employee``, ``job``,
            ``date_contract_start``, ``date_contract_end``,
            ``recommendation`` and ``notes``; empty list when the
            planning has no contract review line
        """
        result = []
        for contract in planning.contract_ids.sorted("id"):
            result.append(
                {
                    "employee": contract.employee_id,
                    "job": contract.job_id,
                    "date_contract_start": contract.date_contract_start,
                    "date_contract_end": contract.date_contract_end,
                    "recommendation": contract.recommendation_id,
                    "notes": contract.notes or "",
                }
            )
        return result

    @api.model
    def _get_report_values(self, docids, data=None):
        """Build the rendering context for the QWeb report engine.

        :param docids: ids of the ``manpower_planning`` records to print
        :param data: unused, present for the report engine signature
        :return: dict with ``doc_ids``, ``doc_model`` and ``docs``;
            each doc holds the planning, its summary lines, the summary
            total and its contract review lines
        """
        plannings = self.env["manpower_planning"].browse(docids)
        docs = []
        for planning in plannings:
            summary_lines = self._get_summary_lines(planning)
            docs.append(
                {
                    "planning": planning,
                    "summary_lines": summary_lines,
                    "summary_total": self._get_summary_total(summary_lines),
                    "contract_lines": self._get_contract_lines(planning),
                }
            )
        return {
            "doc_ids": docids,
            "doc_model": "manpower_planning",
            "docs": docs,
        }
