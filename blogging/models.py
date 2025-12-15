from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))
WEATHER = ((0, "Sunny"), (1, "Overcast"), (2, "Rainy"), (3, "Snowy"), (4, "Windy"), (5, "Foggy"))
BIKE_CHOICES = ((0, "Hardtail"), (1, "Full Suspension"), (2, "Road Bike"), (3, "Hybrid Bike"), (4, "Electric Bike"), (5, "Gravel Bike"))

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogging_posts', default=1)
    location = models.CharField(max_length=50, default='Unknown')
    weather = models.IntegerField(choices=WEATHER, default=0)
    bike_choice = models.IntegerField(choices=BIKE_CHOICES, default=0)
    likes = models.ManyToManyField(User, related_name='blogging_likes', blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        # Sets the default ordering to descending creation date
        ordering = ['-created_at']

    def __str__(self):
        # Returns the title of the post as its string representation
        return self.title

    def number_of_likes(self):
        # Returns the number of likes for the post
        return self.likes.count()
