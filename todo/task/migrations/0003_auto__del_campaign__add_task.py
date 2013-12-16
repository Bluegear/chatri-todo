# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Campaign'
        db.delete_table(u'task_campaign')

        # Adding model 'Task'
        db.create_table(u'task_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('priority', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'task', ['Task'])


    def backwards(self, orm):
        # Adding model 'Campaign'
        db.create_table(u'task_campaign', (
            ('priority', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True, db_index=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'task', ['Campaign'])

        # Deleting model 'Task'
        db.delete_table(u'task_task')


    models = {
        u'task.task': {
            'Meta': {'object_name': 'Task'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['task']