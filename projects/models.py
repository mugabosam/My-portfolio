from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.timezone import now


class Project(models.Model):
    PROJECT_TYPES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('ai', 'AI/ML'),
        ('data', 'Data Science'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    tags = models.CharField(max_length=200)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='web')
    demo_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='project_images/')
    featured = models.BooleanField(default=False)
    orders = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orders']

    def __str__(self):
        return self.title

class Skill(models.Model):
    SKILL_CATEGORIES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('design', 'Design'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    proficiency = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    author = models.CharField(max_length=100)
    author_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonial_images/', blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"Testimonial from {self.author}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    token = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.email

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='blog_images/', blank=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class Experience(models.Model):
    EXPERIENCE_TYPES = [
        ('job', 'Job'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
        ('education', 'Education'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-start_date', 'order']

    def __str__(self):
        return f"{self.title} at {self.company}"

class Certificate(models.Model):
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='certificates/', blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title