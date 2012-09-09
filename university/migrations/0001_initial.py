# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'School'
        db.create_table('university_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('university_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('university', ['School'])


    def backwards(self, orm):
        # Deleting model 'School'
        db.delete_table('university_school')


    models = {
        'university.school': {
            'Meta': {'object_name': 'School'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'university_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['university']