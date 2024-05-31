from django.urls import path
from .views import AllDataView

urlpatterns = [
    path('<str:lang>/combined/', AllDataView.as_view(), name='combined-view'),

]