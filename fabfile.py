"""Fabric configuration for harshp.com

host = bitnami@harshp.com
key  = harshp.pem

prepare_deployment:
    run tests

deploy:
    cd to project directory
    discard any changes
    pull project code
    restart apache

"""

from fabric.api import local
from fabric.api import run
from fabric.api import env
from fabric.api import cd

env.hosts = ['bitnami@harshp.com']
env.key_filename = '~/.ssh/harshp.pem'
project_dir = "/opt/bitnami/apps/django/django_projects/harshp.com/"


def prepare_deployment():
    """Prepare for deployment
    """
    pass


def l_test():
    """local: run tests
    """
    local('python manage.py test')


def l_migrate():
    """local: make migrations and migrate
    """
    local('python manage.py makemigrations')
    local('python manage.py migrate')


def migrate():
    """make migrations and migrate
    """
    with cd(project_dir):
        run("./manage.py migrate")


def restart():
    """restart server
    """
    run("sudo /opt/bitnami/ctlscript.sh restart apache")


def git_update():
    """update git master repo
    """
    with cd(project_dir):
        run("sudo git checkout .")
        run("sudo git checkout master")
        run("sudo git pull")


def install_dependencies():
    """install dependencies via pip
    """
    with cd(project_dir):
        run("sudo pip install -r harshp/requirements/requirements_prod.txt")


def deploy():
    """Deploy to host
    """
    install_dependencies()
    git_update()
    migrate()
    restart()
