# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


# Extends the manpower planning of ``ssi_hr_manpower_planning`` with the
# recruitment vacancies requested from it, the smart button that counts
# them and the header button that opens the request wizard.
class ManpowerPlanning(models.Model):
    _name = "manpower_planning"
    _inherit = ["manpower_planning"]

    recruitment_vacancy_ids = fields.One2many(
        string="Recruitment Vacancies",
        comodel_name="recruitment_vacancy",
        inverse_name="manpower_planning_id",
        readonly=True,
        help="Recruitment vacancies requested from this manpower planning.",
    )
    recruitment_vacancy_count = fields.Integer(
        string="Recruitment Vacancy Count",
        compute="_compute_recruitment_vacancy_count",
        compute_sudo=True,
        help="Number of recruitment vacancies requested from this planning.",
    )

    @api.depends("recruitment_vacancy_ids")
    def _compute_recruitment_vacancy_count(self):
        """Count the recruitment vacancies requested from the planning."""
        for record in self:
            result = len(record.recruitment_vacancy_ids)
            record.recruitment_vacancy_count = result

    def action_create_recruitment_vacancy(self):
        """Open the wizard that requests vacancies for the vacant formation.

        :return: an ``ir.actions.act_window`` dict opening the wizard
        """
        for record in self.sudo():
            result = record._create_recruitment_vacancy()
        return result

    def _create_recruitment_vacancy(self):
        """Build the action that opens the vacancy request wizard.

        The wizard proposes one line per job position that still has
        vacant formation, so this method creates nothing itself.

        :return: an ``ir.actions.act_window`` dict opening the wizard
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Create Recruitment Vacancy",
            "res_model": "create_recruitment_vacancy_from_manpower_planning",
            "view_mode": "form",
            "target": "new",
            "context": {"default_planning_id": self.id},
        }
