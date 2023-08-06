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


class FormTemplateItemForm(Form):
    def __init__(self, context):
        super().__init__(context, [
            TextField('label', "Libellé", min_length=1),
            IntegerField('type', "Type"),
            IntegerField('order', "Ordre"),
            TextField('comment', "Description"),
        ])


def form_template_item_form(request, form_template_item):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    action = get_path(request, context, form_template_item, 'column', space='django')

    form_template = None

    form_template_id = get_integer(request, 'form_template_id', 0)
    if form_template_id > 0:
        form_template = FormTemplate.objects.all().get(id=form_template_id)
    context['form_template_id'] = form_template.id if form_template else 0

    if form_template_item:
        context['column'] = form_template_item

    form_template_items = form_template.items.all() if form_template else []
    context['form_template_items'] = form_template_items

    form = FormTemplateItemForm(context)
    form.read(request.POST if action else {}, form_template_item, defaults={
    })

    context['type_set'] = FORM_TEMPLATE_ITEM_TYPE_SET

    order = (form_template.items.count() + 1) * 10 if form_template else 10

    if len(action) > 0:
        form.validate()

    if context['error']:
        context['error'] = "Veuillez corriger les erreurs ci-dessous"

    if not action or context['error']:
        context['action'] = 'update' if form_template_item else 'create'
        return render(request, 'form_template_item.html', context)

    if action == 'create':
        form_template_item = FormTemplateItem(form_template=form_template)
    form.save(form_template_item)
    if not form_template_item.order:
        form_template_item.order = order
    form_template_item.save()
    if form_template:
        form_template_renumber(form_template)
    log(form_template_item.id, 'template_item', action, request.user, form.old_values, form.new_values)

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
        form_template_item = FormTemplateItem.objects.get(id=pk)
        context['title'] = _('delete_form_template_item_title').format(form_template_item)
        context['cancel'] = reverse('django:form_template_item_update', kwargs={'pk': pk})
        context['message'] = _('delete_form_template_item_message').format(form_template_item)
        return form_template_item

    def execute(form_template_item):
        form_template_item.delete()
        form_template_renumber(form_template_item.template)

    return confirm(request, 'delete', prepare, execute, reverse('django:form_template_items'))
