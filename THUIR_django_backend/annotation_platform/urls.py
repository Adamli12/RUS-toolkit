from django.conf.urls import include, url

from django.contrib import admin
from . import views
from django.views import static
from . import settings
import user_system
import task_manager
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'annotation_platform.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('user_system.urls')),
    url(r'^task/', include('task_manager.urls')),
    url(r'^$', views.index),
]
