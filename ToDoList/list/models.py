from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.

class List(models.Model):
    title = models.CharField(blank=False, null=False, max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
class Task(models.Model):
    title = models.CharField(blank=False, null=False, max_length=200)
    is_completed = models.BooleanField(default=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
class SubTask(models.Model):
    title = models.CharField(blank=False, null=False, max_length=200)
    is_completed = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
@receiver(post_save, sender=User)
def ensure_assigned_list(sender, instance, **kwargs):
    if kwargs.get('created', False):
        List.objects.get_or_create(user=instance, title="lista de {}".format(instance))

@receiver(post_save, sender=SubTask)
def complete_task_if_all_subtasks_completed(sender, instance, **kwargs):
    subtasks = SubTask.objects.filter(task_id=instance.task_id)
    if all(subtask.is_completed for subtask in subtasks):
        task = Task.objects.get(id=instance.task_id)
        if not task.is_completed:
            task.is_completed = True
            task.save()

@receiver(post_save, sender=Task)
def complete_subtasks_if_task_completed(sender, instance, **kwargs):
    if instance.is_completed:
        subtasks = SubTask.objects.filter(task_id=instance.id)
        for subtask in subtasks:
            if not subtask.is_completed:
                subtask.is_completed = True
                subtask.save()