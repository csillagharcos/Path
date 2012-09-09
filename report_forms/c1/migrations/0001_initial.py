# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'c1'
        db.create_table('c1_c1', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient_id', self.gf('django.db.models.fields.IntegerField')()),
            ('case_id', self.gf('django.db.models.fields.IntegerField')()),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('date_of_delivery', self.gf('django.db.models.fields.DateTimeField')()),
            ('number_of_prev_deliveries', self.gf('django.db.models.fields.IntegerField')()),
            ('number_of_prev_deliveries_by_c', self.gf('django.db.models.fields.IntegerField')()),
            ('the_c_section', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('weight_of_the_newborn', self.gf('django.db.models.fields.FloatField')()),
            ('mother_illness', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('specify_mother_illness', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('drg_code', self.gf('django.db.models.fields.CharField')(default='', max_length=4)),
            ('other_diagnoses', self.gf('django.db.models.fields.CharField')(default='', max_length=5)),
        ))
        db.send_create_signal('c1', ['c1'])


    def backwards(self, orm):
        # Deleting model 'c1'
        db.delete_table('c1_c1')


    models = {
        'c1.c1': {
            'Meta': {'object_name': 'c1'},
            'case_id': ('django.db.models.fields.IntegerField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'date_of_delivery': ('django.db.models.fields.DateTimeField', [], {}),
            'drg_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mother_illness': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'number_of_prev_deliveries': ('django.db.models.fields.IntegerField', [], {}),
            'number_of_prev_deliveries_by_c': ('django.db.models.fields.IntegerField', [], {}),
            'other_diagnoses': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5'}),
            'patient_id': ('django.db.models.fields.IntegerField', [], {}),
            'specify_mother_illness': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'the_c_section': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'weight_of_the_newborn': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['c1']