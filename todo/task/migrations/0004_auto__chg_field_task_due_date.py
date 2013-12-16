# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Task.due_date'
        db.alter_column(u'task_task', 'due_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Task.due_date'
        raise RuntimeError("Cannot reverse this migration. 'Task.due_date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Task.due_date'
        db.alter_column(u'task_task', 'due_date', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'task.task': {
            'Meta': {'object_name': 'Task'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['task']