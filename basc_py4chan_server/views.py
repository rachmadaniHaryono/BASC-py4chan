from flask_admin import AdminIndexView, expose

INDEX_TEMPLATE = 'basc_py4chan/index.html'


class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render(INDEX_TEMPLATE)
