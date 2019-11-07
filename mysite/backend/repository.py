from backend.models import Module


class Repository(object):

    def __init__(self):
        pass

    def get_button_list(self, page, per_page):
        pass

    @staticmethod
    def get_module_list():
        module = Module.objects.all()
        module.values_list()
