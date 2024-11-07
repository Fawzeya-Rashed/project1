from odoo import models, fields, api

from Source.odoo16.odoo.tools.populate import compute
from Source.odoo16.odoo.tools.view_validation import validate


class Property (models.Model):

    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread','mail.activity.mixin']

    ref = fields.Char(default='New', readonly=1)

    active = fields.Boolean(default=True)


    name = fields.Char(required=1, default='New', size=10, tracking="1")
    description = fields.Text()
    postcode = fields.Char(required=1)

    date_availability = fields.Date(tracking="1")
    expected_selling_date = fields.Date(tracking="1")
    is_late = fields.Boolean()

    expected_price = fields.Float(digits=(0,4))
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff', store=1)

    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], default='north')

    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
        ('closed','closed')
    ], default='draft')

    owner_id = fields.Many2one('owner')

    owner_phone = fields.Char(related='owner_id.phone')
    owner_address = fields.Char(related='owner_id.address')

    tag_ids = fields.Many2many('tag')

    line_ids = fields.One2many('property.line', 'property_id')

    _sql_constraints = [('unique_name','unique("name")','Name must be Unique')]

    @api.depends('expected_price','selling_price')
    def _compute_diff(self):
        for rec in self:
            print ("Iam in computed method")
            rec.diff = rec.expected_price - rec.selling_price

    # @api.onchange('expected_price')
    # def _onchange_expected_price(self):
    #     for rec in self:
    #         print("Iam in Onchange Method")
    #         return {
    #             'warning': {'title': 'warning', 'message': 'Onchange Test', 'type': 'notification'}
    #         }

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True


    @api.constrains('bedrooms')
    def _check_bedrooms_greeter_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValueError('must enter number of bedrooms')




    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None,access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print("Inside Search Method")
    #     return res
    #
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("Inside write Method")
    #     return res
    #
    # def unlink(self):
    #     res = super(Property, self)
    #     print("Inside Delete Method")
    #     return res

class PropertyLine(models.Model):

    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')