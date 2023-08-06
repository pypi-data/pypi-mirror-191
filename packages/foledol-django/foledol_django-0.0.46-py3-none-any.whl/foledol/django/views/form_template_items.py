from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from foledol.django.tools.table import Table, TableColumn
from foledol.django.utils import get_search, paginate, new_context

from ..models import FormTemplateItem


class FormTemplateItemsTable(Table):
    def __init__(self, rows):
        super().__init__(rows, [
            TableColumn('label', "Libellé")
        ])
        self.update = 'django:form_template_item_update'
        self.create = 'django:form_template_item_create'
        self.search = True


@login_required
@staff_member_required
def form_template_item_list(request):
    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    form_template_items = FormTemplateItem.objects.all()

    search = get_search(request).strip()
    if len(search) > 0:
        form_template_items = FormTemplateItem.objects.filter(label=search)
    context['search'] = search

    columns = form_template_items.order_by('order')

    context['table'] = FormTemplateItemsTable(paginate(request, context, columns))

    return render(request, 'form_template_items.html', context)
