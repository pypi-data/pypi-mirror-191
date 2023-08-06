from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from foledol.django.logger import log
from foledol.django.tools.field import TextField, IntegerField
from foledol.django.tools.form import Form
from foledol.django.tools.handlers import confirm
from foledol.django.utils import pop_path, get_path, get_integer, error, new_context
from .form_templates import form_template_renumber
from ..models import FormTemplateItem, FormTemplate, FORM_TEMPLATE_ITEM_TYPE_SET


class TemplateItemForm(Form):
    def __init__(self, context):
        super().__init__(context, [
            TextField('label', "Libellé", min_length=1),
            IntegerField('type', "Type"),
            IntegerField('order', "Ordre"),
            TextField('comment', "Description"),
        ])


def form_template_item_form(request, column):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    action = get_path(request, context, column, 'column', space='django')

    template = None

    template_id = get_integer(request, 'template_id', 0)
    if template_id > 0:
        template = FormTemplate.objects.all().get(id=template_id)
    context['template_id'] = template.id if template else 0

    if column:
        context['column'] = column

    template_items = template.items.all() if template else []
    context['template_items'] = template_items

    form = TemplateItemForm(context)
    form.read(request.POST if action else {}, column, defaults={
    })

    context['type_set'] = FORM_TEMPLATE_ITEM_TYPE_SET

    order = (template.items.count() + 1) * 10 if template else 10

    if len(action) > 0:
        form.validate()

    if context['error']:
        context['error'] = "Veuillez corriger les erreurs ci-dessous"

    if not action or context['error']:
        context['action'] = 'update' if column else 'create'
        return render(request, 'form_template_item.html', context)

    if action == 'create':
        template_item = FormTemplateItem(template=template)
    form.save(template_item)
    if not template_item.order:
        template_item.order = order
    template_item.save()
    if template:
        form_template_renumber(template)
    log(template_item.id, 'template_item', action, request.user, form.old_values, form.new_values)

    return HttpResponseRedirect(context['back'] + '?path=' + pop_path(request))


@login_required
def form_template_item_create(request):
    return form_template_item_form(request, None)


@login_required
def form_template_item_update(request, pk):
    template_item = FormTemplateItem.objects.filter(id=pk).first()
    return form_template_item_form(request, template_item) if template_item else error(request)


@login_required
def form_template_item_delete(request, pk):
    def prepare(context):
        template_item = FormTemplateItem.objects.get(id=pk)
        context['title'] = _('delete_form_template_item_title').format(template_item)
        context['cancel'] = reverse('django:form_template_item_update', kwargs={'pk': pk})
        context['message'] = _('delete_form_template_item_message').format(template_item)
        return template_item

    def execute(template_item):
        template_item.delete()
        form_template_renumber(template_item.template)

    return confirm(request, 'delete', prepare, execute, reverse('django:form_template_items'))
