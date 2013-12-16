from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bluebear.views.home', name='home'),
    # url(r'^bluebear/', include('bluebear.foo.urls')),

    url(r'^$', 'todo.api.views.hello_world'),
    url(r'^list/', 'todo.api.views.api_list'),
    url(r'^tasks/', 'todo.api.views.tasks'),
)