from django.core.exceptions import SuspiciousOperation
from django.core.exceptions import ObjectDoesNotExist
from djangoldp.views import LDPViewSet, LDPNestedViewSet
from djangoldp_account.models import LDPUser
from rest_framework.exceptions import ValidationError

from ..models import Annotation, NeedleActivity, AnnotationTarget, Tag
from ..models.needle_activity import ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS, \
    ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS
import json
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import random
import string
import requests as requestsLib
from ..request_parser import RequestParser
from requests.exceptions import ReadTimeout, ConnectionError
from django.conf import settings


class AnnotationViewset(LDPViewSet):
    def is_safe_create(self, user, validated_data, *args, **kwargs):
        # TODO: check new annotation owner by current user

        target_url_id = validated_data['target']['urlid']
        user_annotation_with_same_target_count = Annotation.objects.filter(creator=user).filter(
            target__urlid=target_url_id).count()

        if user_annotation_with_same_target_count > 0:
            raise ValidationError({'Attention': ['Vous avez déjà cette ressource dans votre fil.']})
        return True

    def get_queryset(self, *args, **kwargs):
        param_user = LDPUser.objects.get(slug=self.kwargs['slug'])
        return Annotation.objects.filter(creator=param_user)


def create_first_annotation_activity_annotation_with_connections(annotation):
    first_annotation_activity = NeedleActivity(activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS,
                                               title="Grâce à votre fiche, vous croisez déjà d'autres personnes",
                                               content="Découvrez leurs Fils pour faire de nouvelles trouvailles.",
                                               creator=annotation.creator)
    first_annotation_activity.save()


def create_first_annotation_activity_annotation_without_connections(annotation):
    new_annotation_target_activity = NeedleActivity(activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS,
                                                    title="Votre fiche sort de l'ordinaire",
                                                    content="vous êtes la première personne à l'avoir ajoutée à votre Fil.\nAjoutez-en d'autres pour augmenter vos chances de croiser les Fils d'autres personnes, ou bien parcourez les carnets publics existants.",
                                                    creator=annotation.creator)
    new_annotation_target_activity.save()


def create_first_annotation_activity_first_annotation_with_connections(annotation):
    first_annotation_activity = NeedleActivity(activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS,
                                               title="Grâce à votre première fiche, vous croisez déjà d'autres personnes",
                                               content="Découvrez leurs Fils pour faire de nouvelles trouvailles.",
                                               creator=annotation.creator)
    first_annotation_activity.save()


def create_first_annotation_activity_first_annotation_without_connections(annotation):
    new_annotation_target_activity = NeedleActivity(activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS,
                                                    title="Votre première fiche sort de l'ordinaire",
                                                    content="vous êtes la première personne à l'avoir ajoutée à votre Fil.\nAjoutez-en d'autres pour augmenter vos chances de croiser les Fils d'autres personnes, ou bien parcourez les carnets publics existants.",
                                                    creator=annotation.creator)
    new_annotation_target_activity.save()


def init_webdriver():
    firefoxOptions = webdriver.FirefoxOptions()
    firefoxOptions.headless=True
    path = settings.BROWSER_PATH
    driver = webdriver.Firefox(firefox_binary=FirefoxBinary(path)
                                ,                              options=firefoxOptions
                               )
    # chromeOptions = webdriver.ChromeOptions()
    # chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # chromeOptions.add_argument("--no-sandbox")
    # chromeOptions.add_argument("--disable-setuid-sandbox")
    # chromeOptions.add_argument("--disable-dev-shm-usage")
    # chromeOptions.add_argument("--disable-extensions")
    # chromeOptions.add_argument("--disable-gpu")
    # chromeOptions.add_argument("start-maximized")
    # chromeOptions.add_argument("disable-infobars")
    # chromeOptions.add_argument("--headless")
    # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
    #                           options=chromeOptions)
    return driver

