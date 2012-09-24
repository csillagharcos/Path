# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Medicine'
        db.create_table('c23_medicine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dose', self.gf('django.db.models.fields.FloatField')()),
            ('doseUnder', self.gf('django.db.models.fields.FloatField')()),
            ('doseAbove', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('c23', ['Medicine'])

        # Adding model 'c23'
        db.create_table('c23_c23', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('case_id', self.gf('django.db.models.fields.IntegerField')()),
            ('hospital_registration_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('weight_of_patient', self.gf('django.db.models.fields.IntegerField')()),
            ('principal_diagnoses_code', self.gf('django.db.models.fields.CharField')(default='', max_length=5)),
            ('principal_diagnoses_code_other', self.gf('django.db.models.fields.CharField')(default='', max_length=10, null=True, blank=True)),
            ('principal_procedure_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('procedure_planned', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('patient_allergy', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('generic_name_of_drug', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('penicilin_allergy', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('preoperative_infection', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('type_of_infection', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('surgical_incision', self.gf('django.db.models.fields.DateTimeField')()),
            ('antibiotic_given', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('name_of_first_dose', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='First Dose', null=True, to=orm['c23.Medicine'])),
            ('first_dose', self.gf('django.db.models.fields.FloatField')(max_length=10, null=True, blank=True)),
            ('name_of_second_dose', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Second Dose', null=True, to=orm['c23.Medicine'])),
            ('second_dose', self.gf('django.db.models.fields.FloatField')(max_length=10, null=True, blank=True)),
            ('name_of_other_dose', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('other_dose', self.gf('django.db.models.fields.FloatField')(max_length=10, null=True, blank=True)),
            ('route_of_admin', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1, null=True, blank=True)),
            ('date_of_first_dose', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('total_dose_in_24h', self.gf('django.db.models.fields.FloatField')(max_length=10, null=True, blank=True)),
            ('date_of_last_dose', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_of_wound_close', self.gf('django.db.models.fields.DateTimeField')()),
            ('added_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('c23', ['c23'])


    def backwards(self, orm):
        # Deleting model 'Medicine'
        db.delete_table('c23_medicine')

        # Deleting model 'c23'
        db.delete_table('c23_c23')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'c23.c23': {
            'Meta': {'object_name': 'c23'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'added_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'antibiotic_given': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'case_id': ('django.db.models.fields.IntegerField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'date_of_first_dose': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_last_dose': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_wound_close': ('django.db.models.fields.DateTimeField', [], {}),
            'first_dose': ('django.db.models.fields.FloatField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'generic_name_of_drug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'hospital_registration_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_of_first_dose': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'First Dose'", 'null': 'True', 'to': "orm['c23.Medicine']"}),
            'name_of_other_dose': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_of_second_dose': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Second Dose'", 'null': 'True', 'to': "orm['c23.Medicine']"}),
            'other_dose': ('django.db.models.fields.FloatField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'patient_allergy': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'penicilin_allergy': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'preoperative_infection': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'principal_diagnoses_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5'}),
            'principal_diagnoses_code_other': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'principal_procedure_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'procedure_planned': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'route_of_admin': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'second_dose': ('django.db.models.fields.FloatField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'surgical_incision': ('django.db.models.fields.DateTimeField', [], {}),
            'total_dose_in_24h': ('django.db.models.fields.FloatField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'type_of_infection': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'weight_of_patient': ('django.db.models.fields.IntegerField', [], {})
        },
        'c23.medicine': {
            'Meta': {'object_name': 'Medicine'},
            'dose': ('django.db.models.fields.FloatField', [], {}),
            'doseAbove': ('django.db.models.fields.FloatField', [], {}),
            'doseUnder': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['c23']