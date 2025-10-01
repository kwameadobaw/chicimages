from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Photo, Package, Booking, Personality, PersonalityImage

def home(request):
    """
    View for the home page of the photography portfolio website.
    Includes sections for hero banner, testimonials, services, and clients.
    """
    context = {
        'testimonials': [
            {
                'name': 'John Smith',
                'company': 'ABC Corporation',
                'text': 'Chic Images delivered exceptional photography for our corporate event. The team was professional and captured every important moment beautifully.',
                'image': 'client1.jpg',
            },
            {
                'name': 'Sarah Johnson',
                'company': 'Fashion Magazine',
                'text': 'Working with Chic Images was a pleasure. Their attention to detail and creative vision brought our fashion shoot to life.',
                'image': 'client2.jpg',
            },
            {
                'name': 'Michael Brown',
                'company': 'Wedding Planner',
                'text': 'I recommend Chic Images to all my clients. They capture the emotion and beauty of weddings like no other photographer I\'ve worked with.',
                'image': 'client3.jpg',
            },
        ],
        'services': [
            {
                'title': 'Wedding Photography',
                'description': 'Capture your special day with our professional wedding photography services. We focus on candid moments and beautiful compositions.',
                'icon': 'camera-wedding',
            },
            {
                'title': 'Portrait Sessions',
                'description': 'Professional portrait photography for individuals, families, and corporate headshots with attention to lighting and detail.',
                'icon': 'camera-portrait',
            },
            {
                'title': 'Commercial Photography',
                'description': 'High-quality commercial photography for products, real estate, and corporate events to showcase your business.',
                'icon': 'camera-commercial',
            },
            {
                'title': 'Event Coverage',
                'description': 'Comprehensive coverage of special events, conferences, and celebrations with quick turnaround times.',
                'icon': 'camera-event',
            },
        ],
        'clients': [
            {'name': 'ABC Corporation', 'logo': 'logo1.png'},
            {'name': 'XYZ Industries', 'logo': 'logo2.png'},
            {'name': 'Fashion Magazine', 'logo': 'logo3.png'},
            {'name': 'Luxury Hotels', 'logo': 'logo4.png'},
            {'name': 'Wedding Planners Inc', 'logo': 'logo5.png'},
            {'name': 'Tech Innovators', 'logo': 'logo6.png'},
        ]
    }
    return render(request, 'home.html', context)

def about(request):
    # Sample data for team members
    team_members = [
        {
            'name': 'Sarah Johnson',
            'role': 'Lead Photographer',
            'bio': 'With over 10 years of experience, Sarah specializes in wedding and portrait photography. Her work has been featured in several photography magazines.',
            'image': 'team1.jpg'
        },
        {
            'name': 'David Chen',
            'role': 'Creative Director',
            'bio': 'David brings his artistic vision to every project, ensuring that each photo tells a unique story. He has a background in fine arts and commercial photography.',
            'image': 'team2.jpg'
        },
        {
            'name': 'Emily Rodriguez',
            'role': 'Event Photographer',
            'bio': 'Emily has a talent for capturing candid moments at events. Her energetic approach ensures no special moment goes unnoticed.',
            'image': 'team3.jpg'
        }
    ]
    
    # About us content
    about_content = {
        'main_heading': 'About Chic Images',
        'subheading': 'Capturing Moments, Creating Memories',
        'history': 'Founded in 2010, Chic Images has been providing exceptional photography services for over a decade. What started as a small studio has grown into a team of passionate photographers dedicated to capturing life\'s most precious moments.',
        'mission': 'Our mission is to create timeless photographs that tell your unique story. We believe that every moment deserves to be preserved with artistry and attention to detail.',
        'approach': 'We take a personalized approach to every project, working closely with our clients to understand their vision and deliver results that exceed expectations. Our team combines technical expertise with creative vision to produce stunning imagery.'
    }
    
    # Awards and recognition
    awards = [
        'Best Wedding Photography Studio 2022 - Local Business Awards',
        'Top 10 Portrait Photographers 2021 - Photography Magazine',
        'Excellence in Customer Service 2020 - Consumer Choice Awards',
        'Featured in Modern Photography Annual Collection 2019'
    ]
    
    context = {
        'team_members': team_members,
        'about_content': about_content,
        'awards': awards
    }
    
    return render(request, 'about.html', context)

def portfolio(request, category_slug=None):
    categories = Category.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        photos = Photo.objects.filter(category=category)
    else:
        category = None
        photos = Photo.objects.all()
    
    context = {
        'categories': categories,
        'category': category,
        'photos': photos
    }
    
    return render(request, 'portfolio.html', context)

def booking(request):
    packages = Package.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        package_id = request.POST.get('package')
        message = request.POST.get('message')
        session_type = request.POST.get('sessionType')
        
        package = get_object_or_404(Package, id=package_id)
        
        # Create booking object
        booking = Booking(
            name=name,
            email=email,
            phone=phone,
            date=date,
            time=time,
            package=package,
            message=message
        )
        booking.save()
        
        # Add success message
        messages.success(request, "Your booking has been received! We'll contact you shortly to confirm your appointment.")
        
        # Redirect to success page
        return redirect('booking_success')
    
    context = {
        'packages': packages
    }
    
    return render(request, 'booking.html', context)

def booking_success(request):
    return render(request, 'booking_success.html')

def personalities(request):
    personalities = Personality.objects.all().order_by('-date_added')
    
    context = {
        'personalities': personalities
    }
    
    return render(request, 'personalities.html', context)

def personality_detail(request, slug):
    personality = get_object_or_404(Personality, slug=slug)
    images = personality.images.all()
    
    context = {
        'personality': personality,
        'images': images
    }
    
    return render(request, 'personality_detail.html', context)
