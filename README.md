ansible-role-auditbeat
=========

[![GitHub license](https://img.shields.io/github/license/j91321/ansible-role-auditbeat?style=flat-square)](https://github.com/j91321/ansible-role-auditbeat/blob/master/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/j91321/ansible-role-auditbeat.svg?style=flat-square)](https://github.com/j91321/ansible-role-auditbeat/commit/master)
![Build](https://github.com/j91321/ansible-role-auditbeat/workflows/Molecule%20test%20and%20deploy/badge.svg)
[![Twitter](https://img.shields.io/twitter/follow/j91321.svg?style=social&label=Follow)](https://twitter.com/j91321)

An Ansible role that replaces auditd with Auditbeat. Included modified version of rules from [bfuzzy1/auditd-attack](https://github.com/bfuzzy1/auditd-attack).

![MITRE ATT&CK framework mapping](https://raw.githubusercontent.com/j91321/ansible-role-auditbeat/master/extras/layer.svg?sanitize=true)

Please test the rules properly before using on production. Some rules may cause performance impact depending on your setup. For more information on Auditbeat please visit the official [documentation](https://www.elastic.co/guide/en/beats/auditbeat/current/auditbeat-overview.html)

Supported platforms:
- Ubuntu 20.04
- Ubuntu 18.04
- Ubuntu 16.04
- CentOS 8
- CentOS 7
- CentOS 6
- Debian 10
- Debian 9
- Debian 8
- Gentoo \*\*
- Windows 10\*
- Windows Server 2019\*
- Windows Server 2016\*

Auditbeat should also work on Oracle Enterprise Linux but only with RHCK.

\* Auditbeat on Windows supports different set of features. If you wish to achieve similar functionality use Sysmon + Winlogbeat

\*\* If you want to run auditbeat on Gentoo, you will need to create your own ebuild, if you want to use the `system` metricset, you will need to build auditbeat with x-pack folder with the elastic licence. If you want to use Sockets, you will need Kprobe enabled in your kernel's menuconfig

If you wish to run Auditbeat from docker container use the official docker [image](https://hub.docker.com/_/auditbeat) provided by Elastic.

Requirements
------------

None

Role Variables
--------------
Ansible variables from `defaults/main.yml`

    auditbeat_service:
      install_path_windows64: "C:\\Program Files\\Elastic\\auditbeat"
      install_path_windows32: "C:\\Program Files\\Elastic\\auditbeat"
      version: "7.13.1"
      download: true
      config_path: /etc/auditbeat
      install_rules: true
      rule_file: auditd-attack.conf

    auditbeat_output:
      type: "elasticsearch"
      elasticsearch:
        hosts:
          - "localhost:9200"
        security:
          enabled: false
    auditbeat_processors: |
      - add_host_metadata: ~
      - add_cloud_metadata: ~
      - add_docker_metadata: ~
    auditbeat_portage:
      package: =auditbeat-{{ auditbeat_service.version }}
      getbinpkgonly: true

The `auditbeat_service.install_rules` can be changed to false if you don't want to use the rules included.

Variable `auditbeat_service.download` affects only Windows installations. If you don't want the clients to download the Windows zip package from the web, you can set it to `false` and place the Windows zip in `files/` folder. Please preserve the naming of the zip file e.g. `files/auditbeat-7.6.2-windows-x86.zip`.  

Specifies the output configuration to Elasticsearch without Security enabled.

    auditbeat_output:
      type: elasticsearch
      elasticsearch:
        hosts:
          - "localhost:9200"
        security:
          enabled: true
          username: auditbeat_writer
          password: pa$$word
          protocol: https
          ssl_verification_mode: certificate
          ssl_certificate_authorities:
            - "/etc/ca/my_ca.crt"

Specifies the output configuration to Elasticsearch with security enabled, certificate authority must be present on server.

Variable `auditbeat_output.type` takes three values either `logstash`, `elasticsearch` or `redis`. This is because if you have ansible `hash_behaviour` set to `merge` role would install both elasticsearch and logstash outputs when using logstash output type which is wrong.

Example of Redis output:

    auditbeat_output:
      type: redis
      redis:
        hosts:
          - 192.168.100.4
        password: "redis_password"
        key: "auditbeat"

Example of filtering high volume logs using processors

    auditbeat_processors: |
      - add_host_metadata: ~
      - add_cloud_metadata: ~
      - add_docker_metadata: ~
      - drop_event.when.and:
        - equals.event.action: "network_flow"
        - equals.server.port: 10050
        - equals.process.name: "zabbix_agentd"

Ansible variables from `vars/main.yml`

    auditbeat_module:
      auditd:
        enabled: true
       file_integrity:
        enabled: true
        paths:
          - /bin
          - /usr/bin
          - /sbin
          - /usr/sbin
          - /etc
      system:
        enabled: true
        datasets:
          - host
          - login
          - package
          - process
          - socket
          - user
    auditbeat_module_windows:
      file_integrity:
        enabled: true
        paths:
          - C:\windows
          - C:\windows\system32
          - C:\Program Files
          - C:\Program Files (x86)
      system:
        enabled: true
        datasets:
          - host
          - process

These variables are the auditbeat defaults and fit most common use-cases.

Dependencies
------------

None

Example Playbook
----------------

```
- name: Install auditbeat
  hosts:
    - linux
    - windows
  become: yes
  vars:
    auditbeat_service:
      install_path_windows32: "C:\\Program Files\\monitoring\\auditbeat"
      install_path_windows64: "C:\\Program Files\\monitoring\\auditbeat"
      version: "7.13.1"
      download: true
      install_rules: true
      rule_file: auditd-attack.conf
    auditbeat_template:
      enabled: false
    auditbeat_general:
      tags:
        - "auditbeat"
    auditbeat_output:
      type: "elasticsearch"
      elasticsearch:
        hosts:
          - "172.16.0.11:9200"
          - "172.16.0.12:9200"
          - "172.16.0.13:9200"
        security:
          enabled: true
          username: auditbeat
          password: auditbeatpassword
          protocol: http
  roles:
  - ansible-role-auditbeat
```

Extras
------

In the extras folder you can find several prepared Kibana saved searches based on [Sigma auditd rules](https://github.com/Neo23x0/sigma/tree/master/rules/linux/auditd). These saved searches will work with default index pattern auditbeat-\*. If you use different index pattern you must modify the saved objects with appropriate index pattern and field names.

Installation steps:

 1. Go to **Kibana->Management->Index Patterns**
 2. Click **Create index pattern**
 3. Into the **Index pattern field** write *auditbeat-** and click **Next step**
 4. Select *@timestamp* as **Time Filter field name**
 5. Click **Show advanced options**
 6.  Set **Custom index pattern** ID to *auditbeat-**
 7. Click **Create index pattern**

Next import the saved searches from this repository:

 1. Go to **Kibana->Management->Saved Objects**
 2. Click **Import**
 3. Select the saved search json file which you want to import
 4. Click **Import**
 5. Repeat for all saved searches

License
-------

MIT

Author Information
------------------

j91321

Rules by: bfuzzy

Notes
-----

Tests require some further improvements. Waiting for beats issue [#8280](https://github.com/elastic/beats/issues/8280) to be resolved for better tests.
