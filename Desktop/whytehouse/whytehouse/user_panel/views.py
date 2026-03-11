from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from admin_panel.models import TravelPackage, Property, Inquiry, Lead, Blog, Destination
from admin_panel.models import Feedback,BlogCategory,Property
from django.shortcuts import render, get_object_or_404
from admin_panel.models import Blog


def enquire_now(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full_name', '').strip()
            mobile_number = request.POST.get('mobile_number', '').strip()
            email = request.POST.get('email', '').strip()
            place = request.POST.get('place', '').strip()
            message = request.POST.get('message', '').strip()
            enquiry_type = request.POST.get('enquiry_type', 'General')
            
            if not full_name or not mobile_number:
                return JsonResponse({'success': False, 'error': 'Name and mobile number are required'})
            
            # Create Customer record
            from admin_panel.models import Customer
            
            # Split name into first and last
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            # Check if customer already exists with this phone number
            customer, created = Customer.objects.get_or_create(
                contact_number=mobile_number,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'display_name': full_name,
                    'whatsapp_number': mobile_number,
                    'same_as_whatsapp': True,
                    'customer_type': 'Individual',
                    'place': place if place else ''
                }
            )
            
            # Create lead with enquiry type based on page
            Lead.objects.create(
                full_name=full_name,
                mobile_number=mobile_number,
                place=place,
                source='Enquire Now',
                enquiry_type=enquiry_type,
                remarks=f'Email: {email}\nMessage: {message}'
            )
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def index(request):
    packages = TravelPackage.objects.filter(active=True, category='International')[:6]
    
    # Get selected destination from URL parameter
    selected_dest_id = request.GET.get('dest')
    
    # Get international destinations for side tabs (limited to 3, only popular)
    side_tab_destinations = Destination.objects.filter(
        category='International',
        is_popular=True,
        packages__active=True
    ).distinct().order_by('name')[:3]
    
    # Get international destinations for filter tabs (limited to 4, only popular)
    filter_destinations = Destination.objects.filter(
        category='International',
        is_popular=True,
        packages__active=True
    ).distinct().order_by('name')[:4]
    
    # Build destination data with ALL packages for each destination
    destination_data = []
    for dest in filter_destinations:
        packages_list = TravelPackage.objects.filter(active=True, destination=dest)
        destination_data.append({
            'destination': dest,
            'packages': packages_list
        })
    
    # Get all package IDs already shown in destination sections
    shown_package_ids = []
    for data in destination_data:
        shown_package_ids.extend([pkg.id for pkg in data['packages']])
    
    # Get 4 featured packages for the gallery section, excluding already shown ones
    featured_packages = list(TravelPackage.objects.filter(
        active=True, 
        category='International'
    ).exclude(id__in=shown_package_ids)[:4])
    
    # If we don't have 4 unique packages, fill with any available packages
    if len(featured_packages) < 4:
        additional_packages = list(TravelPackage.objects.filter(
            active=True, 
            category='International'
        )[:4])
        featured_packages = additional_packages
    
    # fetch testimonials that have been marked featured
    featured_feedbacks = Feedback.objects.filter(featured=True).order_by('-created_at')[:6]
    
    context = {
        'packages': packages,
        'featured_packages': featured_packages,
        'side_tab_destinations': side_tab_destinations,
        'filter_destinations': filter_destinations,
        'destination_data': destination_data,
        'featured_feedbacks': featured_feedbacks,
        'selected_dest_id': int(selected_dest_id) if selected_dest_id else None,
    }
    
    return render(request, 'user/international.html', context)
