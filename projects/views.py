from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from projects.forms import ContactForm

from django.shortcuts import render
from .models import Project, Skill, Testimonial, BlogPost, Experience, Certificate


def home(request):
    # Featured projects (limit to 6)
    featured_projects = Project.objects.filter(featured=True)[:6]

    # All projects for the projects page
    all_projects = Project.objects.all()

    # Skills categorized
    frontend_skills = Skill.objects.filter(category='frontend').order_by('-proficiency')
    backend_skills = Skill.objects.filter(category='backend').order_by('-proficiency')
    other_skills = Skill.objects.filter(category='other').order_by('-proficiency')

    # Testimonials (limit to 3 featured ones)
    testimonials = Testimonial.objects.filter(featured=True).order_by('-created_at')[:3]

    # Latest blog posts (limit to 3)
    latest_posts = BlogPost.objects.filter(published=True).order_by('-published_at')[:3]

    # Professional experience
    work_experience = Experience.objects.filter(experience_type__in=['job', 'freelance']).order_by('-start_date')
    education = Experience.objects.filter(experience_type='education').order_by('-start_date')

    # Certifications
    certifications = Certificate.objects.filter(featured=True).order_by('-issue_date')

    context = {
        'featured_projects': featured_projects,
        'all_projects': all_projects,
        'frontend_skills': frontend_skills,
        'backend_skills': backend_skills,
        'other_skills': other_skills,
        'testimonials': testimonials,
        'latest_posts': latest_posts,
        'work_experience': work_experience,
        'education': education,
        'certifications': certifications,
    }

    return render(request, 'index.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                'Portfolio Contact - ' + form.cleaned_data['name'],
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                ['popesir112@gmail.com'],
            )
            return JsonResponse({'success': True})
        return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Subscriber
from .forms import SubscribeForm
import uuid


@require_POST
def subscribe_view(request):
    form = SubscribeForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        name = form.cleaned_data.get('name', '')

        # Generate unique token
        token = str(uuid.uuid4())

        # Create or update subscriber
        subscriber, created = Subscriber.objects.update_or_create(
            email=email,
            defaults={
                'name': name,
                'token': token,
                'active': True
            }
        )

        return JsonResponse({
            'success': True,
            'message': 'Thank you for subscribing!'
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)