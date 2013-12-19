from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    
    choices = ((0, 'None'), (1, 'Important'), (2, 'Critical'))
    
    name = models.CharField(max_length=2000)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(default=0, choices=choices)
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True, auto_now=True, db_index=True)
    
    def __unicode__(self):
        return '%s' % self.name
    
    def to_dict(self):
        
        due_date = ''
        
        if self.due_date:
            due_date = str(self.due_date).split(' ')[0]
        
        return {
                "id": self.id,
                "name": u'%s' % self.name,
                "completed": self.completed,
                "due_date": due_date,
                "priority": self.priority
                }
