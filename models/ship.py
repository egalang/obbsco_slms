from odoo import api, models, fields

class Ship(models.Model):
    _name = 'ship.ship'
    _description = 'Ship Profile'
    _inherit = ['mail.thread','mail.activity.mixin']  # enable chatter and attachments

    name = fields.Char(string='Ship Name', required=True, tracking=True)
    imo_number = fields.Char(string='IMO Number', required=True, help='International Maritime Organization number', tracking=True)
    ship_type = fields.Selection([
        ('cargo', 'Cargo'),
        ('tanker', 'Tanker'),
        ('container', 'Container'),
        ('passenger', 'Passenger'),
        ('fishing', 'Fishing'),
        ('naval', 'Naval'),
        ('other', 'Other')
    ], string='Type of Ship', required=True, tracking=True)
    flag = fields.Char(string='Flag State', tracking=True)
    owner_id = fields.Many2one('res.partner', string='Owner', tracking=True)
    operator_id = fields.Many2one('res.partner', string='Operator', tracking=True)
    build_year = fields.Char(string='Year Built', tracking=True)
    shipyard = fields.Char(string='Shipyard', tracking=True)
    status = fields.Selection([
        ('design', 'Design'),
        ('building', 'Under Construction'),
        ('active', 'In Operation'),
        ('maintenance', 'Under Maintenance'),
        ('decommissioned', 'Decommissioned')
    ], string='Lifecycle Status', default='design', tracking=True)

    gross_tonnage = fields.Float(string='Gross Tonnage', tracking=True)
    deadweight = fields.Float(string='Deadweight (DWT)', tracking=True)
    length_overall = fields.Float(string='Length Overall (LOA) in meters', tracking=True)
    beam = fields.Float(string='Beam (Width) in meters', tracking=True)
    draft = fields.Float(string='Draft in meters', tracking=True)
    class_society = fields.Char(string='Class Society', tracking=True)
    home_port = fields.Char(string='Home Port', tracking=True)
    note = fields.Text(string='Notes', tracking=True)
    image_128 = fields.Binary("Image", attachment=True, tracking=True)
    # Relations to other components will be added later
    process_log_ids = fields.One2many(
        'ship.ship_process',
        'ship_id',
        string='Lifecycle Process Logs',
        tracking=True
    )
    process_log_count = fields.Integer(
        string='Process Log Count',
        compute='_compute_process_log_count', 
        tracking=True
    )

    @api.depends('process_log_ids')
    def _compute_process_log_count(self):
        for ship in self:
            ship.process_log_count = len(ship.process_log_ids)
            
    def action_ship_process_logs(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Process Logs',
            'res_model': 'ship.ship_process',
            'view_mode': 'tree,form',
            'domain': [('ship_id', '=', self.id)],
            'context': {'default_ship_id': self.id}
        }

class ShipProcess(models.Model):
    _name = 'ship.process'
    _description = 'Ship Lifecycle Process Type'

    name = fields.Char(required=True)
    description = fields.Text()

class ShipProcessStatus(models.Model):
    _name = 'ship.process.status'
    _description = 'Custom Process Status'

    name = fields.Char(string='Status Name', required=True)
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(default=True)

class ShipProcessLog(models.Model):
    _name = 'ship.ship_process'
    _description = 'Ship Lifecycle Process Entry'
    _inherit = ['mail.thread','mail.activity.mixin']  # enable chatter and attachments

    ship_id = fields.Many2one('ship.ship', string='Ship', required=True, ondelete='cascade')
    process_id = fields.Many2one('ship.process', string='Process Type', required=True)

    date_started = fields.Date(string='Start Date')
    date_completed = fields.Date(string='Completion Date')

    status_id = fields.Many2one('ship.process.status', string='Status')

    preparer_id = fields.Many2one('res.partner', string='Prepared By (Owner)')
    reviewer_id = fields.Many2one('res.partner', string='Reviewed By (Class Society)')
    approver_id = fields.Many2one('res.partner', string='Approved By (MARINA)')

    documents_submitted = fields.Text(string='Documents Submitted')
    notes = fields.Text(string='Remarks / Outcome')