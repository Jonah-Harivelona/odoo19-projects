from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    quality_check_template_id = fields.Many2one(
        'quality.check.template', 
        string='Quality Check Template',
        help="Select the default quality check template to use for this product during receipt."
    )