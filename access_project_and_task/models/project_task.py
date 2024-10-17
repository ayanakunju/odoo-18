# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectTask(models.Model):
    """ To give access for the Tasks """
    _inherit = "project.task"

    task_access_user_ids = fields.Many2many('res.users', string='Access Limited Users')
    user_admin = fields.Boolean(compute='_compute_user',
                                help="To check if the user is an Internal user or not")

    def _compute_user(self):
        for rec in self:
            if rec.env.user.id == rec.env.ref('base.user_admin').id:
                rec.user_admin = True
            else:
                rec.user_admin = False
