# Knust

Knust is a Python module that implements a Raspberry Pi based thermostat. It uses DHT temperature sensors and switched electrical output expedcted to control a heater to regulate the temperature against a target. It installs two componnents, the `knust` service and the `brot` command line interface.

## Components

The thermostat runs as a system service called `knust` that provides the temperatur reading and manages the electrical outputs. The services makes itself available on DBUS.

The command line interface `brot` is used to define thermostat sessions, query the current status and to drop (delete) sessions.

Sessions are persisted, which means the service will continue sessions after a restart.

## Installation

The `knust` package is provided on PyPi:

    $ pip install knust>=0.5
    ...

## License informmation

The `knust` package is released under the APACHE-2 license.
