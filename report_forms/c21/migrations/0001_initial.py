# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'c1OtherDiagnose'
        db.create_table('c1_c1otherdiagnose', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('c1', ['c1OtherDiagnose'])

        # Adding model 'c1'
        db.create_table('c1_c1', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('case_id', self.gf('django.db.models.fields.IntegerField')()),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('date_of_delivery', self.gf('django.db.models.fields.DateTimeField')()),
            ('number_of_prev_deliveries', self.gf('django.db.models.fields.IntegerField')()),
            ('number_of_prev_deliveries_by_c', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('the_c_section', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('weight_of_the_newborn', self.gf('django.db.models.fields.FloatField')()),
            ('mother_illness', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('specify_mother_illness', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('drg_code', self.gf('django.db.models.fields.CharField')(default='', max_length=4)),
            ('added_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('c1', ['c1'])

        # Adding M2M table for field other_diagnoses on 'c1'
        db.create_table('c1_c1_other_diagnoses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('c1', models.ForeignKey(orm['c1.c1'], null=False)),
            ('c1otherdiagnose', models.ForeignKey(orm['c1.c1otherdiagnose'], null=False))
        ))
        db.create_unique('c1_c1_other_diagnoses', ['c1_id', 'c1otherdiagnose_id'])


    def backwards(self, orm):
        # Deleting model 'c1OtherDiagnose'
        db.delete_table('c1_c1otherdiagnose')

        # Deleting model 'c1'
        db.delete_table('c1_c1')

        # Removing M2M table for field other_diagnoses on 'c1'
        db.delete_table('c1_c1_other_diagnoses')


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
        'c1.c1': {
            'Meta': {'object_name': 'c1'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'added_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'case_id': ('django.db.models.fields.IntegerField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'date_of_delivery': ('django.db.models.fields.DateTimeField', [], {}),
            'drg_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mother_illness': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'number_of_prev_deliveries': ('django.db.models.fields.IntegerField', [], {}),
            'number_of_prev_deliveries_by_c': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'other_diagnoses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['c1.c1OtherDiagnose']", 'null': 'True', 'blank': 'True'}),
            'patient_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'specify_mother_illness': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'the_c_section': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'weight_of_the_newborn': ('django.db.models.fields.FloatField', [], {})
        },
        'c1.c1otherdiagnose': {
            'Meta': {'object_name': 'c1OtherDiagnose'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['c1']