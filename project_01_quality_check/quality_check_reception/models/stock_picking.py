from odoo import models, fields, api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    quality_check_ids = fields.One2many(
        'quality.check', 
        'picking_id', 
        string='Quality Checks'
    )
    
    quality_check_state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed')
    ], string='Quality Status', compute='_compute_quality_check_state', store=True)

    @api.depends('quality_check_ids', 'quality_check_ids.state')
    def _compute_quality_check_state(self):
        for picking in self:
            if not picking.quality_check_ids:
                picking.quality_check_state = 'pending'
                continue
                
            states = picking.quality_check_ids.mapped('state')
            
            if 'failed' in states:
                picking.quality_check_state = 'failed'
            elif 'in_progress' in states:
                picking.quality_check_state = 'in_progress'
            elif all(state == 'passed' for state in states):
                picking.quality_check_state = 'passed'
            else:
                picking.quality_check_state = 'pending'

    def button_validate(self):
        for picking in self:
            if picking.picking_type_code == 'incoming':
                
                if not picking.quality_check_ids:
                    raise UserError(
                        "Validation blocked: No quality check sheet has been created for this incoming transfer."
                    )
                
                if picking.quality_check_state == 'failed':
                    raise UserError(
                        "Validation blocked: One or more quality checks have failed. "
                        "Please resolve the non-conformity before validating."
                    )
                    
        return super(StockPicking, self).button_validate()