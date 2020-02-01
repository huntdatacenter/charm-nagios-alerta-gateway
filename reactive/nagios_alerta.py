#!/usr/bin/env python

from charmhelpers.contrib.ansible import apply_playbook
from charmhelpers.core.hookenv import application_version_set
from charmhelpers.core.hookenv import hook_name
from charmhelpers.core.hookenv import log
from charmhelpers.core.hookenv import status_set
from charms.reactive.decorators import hook
from charms.reactive.decorators import when
from charms.reactive.decorators import when_not
from charms.reactive.flags import clear_flag
from charms.reactive.flags import register_trigger
from charms.reactive.flags import set_flag


register_trigger(when='config.changed', clear_flag='gateway.configured')


@when_not('gateway.version')
def set_version():
    try:
        with open(file='repo-info') as f:
            for line in f:
                if line.startswith('commit-short'):
                    commit_short = line.split(':')[-1].strip()
                    application_version_set(commit_short)
    except IOError:
        log('Cannot set application version. Missing repo-info file.')
    set_flag('gateway.version')


@when_not('config.set.api_key')
@when_not('alerta-host.available')
def missing_alerta():
    if hook_name() == 'update-status':
        status_set('waiting', 'waiting on relation to alerta')
    else:
        status_set('blocked', 'missing relation to alerta')


@when_not('config.set.api_key')
@when('alerta-host.available')
def missing_key():
    status_set('blocked', 'missing alerta api_key')


@when_not('gateway.installed')
@when_not('gateway.configured')
@when('config.set.api_key')
@when('alerta-host.available')
def install():
    status_set('maintenance', 'installing nagios-alerta')
    apply_playbook(playbook='ansible/playbook.yaml', tags=['install'])
    status_set('active', 'ready')
    set_flag('gateway.configured')
    set_flag('gateway.installed')


@when_not('gateway.configured')
@when('gateway.installed')
@when('config.set.api_key')
@when('alerta-host.available')
def configure():
    status_set('maintenance', 'configuring nagios-alerta')
    apply_playbook(playbook='ansible/playbook.yaml', tags=['config'])
    status_set('active', 'ready')
    set_flag('gateway.configured')


# Hooks
@hook('upgrade-charm')
def upgrade_charm():
    clear_flag('gateway.version')
    clear_flag('gateway.configured')
    clear_flag('gateway.installed')
