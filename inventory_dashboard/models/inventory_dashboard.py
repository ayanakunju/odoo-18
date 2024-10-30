# -*- coding: utf-8 -*-

from odoo import models, api


class StockPicking(models.Model):
    """stock picking inherited model and provides methods for retrieving data for
    dashboard."""
    _inherit = 'stock.picking'

    @api.model
    def get_inventory_tiles_data(self):
        domain = []
        stock_incoming =  self.search_count(domain + [('picking_type_id.code', '=', 'incoming'),
                                                      ('state', 'not in',['done', 'cancel'])])
        stock_outgoing =  self.search_count(domain + [('picking_type_id.code', '=', 'outgoing'),
                                                     ('state', 'not in',['done', 'cancel'])])
        stock_internal =  self.search_count(domain + [('picking_type_id.code', '=', 'internal'),
                                                      ('state', 'not in',['done', 'cancel'])])
        print('stock_incoming',stock_incoming)
        print('stock_outgoing',stock_outgoing)
        print('stock_internal',stock_internal)

        return {
            'stock_incoming': stock_incoming,
            'stock_outgoing': stock_outgoing,
            'stock_internal': stock_internal,
        }


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def get_stock_move_location(self):
        company_id = self.env.company.id
        query = ('''select stock_location.complete_name, count(stock_move.id) from stock_move 
                inner join stock_location on stock_move.location_id = stock_location.id where stock_move.state = 'done' 
                and stock_move.company_id = %s group by stock_location.complete_name''' % company_id)
        self._cr.execute(query)
        stock_move = self._cr.dictfetchall()
        count = []
        complete_name = []
        for record in stock_move:
            count.append(record.get('count'))
            complete_name.append(record.get('complete_name'))
        value = {'name': complete_name, 'count': count}
        return value
