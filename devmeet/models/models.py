# -*- coding: utf-8 -*-

from odoo import models, fields, api

import secrets
import logging
from odoo.exceptions import ValidationError
import re


# class devmeet(models.Model):
#     _name = 'devmeet.devmeet'
#     _description = 'devmeet.devmeet'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

_logger = logging.getLogger(__name__)
class developer(models.Model):
    _name = 'devmeet.developer'
    _description = 'devmeet.developer'

    name = fields.Char()
    surname = fields.Char()
    dni = fields.Char(string="dni")
    email = fields.Char(string="email")
    password = fields.Char(default=lambda p: secrets.token_urlsafe(12))
    photo = fields.Image(max_width=200,max_height=200)
    last_login = fields.Datetime(default= lambda d: fields.Datetime.now())
    technologies_known = fields.Many2many(comodel_name='devmeet.technology', relation='developers_technology', column1='developer_id', column2='technology_id')
    technologies_interest = fields.Many2many(comodel_name='devmeet.technology', relation='developers_technology_interested', column1='developer_id', column2='technology_id')
    events_assistant = fields.Many2many(comodel_name='devmeet.event', relation='developers_event', column1='developer_id', column2='event_id')
    events_speaker = fields.Many2many(comodel_name='devmeet.event', relation='developers_event_speak', column1='developer_id', column2='event_id')

    @api.constrains('dni')
    def _check_dni(self):
          regex = re.compile('[0-9]{8}[a-z]\Z', re.I)

          for student in self:
               if regex.match(student.dni):
                    _logger.info('correct DNI')
               else:
                    raise ValidationError("Incorrect format DNI")


    _sql_constraints = [('dni_uniq', 'unique(dni)', 'DNI can\'t be repeated')]

    @api.constrains('email')
    def _check_email(self):
        regex = re.compile('^\w+@\w+.\w+$', re.I)

        for developer in self:
            if regex.match(developer.email):
                _logger.info('Correct email')
            else:
                raise ValidationError("Incorrect format email")

    

class technonlogy(models.Model):
    _name = 'devmeet.technology'
    _description = 'devmeet.technology'

    name = fields.Char(string="name")
    official_page = fields.Char(default="https://www.google.com")
    logo = fields.Image(max_width=200,max_height=200)

    developers_know = fields.Many2many(comodel_name='devmeet.developer', relation='developers_technology', column1='technology_id', column2='developer_id')
    developers_interested = fields.Many2many(comodel_name='devmeet.developer', relation='developers_technology_interested', column1='technology_id', column2='developer_id')
    events = fields.Many2many(comodel_name='devmeet.event', relation='technology_event', column1='technology_id', column2='event_id')

    _sql_constraints = [('name_uniq', 'unique(name)', 'That technology already exists')]


class events(models.Model):
    _name = 'devmeet.event'
    _description = 'devmeet.event'

    name = fields.Char()
    start_date = fields.Date(string="start_date")
    end_date = fields.Date(string="end_date")
    attend = fields.Char() #check if the event is online

    assistants = fields.Many2many(comodel_name='devmeet.developer', relation='developers_event', column1='event_id', column2='developer_id')

    speakers = fields.Many2many(comodel_name='devmeet.developer', relation='developers_event_speak', column1='event_id', column2='developer_id')
    technologies = fields.Many2many(comodel_name='devmeet.technology', relation='technology_event', column1='event_id', column2='technology_id')

    classroom = fields.Many2one('devmeet.classroom', ondelete='set null', help='Classroom where the event takes place')

    _sql_constraints = [('check_date', 'check(start_date <= end_date)', 'Starting date can\'t be before the end date')]
    #_sql_constraints = [('check_date', 'check(start_date > getdate())', 'Starting date can\'t be before the end date')]



class classroom(models.Model):
    _name = 'devmeet.classroom'
    _description = 'devmeet.classroom'

    name = fields.Char()
    num_computers = fields.Integer()

    events = fields.One2many(comodel_name='devmeet.event', inverse_name='classroom')