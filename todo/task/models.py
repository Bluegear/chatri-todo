from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    
    choices = (('N', 'None'), ('I', 'Important'), ('C', 'Critical'))
    
    name = models.CharField(max_length=2000)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=1, choices=choices, default='N')
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True, auto_now=True, db_index=True)
    
    def __unicode__(self):
        return '%s' % self.name