def import_external_annotations(external_annotations, annotation_tags_separator):
    driver = init_webdriver()
    index = 0
    for external_annotation in external_annotations:
        index = index + 1
        user_name = external_annotation["user_name"]
        user_email = external_annotation["user_email"]
        user_creation_date = external_annotation["user_creation_date"]
        target_url = external_annotation["target_url"]
        target_title = external_annotation["target_title"]
        target_creation_date = external_annotation["target_creation_date"]
        annotation_description = external_annotation["annotation_description"]
        annotation_date = external_annotation["annotation_date"]
        annotation_tags = external_annotation["annotation_tags"]
        import_external_annotation(user_name, user_email, user_creation_date, target_url, target_title,
                                   target_creation_date, annotation_description, annotation_date, annotation_tags,
                                   annotation_tags_separator, driver)
    print("annotations treated :" + index)


def import_external_annotation(user_name, user_email, user_creation_date, target_url, target_title,
                               target_creation_date, annotation_description, annotation_date, annotation_tags,
                               annotation_tags_separator, driver):
    if driver is None:
        driver = init_webdriver()

    user = None
    print("[USER] " + user_email)
    try:
        user = LDPUser.objects.get(email=user_email)
    except ObjectDoesNotExist:
        print("")
    if user is None:
        print("[USER] NEW " + user_email)
        password = ''.join(random.choices(string.ascii_lowercase, k=5))
        user = LDPUser(email=user_email, first_name='', last_name='',
                       username=user_name,
                       password=password,
                       date_joined=user_creation_date
                       )
        user.save()
    # else:
        # print("user already exists")

    target = None

    targetUrl = target_url

    print("[TARGET] " + targetUrl)
    try:
        target = AnnotationTarget.objects.get(target=targetUrl)
    except ObjectDoesNotExist:
        print("")

    target_content = None

    if target is None:

        targetRequestResponse = False
        try:
            targetRequestResponse = requestsLib.get(targetUrl, verify=False,
                                                    allow_redirects=True, timeout=10)
            # print("target request response code  " + str(targetRequestResponse.status_code))
        except ReadTimeout:
            targetRequestResponse = False
        except ConnectionError:
            targetRequestResponse = False
        if targetRequestResponse and targetRequestResponse.status_code != 200:
            # print("target new use request failed -> use selenium ")
            try:
                # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                #                           options=chromeOptions)
                driver.get(targetUrl)
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
                target_content = driver.page_source
            except TimeoutException:
                print("")
            # finally:
            #     driver.close()
        # else:
        #     target_content = targetRequestResponse.content

    if target_content is not None:
        # print("[TARGET_CONTENT] " + str(target_content))
        parser = RequestParser()
        (result, annotation_target) = parser.parse(targetUrl, target_content)
        try:
            annotation_target_tmp = AnnotationTarget.objects.get(target=annotation_target.target)
            # print("existing target")
            annotation_target = annotation_target_tmp
        except ObjectDoesNotExist:
            # print("no existing target")
            print("[TARGET] NEW " + annotation_target.target)
            annotation_target.save()
        target = annotation_target
    else:
        print("")

    tags = None

    if annotation_tags is not None:
        # print("has tags " + annotation_tags)
        tags = []
        for tagname in annotation_tags.split(annotation_tags_separator):
            # print("has tag " + tagname)
            if len(tagname) > 0:
                tagname = tagname.strip()
                if len(tagname) > 0:
                    if tagname.startswith("#"):
                        tagname = tagname[1:].strip()
                    if len(tagname) > 0:
                        tag = None
                        try:
                            tag = Tag.objects.get(name=tagname)
                        except ObjectDoesNotExist:
                            print("")
                        if tag is None:
                            print("[TAG] NEW " + tagname)
                            tag = Tag(name=tagname)
                            tag.save()
                            tags.append(tag)
                        # else:
                        #     print("tag already exists")

    user_annotation_with_same_target_count = Annotation.objects.filter(creator=user, target=target).count()
    if user_annotation_with_same_target_count == 0:
        print("[ANNOTATION] NEW ")
        if tags is None:
            annotation = Annotation(creation_date=annotation_date,
                                    target=target,
                                    creator=user,
                                    description=annotation_description)
        else:
            annotation = Annotation(creation_date=annotation_date,
                                    target=target,
                                    creator=user,
                                    description=annotation_description)
            annotation.save()
            annotation.tags.set(tags)
        annotation.save()
        if tags is not None:
            for tag in tags:
                annotation.tags.add(tag)
            annotation.save()
    # else:
    #     print("annotation already exists")
