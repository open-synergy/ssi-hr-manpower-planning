# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ManpowerContractRecommendation(models.Model):
    """
    Master data of recommendations given to an employee contract during a
    manpower planning contract review (for example extend, make permanent
    or terminate). A recommendation can be flagged as ending the contract.
    """

    _name = "manpower_contract_recommendation"
    _inherit = ["mixin.master_data"]
    _description = "Manpower Contract Recommendation"

    is_terminate = fields.Boolean(
        string="Terminate Contract",
        default=False,
        help="Check if this recommendation means the employee contract "
        "should be ended instead of continued.",
    )
