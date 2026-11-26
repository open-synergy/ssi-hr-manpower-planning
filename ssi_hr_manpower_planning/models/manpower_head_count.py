# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class ManpowerHeadCount(models.Model):
    """
    Represents a head count snapshot of the employees for one period,
    optionally limited to one department. The compute button builds one
    line per department and job position with the opening, joined,
    terminated and closing head count. Finishing the snapshot locks it so
    the numbers stay as they were when the snapshot was taken.
    """

    _name = "manpower_head_count"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.date_duration",
    ]
    _description = "Manpower Head Count Snapshot"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _statusbar_visible_label = "draft,done"
    _policy_field_order = [
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

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
        readonly=True,
        states={"draft": [("readonly", False)]},
        ondelete="restrict",
        help="Limit the snapshot to the employees of this department. "
        "Leave empty to count all departments.",
    )
    line_ids = fields.One2many(
        string="Lines",
        comodel_name="manpower_head_count_line",
        inverse_name="head_count_id",
        readonly=True,
        copy=False,
        help="Head count per department and job position, built by the "
        "compute button.",
    )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super(ManpowerHeadCount, self)._get_policy_field()
        policy_field = [
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def action_compute_line(self):
        """Rebuild the head count lines of the draft snapshots.

        Triggered by the **Compute Lines** button: the existing lines are
        removed and recreated from the current employee data.

        :return: nothing; the lines of each snapshot are replaced
        """
        for record in self.sudo():
            record._compute_line()

    def _compute_line(self):
        """Replace the lines of this snapshot with freshly counted ones.

        :raises UserError: when the snapshot is not a draft
        """
        self.ensure_one()
        if self.state != "draft":
            error_message = """
Document Type: %s
Context: Compute head count lines
Database ID: %s
Problem: Lines can only be computed while the snapshot is draft
Solution: Restart the snapshot to draft first
""" % (
                self._description.lower(),
                self.id,
            )
            raise UserError(_(error_message))
        self.line_ids.unlink()
        line_obj = self.env["manpower_head_count_line"]
        for values in self._prepare_line_values():
            line_obj.create(values)

    def _get_employee_criteria(self):
        """Build the domain of the employees counted by the snapshot.

        Extension point: override to add more filters.

        :return: search domain of employees (archived ones included)
        """
        self.ensure_one()
        criteria = []
        if self.department_id:
            criteria.append(("department_id", "=", self.department_id.id))
        return criteria

    def _is_employee_active_on(self, employee, date):
        """Tell whether an employee is employed on a given date.

        An employee is employed on a date when the join date is empty or
        not after that date, the termination date is empty or after that
        date, and the employee is not archived without a termination
        date.

        :param employee: a single ``hr.employee`` record
        :param date: the date to check
        :return: True when the employee is employed on the date
        """
        result = True
        if employee.date_join and employee.date_join > date:
            result = False
        if employee.date_termination and employee.date_termination <= date:
            result = False
        if not employee.active and not employee.date_termination:
            result = False
        return result

    def _prepare_line_values(self):
        """Count the employees per department and job position.

        Archived employees are counted too, so employees who already
        left are part of the opening and terminated figures.

        :return: list of ``manpower_head_count_line`` create values;
            groups with only zero figures are left out
        """
        self.ensure_one()
        employee_obj = self.env["hr.employee"].with_context(active_test=False)
        employees = employee_obj.search(self._get_employee_criteria())
        groups = {}
        for employee in employees:
            if not employee.active and not employee.date_termination:
                continue
            key = (employee.department_id.id, employee.job_id.id)
            counts = groups.setdefault(
                key,
                {"opening": 0, "joined": 0, "terminated": 0, "closing": 0},
            )
            if self._is_employee_active_on(employee, self.date_start):
                counts["opening"] += 1
            if self._is_employee_active_on(employee, self.date_end):
                counts["closing"] += 1
            if employee.date_join and (
                self.date_start <= employee.date_join <= self.date_end
            ):
                counts["joined"] += 1
            if employee.date_termination and (
                self.date_start <= employee.date_termination <= self.date_end
            ):
                counts["terminated"] += 1
        result = []
        for key, counts in groups.items():
            if not any(counts.values()):
                continue
            result.append(
                {
                    "head_count_id": self.id,
                    "department_id": key[0],
                    "job_id": key[1],
                    "opening_count": counts["opening"],
                    "joined_count": counts["joined"],
                    "terminated_count": counts["terminated"],
                    "closing_count": counts["closing"],
                }
            )
        return result
