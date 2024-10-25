# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import date


class WizardOrderLines(models.TransientModel):
    _name = 'wizard.order.lines'
    _description = 'Wizard Order Lines'

    starting_date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    template_name = fields.Char(string='Name')
    tmpl_id = fields.Many2one('journal.entry.wizard', string='id')
    template_id = fields.Many2one('recurring.payments', string='Template Reference')


class PostRecurringEntries(models.Model):
    _inherit = 'account.move'

    def _action_post_entries(self):
        """Override to handle recurring entries posting"""
        today = date.today()
        entry = self.env['account.move'].search([('state', '=', 'draft'), ('date', '<=', today)])
        for move in entry:
            move.action_post()

