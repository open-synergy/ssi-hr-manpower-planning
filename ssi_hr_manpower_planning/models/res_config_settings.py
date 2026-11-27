# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    # Shows the contract employment statuses of the company on the
    # Settings screen. The field is not prefixed with ``default_``,
    # ``group_`` or ``module_`` because Odoo treats such names as a
    # setting kind that needs extra attributes.
    _inherit = "res.config.settings"

    manpower_contract_employment_status_ids = fields.Many2many(
        string="Contract Employment Statuses",
        related="company_id.manpower_contract_employment_status_ids",
        readonly=False,
        help="Employment statuses of the employees whose contract is "
        "reviewed in a manpower planning.",
    )
