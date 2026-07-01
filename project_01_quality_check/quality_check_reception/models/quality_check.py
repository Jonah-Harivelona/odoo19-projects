from odoo import models, fields, api

class QualityCheck(models.Model):
    _name = 'quality.check'
    _description = 'Fiche de contrôle qualité'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Référence', readonly=True)
    picking_id = fields.Many2one('stock.picking', string='Réception', required=True)
    template_id = fields.Many2one('quality.check.template', string='Modèle', required=True)
    line_ids = fields.One2many('quality.check.line', 'check_id', string='Lignes de contrôle qualité')
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed')
    ], string='État', default='draft')
    conformity_rate = fields.Float(string='Taux de Conformité', compute='_compute_conformity_rate')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', string='Contrôleur responsable', default=lambda self: self.env.user)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name"):
                vals["name"] = self.env["ir.sequence"].next_by_code("quality.check")

        return super().create(vals_list)
    
    @api.depends('line_ids')
    def _compute_conformity_rate(self):
        for record in self:
            if record.line_ids:
                passed = len(record.line_ids.filtered(lambda l: l.is_conforming))
                record.conformity_rate = (passed / len(record.line_ids)) * 100
            else:
                record.conformity_rate = 0.0
    
    def action_start(self):
        self.state = 'in_progress'
    
    def action_validate(self):
        self._compute_conformity_rate()
        self.state = 'passed' if self.conformity_rate == 100 else 'failed'