from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import Client,Booking,ClassSlot
from datetime import datetime
from django.utils import timezone 
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from django.utils.timezone import now
from django.utils.timezone import localtime



# Create your views here.
def index(request):
    return render(request,'fitSync/index.html')

def about(request):
    return render(request,'fitSync/about.html')

def contact(request):
    return render(request,'fitSync/contact.html')

def services(request):
    return render(request,'fitSync/services.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            client = Client.objects.get(email=email)
            # Check password properly using hash
            if check_password(password, client.password):
                request.session['client_id'] = client.id
                request.session['client_email'] = client.email
                request.session['client_name'] = client.full_name
                messages.success(request, f"Welcome, {client.full_name}!")
                return redirect('home')
            else:
                messages.error(request, "Incorrect email or password.")
        except Client.DoesNotExist:
            messages.error(request, "Incorrect email or password.")
        return redirect('login')
    return render(request,'fitSync/login.html')


def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')
        
        # Check if email already exists
        if Client.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        # Hash password before storing
        hashed_password = make_password(password)

        # Create client
        client = Client.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone,
            password=hashed_password
        )
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')
    return render(request,'fitSync/signup.html')


def home(request):
    if 'client_id' not in request.session:
        return redirect('login')

    client_id = request.session['client_id']
    client = Client.objects.get(id=client_id)
    class_slots = ClassSlot.objects.filter(date__gte=now().date(), available_seats__gt=0).order_by('date', 'start_time')

    user_bookings = Booking.objects.filter(client=client).select_related('class_slot')
    current_time = timezone.now()

    for booking in user_bookings:
        class_datetime = timezone.make_aware(
            datetime.combine(booking.class_slot.date, booking.class_slot.start_time)
        )
        if booking.status == 'upcoming' and class_datetime < current_time:
            booking.status = 'cancelled'
            booking.save()

    upcoming_booking = user_bookings.filter(
        status='upcoming',
        class_slot__date__gte=timezone.localdate()
    ).order_by('class_slot__date', 'class_slot__start_time').first()

    bookings = user_bookings.order_by('-class_slot__date', '-class_slot__start_time')[:5]

    recommended_slots = ClassSlot.objects.filter(
        date__gte=timezone.localdate(),
        available_seats__gt=0
    ).order_by('date', 'start_time')[:3]

    context = {
        'upcoming_booking': upcoming_booking,
        'recommended_slots': recommended_slots,
        'class_slots': class_slots,
        'bookings': bookings,
        'membership': {
            'plan': 'Premium Monthly',
            'renewal': 'July 25, 2025'
        }
    }
    return render(request, 'fitSync/home.html', context)


@require_http_methods(["GET"])
def get_classes(request):
    slots = ClassSlot.objects.filter(date__gte=timezone.localdate()).order_by('date', 'start_time')
    data = [
        {
            "id": slot.id,
            "class_type": slot.class_type,
            "date": slot.date.strftime("%Y-%m-%d"),
            "start_time": slot.start_time.strftime("%I:%M %p"),
            "end_time": slot.end_time.strftime("%I:%M %p"),
            "available_seats": slot.available_seats
        } for slot in slots
    ]
    return JsonResponse(data, safe=False)


def zumba(request):
    current_datetime = localtime()
    today = current_datetime.date()
    current_time = current_datetime.time()

    # Show only future classes or today's upcoming classes
    class_slots = ClassSlot.objects.filter(
        date__gt=today,  # Future days
    ) | ClassSlot.objects.filter(
        date=today,
        start_time__gt=current_time  # Today's upcoming slots
    )

    class_slots = class_slots.filter(
        available_seats__gt=0,
        class_type='zumba'  # Filter for zumba only
    ).order_by('date', 'start_time')

    return render(request, 'fitSync/zumba.html', {'class_slots': class_slots})


def hiit(request):
    current_datetime = localtime()
    today = current_datetime.date()
    current_time = current_datetime.time()

    # Show only future classes or today's upcoming classes
    class_slots = ClassSlot.objects.filter(
        date__gt=today,  # Future days
    ) | ClassSlot.objects.filter(
        date=today,
        start_time__gt=current_time  # Today's upcoming slots
    )

    class_slots = class_slots.filter(
        available_seats__gt=0,
        class_type='hiit'  # Filter for zumba only
    ).order_by('date', 'start_time')

    return render(request, 'fitSync/hiit.html', {'class_slots': class_slots})


