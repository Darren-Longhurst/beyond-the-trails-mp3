from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse

STATUS = ((0, "Draft"), (1, "Published"))
LOCATIONS = (("KAW", "King Alfreds Way"), ("GNT", "Great North Trail"), ("MCW", "Marcher Castles Way"), ("TE", "Traws Eryri"), ("NDW", "North Downs Way"), ("RW", "Rebellion Way"), ("WKW", "West Kernow Way"), ("OTHER", "Other"))
WEATHER = ((0, "Sunny"), (1, "Overcast"), (2, "Rainy"), (3, "Snowy"), (4, "Windy"), (5, "Foggy"))
BIKE_CHOICES = ((0, "Hardtail"), (1, "Full Suspension"), (2, "Road Bike"), (3, "Hybrid Bike"), (4, "Electric Bike"), (5, "Gravel Bike"))

""" Model for blog posts """

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogging_posts', default=1)
    location = models.CharField(max_length=10, choices=LOCATIONS, default="OTHER")
    weather = models.IntegerField(choices=WEATHER, default=0)
    image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True, help_text='A short summary of the post')
    bike_choice = models.IntegerField(choices=BIKE_CHOICES, default=0)
    likes = models.ManyToManyField(User, related_name='blogging_likes', blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    # Location image mapping

    LOCATION_IMAGES = {
        "KAW": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450332/KAW_azhb8h.jpg",
        "GNT": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/GNT_hgmttq.jpg",
        "MCW": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/MCW_vccqz4.jpg",
        "TE": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/TE_dxmhjq.jpg",
        "NDW": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/NDW_trpocy.jpg",
        "RW": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/RW_j5smla.jpg",
        "WKW": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/WKW_gnmghj.jpg",
        "OTHER": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450332/OTHER_pics80.jpg",
    }

    @property
    def get_image_url(self):

        # Checks if the image is the default placeholder
        if "placeholder" in self.image.url:
            return self.LOCATION_IMAGES.get(self.location, self.LOCATION_IMAGES["OTHER"])
        else:
            return self.image.url

    class Meta:
        # Sets the default ordering to descending creation date
        ordering = ['-created_at']

    def __str__(self):
        # Returns the title of the post as its string representation
        return self.title

    def number_of_likes(self):
        # Returns the number of likes for the post
        return self.likes.count()
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

""" Model for comments associated with blog posts """

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        # Sets the default ordering to ascending creation date
        ordering = ['created_at']

    def __str__(self):
        # Returns a string representation of the comment
        return f'Comment by {self.author} on {self.post}'