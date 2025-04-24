from cProfile import Profile
from tokenize import Comment

from django.contrib import admin
from . models import *

admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Testimonial)
admin.site.register(Subscriber)
admin.site.register(BlogPost)
admin.site.register(ContactMessage)
admin.site.register(Experience)
admin.site.register(Certificate)
