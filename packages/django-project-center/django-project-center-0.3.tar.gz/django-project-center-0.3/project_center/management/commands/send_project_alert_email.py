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
from project_center.utils import generate_email_body
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.timezone import make_aware
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group


def full_path(filename):
    return abspath(join(dirname(__file__), filename))


class Command(BaseCommand):
    help = """Sends a Project Alert email to a user or all users in a company"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--project_id', action='store', dest='project_id', default=None,
            help="Project ID"
        )
        parser.add_argument(
            '--user', action='store', dest='user', default=None,
            help="User Login"
        )
        parser.add_argument(
            '--company', action='store', dest='company', default=None,
            help="Group Name"
        )
    def handle(self, *args, **options):

        project_id = options['project_id']
        user_login = options['user']
        project = Project.objects.get(id=project_id)
        user = User.objects.get(username=user_login)
        email_subject = 'Your Project Has Changed - Project: {project_name}'.format(project_name=project.title)
        text = generate_email_body(
            html_template_path=full_path('../../templates/email/activity_alert.txt'),
            project=project
        )
        html = generate_email_body(
            html_template_path=full_path('../../templates/email/activity_alert.html'),
            project=project)
        print(user.send_project_alert_email(subject=email_subject, html=html, text=text))
        tic = time.perf_counter()
        # if reset:
        #     groups = Group.objects.all().delete()

        toc = time.perf_counter()
        print(toc - tic)
        # if user:
        #     user.delete()

        # for x in (get_candidate_data_rest(candidate_id).keys()):
        #     print(x)