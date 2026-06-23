from odoo import models, fields, api

class QualityCheckLine(models.Model):
    _name = 'quality.check.line'
    _description = 'Quality Check Line'
    
    check_id = fields.Many2one('quality.check', required=True)
    name = fields.Char(required=True)
    check_type = fields.Selection([
        ('ok_nok', 'OK/NOK'), 
        ('measure', 'Measure')
    ], required=True)
    result_ok_nok = fields.Selection([
        ('ok', 'OK'), 
        ('nok', 'NOK')]
    , states={'invisible': [('check_type', '!=', 'ok_nok')]})
    result_measure = fields.Float(states=
        {'invisible': [('check_type', '!=', 'measure')]
    })
    min_value = fields.Float()
    max_value = fields.Float()
    is_conforming = fields.Boolean(string='Is Conforming', compute='_compute_is_conforming')

    @api.depends('check_type', 'result_ok_nok', 'result_measure', 'min_value', 'max_value')
    def _compute_is_conforming(self):
        for line in self:
            if line.check_type == 'ok_nok':
                line.is_conforming = line.result_ok_nok == 'ok'
            elif line.check_type == 'measure':
                line.is_conforming = line.min_value <= line.result_measure <= line.max_value
            else:
                line.is_conforming = False

    