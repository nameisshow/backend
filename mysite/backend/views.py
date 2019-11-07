from django.db import IntegrityError
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from backend import helpers
from backend.models import Button


def index(request):
    return HttpResponse('hello world')


def button_list(request, page=1):
    buttons = Button.objects.all()
    result = helpers.get_page_result(buttons, page, 2)
    context = {'pageData': result}
    context.update({'pageUrl': 'button'})
    return render(request, 'backend/button_list.html', context)


def button_edit(request, pk):
    if request.method == 'POST':
        button_id = request.POST.get('id', 0)
        name = request.POST.get('name', '')
        event = request.POST.get('event', '')
        sort = request.POST.get('sort', 0)
        error_message = None
        if id == 0:
            error_message = 'id为空'
        if name == '':
            error_message = '按钮名不能为空'
        if event == '':
            error_message = '按钮事件名不能为空'
        if error_message is not None:
            raise Http404(error_message)
        info = Button.objects.get(pk=button_id)
        info.name = name
        info.event = event
        info.sort = sort
        try:
            info.save()
        except IntegrityError:
            raise Http404('更新错误，唯一值重复')
        return HttpResponseRedirect(reverse('button', args=()))
    else:
        info = Button.objects.get(pk=pk)
        context = {'info': info}
        return render(request, 'backend/button_edit.html', context)
