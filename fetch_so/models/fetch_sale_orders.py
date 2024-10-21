# -*- coding: utf-8 -*-

import xmlrpc.client
from odoo import models
import re


class FetchSaleorder(models.TransientModel):
    _name = 'fetch.sale.order'
    _description = 'Fetch Sale Order'

    def action_fetch_so(self):
        """Fetching details of v17  and v18 db from the wizard and importing"""

    # database 1 version 17
        url_db1 = "http://localhost:8016"
        db_1 = 'saleorder_migration'
        username_db_1 = '1'
        password_db_1 = '1'
        common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
        models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
        print('+++', common_1.version())
        # version_db1 = common_1.version()

    # database 2 version 18
        url_db2 = "http://localhost:8018"
        db_2 = 'data_migration'
        username_db_2 = '2'
        password_db_2 = '2'
        common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
        models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
        # version_db2 = common_2.version()
        print('>>>>>', common_1, db_1, username_db_1, password_db_1)
        uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
        print('uid_db1', uid_db1)
        uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})
        print('uid_db2', uid_db2)

        db_1_so = models_1.execute_kw(db_1, uid_db1, password_db_1, 'sale.order', 'search_read', [], {
            'fields': ['name', 'partner_id', 'user_id', 'amount_total', 'order_line', 'state','date_order'],
            'domain': [('state', '=', 'sale')]
        })
        print('sooooooooo', db_1_so)

        db_1_partner = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [],
                                           {'fields': ['id', 'name', 'email']})
        print('partners', db_1_partner)

        db_1_product = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.template', 'search_read', [],
                                           {'fields': ['id', 'name', 'list_price', 'invoice_policy']})
        print('products', db_1_product)

    # Creating partners in current db from old db
        for rec in db_1_partner:
            db_2_partners = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search_read', [],
                                                {'domain': [('name', '=', rec['name'])]})
            if not db_2_partners:
                new_partners = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'create',
                                                   [{
                                                       'name': rec['name'],
                                                       'id': rec['id'],
                                                       'email': rec['email']
                                                   }]
                                                   )
                print('new_partners', new_partners)

    # Creating products in current db from old db
        for rec in db_1_product:
            db_2_products = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.template', 'search_read', [],
                                                {'domain': [('name', '=', rec['name'])]})
            if not db_2_products:
                new_products = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.template', 'create',
                                                   [{
                                                       'name': rec['name'],
                                                       'id': rec['id'],
                                                       'list_price': rec['list_price'],
                                                       'invoice_policy':rec['invoice_policy']
                                                   }]
                                                   )
                print('new_products', new_products)

    # Creating sale order in current db from old db
        for rec in db_1_so:
            partner = self.env['res.partner'].search([('name', '=', rec['partner_id'][1])])
            sale_order = self.env['sale.order'].sudo().search([('name', '=', rec['name'])]).id
            if not sale_order:
                sale_order = models_2.execute_kw(db_2, uid_db2, password_db_2, 'sale.order', 'create',
                                                 [{
                                                     'name': rec['name'],
                                                     'partner_id': partner.id,
                                                     'amount_total': rec['amount_total'],
                                                     # 'order_line': order_line[0],
                                                     'state': rec['state'],
                                                     'date_order': rec['date_order'],

                                                 }]
                                                 )
                order_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'sale.order.line',
                                                 'search_read', [],
                                                 {'domain': [('order_id', '=', rec['id'])]})
                for record in order_line:
                    product_new = self.env['product.template'].search([('name', '=', 'product_id')])
                    orders = self.env['sale.order'].browse(sale_order)
                    vals = {
                        'name': record['name'],
                        'product_id': product_new.id,
                        'order_id': int(orders.id),
                        'product_uom_qty': record['product_uom_qty'],
                        'price_unit': record['price_unit'],
                        'product_uom': record['product_uom'][0],
                        'display_type': record['display_type']
                    }
                    models_2.execute_kw(db_2, uid_db2, password_db_2, 'sale.order.line', 'create', [vals])


