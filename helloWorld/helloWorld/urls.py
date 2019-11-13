"""helloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#include allows me to unclude another urls file

from django.contrib import admin
from django.urls import path, include # STEP 1
from django.conf import settings # new
from django.conf.urls.static import static # new

urlpatterns = [
    path('', include('helloWorldApp.urls')), # STEP 1
    path('admin/', admin.site.urls),
] + static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
    )

#if settings.DEBUG: # new
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# After Step 1, need create a urls.py for my helloWorldApp folder
# from urls, it checks to see if see if the request is asking for admin urls
# if it doesn't match that, go use the helloWorldApp.urls
# and find something that matches. If i tried to go to localhost/bob
# nothing would render because bob doesn't exist in helloWorldApp.urls
# GO TO helloWorldApp.urls