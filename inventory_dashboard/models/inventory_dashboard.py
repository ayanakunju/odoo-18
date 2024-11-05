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
        print('Avg expense',data)
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

    @api.model
    def get_picking_type_data(self):
        domain = []
        tiles_data = {
            "stock_incoming": self.search_count(domain + [('picking_type_id.code', '=', 'incoming')]),
            "stock_outgoing": self.search_count(domain + [('picking_type_id.code', '=', 'outgoing')]),
            "stock_internal": self.search_count(domain + [('picking_type_id.code', '=', 'internal')])
        }
        print('tile data', tiles_data)
        return tiles_data


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


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    @api.model
    def get_stock_value(self):
        """
        returns stock valuation data
        """
        query = ('''select product_template.name->>'en_US' as name,
       sum(stock_valuation_layer.value)as total_value from stock_valuation_layer
       inner join product_product ON stock_valuation_layer.product_id = product_product.id
       inner join product_template ON product_product.product_tmpl_id = product_template.id
       group by product_template.name->>'en_US' order by total_value ;''')
        self._cr.execute(query)
        stock_value = self._cr.dictfetchall()
        value = []
        name = []
        for record in stock_value:
            value.append(record.get('total_value'))
            name.append(record.get('name'))
        result = {'name': name, 'stock_value': value}
        print('stock moves',result)
        return result


class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    @api.model
    def get_product_moves(self):
        """
        return all the product moves
        """
        user_filter = ''
        # if admin == False:
        user_filter = f"AND stock_move_line.create_uid = {self.env.uid}"
        # {user_filter}

        query = (f'''select product_template.name->>'en_US' as name,
       sum(stock_move_line.quantity)as total_quantity from stock_move_line
       inner join product_product ON stock_move_line.product_id = product_product.id
       inner join product_template ON product_product.product_tmpl_id = product_template.id  {user_filter}

       group by product_template.name->>'en_US' order by total_quantity DESC ;''')
        self._cr.execute(query)
        products_quantity = self._cr.dictfetchall()
        quantity = []
        name = []
        for record in products_quantity:
            quantity.append(record.get('total_quantity'))
            name.append(record.get('name'))
        value = {'name': name, 'count': quantity}
        return value







    # @api.model
    # def get_filter_product_moves(self, admin, filter_type):
    #     """
    #     returns data based on filter in the chart
    #     """
    #     print(admin, "get_filter_product_moves")
    #     time_filter = ''
    #     if filter_type == 'this_week':
    #         time_filter = "EXTRACT('WEEK' FROM stock_move.date) = EXTRACT('WEEK' FROM CURRENT_DATE)"
    #     elif filter_type == 'this_month':
    #         time_filter = "EXTRACT('MONTH' FROM stock_move.date) = EXTRACT('MONTH' FROM CURRENT_DATE)"
    #     elif filter_type == 'this_year':
    #         time_filter = "EXTRACT('YEAR' FROM stock_move.date) = EXTRACT('YEAR' FROM CURRENT_DATE)"
    #
    #     user_filter = ''
    #     if admin == False:
    #         user_filter = f"AND stock_move.create_uid = {self.env.uid}"
    #
    #     query = (f'''select product_template.name->>'en_US' as name,
    #                sum(product_uom_qty) as total_quantity
    #         from stock_move
    # 		inner join stock_picking on stock_move.picking_id = stock_picking.id
    # 		inner join stock_picking_type on stock_picking.picking_type_id = stock_picking_type.id
    #         inner JOIN product_product
    #             on stock_move.product_id = product_product.id
    #         inner JOIN product_template
    #             on product_product.product_tmpl_id = product_template.id
    # 			where {time_filter}{user_filter}
    #         group by product_template.name->>'en_US'
    #         order by total_quantity DESC''')
    #     print(query)
    #     self._cr.execute(query)
    #     products_quantity = self._cr.dictfetchall()
    #     quantity = []
    #     name = []
    #     for record in products_quantity:
    #         quantity.append(record.get('total_quantity'))
    #         name.append(record.get('name'))
    #     value = {'name': name, 'count': quantity}
    #     return value