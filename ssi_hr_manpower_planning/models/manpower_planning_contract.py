# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ManpowerPlanningContract(models.Model):
    """
    Detail line of a manpower planning that reviews the contract of one
    employee. It copies the contract dates from the employee and holds
    the recommendation given for that contract.
    """

    _name = "manpower_planning_contract"
    _description = "Manpower Planning - Contract Review"
    _order = "planning_id, id"

    planning_id = fields.Many2one(
        string="# Manpower Planning",
        comodel_name="manpower_planning",
        required=True,
        ondelete="cascade",
        help="Manpower planning document that owns this review line.",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        required=True,
        help="Employee whose contract is reviewed.",
    )
    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
        related="employee_id.job_id",
        compute_sudo=True,
        store=True,
        help="Job position of the employee, copied from the employee.",
    )
    date_contract_start = fields.Date(
        string="Contract Start Date",
        help="Start date of the employee contract. Filled from the "
        "employee and can be corrected manually.",
    )
    date_contract_end = fields.Date(
        string="Contract End Date",
        help="End date of the employee contract. Filled from the "
        "employee and can be corrected manually.",
    )
    recommendation_id = fields.Many2one(
        string="Recommendation",
        comodel_name="manpower_contract_recommendation",
        help="Recommendation given for the contract of this employee.",
    )
    notes = fields.Text(
        string="Notes",
        help="Free-form remarks about this contract review.",
    )

    @api.onchange("employee_id")
    def onchange_date_contract_start(self):
        self.date_contract_start = False
        if self.employee_id:
            self.date_contract_start = self.employee_id.date_contract_start

    @api.onchange("employee_id")
    def onchange_date_contract_end(self):
        self.date_contract_end = False
        if self.employee_id:
            self.date_contract_end = self.employee_id.date_contract_end

    def _get_employee_duplicate_criteria(self):
        """Build the domain of other review lines of the same employee.

        Extension point: override to widen or narrow the duplicate scope.

        :return: search domain of the duplicate lines of this line
        """
        self.ensure_one()
        return [
            ("planning_id", "=", self.planning_id.id),
            ("employee_id", "=", self.employee_id.id),
            ("id", "!=", self.id),
        ]

    @api.constrains("employee_id", "planning_id")
    def _check_employee_unique(self):
        """Reject a second review line of one employee in a planning.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_employee_unique_condition():
                error_message = """
Context: Create or update a manpower planning contract review line
Database ID: %s
Problem: The employee already has a contract review line in this planning
Solution: Remove the duplicated line
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_employee_unique_condition(self):
        """Tell whether the employee appears only once in the planning.

        :return: True when valid; never raises
        """
        self.ensure_one()
        criteria = self._get_employee_duplicate_criteria()
        return self.search_count(criteria) == 0
