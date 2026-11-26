# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ManpowerPlanningCurriculum(models.Model):
    """
    Master data of the curriculums a school manpower planning can be
    made for. The school modules have no curriculum model, so this simple
    master data lets a planning state which curriculum it follows.
    """

    _name = "manpower_planning_curriculum"
    _inherit = ["mixin.master_data"]
    _description = "Manpower Planning Curriculum"

    description = fields.Text(
        string="Description",
        help="Free-form description of the curriculum.",
    )