def domestic(request):
    packages = TravelPackage.objects.filter(active=True, category='Domestic')[:6]
    
    # Get domestic destinations for the explorer section
    domestic_destinations = Destination.objects.filter(category='Domestic').order_by('name')[:4]
    
    # Get featured package for each destination (Kozhikode, Munnar, Wayanad, Ooty)
    kozhikode_package = TravelPackage.objects.filter(active=True, category='Domestic', destination__name__icontains='Kozhikode').first()
    munnar_package = TravelPackage.objects.filter(active=True, category='Domestic', destination__name__icontains='Munnar').first()
    wayanad_package = TravelPackage.objects.filter(active=True, category='Domestic', destination__name__icontains='Wayanad').first()
    ooty_package = TravelPackage.objects.filter(active=True, category='Domestic', destination__name__icontains='Ooty').first()
    
    # Get ALL domestic destinations for gallery (show 3 at a time with navigation)
    gallery_destinations = Destination.objects.filter(category='Domestic').order_by('name')
    
    # Get all properties for hospitality section (show 3 at a time)
    properties = Property.objects.all()
    
    context = {
        'packages': packages,
        'domestic_destinations': domestic_destinations,
        'gallery_destinations': gallery_destinations,
        'properties': properties,
        'kozhikode_package': kozhikode_package,
        'munnar_package': munnar_package,
        'wayanad_package': wayanad_package,
        'ooty_package': ooty_package,
    }
    
    return render(request, 'user/domestic.html', context)


def about(request):
    return render(request, 'user/about.html')






def blog_list(request):
    from admin_panel.models import BlogCategory
    
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    
    blogs = Blog.objects.filter(status="published").order_by("-publish_date")

    if q:
        blogs = blogs.filter(title__icontains=q)
    
    if category:
        blogs = blogs.filter(category=category)

    for b in blogs:
        raw = getattr(b, "tags", "") or getattr(b, "hashtags", "") or getattr(b, "hashtag", "") or ""
        b.tag_list = [t.strip() for t in str(raw).split(",") if t.strip()]
    
    all_count = Blog.objects.filter(status="published").count()
    categories = [(cat.slug, cat.name) for cat in BlogCategory.objects.filter(is_active=True).order_by('order', 'name')]
    category_counts = {cat[0]: Blog.objects.filter(status="published", category=cat[0]).count() for cat in categories}

    return render(request, "user/blog.html", {
        "blogs": blogs, 
        "q": q,
        "selected_category": category,
        "all_count": all_count,
        "category_counts": category_counts,
        "categories": categories
    })


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status="published")
    raw = getattr(blog, "tags", "") or getattr(blog, "hashtags", "") or getattr(blog, "hashtag", "") or ""
    tags = [t.strip() for t in str(raw).split(",") if t.strip()]

    # Replace {{image1}}, {{image2}}, etc. with actual image HTML
    content = blog.content
    content_images = blog.images.all()
    
    # Normalize line endings and split content
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Split by lines and process
    lines = content.split('\n')
    processed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # Check if this line contains an image tag
        has_image = False
        
        for idx, img in enumerate(content_images):
            image_num = idx + 1
            
            # Check for left positioned image
            placeholder_left = f"{{{{image{image_num}-left}}}}"
            if placeholder_left in line:
                # Get the text before the image tag (could be on same line or previous lines)
                text_content = line.replace(placeholder_left, '').strip()
                
                # If no text on this line, look at previous non-empty lines
                if not text_content and processed_lines:
                    # Get previous paragraph
                    prev_content = []
                    while processed_lines and not processed_lines[-1].startswith('<'):
                        prev_content.insert(0, processed_lines.pop())
                    text_content = ' '.join(prev_content)
                
                # Create side-by-side layout with image on left
                processed_lines.append(f'''
                    <div class="content-row">
                        <figure class="content-image-left">
                            <img src="{img.image.url}" alt="Content image {image_num}">
                        </figure>
                        <div class="content-text"><p>{text_content}</p></div>
                    </div>
                ''')
                has_image = True
                break
            
            # Check for right positioned image
            placeholder_right = f"{{{{image{image_num}-right}}}}"
            if placeholder_right in line:
                # Get the text before the image tag
                text_content = line.replace(placeholder_right, '').strip()
                
                # If no text on this line, look at previous non-empty lines
                if not text_content and processed_lines:
                    # Get previous paragraph
                    prev_content = []
                    while processed_lines and not processed_lines[-1].startswith('<'):
                        prev_content.insert(0, processed_lines.pop())
                    text_content = ' '.join(prev_content)
                
                # Create side-by-side layout with image on right
                processed_lines.append(f'''
                    <div class="content-row">
                        <div class="content-text"><p>{text_content}</p></div>
                        <figure class="content-image-right">
                            <img src="{img.image.url}" alt="Content image {image_num}">
                        </figure>
                    </div>
                ''')
                has_image = True
                break
            
            # Check for center positioned image
            placeholder_center = f"{{{{image{image_num}-center}}}}"
            if placeholder_center in line:
                text_content = line.replace(placeholder_center, '').strip()
                if text_content:
                    processed_lines.append(f'<p>{text_content}</p>')
                processed_lines.append(f'''
                    <figure class="content-image-center">
                        <img src="{img.image.url}" alt="Content image {image_num}">
                    </figure>
                ''')
                has_image = True
                break
            
            # Check for default (center) positioned image
            placeholder_default = f"{{{{image{image_num}}}}}"
            if placeholder_default in line:
                text_content = line.replace(placeholder_default, '').strip()
                if text_content:
                    processed_lines.append(f'<p>{text_content}</p>')
                processed_lines.append(f'''
                    <figure class="content-image-center">
                        <img src="{img.image.url}" alt="Content image {image_num}">
                    </figure>
                ''')
                has_image = True
                break
        
        # If no image found in this line, add it as regular text
        if not has_image and line:
            processed_lines.append(line)
        
        i += 1
    
    content = '\n'.join(processed_lines)

    return render(request, "user/blog_detail.html", {"blog": blog, "tags": tags, "processed_content": content})
