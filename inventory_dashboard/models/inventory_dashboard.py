# -*- coding: utf-8 -*-

from odoo import models, api


class StockPicking(models.Model):
    """stock picking inherited model and provides methods for retrieving data for
    dashboard."""
    _inherit = 'stock.picking'

    @api.model
    def get_inventory_tiles_data(self):
        domain = []
        tiles_data = {
            "stock_incoming": self.search_count(domain + [('picking_type_id.code', '=', 'incoming'),
                                                          ('state', 'not in', ['done', 'cancel'])]),
            "stock_outgoing": self.search_count(domain + [('picking_type_id.code', '=', 'outgoing'),
                                                          ('state', 'not in', ['done', 'cancel'])]),
            "stock_internal": self.search_count(domain + [('picking_type_id.code', '=', 'internal'),
                                                          ('state', 'not in', ['done', 'cancel'])])
        }
        print('tile data',tiles_data)
        return tiles_data

    @api.model
    def get_product_average_expense(self):
        """ calculate the average cost"""
        products = self.env['product.product'].search([])
        data = {}
        for product in products:
            if product.standard_price > 0:
                data.update({product.name: product.standard_price})
        print('expense',data)
        return data

    @api.model
    def get_locations(self):
        stock_quant_ids = self.env['stock.quant'].search([])
        locations = stock_quant_ids.mapped('location_id')
        value = {}
        for rec in locations:
            loc_stock_quant = stock_quant_ids.filtered(lambda x: x.location_id == rec)
            on_hand_quantity = sum(loc_stock_quant.mapped('inventory_quantity_auto_apply'))
            value[rec.name] = on_hand_quantity
        print('valueeee', value)
        return value


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def get_stock_move_location(self):
        query = ('''select stock_location.name, count(stock_move.id) from stock_move
                       inner join stock_location on stock_move.location_id = stock_location.id where stock_move.state = 'done'
                       group by stock_location.name''')
        self._cr.execute(query)
        stock_move = self._cr.dictfetchall()
        count = []
        name = []
        for record in stock_move:
            count.append(record.get('count'))
            name.append(record.get('name'))
        value = {'name': name, 'count': count}
        print('location count',value)
        return value


# class StockValuationLayer(models.Model):
#     _inherit = 'stock.valuation.layer'
#
#     @api.model
#     def get_stock_value(self):
#         """
#         returns stock valuation data
#         """
#         query = ('''select product_template.name->>'en_US' as name,
#        sum(stock_valuation_layer.value)as total_value from stock_valuation_layer
#        inner join product_product ON stock_valuation_layer.product_id = product_product.id
#        inner join product_template ON product_product.product_tmpl_id = product_template.id
#        group by product_template.name->>'en_US' order by total_value DESC;''')
#         self._cr.execute(query)
#         stock_value = self._cr.dictfetchall()
#         value = []
#         name = []
#         for record in stock_value:
#             value.append(record.get('total_value'))
#             name.append(record.get('name'))
#         result = {'name': name, 'stock_value': value}
#         print('stock moves',result)
#         return result
