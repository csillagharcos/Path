# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'c1.added_on'
        db.add_column('c1_c1', 'added_on',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 9, 8, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'c1.added_on'
        db.delete_column('c1_c1', 'added_on')


    models = {
        'c1.c1': {
            'Meta': {'object_name': 'c1'},
            'added_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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