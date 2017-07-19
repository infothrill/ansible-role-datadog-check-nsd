# -*- coding: utf-8 -*-
"""
Datadog check for NSD (https://www.nlnetlabs.nl/projects/nsd/)

This will use the nsd provided command line tool nsd-control to query for
statistics, parse the stdout and feed them into datadog.
See also https://www.nlnetlabs.nl/projects/nsd/nsd-control.8.html
"""
import os
import re

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

        for metric in re.findall(r'(\S+)=(.*\d)', output):
            if len(metrics) == 0 or metric[0] in metrics:
                self.log.debug('nsd.{}:{}'.format(metric[0], metric[1]))
                if 'num.' in metric[0]:
                    self.rate(METRIC_PREFIX + metric[0], float(metric[1]), tags=tags)
                else:
                    self.gauge(METRIC_PREFIX + metric[0], float(metric[1]), tags=tags)
            #else:
            #    self.log.warn('nsd.{}:{}'.format(metric[0], metric[1]))
