from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import random
from customers.models import *
from django.contrib.auth.models import User 


from users.models import *


from property.models import *
from .forms import *


from django.db.models import Q



from django.shortcuts import redirect


from django.core.paginator import Paginator

from django.contrib import messages

from django.http import JsonResponse
from django.template.loader import render_to_string


def index(request):
    # Fetch all properties with 'new_launch' construction status
    properties = PropertyListing.objects.all()

    # Apply filters if provided
    category_filter = request.GET.get('category')
    if category_filter:
        properties = properties.filter(category__name=category_filter)
    
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        properties = properties.filter(price__gte=price_min)
    if price_max:
        properties = properties.filter(price__lte=price_max)
    
    # Pagination: Display 10 properties per page
    paginator = Paginator(properties, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "properties": properties,
        "category_filter": category_filter,
        "price_min": price_min,
        "price_max": price_max,
    }

    return render(request, 'web/index.html', context)


def addform(request):
    categories = Category.objects.all()
    mainplaces = MainPlace.objects.all()
    properties = PropertyListing.objects.all()

    

    context = {
        "categories": categories,
        "mainplaces": mainplaces,
        "properties": properties,
    }

    return render(request, 'web/addForm.html', context=context)



# def get_form(request):
#     category = request.GET.get('category')
#     form = None

#     if category == 'apartments':
#         form = ApartmentForm()
#     elif category == 'farm_houses':
#         form = FarmHouseForm()
#     elif category == 'pg':
#         form = PGForm()
#     elif category == 'builder_floors':
#         form = BuilderFloorForm()

#     if form:
#         html = render_to_string('partials/form.html', {'form': form})
#         return JsonResponse({'form_html': html})
#     return JsonResponse({'error': 'Invalid category'}, status=400)



def profile(request):
    
    return render(request, 'web/profile.html')

def contact(request):
    
    return render(request, 'web/contact.html')

def favourite(request):
    properties = PropertyListing.objects.filter(is_favarite=True)


    context = {
        "properties": properties,
    }

    return render(request, 'web/favourite.html', context=context)

def propertydetail(request, id):
    # Get the current property by ID
    property = get_object_or_404(PropertyListing, id=id)
    
    # Retrieve the recently viewed properties from the session
    recently_viewed = request.session.get('recently_viewed', [])

    # If the current property is not already in the list, add it to the front
    if id not in recently_viewed:
        recently_viewed.insert(0, id)
    
    # Limit the number of recently viewed properties (e.g., to the last 5 properties)
    if len(recently_viewed) > 5:
        recently_viewed = recently_viewed[:5]
    
    # Store the updated list back to the session
    request.session['recently_viewed'] = recently_viewed

    # Fetch the recently viewed property objects from the database
    recentviewedproperty = PropertyListing.objects.filter(id__in=recently_viewed)

    # Create context for the template
    context = {
        "property": property,
        "recentviewedproperty": recentviewedproperty,
    }

    return render(request, 'web/property-detail.html', context=context)


def post_property(request):
    categories = Category.objects.all()
    mainplaces = MainPlace.objects.all()
    properties = PropertyListing.objects.all()

    # Print each category name for debugging
    for category in categories:
        print(category.name)

    context = {
        "categories": categories,
        "mainplaces": mainplaces,
        "properties": properties,
    }

    return render(request, 'post_property.html', context=context)


def user_properties(request):
    if not request.user.is_authenticated:
        return redirect('login')

    properties = PropertyListing.objects.all()

    context = {
        "properties": properties,
    }
    return render(request, "web/user_properties.html", context)


def mark_active(request, id):
    instance = PropertyListing.objects.get(id=id)
    if instance.is_active == False:
        instance.is_active = True
        instance.save()

    else :
        instance.is_active = False
        instance.save()
    instance.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_property(request, id):
    instance = PropertyListing.objects.get(id=id)
    instance.delete()
    instance.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def favourite(request):
    properties = PropertyListing.objects.filter(is_favarite=True)


    context = {
        "properties": properties,
    }

    return render(request, 'web/favourite.html', context=context)


def favorat(request, id):
    instance = PropertyListing.objects.get(id=id)
    if instance.is_favarite == False:
        instance.is_favarite = True
        instance.save()

    else :
        instance.is_favarite = False
        instance.save()
    instance.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        User =authenticate(request, email=email, password=password)
        if User is not None:
            auth_login(request,User)
            return HttpResponseRedirect(reverse('web:index'))
        else:
            context = {'error_message': 'Invalid email address'}
            return render(request, 'web/login.html', context)
    else:
        return render(request,'web/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            context = {'error_message': 'Email is already registered'}
            return render(request, 'web/signup.html', context)

        user = User.objects.create_user(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            password=password,
            is_customer=True
        )
        user.save()
        customer = Customer.objects.create(
            user=user
        )
        customer.save()
        return HttpResponseRedirect (reverse('web:login'))
    else:
        return render(request,'web/signup.html')