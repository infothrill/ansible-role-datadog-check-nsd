# -*- coding: utf-8 -*-
"""
Datadog check for NSD (https://www.nlnetlabs.nl/projects/nsd/)

This will use the nsd provided command line tool nsd-control to query for
statistics, parse the stdout and feed them into datadog.
See also https://www.nlnetlabs.nl/projects/nsd/nsd-control.8.html
"""
import os

from checks import AgentCheck
from utils.subprocess_output import get_subprocess_output

METRIC_PREFIX = "nsd."


class NsdCheck(AgentCheck):
    def check(self, instance):
        config = self._get_config(instance)
        tags = config['tags']
        metrics = config['metrics']
        self._get_nsd_control_stats(tags, metrics)

    def _get_config(self, instance):
        tags = instance.get('tags', [])
        metrics = instance.get('metrics', [])

        instance_config = {
            'tags': tags,
            'metrics': metrics,
        }
        return instance_config

    def _get_nsd_control_stats(self, tags, metrics):
        output = None
        if os.geteuid() == 0:
            # dd-agent is running as root (not recommended)
            output = get_subprocess_output(['nsd-control', 'stats'], self.log,
                                           False)
        else:
            # can dd-agent user run sudo?
            test_sudo = os.system('setsid sudo -l < /dev/null')
            if test_sudo == 0:
                output, _, _ = get_subprocess_output(
                    ['sudo', 'nsd-control', 'stats'],
                    self.log, False)
            else:
                raise Exception('The dd-agent user does not have sudo access')

        # map keys with counter vs gauge:
        keys = {
            "server0.queries": "c",
            "num.queries": "c",
            # time.boot=96270.772702
            # time.elapsed=8.148725
            "size.db.disk": "g",
            "size.db.mem": "g",
            "size.xfrd.mem": "g",
            "size.config.disk": "g",
            "size.config.mem": "g",
            "num.type.A": "c",
            "num.type.NS": "c",
            "num.type.MD": "c",
            "num.type.MF": "c",
            "num.type.CNAME": "c",
            "num.type.SOA": "c",
            "num.type.MB": "c",
            "num.type.MG": "c",
            "num.type.MR": "c",
            "num.type.NULL": "c",
            "num.type.WKS": "c",
            "num.type.PTR": "c",
            "num.type.HINFO": "c",
            "num.type.MINFO": "c",
            "num.type.MX": "c",
            "num.type.TXT": "c",
            "num.type.RP": "c",
            "num.type.AFSDB": "c",
            "num.type.X25": "c",
            "num.type.ISDN": "c",
            "num.type.RT": "c",
            "num.type.NSAP": "c",
            "num.type.SIG": "c",
            "num.type.KEY": "c",
            "num.type.PX": "c",
            "num.type.AAAA": "c",
            "num.type.LOC": "c",
            "num.type.NXT": "c",
            "num.type.SRV": "c",
            "num.type.NAPTR": "c",
            "num.type.KX": "c",
            "num.type.CERT": "c",
            "num.type.DNAME": "c",
            "num.type.OPT": "c",
            "num.type.APL": "c",
            "num.type.DS": "c",
            "num.type.SSHFP": "c",
            "num.type.IPSECKEY": "c",
            "num.type.RRSIG": "c",
            "num.type.NSEC": "c",
            "num.type.DNSKEY": "c",
            "num.type.DHCID": "c",
            "num.type.NSEC3": "c",
            "num.type.NSEC3PARAM": "c",
            "num.type.TLSA": "c",
            "num.type.SPF": "c",
            "num.type.NID": "c",
            "num.type.L32": "c",
            "num.type.L64": "c",
            "num.type.LP": "c",
            "num.type.EUI48": "c",
            "num.type.EUI64": "c",
            "num.opcode.QUERY": "c",
            "num.class.IN": "c",
            "num.rcode.NOERROR": "c",
            "num.rcode.FORMERR": "c",
            "num.rcode.SERVFAIL": "c",
            "num.rcode.NXDOMAIN": "c",
            "num.rcode.NOTIMP": "c",
            "num.rcode.REFUSED": "c",
            "num.rcode.YXDOMAIN": "c",
            "num.edns": "c",
            "num.ednserr": "c",
            "num.udp": "c",
            "num.udp6": "c",
            "num.tcp": "c",
            "num.tcp6": "c",
            "num.answer_wo_aa": "c",
            "num.rxerr": "c",
            "num.txerr": "c",
            "num.raxfr": "c",
            "num.truncated": "c",
            "num.dropped": "c",
            "zone.master": "g",
            "zone.slave": "g",
        }
        if len(metrics) == 0:
            # if no metrics were configured, report all metrics
            metrics = list(keys.keys())

        for line in output.splitlines():
            key, value = line.strip().split("=", 2)
            if key in keys and key in metrics:
                if keys[key] == 'g':
                    self.gauge(METRIC_PREFIX + key, int(value), tags=tags)
                elif keys[key] == 'c':
                    self.count(METRIC_PREFIX + key, int(value), tags=tags)
