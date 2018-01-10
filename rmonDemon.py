#!/usr/bin/python
import daemon

from rmonAgent import rmonAgent

with daemon.DaemonContext():
    rmonAgent()