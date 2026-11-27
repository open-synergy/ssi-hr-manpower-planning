# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class ManpowerPlanning(models.Model):
    """
    Represents a manpower planning (MPP) document of one department for one
    period. It lists the planned formation per job position, reviews the
    employee contracts of the department and goes through multiple
    approval before it is opened. The summary tab compares the needed
    manpower with the filled one per job position.
    """

    _name = "manpower_planning"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.date_duration",
    ]
    _description = "Manpower Planning"

    # Multiple approval attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_button = False
    _automatically_insert_open_policy_fields = False
    _automatically_insert_multiple_approval_page = True

    # Attributes related to add element on form view automatically
    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        ondelete="restrict",
        help="Department the manpower planning is made for.",
    )
    formation_ids = fields.One2many(
        string="Formations",
        comodel_name="manpower_planning_formation",
        inverse_name="planning_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=True,
        help="Planned formation per job position of the department.",
    )
    contract_ids = fields.One2many(
        string="Contract Reviews",
        comodel_name="manpower_planning_contract",
        inverse_name="planning_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=True,
        help="Contract reviews of the employees of the department.",
    )
    summary_ids = fields.One2many(
        string="Summaries",
        comodel_name="manpower_planning_summary",
        inverse_name="planning_id",
        readonly=True,
        help="Needed, filled and vacant manpower per job position.",
    )
    quantity_needed = fields.Integer(
        string="Quantity Needed",
        compute="_compute_quantity_needed",
        compute_sudo=True,
        store=True,
        help="Total manpower needed, the sum of all formation lines.",
    )
    quantity_filled = fields.Integer(
        string="Quantity Filled",
        compute="_compute_quantity_filled",
        compute_sudo=True,
        store=True,
        help="Total manpower already filled by an employee.",
    )
    quantity_vacant = fields.Integer(
        string="Quantity Vacant",
        compute="_compute_quantity_vacant",
        compute_sudo=True,
        store=True,
        help="Total manpower still vacant: needed minus filled.",
    )

    contract_continue_percent = fields.Float(
        string="Continued Contracts (%)",
        compute="_compute_contract_continue_percent",
        compute_sudo=True,
        store=False,
        help="Percentage of the contract review lines that are not "
        "ended: lines with a recommendation that does not terminate "
        "the contract, divided by all review lines. Shown as is, "
        "without rounding up.",
    )

    @api.depends("formation_ids", "formation_ids.quantity")
    def _compute_quantity_needed(self):
        """Sum the quantity needed of all formation lines."""
        for record in self:
            result = 0
            for formation in record.formation_ids:
                result += formation.quantity
            record.quantity_needed = result

    @api.depends("formation_ids", "formation_ids.quantity_filled")
    def _compute_quantity_filled(self):
        """Sum the quantity filled of all formation lines."""
        for record in self:
            result = 0
            for formation in record.formation_ids:
                result += formation.quantity_filled
            record.quantity_filled = result

    @api.depends("quantity_needed", "quantity_filled")
    def _compute_quantity_vacant(self):
        """Subtract the filled manpower from the needed manpower."""
        for record in self:
            result = record.quantity_needed - record.quantity_filled
            record.quantity_vacant = result

    @api.depends(
        "contract_ids",
        "contract_ids.recommendation_id",
        "contract_ids.recommendation_id.is_terminate",
    )
    def _compute_contract_continue_percent(self):
        """Compute the share of contract lines that are continued.

        The numerator counts the review lines that have a
        recommendation which does not terminate the contract; the
        denominator counts every review line. A planning without any
        review line gets ``0.0``.
        """
        for record in self:
            result = 0.0
            total = len(record.contract_ids)
            if total:
                continued = len(
                    record.contract_ids.filtered(
                        lambda r: r.recommendation_id
                        and not r.recommendation_id.is_terminate
                    )
                )
                result = continued * 100.0 / total
            record.contract_continue_percent = result

    def action_generate_contract(self):
        """Add contract review lines for the employees on contract.

        Triggered by the **Generate Contract** button of a draft
        planning. Employees that already have a review line are kept
        as they are.

        :return: nothing; the new lines appear on the Contract Reviews
            tab
        """
        for record in self.sudo():
            record._generate_contract()

    def _generate_contract(self):
        """Create one review line per employee on a contract status.

        The lines copy the contract dates of the employee and leave the
        recommendation empty. An employee that already has a line in
        this planning is skipped, so the action can run again safely.
        When no employee matches nothing is created.

        :raises UserError: when the planning is not a draft, or when
            the company has no contract employment status configured
        """
        self.ensure_one()
        if self.state != "draft":
            error_message = """
Document Type: %s
Context: Generate contract review lines
Database ID: %s
Problem: Contract review lines can only be generated while the planning is draft
Solution: Restart the planning to draft first
""" % (
                self._description.lower(),
                self.id,
            )
            raise UserError(_(error_message))
        if not self.company_id.manpower_contract_employment_status_ids:
            error_message = """
Document Type: %s
Context: Generate contract review lines
Database ID: %s
Problem: The company has no contract employment status configured
Solution: Configure contract employment statuses in the Settings first
""" % (
                self._description.lower(),
                self.id,
            )
            raise UserError(_(error_message))
        contract_obj = self.env["manpower_planning_contract"]
        existing = self.contract_ids.mapped("employee_id")
        employees = self.env["hr.employee"].search(
            self._get_contract_employee_criteria()
        )
        for employee in employees - existing:
            contract_obj.create(self._prepare_contract_values(employee))

    def _get_contract_employee_criteria(self):
        """Build the domain of the employees given a review line.

        Extension point: override to add more filters.

        :return: search domain of active employees of the company of
            the planning that have a contract employment status, and
            that belong to the department of the planning when it is set
        """
        self.ensure_one()
        status_ids = self.company_id.manpower_contract_employment_status_ids.ids
        criteria = [
            ("company_id", "=", self.company_id.id),
            ("active", "=", True),
            ("employment_status_id", "in", status_ids),
        ]
        if self.department_id:
            criteria.append(("department_id", "=", self.department_id.id))
        return criteria

    def _prepare_contract_values(self, employee):
        """Build the create values of the review line of an employee.

        Extension point: override to fill more fields of the line.

        :param employee: a single ``hr.employee`` record
        :return: ``manpower_planning_contract`` create values with the
            contract dates copied from the employee
        """
        self.ensure_one()
        return {
            "planning_id": self.id,
            "employee_id": employee.id,
            "date_contract_start": employee.date_contract_start,
            "date_contract_end": employee.date_contract_end,
        }

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super(ManpowerPlanning, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res
