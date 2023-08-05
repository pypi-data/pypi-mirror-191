import time
from genericpath import exists
from os.path import abspath, join, dirname
import requests

from sqlalchemy import create_engine
from sqlalchemy import text

from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

from django.core.management.base import BaseCommand
from project_center.models import Project, ProjectCategory, ProjectStatus, ProjectStage, ProjectActivity, User, Company
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.timezone import make_aware
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group


def full_path(filename):
    return abspath(join(dirname(__file__), filename))


class Command(BaseCommand):
    help = """Sets up the project center following installation"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit', action='store', dest='limit', default=None,
            help="Import Limit"
        )
        parser.add_argument(
            '--order', action='store', dest='order', default=None,
            help="Import Order"
        )
        parser.add_argument(
            '--reset', action='store_true', dest='reset', default=False,
            help="Clear all projects before importing"
        )
    def handle(self, *args, **options):

        reset = options['reset']
        tic = time.perf_counter()
        if reset:
            groups = Group.objects.all().delete()

        toc = time.perf_counter()
        print(toc - tic)
        # if user:
        #     user.delete()

        # for x in (get_candidate_data_rest(candidate_id).keys()):
        #     print(x)