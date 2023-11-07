from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class Election(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('completed', 'Completed')])
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='candidates/', null=True, blank=True)
    description = models.TextField()
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    votes = models.PositiveIntegerField(default=0)  # Add a field to track votes

    def __str__(self):
        return self.name

from django.contrib.auth.models import User
from .models import Candidate

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} voted for {self.candidate.name}"




class BlockchainCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    code = models.CharField(max_length=64)  # Assuming the blockchain code is a 64-character hash
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blockchain Code: {self.code} for Vote by {self.user.username} on {self.timestamp}"
    

@receiver(post_delete, sender=Vote)
def update_candidate_vote_count(sender, instance, **kwargs):
    # Update the associated candidate's vote count when a vote is deleted
    instance.candidate.votes -= 1
    instance.candidate.save()