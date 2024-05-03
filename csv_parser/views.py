from django.http import JsonResponse
from django.shortcuts import render
import csv
from django.http import HttpResponseRedirect
import os
from django.conf import settings
from .models import Sponsors

from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
import json
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError, MultipleObjectsReturned, PermissionDenied
from django.http import QueryDict
from django.db.models import F, ExpressionWrapper, fields, Sum
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.db.models import Q

"""HELPER FUNCTIONS"""
def parse_csv(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'UkTiersponsors_All.csv')

    # Check if the file exists
    if os.path.exists(csv_file_path):
        # Open and read the CSV file
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                new_record = Sponsors(organisation_name=row['Organisation Name'], town=row['Town'], industry=row['Industry'], main_tier=row['Main Tier'], sub_tier=row['Sub Tier'], date_added=row['Date Added'])

                new_record.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'error': 'file not found'})

# Create your views here.
def index(request):
    return JsonResponse({'message': "App is working"})


"""PAGINATION"""
def paginate_results_objects(request, query_results, view_url, items_per_page=100):
    items_per_page = items_per_page

    page_number = request.GET.get('page', 1)

    paginator = Paginator(query_results, items_per_page)

    try:
        page_obj = paginator.get_page(page_number)
    
    except EmptyPage:
        return JsonResponse({"error": "Page not found"}, status=404)
    
    items_on_current_page = page_obj.object_list

    json_data = {
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'query_results': [item.to_dict() for item in items_on_current_page],
    }
    
    if page_obj.has_previous():
        if "page=" in view_url:
            json_data['previous_page'] = f"{view_url[:view_url.rfind('page=')]}page={page_obj.previous_page_number()}"
        else:
            json_data['previous_page'] = f"{view_url}?page={page_obj.previous_page_number()}"

    if page_obj.has_next():
        if "page=" in view_url:
            json_data['next_page'] = f"{view_url[:view_url.rfind('page=')]}page={page_obj.next_page_number()}"
        else:
            json_data['next_page'] = f"{view_url}?page={page_obj.next_page_number()}"
    
    return json_data

def paginate_results_list(request, query_results, view_url, items_per_page=100):
    items_per_page = items_per_page

    page_number = request.GET.get('page', 1)

    paginator = Paginator(query_results, items_per_page)

    try:
        page_obj = paginator.get_page(page_number)
    
    except EmptyPage:
        return JsonResponse({"error": "Page not found"}, status=404)
    
    items_on_current_page = page_obj.object_list

    json_data = {
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'query_results': [(item[0], f"http://127.0.0.1:8000/csv_parser/search?q={item[0]}") for item in items_on_current_page],
    }
    
    if page_obj.has_previous():
        if "page=" in view_url:
            json_data['previous_page'] = f"{view_url[:view_url.rfind('page=')]}page={page_obj.previous_page_number()}"
        else:
            json_data['previous_page'] = f"{view_url}?page={page_obj.previous_page_number()}"

    if page_obj.has_next():
        if "page=" in view_url:
            json_data['next_page'] = f"{view_url[:view_url.rfind('page=')]}page={page_obj.next_page_number()}"
        else:
            json_data['next_page'] = f"{view_url}?page={page_obj.next_page_number()}"
    
    return json_data

"""QUERIES"""

def get_all_records(request):
    view_url = request.build_absolute_uri()

    all_records = Sponsors.objects.all()

    # return JsonResponse([record.to_dict() for record in all_records], safe=False)
    return JsonResponse(paginate_results_objects(request, all_records, view_url), safe=False)

def get_towns(request):
    view_url = request.build_absolute_uri()

    unique_towns = Sponsors.objects.values_list('town', flat=False).distinct()

    # return JsonResponse({'towns': list(unique_towns)})

    return JsonResponse(paginate_results_list(request, unique_towns, view_url), safe=False)

def get_industries(request):
    view_url = request.build_absolute_uri()

    unique_industries = Sponsors.objects.values_list('industry', flat=False).distinct()

    return JsonResponse(paginate_results_list(request, unique_industries, view_url), safe=False)

def get_main_tiers(request):
    view_url = request.build_absolute_uri()

    unique_main_tiers = Sponsors.objects.values_list('main_tier', flat=False).distinct()

    return JsonResponse(paginate_results_list(request, unique_main_tiers, view_url), safe=False)

def get_sub_tiers(request):
    view_url = request.build_absolute_uri()

    unique_sub_tiers = Sponsors.objects.values_list('sub_tier', flat=False).distinct()

    return JsonResponse(paginate_results_list(request, unique_sub_tiers, view_url), safe=False)

"""SEARCH"""
def search_field(request):
    view_url = request.build_absolute_uri()

    query = request.GET.get('q')

    if query:
        search_results = Sponsors.objects.filter(
            Q(organisation_name__icontains=query) |
            Q(town__icontains=query) |
            Q(industry__icontains=query) |
            Q(main_tier__icontains=query) |
            Q(sub_tier__icontains=query)
        )
    
    else:
        search_results = None
    
    return JsonResponse(paginate_results_objects(request, search_results, view_url), safe=False)