# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class SchemeProgramRule(models.Model):
    _inherit = 'fal.pos.promotional.scheme.rule'
    _rec_name = 'product_id'


class GenerateSchemeProgram(models.Model):
    _name = 'generate.pos.promotional.scheme'

    name = fields.Char("Name", required=True)
    scheme_type = fields.Selection(
        [('product', 'Product'),
         ('discount', 'Discount')], required=True, default='discount')
    discount_percentage = fields.Float("Discount (%)")
    product_id = fields.Many2one('product.product', string="Product",
                                 domain="[('sale_ok', '=', 1), ('available_in_pos', '=', 1)]")
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision(
        'Product Unit of Measure'), default=1.0)
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.user.company_id.currency_id, string="Currency")
    price_unit = fields.Monetary(
        'Unit Price', required=True, digits=dp.get_precision('Product Price'), default=1.0)
    active = fields.Boolean('Active', default=True)
    repeatable = fields.Boolean("Allow Multiple", default=True)
    auto_check = fields.Boolean('Auto Check', default=True)
    pos_config_promotional_scheme_ids = fields.Many2many("pos.config", string="Available on PoS")
    date_start = fields.Date("Date Start")
    date_end = fields.Date("Date End")
    product_ids = fields.Many2many('product.product', string='Produk',
                                   domain="[('sale_ok', '=', 1), ('available_in_pos', '=', 1)]")

    def create_pos_promotional_scheme(self):
        pos_config_promotional_scheme_ids = self.pos_config_promotional_scheme_ids.mapped('id')
        product_ids = self.product_ids.mapped('id')
        for rec in product_ids:
            self.env['fal.pos.promotional.scheme'].create({
                'generate_id': self.id,
                'name': self.name,
                'date_start': self.date_start,
                'date_end': self.date_end,
                'scheme_type': self.scheme_type,
                'product_id': self.product_id,
                'repeatable': self.repeatable,
                'auto_check': self.auto_check,
                'discount_after_tax': True,
                'discount_percentage': self.discount_percentage,
                'pos_config_promotional_scheme_ids': [(6, 0, pos_config_promotional_scheme_ids)],
                'rule_ids': [(0, 0, {
                    'rule_type': 'purchase_product',
                    'product_id': rec,
                    'product_uom_qty': 1
                })]
            })

    def remove_pos_promotional_scheme(self):
        obj_promotional = self.env['fal.pos.promotional.scheme'].search([('generate_id', '=', self.id)])
        obj_promotional_ids = obj_promotional.mapped('id')
        self.env['fal.pos.promotional.scheme'].browse(obj_promotional_ids).unlink()


class SchemeProgram(models.Model):
    _inherit = 'fal.pos.promotional.scheme'

    generate_id = fields.Many2one(comodel_name='generate.pos.promotional.scheme', string='Generate from')
    

