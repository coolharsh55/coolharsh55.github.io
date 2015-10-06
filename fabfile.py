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
from fabric.context_managers import settings

env.hosts = ['bitnami@harshp.com']
env.key_filename = '~/.ssh/harshp.pem'
project_dir = "/opt/bitnami/apps/django/django_projects/harshp.com/"


def test():
    """testrun"""
    print 'test'
    local('./manage.py test harshp --keepdb')


def prepare_deployment():
    """Prepare for deployment
    """
    pass


def sync_requirements(file_suffix):
    """sync requirements
    """
    local("pip-sync harshp/requirements/requirements_%s.txt" % file_suffix)


def update_requirements():
    """use pip-tools to update requirements
    """
    def pip_compile(file_suffix):
        """prepare statement to be run with the requirement file suffix
        """
        return ("pip-compile "
                "harshp/requirements/requirements_%s.in > "
                "harshp/requirements/requirements_%s.txt ") % (
                    file_suffix, file_suffix)

    local(pip_compile('dev'))
    local(pip_compile('prod'))
    local(pip_compile('test'))


def l_test():
    """local: run tests
    """
    def run_stmt(module, db):
        """construct the statement to be run"""
        s = ("coverage run "
             "-p --source={0} "
             "manage.py test {0} --{1} "
             "> testruns/{2}.txt").format(
            module, db, module)
        return s

    with settings(warn_only=True):
        # l_sync('test')
        local(run_stmt('blog', "noinput"))
        local(run_stmt('articles', 'keepdb'))
        local(run_stmt('stories', 'keepdb'))
        local(run_stmt('poems', 'keepdb'))
        local(run_stmt('lifeX', 'keepdb'))
        local(run_stmt('brainbank', 'noinput'))
        local(run_stmt('sitedata', 'keepdb'))
        local(run_stmt('hobbies', 'keepdb'))
        local(run_stmt('harshp', 'keepdb'))
        local(run_stmt('devblog', 'keepdb'))
        local('coverage combine')
        local('coverage html')


def l_migrate():
    """local: make migrations and migrate
    """
    local('python manage.py makemigrations')
    local('python manage.py migrate')


def l_compile(mode='dev'):
    """local: sync packages with requirements_dev.in
    """
    local('pip-compile harshp/requirements/requirements_%s.in' % mode)


def l_sync(mode='dev'):
    """local: sync packages with requirements_dev.in
    """
    l_compile(mode)
    local('pip-sync harshp/requirements/requirements_%s.txt' % mode)


def l_compile_all():
    """local: sycn all packages with requirements_xxx.in
    """
    l_compile('dev')
    l_compile('test')
    l_compile('prod')


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
        run("git checkout .")
        run("git checkout master")
        run("git pull origin master")


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
