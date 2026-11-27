# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    # Adds the employment statuses that count as a contract to the
    # company, so a manpower planning can generate its contract review
    # lines from them.
    _inherit = "res.company"

    manpower_contract_employment_status_ids = fields.Many2many(
        string="Contract Employment Statuses",
        comodel_name="hr.employment_status",
        relation="company_manpower_contract_status_rel",
        column1="company_id",
        column2="employment_status_id",
        help="Employment statuses of the employees whose contract is "
        "reviewed in a manpower planning. The Generate Contract "
        "button of a manpower planning takes the employees of the "
        "company that have one of these statuses.",
    )
