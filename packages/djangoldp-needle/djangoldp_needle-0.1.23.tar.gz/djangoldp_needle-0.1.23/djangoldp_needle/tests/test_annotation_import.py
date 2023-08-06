import requests_mock
from django.db import transaction
from djangoldp_account.models import LDPUser
from rest_framework.test import APITestCase, APIClient, APITransactionTestCase
import json
from pkg_resources import resource_string

from ..models import AnnotationTarget, Annotation, NeedleActivity

from ..models.needle_activity import ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS, \
    ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS, ACTIVITY_TYPE_NEW_USER

from ..management.commands.needle_old_data import needleImportDatas
from ..views.annotation import import_external_annotation

class TestAnnotationTargetAdd(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_import_old_needle_data(self):
        user_name = "Chenille 30011407"
        user_email="test@test.test"
        user_creation_date="2018-02-18 20:54:54"
        target_url="http://tempsreel.nouvelobs.com/monde/20160129.OBS3681/l-etat-islamique-est-une-revolution-par-scott-atran.html"
        target_title="L'Etat islamique est une révolution, par Scott Atran - L'Obs"
        target_creation_date="2016-02-03 14:27:20"
        annotation_description="#anthropologie #radicalisation"
        annotation_date="2016-02-03 14:27:20"
        annotation_tags="anthropologie  radicalisation"

        import_external_annotation(user_name, user_email, user_creation_date, target_url, target_title,
                                   target_creation_date, annotation_description, annotation_date, annotation_tags,
                                   " ", None)
