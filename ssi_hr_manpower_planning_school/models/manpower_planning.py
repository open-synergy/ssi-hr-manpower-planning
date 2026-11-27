# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


# Extends the manpower planning of ``ssi_hr_manpower_planning`` with the
# school context (school unit, academic year, curriculum), the teaching
# assignment plan per subject and class, the additional assignments and
# the workload recap per employee. Every new field is optional, so a
# planning without school data keeps working as before.
class ManpowerPlanning(models.Model):
    _name = "manpower_planning"
    _inherit = ["manpower_planning"]

    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        readonly=True,
        states={"draft": [("readonly", False)]},
        ondelete="restrict",
        help="School unit this manpower planning is made for. Optional.",
    )
    school_branch_id = fields.Many2one(
        string="School Branch",
        comodel_name="school_branch",
        related="school_id.branch_id",
        store=True,
        compute_sudo=True,
        help="Branch of the selected school, copied from the school.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        readonly=True,
        states={"draft": [("readonly", False)]},
        ondelete="restrict",
        help="Academic year this manpower planning is made for. "
        "Selecting it fills the planning period.",
    )
    curriculum_id = fields.Many2one(
        string="Curriculum",
        comodel_name="manpower_planning_curriculum",
        readonly=True,
        states={"draft": [("readonly", False)]},
        ondelete="restrict",
        help="Curriculum this manpower planning follows. Optional.",
    )
    teaching_ids = fields.One2many(
        string="Teaching Assignments",
        comodel_name="manpower_planning_teaching",
        inverse_name="planning_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=True,
        help="Teaching assignment plan per subject, grade and class.",
    )
    assignment_ids = fields.One2many(
        string="Additional Assignments",
        comodel_name="manpower_planning_assignment",
        inverse_name="planning_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=True,
        help="Structural, additional duty, non-teacher, picket, coaching "
        "and extracurricular coach assignments.",
    )
    workload_ids = fields.One2many(
        string="Workloads",
        comodel_name="manpower_planning_workload",
        inverse_name="planning_id",
        readonly=True,
        help="Teaching and additional hours recap per employee.",
    )

    @api.onchange("academic_year_id")
    def onchange_date_start(self):
        self.date_start = False
        if self.academic_year_id:
            self.date_start = self.academic_year_id.date_start

    @api.onchange("academic_year_id")
    def onchange_date_end(self):
        self.date_end = False
        if self.academic_year_id:
            self.date_end = self.academic_year_id.date_end

    def action_import_teaching_assignment(self):
        """Open the wizard that imports teaching lines from assignments.

        :return: an ``ir.actions.act_window`` dict opening the wizard
        """
        for record in self.sudo():
            result = record._import_teaching_assignment()
        return result

    def _import_teaching_assignment(self):
        """Build the action that opens the import wizard.

        The wizard creates nothing until it is confirmed, so this method
        writes nothing itself.

        :return: an ``ir.actions.act_window`` dict opening the wizard
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Import from Teaching Assignment",
            "res_model": "import_teaching_assignment",
            "view_mode": "form",
            "target": "new",
            "context": {"default_planning_id": self.id},
        }
