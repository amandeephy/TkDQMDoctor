from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

from django_tables2 import RequestConfig

from .models import *
from .forms import *
from .tables import *

def index(request):
    return render(request, 'certhelper/index.html')

class CreateRun(generic.CreateView):
    model = RunInfo
    form_class = RunInfoForm
    template_name_suffix = '_form'
    success_url = '/'

def listruns(request):
    # template_name = 'certhelper/list.html'
    # context_object_name = 'list'

    # def get_queryset(self):
    #     return RunInfo.objects.all().order_by('run_number')
    table = RunInfoTable(RunInfo.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'certhelper/list.html', {'table': table})

class ListBlocks(generic.ListView):
    template_name = 'certhelper/references.html'
    context_object_name = 'references'

    def get_queryset(self):
        return ReferenceRun.objects.all()

class UpdateRun(generic.UpdateView):
    model = RunInfo
    form_class = RunInfoForm
    success_url = '/'
    template_name_suffix = '_update_form'

class DeleteRun(generic.DeleteView):
    model = RunInfo
    form_class = RunInfoForm
    success_url = '/'
    template_name_suffix = '_delete_form'


class CreateType(generic.CreateView):
    model = Type
    form_class = TypeForm
    template_name_suffix = '_form'
    success_url = '/create'

class SummaryView(generic.ListView):
    template_name = 'certhelper/summary.html'
    context_object_name = 'runs'

    def get_queryset(self):
        return RunInfo.objects.all()