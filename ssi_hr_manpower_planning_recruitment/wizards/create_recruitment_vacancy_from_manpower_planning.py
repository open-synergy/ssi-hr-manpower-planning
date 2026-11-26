# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CreateRecruitmentVacancyFromManpowerPlanning(models.TransientModel):
    """
    Wizard that requests recruitment vacancies from a running manpower
    planning. It proposes one line per job position that still has vacant
    formation, lets the user complete the quantity, expected join date and
    reason, then creates one draft recruitment vacancy per line.
    """

    _name = "create_recruitment_vacancy_from_manpower_planning"
    _description = "Create Recruitment Vacancy from Manpower Planning"

    planning_id = fields.Many2one(
        string="# Manpower Planning",
        comodel_name="manpower_planning",
        required=True,
        ondelete="cascade",
        help="Manpower planning the vacancies are requested from.",
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
        default=lambda self: fields.Date.context_today(self),
        help="Start date of the created vacancies. Every expected join "
        "date must be on or after it.",
    )
    line_ids = fields.One2many(
        string="Lines",
        comodel_name="create_recruitment_vacancy_from_manpower_planning_line",
        inverse_name="wizard_id",
        help="One line per recruitment vacancy to create.",
    )

    @api.model
    def default_get(self, fields_list):
        """Prefill the planning and one line per job with remaining need.

        The planning comes from the default of the opening button or,
        failing that, from the active record of the context.

        :param fields_list: field names requested by the client
        :return: dict of default values
        """
        res = super().default_get(fields_list)
        context = self.env.context
        planning_id = res.get("planning_id")
        if not planning_id and context.get("active_model") == "manpower_planning":
            planning_id = context.get("active_id")
            if planning_id and "planning_id" in fields_list:
                res["planning_id"] = planning_id
        if planning_id and "line_ids" in fields_list:
            planning = self.env["manpower_planning"].browse(planning_id)
            res["line_ids"] = [
                (0, 0, values) for values in self._prepare_default_line_values(planning)
            ]
        return res

    @api.model
    def _prepare_default_line_values(self, planning):
        """Build the proposed lines for a planning.

        Per job position, the remaining need is the vacant quantity of
        the formation lines minus the quantity already requested by the
        non-cancelled vacancies of the planning. Jobs with nothing left
        are not proposed.

        Extension point: override to add proposed lines or fields.

        :param planning: the ``manpower_planning`` record
        :return: list of dicts of line values, ordered by job position
        """
        planning = planning.sudo()
        remaining = defaultdict(int)
        for formation in planning.formation_ids.filtered("is_vacant"):
            remaining[formation.job_id.id] += formation.quantity
        vacancies = planning.recruitment_vacancy_ids.filtered(
            lambda x: x.state != "cancel"
        )
        for vacancy in vacancies:
            remaining[vacancy.job_id.id] -= vacancy.applicant_number
        return [
            {"job_id": job_id, "quantity": quantity}
            for job_id, quantity in sorted(remaining.items())
            if quantity > 0
        ]

    @api.constrains("date_start")
    def _check_date_start(self):
        """Re-validate the expected join date of every line.

        :raises ValidationError: when a line joins before the new start
            date
        """
        for record in self.sudo():
            record.line_ids._check_expected_join_date()

    def action_confirm(self):
        """Create one draft recruitment vacancy per wizard line.

        :return: an ``ir.actions.act_window`` dict listing the vacancies
        """
        for record in self.sudo():
            result = record._create_recruitment_vacancy()
        return result

    def _check_planning_state_condition(self):
        """Tell whether the planning is open and accepts vacancy requests.

        :return: True when the planning state is ``open``; never raises
        """
        self.ensure_one()
        return self.planning_id.state == "open"

    def _create_recruitment_vacancy(self):
        """Create the draft vacancies and link them to the planning.

        Side effect: creates one ``recruitment_vacancy`` per line.

        :raises UserError: when the planning is not open
        :return: an ``ir.actions.act_window`` dict listing the vacancies
        """
        self.ensure_one()
        if not self._check_planning_state_condition():
            error_message = """
Context: Create recruitment vacancy from manpower planning
Database ID: %s
Problem: Manpower planning is not in the open state
Solution: Open the manpower planning before requesting vacancies
""" % (
                self.planning_id.id,
            )
            raise UserError(_(error_message))
        vacancies = self.env["recruitment_vacancy"]
        for line in self.line_ids:
            vacancies |= vacancies.create(self._prepare_vacancy_values(line))
        return {
            "type": "ir.actions.act_window",
            "name": "Recruitment Vacancies",
            "res_model": "recruitment_vacancy",
            "view_mode": "tree,form",
            "domain": [("id", "in", vacancies.ids)],
        }

    def _prepare_vacancy_values(self, line):
        """Build the values of the vacancy created for one line.

        Extension point: override to fill more fields of the vacancy.

        :param line: the wizard line the vacancy is created for
        :return: dict of ``recruitment_vacancy`` values
        """
        self.ensure_one()
        return {
            "job_id": line.job_id.id,
            "applicant_number": line.quantity,
            "date_start": self.date_start,
            "date_end": line.expected_join_date,
            "expected_join_date": line.expected_join_date,
            "reason": line.reason,
            "manpower_planning_id": self.planning_id.id,
        }
