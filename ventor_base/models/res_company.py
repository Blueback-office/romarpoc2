# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import models, fields


class Company(models.Model):
    _inherit = 'res.company'

    force_lot_validation_on_inventory_adjustment = fields.Boolean(
        string='Force Lot Validation on Inventory Adjustment',
    )
