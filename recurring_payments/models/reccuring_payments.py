# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields, models,api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# class FilterRecurringEntries(models.Model):
#     _inherit = 'account.move'
#
#     recurring_ref = fields.Char()


class RecurringPayments(models.Model):
    _name = 'recurring.payments'
    _description = 'Recurring Payments'

    name = fields.Char(string='Name')
    pay_time = fields.Selection([('pay_now', 'Pay Now'),('pay_later','Pay Later')],string='Pay Time')
    credit_account = fields.Many2one('account.account', string='Credit Account')
    debit_account = fields.Many2one('account.account',string='Debit Account')
    journal = fields.Many2one('account.journal', string='Journals')
    recurring_period = fields.Selection ([('days', 'Days'), ('weeks', 'Weeks'),
                                           ('months', 'Months'),('years', 'Years'),],
                                          string='Recurring Period')
    recurring_interval = fields.Integer(string='Recurring Interval')
    starting_date = fields.Date(string='Starting Date')
    next_schedule = fields.Date(string='Next Schedule',readonly=True, compute='_compute_next_schedule',store=True)
    ending_date = fields.Date(string='Ending Date')
    amount = fields.Float(string='Amount')
    generate_journal = fields.Selection([('posted','Posted'),('unposted', 'Unposted')],
                                        string='Generate Journal As')
    state = fields.Selection([('draft','Draft'),('running','Running')],default='draft')
    description = fields.Text(string='Description')
    recurring_lines = fields.One2many('journal.entry.wizard', 'tmpl_id')

    @api.depends('starting_date','recurring_period','recurring_interval')
    def _compute_next_schedule(self):
        if self.starting_date:
            recurr_dates = []
            today = datetime.today()
            start_date = datetime.strptime(str(self.starting_date), '%Y-%m-%d')
            while start_date <= today:
                recurr_dates.append(str(start_date.date()))
                if self.recurring_period == 'days':
                    start_date += relativedelta(days=self.recurring_interval)
                elif self.recurring_period == 'weeks':
                    start_date += relativedelta(weeks=self.recurring_interval)
                elif self.recurring_period == 'months':
                    start_date += relativedelta(months=self.recurring_interval)
                else:
                    start_date += relativedelta(years=self.recurring_interval)
            self.next_schedule = start_date.date()
