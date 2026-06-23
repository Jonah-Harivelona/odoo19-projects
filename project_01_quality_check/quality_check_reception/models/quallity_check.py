from odoo import models, fields, api

class QualityCheck(models.Model):
    _name = 'quality.check'
    _description = 'Quality Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Quality Check Reference', required=True, readonly=True)
    picking_id = fields.Many2one('stock.picking', string='Picking', required=True)
    template_id = fields.Many2one('quality.check.template', string='Template', required=True)
    line_ids = fields.One2many('quality.check.line', 'check_id', string='Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed')
    ], string='State', default='draft')
    conformity_rate = fields.Float(string='Conformity Rate', compute='_compute_conformity_rate')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    
    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = self.env['ir.sequence'].next_by_code('quality.check')
        return super().create(vals)
    
    @api.depends('line_ids')
    def _compute_conformity_rate(self):
        for record in self:
            if record.line_ids:
                passed = len(record.line_ids.filtered(lambda l: l.result == 'passed'))
                record.conformity_rate = (passed / len(record.line_ids)) * 100
            else:
                record.conformity_rate = 0.0
    
    def action_start(self):
        self.state = 'in_progress'
    
    def action_validate(self):
        self._compute_conformity_rate()
        self.state = 'passed' if self.conformity_rate == 100 else 'failed'