def contact(request):
    if request.method == 'POST':
        import re
        
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        package = (request.POST.get('package') or '').strip()
        message = (request.POST.get('message') or '').strip()
        source_page = (request.POST.get('source_page') or 'General').strip()

        # Validation
        errors = []
        
        # Name validation
        if not name or len(name) < 2:
            errors.append('Name is required and must be at least 2 characters.')
        
        # Email validation
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not email or not re.match(email_pattern, email):
            errors.append('Please enter a valid email address.')
        
        # Phone validation (international format: 10-15 digits with optional +, -, spaces, parentheses)
        phone_pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'
        phone_digits = re.sub(r'\D', '', phone)  # Extract only digits
        
        if not phone:
            errors.append('Phone number is required.')
        elif len(phone_digits) < 10:
            errors.append('Phone number must be at least 10 digits.')
        elif not re.match(phone_pattern, phone):
            errors.append('Please enter a valid phone number.')
        
        # Message validation
        if not message or len(message) < 10:
            errors.append('Message is required and must be at least 10 characters.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('user_panel:contact')

        # Create Customer record
        from admin_panel.models import Customer
        
        # Split name into first and last
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Check if customer already exists with this phone number
        customer, created = Customer.objects.get_or_create(
            contact_number=phone,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'display_name': name,
                'whatsapp_number': phone,
                'same_as_whatsapp': True,
                'customer_type': 'Individual',
                'place': ''
            }
        )

        # ✅ 1) Find existing lead by phone (or create new)
        lead = Lead.objects.filter(mobile_number=phone).first()

        if lead:
            # Update basic info if needed (optional)
            if lead.full_name != name:
                lead.full_name = name
            # Keep latest message in remarks (optional)
            lead.remarks = (lead.remarks or "") + f"\n\n[{package or 'General Inquiry'}] {email}: {message}"
            lead.source = 'Website'
            lead.enquiry_type = source_page  # Set enquiry type based on source page
            lead.save()
        else:
            lead = Lead.objects.create(
                full_name=name,
                mobile_number=phone,
                place=None,
                source='Website',
                enquiry_type=source_page,  # Set enquiry type based on source page
                remarks=f"Email: {email}\nPackage: {package or 'General Inquiry'}\nMessage: {message}"
            )

        # ✅ 2) Create inquiry AND link it to lead
        Inquiry.objects.create(
            lead=lead,
            name=name,
            email=email,
            phone=phone,
            package=package or 'General Inquiry',
            message=message,
            status='New'
        )

        messages.success(request, 'Thank you! Your inquiry has been submitted successfully.')
        return redirect('user_panel:contact')

    return render(request, 'user/contact.html')

