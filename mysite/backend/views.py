from django.db import IntegrityError
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse

from backend import helpers
from backend.helpers import SuccessResponseJson, ErrorResponseJson
from backend.models import Button


def index(request):
    return HttpResponse('hello world')


def button_list(request, page=1):
    """
    按钮列表
    :param request:
    :param page:
    :return:
    """
    buttons = Button.objects.all()
    result = helpers.get_page_result(buttons, page, 10)
    context = {'pageData': result}
    context.update({'pageUrl': 'button'})
    context.update({'pageNow': page})
    return render(request, 'backend/button_list.html', context)


def button_add(request):
    """
    添加按钮
    :param request:
    :return:
    """
    if request.method == 'POST':
        name = request.POST.get('name', '')
        event = request.POST.get('event', '')
        sort = request.POST.get('sort', None) if request.POST.get('sort', 0) else 0
        error_message = None
        if name == '':
            error_message = '按钮名不能为空'
        if event == '':
            error_message = '按钮事件名不能为空'
        if error_message is not None:
            return ErrorResponseJson(error_message)()
        button = Button(name=name, event=event, type='', sort=sort)
        try:
            button.save()
        except IntegrityError as e:
            print(e)
            return ErrorResponseJson('唯一字段重复')()
        return SuccessResponseJson('success')()
    else:
        context = {}
        context.update({'pageUrl': 'button_add'})
        return render(request, 'backend/button_add.html', context)


def button_edit(request, pk):
    if request.method == 'POST':
        button_id = request.POST.get('id', 0)
        name = request.POST.get('name', '')
        event = request.POST.get('event', '')
        sort = request.POST.get('sort', 0)
        error_message = None
        if button_id == 0:
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


def button_delete(request, pk):
    """
    删除按钮
    :param request:
    :param pk:
    :return:
    """
    if not pk:
        raise Http404('删除错误，参数为空')
    rows, _ = Button.objects.filter(pk=pk).delete()
    if rows == 0:
        raise Http404('没有内容被删除')
    return HttpResponseRedirect(reverse('button', args=()))
