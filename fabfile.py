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


def prepare_deployment():
    """Prepare for deployment

    Runs tests

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    local('python manage.py test')


def deploy():
    """Deploy to host

    Discard any changes and pull in updated repo. Finally, restart Apache

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    project_dir = "/opt/bitnami/apps/django/django_projects/harshp.com/"
    with cd(project_dir):
        run("sudo git checkout .")
        run("sudo git pull")
        run("sudo pip install -r requirements.txt")
        run("./manage.py migrate")
        run("sudo /opt/bitnami/ctlscript.sh restart apache")
