from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'todo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', 'todo.web.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('todo.api.urls')),
    url(r'^signin/', 'userena.views.signin', {'template_name': 'accounts/signin.html'}, name="signin"),
    url(r'^signup/', 'userena.views.signup', {'template_name': 'accounts/signup.html', 'success_url': '/'}, name="signup"),
    url(r'^signout/', 'userena.views.signout', {'next_page': '/'}, name="singout"),
)
