from django.urls import path

from .views import CheckElementView, RefbookElementView, RefbookListView

urlpatterns = [
    path("refbooks/", RefbookListView.as_view(), name="refbooks-list"),
    path("refbooks/<int:id>/elements/", RefbookElementView.as_view(), name="refbooks-elements"),
    path("refbooks/<int:id>/check_element/", CheckElementView.as_view(), name="check-element"),
]
