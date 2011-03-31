import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric import utils
from fabric.decorators import hosts



env.home = '/home/nick/code/python/'
env.project = 'beersocial'


def _setup_path():
    env.root = env.home
    env.virtualenv_root = os.path.join(env.root, env.project)
    env.git_dir = os.path.join(env.home, env.virtualenv_root, 'src')
    env.code_root = os.path.join(env.git_dir, env.project)
    env.settings = '%(environment)s_settings' % env


def staging():
    """ use staging environment on remote host"""
    env.user = 'nick'
    env.environment = 'staging'
    env.hosts = ['174.143.233.144:30000']
    _setup_path()


def production():
    """ use production environment on remote host"""
    utils.abort('Production deployment not yet implemented.')


def bootstrap():
    """ initialize remote host environment (virtualenv, deploy, update) """
    require('root', provided_by=('staging', 'production'))
    run('mkdir -p %(root)s' % env)
    run('mkdir -p %s' % os.path.join(env.home, 'log'))
    create_virtualenv()
    deploy()
    run('export PYTHONPATH=/home/nick/code/python/beersocial/src/beersocial:$PYTHONPATH')
    run('/home/nick/code/python/beersocial/bin/python %s syncdb --settings=%s' %
            (os.path.join(env.git_dir, 'beersocial', 'manage.py'), env.settings) )
    run('/home/nick/code/python/beersocial/bin/python %s migrate --settings=%s' %
            (os.path.join(env.git_dir, 'beersocial', 'manage.py'), env.settings) )


def create_virtualenv():
    """ setup virtualenv on remote host """
    require('virtualenv_root', provided_by=('staging', 'production'))
    args = '--clear --distribute --no-site-packages'
    try:
        run('rm -rf %s' % env.virtualenv_root)
    except:
        pass
    
    run('virtualenv %s %s' % (args, env.virtualenv_root))
    run('mkdir -p %s' % env.git_dir)
    with cd("%s" % env.git_dir):
        run('git clone git://github.com/fxdgear/beersocial.git')

def deploy():
    """ rsync code to remote host """
    require('root', provided_by=('staging', 'production'))
    if env.environment == 'production':
        if not console.confirm('Are you sure you want to deploy production?',
                               default=False):
            utils.abort('Production deployment aborted.')
    with cd("%s" % os.path.join(env.git_dir, env.project)):
        run("find . -name '*.pyc' -delete" )
        run('git pull origin master')
    #update_requirements()
    touch()


def update_requirements():
    """ update external dependencies on remote host """
    require('code_root', provided_by=('staging', 'production'))
    requirements = os.path.join(env.virtualenv_root, 'src', env.project )
    with cd(requirements):
        cmd = ['pip install']
        cmd += ['-E %(virtualenv_root)s' % env]
        cmd += ['--requirement %s' % os.path.join(requirements, 'requirements.txt')]
        run(' '.join(cmd))


def touch():
    """ touch wsgi file to trigger reload """
    require('code_root', provided_by=('staging', 'production'))
    apache_dir = os.path.join(env.code_root, 'apache')
    with cd(apache_dir):
        run('touch %s.wsgi' % env.environment)


def update_apache_conf():
    """ upload apache configuration to remote host """
    require('root', provided_by=('staging', 'production'))
    source = os.path.join('apache', '%(environment)s.conf' % env)
    dest = os.path.join(env.home, 'apache.conf.d')
    put(source, dest, mode=0755)
    apache_reload()


def configtest():    
    """ test Apache configuration """
    require('root', provided_by=('staging', 'production'))
    run('apache2ctl configtest')


def apache_reload():    
    """ reload Apache on remote host """
    require('root', provided_by=('staging', 'production'))
    run('sudo /etc/init.d/apache2 reload')


def apache_restart():    
    """ restart Apache on remote host """
    require('root', provided_by=('staging', 'production'))
    run('sudo /etc/init.d/apache2 restart')


def symlink_django():    
    """ create symbolic link so Apache can serve django admin media """
    require('root', provided_by=('staging', 'production'))
    admin_media = os.path.join(env.virtualenv_root,
                               'src/django/django/contrib/admin/media/')
    media = os.path.join(env.code_root, 'media/admin')
    if not files.exists(media):
        run('ln -s %s %s' % (admin_media, media))


def reset_local_media():
    """ Reset local media from remote host """
    require('root', provided_by=('staging', 'production'))
    media = os.path.join(env.code_root, 'media', 'upload')
    local('rsync -rvaz %s@%s:%s media/' % (env.user, env.hosts[0], media))