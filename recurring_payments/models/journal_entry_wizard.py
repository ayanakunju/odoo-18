# -*- coding: utf-8 -*-

from odoo import fields, models, api, Command
from dateutil.relativedelta import relativedelta


class JournalEntryWizard(models.TransientModel):
    _name = 'journal.entry.wizard'
    _description = 'Journal Entry Wizard'

    starting_date = fields.Date(string='Starting Date', required=True)
    ending_date = fields.Date(string='Ending Date', required=True)
    recurring_lines = fields.One2many('wizard.order.lines', 'tmpl_id',
                                      compute='_compute_order_lines', store=True)


    @api.depends('starting_date', 'ending_date')
    def _compute_order_lines(self):
        """Generate recurring lines when dates are changed"""
        if self.starting_date and self.ending_date:
            recurring_templates = self.env['recurring.payments'].search([
                ('state', '=', 'running')
            ])
            recurring_lines = []
            for template in recurring_templates:
                current_date = template.next_schedule
                while current_date and current_date <= self.ending_date:
                    if current_date >= self.starting_date:
                        recurring_lines.append(Command.create({
                            'starting_date': current_date,
                            'template_name': template.name,
                            'amount': template.amount,
                            'template_id': template.id
                        }))

                    if template.recurring_period == 'days':
                        current_date += relativedelta(days=template.recurring_interval)
                    elif template.recurring_period == 'weeks':
                        current_date += relativedelta(weeks=template.recurring_interval)
                    elif template.recurring_period == 'months':
                        current_date += relativedelta(months=template.recurring_interval)
                    else:
                        current_date += relativedelta(years=template.recurring_interval)

                    if template.ending_date and current_date > template.ending_date:
                        break

            self.recurring_lines = recurring_lines

    def action_generate_entry(self):
        """Generate journal entries for selected recurring lines"""
        for line in self.recurring_lines:
            template = line.template_id
            print(template)

            # Create journal entry
            move_vals = {
                'date': line.starting_date,
                'journal_id': template.journal.id,
                'ref': f'{template.name}',
                'line_ids': [
                    Command.create({
                        'account_id': template.debit_account.id,
                        'debit': line.amount,
                        'credit': 0.0,
                        'name': template.name,
                    }),
                    Command.create({
                        'account_id': template.credit_account.id,
                        'debit': 0.0,
                        'credit': line.amount,
                        'name': template.name,
                    })
                ]
            }

            move = self.env['account.move'].create(move_vals)
            if template.generate_journal == 'posted':
                move.action_post()
            template._compute_next_schedule()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Journal entries have been generated successfully',
                'next': {'type': 'ir.actions.act_window_close'},
                'type': 'success'
            }
        }
