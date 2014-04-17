from django.conf.urls import patterns, include, url
from vpnlist.views import ip_list, ping_ip, item_select, homepage, dl_file, get_serv_info
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^$', homepage),
                       url(r'^download/(.*)/$', dl_file),
                       url(r'^iplist/$', ip_list),
                       url(r'^ping/(.*)/$', ping_ip),
                       url(r'^select/(.*)/(.*)/$', item_select),
                       url(r'^getinfo/(.*)/$', get_serv_info),
                       url(r'^admin/', include(admin.site.urls)),
                    )