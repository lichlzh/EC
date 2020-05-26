from django.conf.urls import url
from . import views
urlpatterns = [
    url('compute',views.compute),
    url('ERP',views.ERP),
    url('BOM',views.BOM),
    url('COA',views.COA),
    url('MAS',views.MAS),
    url('stk',views.stk),
    url('homepage',views.homepage),
    
    url('getbom',views.getbom),
    url('updbom',views.updbom),
    url('getmas',views.getmas),
    url('updmas',views.updmas),
    url('getcoa',views.getcoa),
    url('updcoa',views.updcoa),
    url('getstock',views.getstock),
    url('updstock',views.updstock)
]
