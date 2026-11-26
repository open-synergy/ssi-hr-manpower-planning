# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


# Extends the recruitment vacancy of ``ssi_hr_recruitment`` with the link
# to the manpower planning the vacancy was requested from. The expected
# join date and the reason already live in ``ssi_hr_recruitment``.
class RecruitmentVacancy(models.Model):
    _name = "recruitment_vacancy"
    _inherit = ["recruitment_vacancy"]

    manpower_planning_id = fields.Many2one(
        string="Manpower Planning",
        comodel_name="manpower_planning",
        readonly=True,
        ondelete="restrict",
        help="Manpower planning this vacancy was requested from. Optional "
        "and filled when the vacancy is created from a manpower planning.",
    )
