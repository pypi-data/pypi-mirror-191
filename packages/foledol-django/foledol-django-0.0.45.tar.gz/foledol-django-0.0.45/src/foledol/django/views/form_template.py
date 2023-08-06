import io

import xlsxwriter
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.expressions import RawSQL, F
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from foledol.django.logger import log
from foledol.django.models import Grid, ConditionGroup, Condition, ORDER_BY_ASC, ORDER_BY_DESC, FormTemplate
from foledol.django.reports.grid import GridReport
from foledol.django.templatetags.form_extras import value, value_as_str
from foledol.django.tools.field import TextField, DateField, BooleanField
from foledol.django.tools.form import Form
from foledol.django.tools.handlers import confirm
from foledol.django.tools.table import Table, TableColumn
from foledol.django.utils import pop_path, get_path, get_param, error, paginate, new_context, print_report, delete_all, \
    get_integer


class FormTemplateForm(Form):
    def __init__(self, context):
        super().__init__(context, [
            TextField('name', "Nom", min_length=1),
            TextField('comment', "Description"),
        ])


class FormTemplateItemSubTable(Table):
    def __init__(self, rows, read_only=False):
        super().__init__(rows, [
            TableColumn('label', "Libellé"),
            TableColumn('order', "Ordre")
        ])
        self.heading = 'Paragraphes'
        self.update = 'django:form_template_item_update' if not read_only else None
        self.create = 'django:form_template_item_create' if not read_only else None
        self.placeholder = "Ajouter un paragraphe"


def form_template_form(request, template, read_only=False):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    action = get_path(request, context, template, 'template', space='django')
    if action == 'clone':
        template = template.clone()
        request.session['path'] = request.POST['path']
        return HttpResponseRedirect(reverse('django:template_update', kwargs={'pk': template.id}) + '?back')

    context['read_only'] = read_only

    get_param(request, context, 'template_sort', '')

    if template:
        context['template'] = template
    context['template_url'] = reverse('django:template_update', kwargs={'pk': template.id}) if template else None

    form = FormTemplateForm(context)
    form.read(request.POST if action else {}, template)

    if len(action) > 0:
        form.validate()

    template_items = template.items.all().order_by('order') if template else None
    template_items_form = build_form(template, context) if template else None

    context['template_items'] = template_items
    context['template_items_form'] = template_items_form
    context['table_template_items'] = FormTemplateItemSubTable(template_items, read_only=not request.user.is_staff)

    if context['error']:
        context['error_message'] = "Veuillez corriger les erreurs ci-dessous"
    if not action or context['error']:
        context['action'] = 'update' if template else 'create'
        return render(request, 'template.html', context)

    if action == 'update':
        form.save(template)

    if action == 'create':
        template = FormTemplate()

    form.save_and_log(template, 'template', action, request)

    if action == 'update' or action == 'edit' or action == 'done':
        context['action'] = 'update'
        return render(request, 'template.html', context)
    return HttpResponseRedirect(context['back'] + '?path=' + pop_path(request))


@login_required
def form_template_create(request):
    return form_template_form(request, None)


@login_required
def form_template_update(request, pk):
    template = FormTemplate.objects.filter(id=pk).first()
    return form_template_form(request, template) if template else error(request)


@login_required
def form_template_delete(request, pk):

    def prepare(context):
        template = FormTemplate.objects.get(id=pk)
        context['title'] = _('delete_form_template_title').format(template)
        context['cancel'] = reverse('django:form_template_update', kwargs={'pk': pk})
        context['message'] = _('delete_form_template_message').format(template)
        return template

    def execute(template):
        delete_all(template.items.all())
        template.delete()

    return confirm(request, 'delete', prepare, execute, reverse('django:form_templates'))


def build_form(template, context):
    fields = []
    for template_item in template.items.all():
        fields.append(TextField(template_item.id_as_str(), template_item.label))
    return Form(context, fields)
