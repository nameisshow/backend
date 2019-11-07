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
