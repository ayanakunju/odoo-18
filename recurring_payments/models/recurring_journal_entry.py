# -*- coding: utf-8 -*-

from odoo import fields, models

class JournalEntryWizard(models.TransientModel):
    _name = 'journal.entry.wizard'
    _description = 'Journal Entry Wizard'

    starting_date = fields.Date(string='Starting Date')
    ending_date = fields.Date(string='Ending Date')
    tmpl_id = fields.Many2one('recurring.payments', string='id')
    amount = fields.Float('Amount')
    template_name = fields.Char('Name')




