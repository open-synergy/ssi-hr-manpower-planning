# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ManpowerHeadCountLine(models.Model):
    """
    Detail line of a head count snapshot. One line holds the opening,
    joined, terminated and closing head count of one job position in
    one department for the period of the snapshot.
    """

    _name = "manpower_head_count_line"
    _description = "Manpower Head Count - Line"
    _order = "head_count_id, department_id, job_id, id"

    head_count_id = fields.Many2one(
        string="# Head Count Snapshot",
        comodel_name="manpower_head_count",
        required=True,
        ondelete="cascade",
        help="Head count snapshot that owns this line.",
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        help="Department the head count is counted for.",
    )
    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
        help="Job position the head count is counted for.",
    )
    opening_count = fields.Integer(
        string="Opening",
        default=0,
        help="Number of employees active on the first day of the period.",
    )
    joined_count = fields.Integer(
        string="Joined",
        default=0,
        help="Number of employees who joined during the period.",
    )
    terminated_count = fields.Integer(
        string="Terminated",
        default=0,
        help="Number of employees whose employment ended during the " "period.",
    )
    closing_count = fields.Integer(
        string="Closing",
        default=0,
        help="Number of employees active on the last day of the period.",
    )
