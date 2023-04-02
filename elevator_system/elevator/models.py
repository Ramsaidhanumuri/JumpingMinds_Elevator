from django.db import models

class Elevator(models.Model):
    STATUS_CHOICES = [
        ('idle', 'Idle'),
        ('moving', 'Moving'),
        ('maintenance', 'Maintenance'),
    ]

    DIRECTION_CHOICES = [
        ('up', 'Up'),
        ('down', 'Down'),
        (None, 'None'),
    ]

    current_floor = models.IntegerField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES, null=True)
    top_target_floor = models.IntegerField()
    ground_target_floor = models.IntegerField(default=0)

class Request(models.Model):
    floor = models.IntegerField()
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
