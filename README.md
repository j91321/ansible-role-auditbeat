ansible-role-auditbeat
=========

An Ansible role that replaces auditd with Auditbeat. Included modified version of rules from [bfuzzy/auditd-attack](https://github.com/bfuzzy/auditd-attack). 

Please test the rules properly before using on production. Some rules may cause performance impact depending on your setup. For more information on Auditbeat please visit the official [documentation](https://www.elastic.co/guide/en/beats/auditbeat/current/auditbeat-overview.html)

Supported platfroms:
- Ubuntu 18.04
- Ubuntu 16.04
- CentOS 7
- CentOS 6
- Debian 9
- Debian 8

Auditbeat should also work on Oracle Enterprise Linux but only with RHCK.

If you wish to run Auditbeat from docker container use the official docker [image](https://hub.docker.com/_/auditbeat) provided by Elastic.

Requirements
------------

None

Role Variables
--------------
Ansible variables from `defaults/main.yml`

    auditbeat_output:
      elasticsearch:
        hosts:
          - "localhost:9200"
        security:
          enabled: false

Specifies the output configuration to Elasticsearch without Security enabled.

    auditbeat_output:
      elasticsearch:
        hosts:
          - "localhost:9200"
        security:
          enabled: true
          username: auditbeat_writer
          password: pa$$word
          protocol: https
          ssl_certificate_authorities:
            - "/etc/ca/my_ca.crt"

Specifies the output configuration to Elasticsearch with security enabled, certificate authority must be present on server.

Ansible variables from `vars/main.yml`

    auditbeat_service:
      config_path: /etc/auditbeat
      install_rules: true
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

These variables are the auditbeat defaults and fit most common use-cases. The `auditbeat_service.install_rules` can be changed to false if you don't want to use the rules included.

Dependencies
------------

None

Example Playbook
----------------


    - name: Install auditbeat
      hosts:
        - linux
      vars:
        auditbeat_output:
          elasticsearch:
            hosts:
              - "172.16.0.11:9200"
              - "172.16.0.12:9200"
              - "171.16.0.13:9200"
            security:
              enabled: true
              username: auditbeat
              password: auditbeatpassword
              protocol: http

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

