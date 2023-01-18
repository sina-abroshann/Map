from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Submit_Information_Form
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Submit_Information_Model
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import CharField
from django.db.models import  Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jalali_date import datetime2jalali, date2jalali
import jdatetime
import os


def Submit_Information_View(request):
    global form
    if request.method == "POST":
        SubmitInformation = Submit_Information_Form(request.POST or None, request.FILES or None)
        if SubmitInformation.is_valid():
            project_employer = request.POST.get('project_employer', False)
            project_manager = request.POST.get('project_manager', False)
            date_letter = request.POST.get('date_letter', False)
            letter_number = request.POST.get('letter_number', False)
            recipiant = request.POST.get('recipiant', False)
            coordinator = request.POST.get('coordinator', False)
            description_letter = request.POST.get('description_letter', False)
            phone = request.POST.get('phone', False)
            state = request.POST.get('state', False)
            date_deposit = request.POST.get('date_deposit', False)
            description = request.POST.get('description', False)
            amount_deposit = request.POST.get('amount_deposit', False)
            tracking_code = request.POST.get('tracking_code', False)
            status = request.POST.get('status', False)
            try:
                shp_file = request.POST['shp_file']
            except MultiValueDictKeyError:
                shp_file = False

            try:
                doc_file = request.POST['doc_file']
            except MultiValueDictKeyError:
                doc_file = False

            SubmitInformation.project_employer = project_employer
            SubmitInformation.project_manager = project_manager
            SubmitInformation.date_letter = date_letter
            SubmitInformation.letter_number = letter_number
            SubmitInformation.recipiant = recipiant
            SubmitInformation.coordinator = coordinator
            SubmitInformation.description_letter = description_letter
            SubmitInformation.phone = phone
            SubmitInformation.state = state
            SubmitInformation.date_deposit = date_deposit
            SubmitInformation.description = description
            SubmitInformation.amount_deposit = amount_deposit
            SubmitInformation.tracking_code = tracking_code
            SubmitInformation.status = status
            SubmitInformation.shp_file = shp_file
            SubmitInformation.doc_file = doc_file

            SubmitInformation.save()
            messages.success(request, 'فرم با موفقیت ثبت شد')
            return render(request, 'Submit_Information.html', {'form': Submit_Information_Form(request.GET)})
        else:
            messages.error(request, 'مشکلی در ثبت فرم وجود دارد')
            messages.error(request, SubmitInformation.errors)
    else:
        form = Submit_Information_Form(use_required_attribute=False)
    return render(request, 'Submit_Information.html', {'form': form})


def home(request):
    return render(request, 'welcome.html')

def Cartable(request):
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(project_employer__icontains=q) | Q(project_manager__icontains=q) | Q(date_letter__icontains=q) |
                        Q(letter_number__icontains=q) | Q(recipiant__icontains=q) | Q(coordinator__icontains=q) |
                        Q(description_letter__icontains=q) | Q(phone__icontains=q) | Q(state__icontains=q) | 
                        Q(date_deposit__icontains=q) | Q(description__icontains=q) | Q(amount_deposit__icontains=q) | 
                        Q(tracking_code__icontains=q) | Q(status__icontains=q)
                        )

        Cartables = Submit_Information_Model.objects.filter(multiple_q).order_by('-add_time')
    else:
        Cartables = Submit_Information_Model.objects.all().order_by('-add_time')
    default_page = 1
    page = request.GET.get('page', default_page)
    items_per_page = 15
    paginator = Paginator(Cartables, items_per_page)
    try:
        Cartables = paginator.page(page)
    except PageNotAnInteger:
        Cartables = paginator.page(default_page)
    except EmptyPage:
        Cartables = paginator.page(paginator.num_pages)
    return render(request, 'Cartable.html', {'Cartables': Cartables})
    
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect,
                              HttpResponse)
def Cartable_Details(request, id):
    Cartable = Submit_Information_Model.objects.get(pk = id)
    form = Submit_Information_Form(request.POST or None, instance=Cartable)
    if 'update' in request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Cartable")
    elif 'delete' in request.POST:
        obj = get_object_or_404(Submit_Information_Model, project_id = id)
        obj.delete()
        return HttpResponseRedirect("/Cartable")
    return render(request, 'Cartable_Details.html', {'form':form})
from django.conf import settings
from django.http import Http404

def Download(requset, path):
    Cartables = Submit_Information_Model.objects.all()
    file_path=os.path.join(settings.STATIC_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(),content_type='application/doc_file')
            response['Content-Disposition']='inline;filename='+os.path(file_path)
            return render(response, 'Cartable.html')
    return Http404