{#- Get the `tplroot` from `tpldir` #}
{%- set tplroot = tpldir.split('/')[0] %}

{%- from tplroot ~ "/map.jinja" import mapdata as forescout with context %}

ForeScout SecureConnector Dependencies Installed:
  pkg.installed:
    - pkgs:
        - bzip2
        - wget

ForeScout SecureConnector Archive Extracted:
  archive.extracted:
    - name: {{ forescout.package.archive.extract_directory }}
    - source: {{ forescout.package.archive.source }}
    - source_hash: {{ forescout.package.archive.source_hash }}
    - user: root
    - group: root
    - mode: 0700

{%- if forescout.package.daemon.get('source') %}
ForeScout SecureConnector Daemon Installed:
  pkg.installed:
    - sources:
      - {{ forescout.package.daemon.name }}: {{ forescout.package.daemon.source }}
    - skip_verify: True
    - require_in:
      - cmd: ForeScout SecureConnector Installed
{%- endif %}

ForeScout SecureConnector Installed:
  cmd.run:
    - name: {{ forescout.package.archive.extract_directory }}/{{ forescout.package.install_cmd }}
    - unless: {{ forescout.package.installed_test }}
    - require:
      - archive: ForeScout SecureConnector Archive Extracted
      - pkg: ForeScout SecureConnector Dependencies Installed
