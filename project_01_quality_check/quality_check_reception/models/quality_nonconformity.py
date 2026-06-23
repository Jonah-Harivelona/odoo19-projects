from odoo import models, fields, api


class QualityNonConconformity(models.Model):
    _name = 'quality.nonconformity'
    _description = 'Quality Non-Conformity'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Number', 
        required=True
    )
    
    check_id = fields.Many2one(
        'quality.check', 
        string='Quality Check', 
        required=True,
        tracking=True
    )
    
    picking_id = fields.Many2one(
        'stock.picking', 
        string='Transfer', 
        tracking=True
    )
    
    partner_id = fields.Many2one(
        'res.partner', 
        string='Vendor', 
        tracking=True
    )
    
    description = fields.Text(
        string='Description'
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_analysis', 'In Analysis'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], string='Status', default='draft', required=True, tracking=True)
    
    date = fields.Datetime(
        string='Date', 
        default=fields.Datetime.now, 
        required=True,
        tracking=True
    )
    
    action_taken = fields.Text(
        string='Action Taken'
    )

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('quality.nonconformity') or '/'
        return super(QualityNonConconformity, self).create(vals)