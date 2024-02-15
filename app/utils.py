menu = [
    {'title': "Добавить продукт", 'url_name': 'addproduct'},
    {'title': "О нас", 'url_name': 'about'},
]


class DataMixin:
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context.update(kwargs)
        return context
