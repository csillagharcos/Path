# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'joblist'
        db.create_table('c13_joblist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_english', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('job_hungarian', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('c13', ['joblist'])

        # Adding model 'c13'
        db.create_table('c13_c13', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['c13.joblist'])),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=2012)),
            ('needlestick_injuries', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('staff_beginning', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('staff_end', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('working_hours_beginning', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('working_hours_end', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('added_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('c13', ['c13'])


    def backwards(self, orm):
        # Deleting model 'joblist'
        db.delete_table('c13_joblist')

        # Deleting model 'c13'
        db.delete_table('c13_c13')


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
        'c13.c13': {
            'Meta': {'object_name': 'c13'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'added_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['c13.joblist']"}),
            'needlestick_injuries': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'staff_beginning': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'staff_end': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'working_hours_beginning': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'working_hours_end': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2012'})
        },
        'c13.joblist': {
            'Meta': {'object_name': 'joblist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_english': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'job_hungarian': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['c13']