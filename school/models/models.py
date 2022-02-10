# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
     _name = 'school.student'
     _description = 'school.student'

     name = fields.Char()
     birth_year = fields.Integer()
     description = fields.Text()
     Inscription_date = fields.Date()
     last_login = fields.Datetime()
     is_student = fields.Boolean()
     photo = fields.Image(max_width=200,max_height=200)

     classroom = fields.Many2one('school.classroom') #muchos estudiantes en una clase

class classroom(models.Model):
     _name = 'school.classroom'
     _description = 'Las clases'

     name = fields.Char()
     students = fields.One2many('school.student', 'classroom') #en una clase, muchos estudiantes
     teachers = fields.Many2many('school.teacher', 'classroom')

class teacher(models.Model):
     _name = 'school.teacher'
     _description = 'Los profesores'

     name = fields.Char()
     classrooms = fields.Many2many('school.classroom', 'teacher')


#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
