# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ManpowerPlanningFormation(models.Model):
    """
    Detail line of a manpower planning. One line states how many people
    of one job position the department needs, and who already fills the
    position (if anybody). Lines without an employee are vacant.
    """

    _name = "manpower_planning_formation"
    _description = "Manpower Planning - Formation"
    _order = "planning_id, id"

    planning_id = fields.Many2one(
        string="# Manpower Planning",
        comodel_name="manpower_planning",
        required=True,
        ondelete="cascade",
        help="Manpower planning document that owns this formation line.",
    )
    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
        required=True,
        help="Job position this formation line is planned for.",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        help="Employee who already fills this position. Leave empty when "
        "the position is vacant.",
    )
    is_vacant = fields.Boolean(
        string="Vacant",
        compute="_compute_is_vacant",
        compute_sudo=True,
        store=True,
        help="Checked automatically when no employee fills this line.",
    )
    quantity = fields.Integer(
        string="Quantity Needed",
        default=1,
        required=True,
        help="Number of people needed for this job position. It must be "
        "exactly 1 when an employee is selected.",
    )
    quantity_filled = fields.Integer(
        string="Quantity Filled",
        compute="_compute_quantity_filled",
        compute_sudo=True,
        store=True,
        help="Number of people already filling this line: 1 when an "
        "employee is selected, otherwise 0.",
    )
    notes = fields.Text(
        string="Notes",
        help="Free-form remarks about this formation line.",
    )

    @api.depends("employee_id")
    def _compute_is_vacant(self):
        """Flag the line as vacant when no employee is selected."""
        for record in self:
            result = True
            if record.employee_id:
                result = False
            record.is_vacant = result

    @api.depends("employee_id")
    def _compute_quantity_filled(self):
        """Count one filled position per line that has an employee."""
        for record in self:
            result = 0
            if record.employee_id:
                result = 1
            record.quantity_filled = result

    @api.constrains("quantity")
    def _check_quantity(self):
        """Reject lines whose quantity is lower than one.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_quantity_condition():
                error_message = """
Context: Create or update a manpower planning formation line
Database ID: %s
Problem: Quantity needed must be at least 1
Solution: Set the quantity needed to 1 or more
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_quantity_condition(self):
        """Tell whether the quantity needed is at least one.

        Extension point: override to change the minimum quantity.

        :return: True when valid; never raises
        """
        self.ensure_one()
        return self.quantity >= 1

    @api.constrains("quantity", "employee_id")
    def _check_employee_quantity(self):
        """Reject lines with an employee and a quantity other than one.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_employee_quantity_condition():
                error_message = """
Context: Create or update a manpower planning formation line
Database ID: %s
Problem: A line with an employee must have a quantity of exactly 1
Solution: Set the quantity to 1 or remove the employee
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _check_employee_quantity_condition(self):
        """Tell whether a line with an employee has quantity one.

        :return: True when valid; never raises
        """
        self.ensure_one()
        if not self.employee_id:
            return True
        return self.quantity == 1

    def _get_employee_duplicate_criteria(self):
        """Build the domain of other lines using the same employee.

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
        """Reject a second formation line of one employee in a planning.

        :raises ValidationError: when the condition method returns False
        """
        for record in self.sudo():
            if not record._check_employee_unique_condition():
                error_message = """
Context: Create or update a manpower planning formation line
Database ID: %s
Problem: The employee already has a formation line in this planning
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
        if not self.employee_id:
            return True
        criteria = self._get_employee_duplicate_criteria()
        return self.search_count(criteria) == 0