def packages(request):
    country = request.GET.get('country', 'all')
    search_query = request.GET.get('search', '').strip()
    
    # Filter packages
    if country == 'all':
        all_packages = TravelPackage.objects.filter(active=True)
    else:
        all_packages = TravelPackage.objects.filter(active=True, country__iexact=country)
    
    # Apply search filter
    if search_query:
        all_packages = all_packages.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
    
    return render(request, 'user/packages.html', {
        'packages': all_packages, 
        'selected_country': country,
        'search_query': search_query
    })

def domestic_packages(request):
    destination_id = request.GET.get('dest')
    search_query = request.GET.get('search', '').strip()
    
    # Get all domestic destinations
    destinations = Destination.objects.filter(category='Domestic').order_by('name')
    
    # Filter packages
    packages = TravelPackage.objects.filter(active=True, category='Domestic')
    
    # Apply search filter
    if search_query:
        packages = packages.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
    
    # Apply destination filter
    if destination_id:
        packages = packages.filter(destination_id=destination_id)
    
    packages = packages.order_by('-created_at')
    
    # Get selected destination object
    selected_destination = None
    if destination_id:
        try:
            selected_destination = Destination.objects.get(id=destination_id)
        except Destination.DoesNotExist:
            pass
    
    context = {
        'packages': packages,
        'destinations': destinations,
        'selected_destination': int(destination_id) if destination_id else None,
        'selected_destination_obj': selected_destination,
        'category': 'Domestic',
        'search_query': search_query
    }
    return render(request, 'user/packages.html', context)

def international_packages(request):
    destination_id = request.GET.get('dest')
    search_query = request.GET.get('search', '').strip()
    
    # Get all international destinations
    destinations = Destination.objects.filter(category='International').order_by('name')
    
    # Filter packages
    packages = TravelPackage.objects.filter(active=True, category='International')
    
    # Apply search filter
    if search_query:
        packages = packages.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
    
    # Apply destination filter
    if destination_id:
        packages = packages.filter(destination_id=destination_id)
    
    packages = packages.order_by('-created_at')
    
    # Get selected destination object
    selected_destination = None
    if destination_id:
        try:
            selected_destination = Destination.objects.get(id=destination_id)
        except Destination.DoesNotExist:
            pass
    
    context = {
        'packages': packages,
        'destinations': destinations,
        'selected_destination': int(destination_id) if destination_id else None,
        'selected_destination_obj': selected_destination,
        'category': 'International',
        'search_query': search_query
    }
    return render(request, 'user/packages.html', context)

def package_detail(request, slug):
    from datetime import datetime
    package = get_object_or_404(TravelPackage, id=slug, active=True)
    
    if request.method == 'POST':
        import re
        from admin_panel.models import Customer
        
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        guests = request.POST.get('guests', '1').strip()
        start_date = request.POST.get('start_date', '').strip()
        
        # Validation
        errors = []
        
        # Name validation
        if not name or len(name) < 2:
            errors.append('Name is required and must be at least 2 characters.')
        
        # Email validation
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not email or not re.match(email_pattern, email):
            errors.append('Please enter a valid email address.')
        
        # Phone validation (exactly 10 digits)
        phone_digits = re.sub(r'\D', '', phone)
        
        if not phone:
            errors.append('Phone number is required.')
        elif len(phone_digits) != 10:
            errors.append('Phone number must be exactly 10 digits.')
        elif not phone_digits.isdigit():
            errors.append('Phone number must contain only digits.')
        
        # Guests validation
        try:
            guests_int = int(guests)
            if guests_int < 1:
                errors.append('Number of guests must be at least 1.')
            elif guests_int > 50:
                errors.append('Number of guests cannot exceed 50.')
        except ValueError:
            errors.append('Please enter a valid number of guests.')
        
        # Start date validation
        if not start_date:
            errors.append('Start date is required.')
        else:
            try:
                date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                today = datetime.now().date()
                if date_obj.date() < today:
                    errors.append('Start date cannot be in the past.')
            except ValueError:
                errors.append('Please enter a valid date.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'user/package_detail.html', {
                'package': package,
                'today': datetime.now(),
                'form_data': {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'guests': guests,
                    'start_date': start_date
                }
            })
        
        # If validation passes, create customer and lead
        # Split name into first and last
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Check if customer already exists with this phone number
        customer, created = Customer.objects.get_or_create(
            contact_number=phone,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'display_name': name,
                'whatsapp_number': phone,
                'same_as_whatsapp': True,
                'customer_type': 'Individual',
                'place': f'Booking: {package.name}'
            }
        )
        
        Lead.objects.create(
            full_name=name,
            mobile_number=phone,
            source='Website',
            enquiry_type=package.category,  # Use package category (Domestic/International)
            remarks=f'Package: {package.name} | Email: {email} | Guests: {guests} | Start Date: {start_date}'
        )
        
        messages.success(request, 'Booking request submitted! Our team will contact you soon.')
        return redirect('user_panel:package_detail', slug=slug)
    
    return render(request, 'user/package_detail.html', {
        'package': package,
        'today': datetime.now()
    })

