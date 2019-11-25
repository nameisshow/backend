from django.db import IntegrityError
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse

from backend import helpers
from backend.helpers import SuccessResponseJson, ErrorResponseJson
from backend.models import Button, Module


def index(request):
    return HttpResponse('hello world')


def button_list(request, page=1):
    """
    按钮列表
    :param request:
    :param page:
    :return:
    """
    name = request.GET.get('name', '')
    event = request.GET.get('event', '')
    where = search = {}
    if name:
        where.update({'name': name})
        search.update({'name': name})
    if event:
        where.update({'event': event})
        search.update({'event': event})
    if len(where) > 0:
        buttons = Button.objects.filter(**where)
    else:
        buttons = Button.objects.all()
    # buttons = Button.objects.get(pk=5)
    # print(Button.objects.print(pk=5))
    result = helpers.get_page_result(buttons, page, 10)
    context = {'pageData': result}
    context.update({'pageUrl': 'button'})
    context.update({'pageNow': page})
    context.update({'search': search})
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
        return ErrorResponseJson('删除错误，参数为空')()
    rows, _ = Button.objects.filter(pk=pk).delete()
    if rows == 0:
        return ErrorResponseJson('没有内容被删除')()
    return SuccessResponseJson('success')()


def module_list(request, page=1):
    """
    模块列表
    :param request:
    :param page:
    :return:
    """
    # if name:
    #     where.update({'name__contains': name})  # __contains模糊查询
    #     search.update({'name': name})
    modules = Module.objects.all().filter(level=1)
    module_top = helpers.get_page_result(modules, page, 10)
    for mt in module_top:
        module_middle = Module.objects.filter(level=2, pid=mt.id)
        mt.module_middle = module_middle
        for mm in module_middle:
            module_low = Module.objects.filter(level=3, pid=mm.id)
            mm.module_low = module_low
            for ml in module_low:
                buttons = ml.buttons.all()
                buttons_name = buttons.values('name')
                ml.buttons_str = ','.join([list(i.values())[0] for i in buttons_name])
    context = {'pageData': module_top}
    context.update({'pageUrl': 'module'})
    context.update({'pageNow': page})
    return render(request, 'backend/module_list.html', context)


def module_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        pid = request.POST.get('pid', None) if request.POST.get('pid', 0) else 0
        url = request.POST.get('url', '')
        sort = request.POST.get('sort', None) if request.POST.get('sort', 0) else 0
        if not name:
            return ErrorResponseJson('模块名为空')()
        if pid == 0:
            level = Module.MODULE_LEVEL_TOP
        else:
            parent_module = Module.objects.filter(id=pid)
            if len(parent_module) < 1:
                return ErrorResponseJson('父级菜单不存在')()
            parent_module = parent_module.get()
            if parent_module.level < Module.MODULE_LEVEL_LOW:
                level = parent_module.level + 1
            else:
                return ErrorResponseJson('菜单等级不合法')()
        module = Module(name=name, pid=pid, url=url, sort=sort, level=level)
        try:
            module.save()
        except IntegrityError:
            return ErrorResponseJson('唯一性字段重复')()
        return SuccessResponseJson('添加成功')()
    else:
        module_top = Module.objects.all().filter(level=1)
        for mt in module_top:
            module_middle = Module.objects.filter(level=2, pid=mt.id)
            mt.module_middle = module_middle
        context = {'module': module_top}
        context.update({'pageUrl': 'module_add'})
        return render(request, 'backend/module_add.html', context)


def module_edit(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        pid = request.POST.get('pid', None) if request.POST.get('pid', 0) else 0
        url = request.POST.get('url', '')
        sort = request.POST.get('sort', None) if request.POST.get('sort', 0) else 0

        if not name:
            return ErrorResponseJson('模块名不能为空')()
        if pid == 0:
            level = Module.MODULE_LEVEL_TOP
        else:
            parent_module = Module.objects.filter(id=pid)
            if len(parent_module) < 1:
                return ErrorResponseJson('父级菜单不存在')()
            parent_module = parent_module.get()
            if parent_module.level < Module.MODULE_LEVEL_LOW:
                level = parent_module.level + 1
            else:
                return ErrorResponseJson('菜单等级不合法')()

        module = Module.objects.get(pk=pk)
        module.name = name
        module.url = url
        module.pid = pid
        module.sort = sort
        module.level = level

        try:
            module.save()
        except IntegrityError:
            return ErrorResponseJson('唯一性字段重复')()
        return SuccessResponseJson('更新成功')()

    else:
        module_top = Module.objects.all().filter(level=1)
        for mt in module_top:
            module_middle = Module.objects.filter(level=2, pid=mt.id)
            mt.module_middle = module_middle
        info = Module.objects.get(pk=pk)
        context = {'info': info}
        context.update({'modules': module_top})
        context.update({'pageUrl': 'module_edit'})
        return render(request, 'backend/module_edit.html', context)


def module_delete(request, pk):
    if not pk:
        return ErrorResponseJson('主键为空')()
    rows, _ = Module.objects.filter(pk=pk).delete()
    if rows == 0:
        return ErrorResponseJson('没有内容被删除')()
    return SuccessResponseJson('success')()


def module_assign_button(request, pk):
    # pk = request.GET.get('id', 0)
    if request.method == 'POST':
        pass
    else:
        module = Module.objects.filter(pk=pk).first()
        buttons_in_module = module.buttons.filter()
        all_buttons = Button.objects.all()
        context = {'module_id': pk}
        context.update({'all_buttons': all_buttons})
        context.update({'buttons_in_module': buttons_in_module})
        context.update({'pageUrl': 'module_assign_button'})
        return render(request, 'backend/module_assign_button.html', context)
