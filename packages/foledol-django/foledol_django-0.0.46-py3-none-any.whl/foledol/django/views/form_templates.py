from django.conf import settings


from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from foledol.django.tools.table import Table, TableColumn
from foledol.django.utils import get_search, paginate, new_context, get_param_from_get_or_request

from ..models import FormTemplate


class FormTemplateTables(Table):
    def __init__(self, rows):
        super().__init__(rows, [
            TableColumn('name', "Nom", sortable=True),
        ])
        self.update = 'django:form_template_update'
        self.create = 'django:form_template_create'
        self.search = True


@login_required
@staff_member_required
def form_template_list(request):
    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    form_templates = FormTemplate.objects.all()

    search = get_search(request).strip()
    if len(search) > 0:
        form_templates = FormTemplate.objects.filter(name=search)
    context['search'] = search

    sort = get_param_from_get_or_request(request, context, 'form_templates', 'form_template_sort', 'name_asc')
    if sort == 'name_asc':
        form_templates = form_templates.order_by('name')
    elif sort == 'name_desc':
        form_templates = form_templates.order_by('-name')

    context['table'] = FormTemplateTables(paginate(request, context, form_templates))

    return render(request, 'form_templates.html', context)


def form_template_renumber(form_template):
    order = 10
    for item in form_template.items.all().order_by('order'):
        if item.order != order:
            item.order = order
            item.save()
        order += 10