def hospitality(request):
    properties = Property.objects.all()
    testimonials = Feedback.objects.filter(feedback_type='Property Management', featured=True).prefetch_related('images')
    return render(request, 'user/hospitality.html', {'properties': properties, 'testimonials': testimonials})

def hospitality_detail(request, property_id):
    """
    Display detailed information about a specific hospitality property
    """
    property = get_object_or_404(Property, id=property_id)
    # Get related properties (same type or location)
    related_properties = Property.objects.filter(
        Q(property_type=property.property_type) | Q(location=property.location)
    ).exclude(id=property.id)[:3]
    
    return render(request, 'user/hospitality_detail.html', {
        'property': property,
        'related_properties': related_properties
    })

def feedback_form_submit(request):
    """
    Handle user feedback form submission from user feedback template
    """
    if request.method == "POST":
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            mobile_number = request.POST.get('mobile_number', '').strip()
            rating = request.POST.get('rating', '')
            feedback_text = request.POST.get('feedback', '').strip()
            
            if not all([name, email, mobile_number, rating, feedback_text]):
                return JsonResponse({'success': False, 'error': 'All fields are required'})
            
            Feedback.objects.create(
                name=name,
                email=email,
                mobile_number=mobile_number,
                rating=int(rating),
                feedback=feedback_text
            )
            
            # after submission send admin to feedback management page for immediate review
            return JsonResponse({'success': True, 'message': 'Thank you! Your feedback has been submitted successfully.', 'redirect': '/admin/feedback/'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def feedback_page(request):
    return render(request, 'user/feedback.html')


def feedback_form(request):
    """Render a simple feedback form (no sidebar). On POST, save and show
    success message on the same page.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        feedback_type = request.POST.get('feedback_type', '').strip()
        rating = request.POST.get('rating', '')
        feedback_text = request.POST.get('feedback', '').strip()
        images = request.FILES.getlist('feedback_images')

        if not all([name, email, feedback_type, rating, feedback_text]):
            return render(request, 'user/feedback_form.html', {
                'error': 'Please fill required fields.',
                'feedback_type_choices': Feedback.FEEDBACK_TYPE_CHOICES
            })

        feedback = Feedback.objects.create(
            name=name,
            email=email,
            mobile_number=mobile_number,
            feedback_type=feedback_type,
            rating=int(rating),
            feedback=feedback_text
        )
        
        # Save multiple images
        from admin_panel.models import FeedbackImage
        for image in images:
            FeedbackImage.objects.create(feedback=feedback, image=image)
        
        # show success message on the same page
        return render(request, 'user/feedback_form.html', {'success': True})

    return render(request, 'user/feedback_form.html', {
        'feedback_type_choices': Feedback.FEEDBACK_TYPE_CHOICES
    })



