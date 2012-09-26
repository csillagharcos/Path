# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'r1.if_unplanned'
        db.add_column('r1_r1', 'if_unplanned',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'r1.if_unplanned'
        db.delete_column('r1_r1', 'if_unplanned')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'r1.r1': {
            'AI_applied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'AI_applied_discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'AI_date_of_assess': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'AI_date_of_assess_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'AI_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'AI_score_discharge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'BI_applied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'BI_applied_discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'BI_date_of_assess': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'BI_date_of_assess_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'BI_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'BI_score_discharge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'FEV_applied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'FEV_applied_discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'FEV_date_of_assess': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'FEV_date_of_assess_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'FEV_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'FEV_score_discharge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'FIM_applied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'FIM_applied_discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'FIM_date_of_assess': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'FIM_date_of_assess_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'FIM_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'FIM_score_discharge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'r1'},
            'Other_applied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'Other_applied_discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'Other_date_of_assess': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'Other_date_of_assess_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'Other_name_of': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'Other_name_of_discharge': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'Other_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Other_score_discharge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'SAT_applied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'SAT_applied_discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'SAT_date_of_assess': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SAT_date_of_assess_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SAT_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'SAT_score_discharge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'SCI_applied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'SCI_applied_discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'SCI_date_of_assess': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SCI_date_of_assess_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SCI_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'SCI_score_discharge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'SF_applied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'SF_applied_discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'SF_date_of_assess': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SF_date_of_assess_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SF_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'SF_score_discharge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'SMWT_applied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'SMWT_applied_discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'SMWT_date_of_assess': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SMWT_date_of_assess_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SMWT_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'SMWT_score_discharge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'SNC_applied': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'SNC_applied_discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'SNC_date_of_assess': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SNC_date_of_assess_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SNC_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'SNC_score_discharge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'added_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'case_id': ('django.db.models.fields.IntegerField', [], {}),
            'date_of_admission': ('django.db.models.fields.DateField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'date_of_discharge': ('django.db.models.fields.DateField', [], {}),
            'discharge': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'field_of_rehab': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'field_of_rehab_other': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'if_unplanned': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'patient_discharge_status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'patient_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['r1']