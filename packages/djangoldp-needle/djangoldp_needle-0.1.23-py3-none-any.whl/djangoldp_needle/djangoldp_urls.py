from django.conf.urls import url
from django.urls import path
from .models import Annotation, Tag, AnnotationTarget, NeedleActivity, AnnotationIntersectionRead, ContactMessage
from .views import AnnotationViewset, AnnotationTargetViewset, TagViewset, AnnotationTargetIntersectionViewset, \
    AnnotationIntersectionsAfterViewset, AnnotationIntersectionsBeforeViewset, AnnotationIntersectionReadViewset, \
    ContactMessageView

urlpatterns = [
    url(r'^annotationtargets/', AnnotationTargetViewset.urls(model_prefix="annotationtarget", model=AnnotationTarget)),
    url(r'^annotationintersectionreads/', AnnotationIntersectionReadViewset.urls(model_prefix="annotationintersectionread", model=AnnotationIntersectionRead)),
    path('annotationtargetsintersection/<url>/<date>', AnnotationTargetIntersectionViewset.as_view({'get': 'list'}, model=AnnotationTarget)),
    path('annotationintersections/before/<url>/<date>',
        AnnotationIntersectionsBeforeViewset.as_view({'get': 'list'}, model=Annotation)),
    path('annotationintersections/after/<url>/<date>',
        AnnotationIntersectionsAfterViewset.as_view({'get': 'list'}, model=Annotation)),
    url(r'^users/(?P<slug>[\w\-\.]+)/yarn/', AnnotationViewset.urls(model_prefix="yarn", model=Annotation)),
    url(r'^users/(?P<slug>[\w\-\.]+)/tags', TagViewset.urls(model_prefix="tags", model=Tag)),
    url(r'^contact_messages/', ContactMessageView.as_view({'post': 'create'},  model=ContactMessage))
]
