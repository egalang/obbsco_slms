from odoo import http
from odoo.http import request

class ShipPortal(http.Controller):

    @http.route(['/my/ships'], type='http', auth='user', website=True, csrf=True)
    def portal_my_ships(self, **post):
        partner = request.env.user.partner_id
        Ship = request.env['ship.ship'].sudo()

        if post and 'name' in post:
            # Ship registration form was submitted
            ship_vals = {
                'name': post.get('name'),
                'imo_number': post.get('imo_number'),
                'ship_type': post.get('ship_type'),
                'flag': post.get('flag'),
                'build_year': post.get('build_year'),
                'shipyard': post.get('shipyard'),
                'owner_id': partner.id,
            }
            Ship.create(ship_vals)
            return request.redirect('/my/ships')

        ships = Ship.search([('owner_id', '=', partner.id)])
        return request.render('slms.portal_my_ships', {
            'ships': ships
        })
