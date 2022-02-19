# -*- coding: utf-8 -*-

import secrets
#from odoo import _
#from odoo.exceptions import Warning
import logging
from odoo.exceptions import ValidationError
import re
from odoo import models, fields, api


_logger = logging.getLogger(__name__)
class student(models.Model):
     _name = 'school.student'
     _description = 'school.student'

     name = fields.Char()
     birth_year = fields.Integer()

     dni = fields.Char(string="DNI") #acompañado de la restriccion mas abajo


     #@api.depends('name') #esto es para que ocurriera cuando cambia name?
     #def _get_password(self):
     #     
     #     for student in self:
     #          password = secrets.token_urlsafe(12)
     #          #print('\033[94m', student, '\033[0m')
     #          #raise Warning(_('Se ha producido un Warning!'))
     #          _logger.debug('\033[94m', student, '\033[0m')
     #          return password

     #password computada
     #password = fields.Char(compute='_get_password', store=True)
     #password por defecto
     #password = fields.Char(default='1234')
     #password = fields.Char(default=_get_password)
     password = fields.Char(default=lambda p: secrets.token_urlsafe(12))

     description = fields.Text()
     #las fechas se ponen con el lambda por que asi ocurre cuando se vaya a crear el objeto
     #si pusiera lambda=fields.Date.today() me sacaria el dato en el momento de arrancar odoo
     Inscription_date = fields.Date(default= lambda d: fields.Date.today())
     last_login = fields.Datetime(default= lambda d: fields.Datetime.now())
     is_student = fields.Boolean()
     photo = fields.Image(max_width=200,max_height=200)

     classroom = fields.Many2one('school.classroom', ondelete='set null', help='Clase a la que pertenece') #muchos estudiantes en una clase

     #mostrar que profesores le dan clase sin generar una tabla
     teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)

     #el guion es porque es privado
     #le llega una lista, aunque sea de solo un elemento
     #@api.one permite que llegue solo un elemento
     

     @api.constrains('DNI')
     def _check_dni(self):
          regex = re.compile('[0-9]{8}[a-z]\Z', re.I)

          for student in self:
               if regex.match(student.dni):
                    _logger.info('DNI correcto')
               else:
                    raise ValidationError("Formato incorrecto en DNI")


     _sql_constraints = [('dni_uniq', 'unique(dni)', 'DNI can\'t be repeated')]

class classroom(models.Model):
     _name = 'school.classroom'
     _description = 'Las clases'

     name = fields.Char()
     #students = fields.One2many('school.student', 'classroom') #en una clase, muchos estudiantes
     students = fields.One2many(string='Alumnos', comodel_name='school.student', inverse_name='classroom')
     #teachers = fields.Many2many('school.teacher')
     teachers = fields.Many2many(comodel_name='school.teacher', relation='teachers_classroom', column1='classroom_id', column2='teacher_id')
     teachers_last_year = fields.Many2many(comodel_name='school.teacher', relation='teachers_classroom_ly', column1='classroom_id', column2='teacher_id')

     #un coordinator es un profesor, puede coordinar muchas clases
     coordinator = fields.Many2one('school.teacher', compute='_get_coordinator')

     all_teachers = fields.Many2many('school.teacher', compute='_get_allteachers')

     def _get_coordinator(self):
          for classroom in self: #self es una lista de classroom
               if len(classroom.teachers) > 0:
                    classroom.coordinator = classroom.teachers[0].id
               else:
                    classroom.coordinator = None

     def _get_allteachers(self):
          for classroom in self:
               classroom.all_teachers = classroom.teachers + classroom.teachers_last_year

class teacher(models.Model):
     _name = 'school.teacher'
     _description = 'Los profesores'

     name = fields.Char()
     #classrooms = fields.Many2many('school.classroom')
     classrooms = fields.Many2many(comodel_name='school.classroom', relation='teachers_classroom', column1='teacher_id', column2='classroom_id')
     classrooms_last_year = fields.Many2many(comodel_name='school.classroom', relation='teachers_classroom_ly', column1='teacher_id', column2='classroom_id')


#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
