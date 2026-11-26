# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CreateRecruitmentVacancyFromManpowerPlanningLine(models.TransientModel):
    """
    Line of the vacancy request wizard. One line becomes one recruitment
    vacancy: the job position, the number of people to recruit, the date
    the new employees are expected to join, and the reason.
    """

    _name = "create_recruitment_vacancy_from_manpower_planning_line"
    _description = "Create Recruitment Vacancy from Manpower Planning - Line"
    _order = "wizard_id, id"

    wizard_id = fields.Many2one(
        string="# Wizard",
        comodel_name="create_recruitment_vacancy_from_manpower_planning",
        required=True,
        ondelete="cascade",
        help="Vacancy request wizard that owns this line.",
    )
    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
        required=True,
        help="Job position the vacancy is requested for.",
    )
    quantity = fields.Integer(
        string="Quantity",
        default=1,
        required=True,
        help="Number of new employees to recruit. It must be at least 1.",
    )
    expected_join_date = fields.Date(
        string="Expected Join Date",
        required=True,
        help="Date on which the new employees are expected to join. It "
        "must be on or after the start date of the wizard.",
    )
    reason = fields.Text(
        string="Reason",
        help="Reason why this vacancy is needed.",
    )

    @api.constrains("quantity")
    def _check_quantity(self):
        """Reject lines whose quantity is lower than one.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_quantity_condition():
                error_message = """
Context: Create or update a vacancy request line
Database ID: %s
Problem: Quantity must be at least 1
Solution: Set the quantity to 1 or more
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_quantity_condition(self):
        """Tell whether the quantity is at least one.

        :return: True when valid; never raises
        """
        self.ensure_one()
        return self.quantity >= 1

    @api.constrains("expected_join_date", "wizard_id")
    def _check_expected_join_date(self):
        """Reject lines that join before the start date of the wizard.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_expected_join_date_condition():
                error_message = """
Context: Create or update a vacancy request line
Database ID: %s
Problem: Expected join date is earlier than the start date
Solution: Set the expected join date on or after the start date
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_expected_join_date_condition(self):
        """Tell whether the expected join date is not before the start date.

        :return: True when valid; never raises
        """
        self.ensure_one()
        date_start = self.wizard_id.date_start
        if not self.expected_join_date or not date_start:
            return True
        return self.expected_join_date >= date_start
