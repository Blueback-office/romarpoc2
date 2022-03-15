# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import struct
import logging

_logger = logging.getLogger(__name__)

LOGOTYPE_W = 500
LOGOTYPE_H = 500


class VentorConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    logotype_file = fields.Binary('Ventor Application Logo File')
    logotype_name = fields.Char('Ventor Application Logo Filename')

    module_outgoing_routing = fields.Boolean(
        string='Outgoing Routing'
    )

    add_barcode_on_view = fields.Boolean(
        string='Show the Location barcode field on the form',
    )

    base_version = fields.Char(
        string='Base Module Version',
        compute='_compute_base_version',
        store=False,
    )

    force_lot_validation_on_inventory_adjustment = fields.Boolean(
        string='Force Lot Validation on Inventory Adjustment',
        readonly=False,
        related='company_id.force_lot_validation_on_inventory_adjustment',
    )

    custom_package_name = fields.Char(
        string='Custom package name',
        config_parameter='ventor_base.custom_package_name',
    )

    @api.depends('company_id')
    def _compute_base_version(self):
        self.env.cr.execute(
            "SELECT latest_version FROM ir_module_module WHERE name='ventor_base'"
        )
        result = self.env.cr.fetchone()
        full_version = result and result[0]
        split_value = full_version and full_version.split('.')
        self.base_version = split_value and '.'.join(split_value[-3:])

    @api.model
    def get_values(self):
        res = super(VentorConfigSettings, self).get_values()

        conf = self.env['ventor.config'].sudo()

        logo = conf.get_param('logo.file', default=None)
        name = conf.get_param('logo.name', default=None)

        res.update({
            'logotype_file': logo or False,
            'logotype_name': name or False,
        })

        view_with_barcode = self.env.ref('ventor_base.view_location_form_inherit_additional_barcode')
        res['add_barcode_on_view'] = view_with_barcode.active

        return res

    def _set_manage_packages(self, previous_group):
        operation_type_ids = self.env['stock.picking.type'].search([])
        group_stock_tracking_lot = previous_group.get('group_stock_tracking_lot')

        if group_stock_tracking_lot != self.group_stock_tracking_lot:
            operation_type_ids.manage_packages = self.group_stock_tracking_lot
            if not self.group_stock_tracking_lot:
                operation_type_ids.show_put_in_pack_button = self.group_stock_tracking_lot
                operation_type_ids.scan_destination_package = self.group_stock_tracking_lot

    def _set_manage_product_owner(self, previous_group):
        operation_type_ids = self.env['stock.picking.type'].search([])
        group_stock_tracking_owner = previous_group.get('group_stock_tracking_owner')

        if (
            group_stock_tracking_owner != self.group_stock_tracking_owner
            and not self.group_stock_tracking_owner
        ):
            operation_type_ids.manage_product_owner = self.group_stock_tracking_owner

    def set_values(self):
        previous_group = self.default_get(['group_stock_tracking_lot', 'group_stock_tracking_owner'])
        res = super(VentorConfigSettings, self).set_values()

        conf = self.env['ventor.config'].sudo()

        self._validate_logotype()
        conf.set_param('logo.file', self.logotype_file or False)
        conf.set_param('logo.name', self.logotype_name or False)

        view_with_barcode = self.env.ref('ventor_base.view_location_form_inherit_additional_barcode')
        view_with_barcode.active = self.add_barcode_on_view

        self.sudo()._set_manage_packages(previous_group)
        self.sudo()._set_manage_product_owner(previous_group)
        return res

    def _validate_logotype(self):
        if not self.logotype_file:
            return False

        dat = base64.decodebytes(self.logotype_file)

        png = (dat[:8] == b'\211PNG\r\n\032\n' and (dat[12:16] == b'IHDR'))
        if not png:
            raise UserError(_('Apparently, the logotype is not a .png file.'))

        width, height = struct.unpack('>LL', dat[16:24])
        if int(width) < LOGOTYPE_W or int(height) < LOGOTYPE_H:
            raise UserError(_('The logotype can\'t be less than {}x{} px.'.format(LOGOTYPE_W, LOGOTYPE_H)))

        return True
