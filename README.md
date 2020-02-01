# Nagios-to-Alerta Gateway

![GitHub Action CI badge](https://github.com/huntdatacenter/charm-nagios-alerta-gateway/workflows/ci/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Usage

```
juju deploy cs:~huntdatacenter/nagios-alerta-gateway
juju deploy cs:~huntdatacenter/alerta
juju deploy nagios
juju add-relation nagios-alerta-gateway:alerta-host alerta:http
juju add-relation nagios-alerta-gateway:nagios-host nagios:juju-info
```

```
juju config nagios-alerta-gateway api_key=<key>
```

## Development

Here are some helpful commands to get started with development and testing:

```
lint                 Run linter
build                Build charm
deploy               Deploy charm
upgrade              Upgrade charm
force-upgrade        Force upgrade charm
test-bionic-bundle   Test Bionic bundle
push                 Push charm to stable channel
clean                Clean .tox and build
help                 Show this help
```

## Further information

### Links
