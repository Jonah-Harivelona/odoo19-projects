from odoo import models, fields

class  QualityCheckTemplateLine(models.Model):
    _name = 'quality.check.template.line'
    _description = 'Quality Check Template Line'
    
    template_id = fields.Many2one('quality.check.template', string='Template', required=True)
    name = fields.Char(string='Check Name', required=True)
    check_type = fields.Selection([
        ('ok', 'Ok'),
        ('nok', 'Nok'),
        ('measure', 'Measure'),
       
    ], string='Check Type', required=True, default='ok')
    min_value = fields.Float(string='Minimum Value', )
    sequence = fields.Integer(string='Sequence', default=10)