import ConfigParser
from fabric.context_managers import cd, prefix
from fabric.operations import require, sudo, get, put
from path import path
from fabric.api import run, env
from fabric.decorators import task

LOCAL_PATH = path(__file__).abspath().parent


def enviroment(location='staging'):
    config = ConfigParser.RawConfigParser()
    config.read(LOCAL_PATH / 'fabenv.ini')
    env.update(config.items(section=location))
    env.sandbox_activate = path(env.sandbox) / 'bin' / 'activate'
    env.deployment_location = location


@task
def staging():
    enviroment('staging')


@task
def production():
    enviroment('production')


@task
def deploy():
    require('project_root')

    with cd(env.project_root), prefix('source %(sandbox_activate)s' % env):
        run('git pull --rebase')
        run('pip install -r requirements.txt')
        run('python manage.py db upgrade')
        run('supervisorctl -c ../supervisord.conf restart all')


@task
def export():
    require('project_root')

    with cd(env.project_root), prefix('source %(sandbox_activate)s' % env):
        run('mkdir -p /tmp/export')
        run('python manage.py export all_species -d /tmp/export')
        run('python manage.py export all_habitat -d /tmp/export')
        run('tar czf /tmp/export.tgz /tmp/export/*')
        get('/tmp/export.tgz', '.')
        run('rm -rf /tmp/export.tgz /tmp/export')


@task
def upload_data():
    require('refval_dir')

    with cd(env.refval_dir):
        put('data/species.json', '.')
        put('data/habitats.json', '.')
