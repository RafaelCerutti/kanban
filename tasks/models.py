from django.db import models
from django.contrib.auth.models import User
import uuid
 

class Board(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,editable=False)
    title = models.CharField(max_length=200, blank=False,null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Status(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    title = models.CharField(max_length=200,blank=False,null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='statuses')

    def __str__(self):
        return self.title
    

class Card(models.Model):
    TASK_CLASSIFICATION = {
         'bug':'Bug',
         'melhoria':'Melhoria',
         'tarefa':'Tarefa',
         'administrativa':'Administrativa',
    }
    
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    title = models.CharField(max_length=200,blank=False, null=False)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,related_name='cards') 
    board = models.ForeignKey(Board, on_delete=models.CASCADE,related_name='cards')
    classification = models.CharField(max_length=30, choices=TASK_CLASSIFICATION)
    responsible = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}, {self.responsible}'