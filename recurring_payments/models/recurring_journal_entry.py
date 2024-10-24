# -*- coding: utf-8 -*-

from odoo import fields, models, api, Command
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class JournalEntryWizard(models.TransientModel):
    _name = 'journal.entry.wizard'
    _description = 'Journal Entry Wizard'

    starting_date = fields.Date(string='Starting Date')
    ending_date = fields.Date(string='Ending Date')
    recurring_lines = fields.One2many('wizard.order.lines', 'tmpl_id',
                                      compute='_compute_order_lines', store=True)
    # template_name = fields.Char(string='Name')
    # tmpl_id = fields.Many2one('wizard.order.lines', string='id')

    # @api.depends('starting_date')
    # def _compute_order_lines(self):
    #     starting_date = self.starting_date
    #     while starting_date < self.ending_date:
    #         date = starting_date
    #         # self.action_create_lines(date)
    #         starting_date = self.compute_next_date(date)
    #     ids = self.env['wizard.order.lines']
    #     vals = {
    #         # 'template_name': self.template_name,
    #         # 'amount': self.amount,
    #         'starting_date': date,
    #         # 'tmpl_id': self.id,
    #         # 'journal_id': self.journal_id.id,
    #         # 'currency_id': self.currency_id.id,
    #         # 'state': 'draft'
    #     }
    #     ids.create(vals)


    def action_generate_entry(self):
        data = self.env['recurring.payments'].search([('state', '=', 'running')])
        print(data)


class WizardOrderLines(models.TransientModel):
    _name = 'wizard.order.lines'

    starting_date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    template_name = fields.Char(string='Name')
    tmpl_id = fields.Many2one('journal.entry.wizard', string='id')


    # recurring_lines = fields.One2many('journal.entry.wizard', 'tmpl_id')
    # ending_date = fields.Date(string='Ending Date')

    # @api.model
    # def _compute_generate_entries(self):
    #     data = self.env['recurring.payments'].search(
    #         [('state', '=', 'running')])
    #     entries = self.env['account.move'].search(
    #         [('recurring_ref', '!=', False)])
    #     journal_dates = []
    #     journal_codes = []
    #     remaining_dates = []
    #     for entry in entries:
    #         journal_dates.append(str(entry.starting_date))
    #         if entry.recurring_ref:
    #             journal_codes.append(str(entry.recurring_ref))
    #     today = datetime.today()
    #     for line in data:
    #         if line.starting_date:
    #             recurr_dates = []
    #             start_date = datetime.strptime(str(line.date_creation), '%Y-%m-%d')
    #             while start_date <= today:
    #                 recurr_dates.append(str(start_date.date()))
    #                 if line.recurring_period == 'days':
    #                     start_date += relativedelta(
    #                         days=line.recurring_interval)
    #                 elif line.recurring_period == 'weeks':
    #                     start_date += relativedelta(
    #                         weeks=line.recurring_interval)
    #                 elif line.recurring_period == 'months':
    #                     start_date += relativedelta(
    #                         months=line.recurring_interval)
    #                 else:
    #                     start_date += relativedelta(
    #                         years=line.recurring_interval)
    #             for rec in recurr_dates:
    #                 recurr_code = str(line.id) + '/' + str(rec)
    #                 if recurr_code not in journal_codes:
    #                     remaining_dates.append({
    #                         'starting_date': rec,
    #                         'template_name': line.name,
    #                         'amount': line.amount,
    #                         'tmpl_id': line.id,
    #                     })
    #     child_ids = self.recurring_lines.create(remaining_dates)
    #     for line in child_ids:
    #         tmpl_id = line.tmpl_id
    #         recurr_code = str(tmpl_id.id) + '/' + str(line.starting_date)
    #         line_ids = [Command.create({
    #             'account_id': tmpl_id.credit_account.id,
    #             'credit': line.amount,
    #         }), Command.create({
    #             'account_id': tmpl_id.debit_account.id,
    #             'debit': line.amount,
    #         })]
    #         vals = {
    #             'starting_date': line.starting_date,
    #             'recurring_ref': recurr_code,
    #             'journal_id': tmpl_id.journal_id.id,
    #             'ref': line.template_name,
    #             'line_ids': line_ids
    #         }
    #         move_id = self.env['account.move'].create(vals)
    #         if tmpl_id.journal_state == 'posted':
    #             move_id.post()


class FilterRecurringEntries(models.Model):
    _inherit = 'account.move'

#     recurring_ref = fields.Char()
