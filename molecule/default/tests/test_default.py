import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_auditbeat_package(host):
    package_auditbeat = host.package('auditbeat')
    assert package_auditbeat.is_installed


def test_auditbeat_config(host):
    config = host.file("/etc/auditbeat/auditbeat.yml")
    assert config.exists
    assert config.is_file


def test_auditbeat_rules(host):
    rules = host.file("/etc/auditbeat/audit.rules.d/auditd-attack.conf")
    assert rules.exists
    assert rules.is_file


def test_auditbeat_rules_installation(host):
    list_rules = host.run("auditbeat show auditd-rules")
    assert len(list_rules.stdout) > 
