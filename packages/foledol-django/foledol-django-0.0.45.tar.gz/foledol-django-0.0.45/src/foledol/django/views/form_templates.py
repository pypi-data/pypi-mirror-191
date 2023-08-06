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
        self.update = 'django:template_update'
        self.create = 'django:template_create'
        self.search = True


@login_required
@staff_member_required
def form_template_list(request):
    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    templates = FormTemplate.objects.all()

    search = get_search(request).strip()
    if len(search) > 0:
        templates = FormTemplate.objects.filter(name=search)
    context['search'] = search

    sort = get_param_from_get_or_request(request, context, 'templates', 'template_sort', 'name_asc')
    if sort == 'name_asc':
        templates = templates.order_by('name')
    elif sort == 'name_desc':
        templates = templates.order_by('-name')

    context['table'] = FormTemplateTables(paginate(request, context, templates))

    return render(request, 'form_templates.html', context)


def form_template_renumber(template):
    order = 10
    for template_item in template.items.all().order_by('order'):
        if template_item.order != order:
            template_item.order = order
            template_item.save()
        order += 10






