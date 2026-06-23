from odoo import models, fields, api
from odoo.exceptions import ValidationError

class QualityCheckTemplate(models.Model):
    _name = 'quality.check.template'
    _description = 'Quality Check Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
     
    name = fields.Char(string='Template Name', required=True)
    product_id = fields.Many2one('product.template', string='Product')
    product_category_id = fields.Many2one('product.category', string='Product Category')
    line_ids = fields.One2many('quality.check.template.line', 'template_id', string='Quality Check Lines')
    active = fields.Boolean(string='Active', default=True)
     
    @api.constrains('product_id', 'product_category_id')
    def _check_product_or_category(self):
        for record in self:
            if not record.product_id and not record.product_category_id:
                raise ValidationError(
                    "Vous devez spécifier au moins un produit ou une catégorie de produit."
                )
                
    