def yoga(request):
    current_datetime = localtime()
    today = current_datetime.date()
    current_time = current_datetime.time()

    # Show only future classes or today's upcoming classes
    class_slots = ClassSlot.objects.filter(
        date__gt=today,  # Future days
    ) | ClassSlot.objects.filter(
        date=today,
        start_time__gt=current_time  # Today's upcoming slots
    )

    class_slots = class_slots.filter(
        available_seats__gt=0,
        class_type='yoga'  # Filter for zumba only
    ).order_by('date', 'start_time')

    return render(request, 'fitSync/yoga.html', {'class_slots': class_slots})



# API: GET /bookings?email=...
@require_http_methods(["GET"])
def get_bookings(request):

    # Session-based client (browser)
    if 'client_id' in request.session:
        client = Client.objects.filter(id=request.session['client_id']).first()
        is_api = False
    else:
        # API request using ?email=
        email = request.GET.get("email")
        if not email:
            return JsonResponse({"error": "Email is required."}, status=400)
        client = Client.objects.filter(email=email).first()
        is_api = True

    if not client:
        return JsonResponse({"error": "Client not found."}, status=404)

    now_time = timezone.localtime()

    upcoming = Booking.objects.filter(
        client=client
    ).filter(
        Q(class_slot__date__gt=now_time.date()) |
        Q(class_slot__date=now_time.date(), class_slot__start_time__gt=now_time.time())
    ).order_by('class_slot__date', 'class_slot__start_time')

    history = Booking.objects.exclude(id__in=upcoming.values_list('id', flat=True)).filter(
        client=client
    ).order_by('-class_slot__date', '-class_slot__start_time')

    if is_api:
        return JsonResponse({
            "upcoming": [
                {
                    "class_type": b.class_slot.class_type,
                    "date": b.class_slot.date,
                    "start_time": b.class_slot.start_time.strftime("%I:%M %p"),
                    "end_time": b.class_slot.end_time.strftime("%I:%M %p"),
                    "status": b.status
                } for b in upcoming
            ],
            "history": [
                {
                    "class_type": b.class_slot.class_type,
                    "date": b.class_slot.date,
                    "start_time": b.class_slot.start_time.strftime("%I:%M %p"),
                    "end_time": b.class_slot.end_time.strftime("%I:%M %p"),
                    "status": b.status
                } for b in history
            ]
        })

    # Render template for browser
    return render(request, 'fitSync/bookings.html', {
        'upcoming_bookings': upcoming,
        'booking_history': history,
    })


# Logging  booking attempt
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def book_class(request):
    try:
        # Check if request is JSON (API)
        if request.content_type == "application/json":
            data = json.loads(request.body)
            email = data.get('email') or request.session.get('client_email')
            slot_id = data.get('slot_id')
        else:
            # Form submission (HTML form)
            email = request.POST.get('email') or request.session.get('client_email')
            slot_id = request.POST.get('slot_id')
            
        
        logger.info(f"Booking attempt by {email} for slot {slot_id}")

        if not email or not slot_id:
            if request.content_type == "application/json":
                return JsonResponse({"error": "Email and slot_id are required."}, status=400)
            messages.error(request, "Email and slot must be provided.")
            return redirect('home')

        client = Client.objects.filter(email=email).first()
        if not client:
            if request.content_type == "application/json":
                return JsonResponse({"error": "User not found."}, status=404)
            messages.error(request, "User not found.")
            return redirect('home')

        class_slot = ClassSlot.objects.filter(id=slot_id).first()
        if not class_slot:
            if request.content_type == "application/json":
                return JsonResponse({"error": "Selected slot does not exist."}, status=404)
            messages.error(request, "Selected slot does not exist.")
            return redirect('home')

        if class_slot.available_seats <= 0:
            if request.content_type == "application/json":
                return JsonResponse({"error": "No seats available."}, status=400)
            messages.error(request, "No seats available for this slot.")
            return redirect('home')

        if Booking.objects.filter(client=client, class_slot=class_slot).exists():
            if request.content_type == "application/json":
                return JsonResponse({"error": "You have already booked this slot."}, status=400)
            messages.warning(request, "You have already booked this slot.")
            return redirect('home')

        Booking.objects.create(
            email=client.email,
            client=client,
            class_slot=class_slot
        )

        class_slot.available_seats -= 1
        class_slot.save()

        if request.content_type == "application/json":
            return JsonResponse({"message": "Class booked successfully!"}, status=201)
        messages.success(request, "Class booked successfully!")
        return redirect('home')
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    except Exception as e:
        if request.content_type == "application/json":
            return JsonResponse({"error": str(e)}, status=500)
        messages.error(request, "Something went wrong.")
        return redirect('home')
    

def logout(request):
    request.session.flush()
    return redirect('login')
