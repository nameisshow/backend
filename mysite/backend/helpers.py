from django.db import models
from django.http import JsonResponse


def get_page_result(data_object, page, limit=10):
    """
    获取分页
    :param data_object:数据对象
    :param page: 页数
    :param limit: 每页数量
    :return:
    """
    from django.core.paginator import Paginator
    from django.core.paginator import PageNotAnInteger
    from django.core.paginator import EmptyPage
    paginator = Paginator(data_object, limit)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result


def get_response_json_data(status: bool, msg: str, data=None, level=0):
    if status is False:
        status = 500
    else:
        status = 200
    res = {'status': status, 'msg': msg, 'data': data, 'level': level}
    return res


class SuccessResponseJson(object):
    """
    返回正确的json
    """
    def __init__(self, msg='', data=None):
        self.res = get_response_json_data(True, msg, data)

    def __call__(self, *args, **kwargs):
        return JsonResponse(self.res)

    def __str__(self):
        return self.res

    def __repr__(self):
        return self.res


class ErrorResponseJson(object):
    """
    返回错误的json
    """
    def __init__(self, msg='', data=None, level=0):
        self.res = get_response_json_data(False, msg, data, level=level)

    def __call__(self, *args, **kwargs):
        return JsonResponse(self.res)

    def __str__(self):
        return self.res

    def __repr__(self):
        return self.res


def append_attr():
    def db_print(self, **kwargs):
        res = self.get(**kwargs)
        return {'id': res.id, 'name': res.name, 'event': res.event, 'type': res.type, 'sort': res.sort}

    models.Manager.print = db_print
