# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'c20'
        db.create_table('c20_c20', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('case_id', self.gf('django.db.models.fields.IntegerField')()),
            ('hospital_registration_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('diagnosis_code', self.gf('django.db.models.fields.CharField')(default='', max_length=3)),
            ('type_of_unit', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('patient_allergic_aspirin', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('aspirin_intolerance', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('type_of_discharge', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('type_of_discharge_empty', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('aspirin_refusal', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('aspirin_at_discharge', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('non_aspirin_platelet', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('date_of_discharge', self.gf('django.db.models.fields.DateField')()),
            ('added_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('c20', ['c20'])


    def backwards(self, orm):
        # Deleting model 'c20'
        db.delete_table('c20_c20')


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
        'c20.c20': {
            'Meta': {'object_name': 'c20'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'added_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'aspirin_at_discharge': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'aspirin_intolerance': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'aspirin_refusal': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'case_id': ('django.db.models.fields.IntegerField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'date_of_discharge': ('django.db.models.fields.DateField', [], {}),
            'diagnosis_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3'}),
            'hospital_registration_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'non_aspirin_platelet': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'patient_allergic_aspirin': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'type_of_discharge': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'type_of_discharge_empty': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type_of_unit': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['c20']