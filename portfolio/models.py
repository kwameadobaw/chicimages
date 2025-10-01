from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Photo(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    orientation = models.CharField(max_length=20, choices=[('portrait', 'Portrait'), ('landscape', 'Landscape')], default='landscape')
    
    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        # If this is a new photo (no ID yet) or orientation not set, determine orientation
        if not self.orientation or not self.id:
            from PIL import Image
            img = Image.open(self.image)
            width, height = img.size
            self.orientation = 'portrait' if height > width else 'landscape'
        super().save(*args, **kwargs)

class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    features = models.TextField(help_text="Enter features separated by new lines")
    
    def __str__(self):
        return self.name
    
    def feature_list(self):
        return self.features.split('\n')

class Personality(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100, default="Photographer")
    short_description = models.TextField()
    full_description = models.TextField()
    featured_image = models.ImageField(upload_to='personalities/')
    date_added = models.DateTimeField(auto_now_add=True)
    orientation = models.CharField(max_length=20, choices=[('portrait', 'Portrait'), ('landscape', 'Landscape')], default='portrait')
    
    class Meta:
        verbose_name_plural = 'Personalities'
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        # If this is a new personality or orientation not set, determine orientation
        if not self.orientation or not self.id:
            from PIL import Image
            img = Image.open(self.featured_image)
            width, height = img.size
            self.orientation = 'portrait' if height > width else 'landscape'
        super().save(*args, **kwargs)

class PersonalityImage(models.Model):
    personality = models.ForeignKey(Personality, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='personalities/')
    caption = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Image for {self.personality.name}"
        
class Booking(models.Model):
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking by {self.name} on {self.date}"
