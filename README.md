ansible-role-auditbeat
=========

An Ansible role that replaces auditd with Auditbeat. Included modified version of rules from [bfuzzy1/auditd-attack](https://github.com/bfuzzy1/auditd-attack). 

![MITRE ATT&CK framework mapping](https://raw.githubusercontent.com/j91321/ansible-role-auditbeat/master/extras/layer.svg?sanitize=true)

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
      type: elasticsearch
      elasticsearch:
        hosts:
          - "localhost:9200"
        security:
          enabled: false

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
          ssl_certificate_authorities:
            - "/etc/ca/my_ca.crt"

Specifies the output configuration to Elasticsearch with security enabled, certificate authority must be present on server.

Variable `auditbeat_output.type` takes two values either `logstash` or `elasticsearch`. This is because if you have ansible `hash_behaviour` set to `merge` role would install both elasticsearch and logstash outputs when using logstash output type which is wrong.

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
              - "172.16.0.13:9200"
            security:
              enabled: true
              username: auditbeat
              password: auditbeatpassword
              protocol: http


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

