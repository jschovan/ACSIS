"""
    fetch_host_info ... get properties of ATLAS CS hosts
    
"""
import commands
import ConfigParser
import json
import logging
import os
import re
import sys
from datetime import datetime


class HostInfoFetcher(object):
    ### configuration
    _config_file = '/tmp/ACSIS/collectors/settings/host_info.cfg'
    _ts = datetime.utcnow().strftime('%F.%H%M%S')
    _config = None
    _logger = None
    ### logger
    _logger_name = 'host_info_fetcher'
    _logger_level = 'INFO'
    _logger_file = '/tmp/ACSIS/collectors/logs/logger.' + _logger_name + '.log'
    ### hosts
    _input_file = '/tmp/ACSIS/collectors/output/hosts_in_hostgroups.json'
    _hosts_in_hostgroups = {}
    _hosts = []
    _host_info = {}


    def __init__(self, config_file=None):
        if config_file is not None:
            self._config_file = config_file
        self.configure()


    def configure(self):
        self._config = ConfigParser.ConfigParser()
        self._config.read(self._config_file)
        ### logging config
        self.configure_logger()
        ### hosts list config
        self.configure_hosts()
        ### configure local file paths
        self.configure_local_paths()


    def configure_logger(self):
        self._logger_name = self._config.get("host_info", "log_name")
        self._logger_level = self._config.get("host_info", "log_level")
        self._logger_file = self._config.get("host_info", "log_file")
        self._logger = self.logger(self._logger_name, self._logger_level, self._logger_file)


    def configure_hosts(self):
        self._input_file = self._config.get("host_info", "input")
        ### Read input
        self.read_input_json()
        ### Get list of hosts in hostgroups
        self.get_all_hosts_names()
        ### hosts
        self._hosts = str(self._config.get("host_info", "hosts")).split(',')
        self._logger.debug('hosts: ' + str(self._hosts))
        if 'ALL' in self._hosts:
            self.get_all_hosts_names()
        self._logger.debug('hosts: ' + str(self._hosts))


    def configure_local_paths(self):
        self._dir_output = self._config.get("host_info", "dir_output")
        ### make sure _dir_output exists
        try:
            cmd = 'mkdir -p %(dirname)s' % {'dirname': self._dir_output}
            status, output = commands.getstatusoutput(cmd)
            if status != 0:
                self._logger.error('Ran [%(cmd)s]. Status [%(status)s]. Output[%(output)s]' \
                                   % {'cmd': cmd, 'status': str(status), 'output': output})
            else:
                self._logger.debug('Dir for output exists: ' + str(self._dir_output))
        except:
            pass


    def logger(self, log_title, log_level, log_file_name):
        LEVEL = {\
            'debug': logging.DEBUG, \
            'DEBUG': logging.DEBUG, \
            'info': logging.INFO, \
            'INFO': logging.INFO, \
            'warning': logging.WARNING, \
            'WARNING': logging.WARNING, \
            'error': logging.ERROR, \
            'ERROR': logging.ERROR, \
            'critical': logging.CRITICAL, \
            'CRITICAL': logging.CRITICAL \
        }
        logging.basicConfig(level=LEVEL[log_level],
                        format='%(asctime)s %(name)s:%(lineno)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_file_name,
                        filemode='a')
        #                    format='%(asctime)s %(name)-12s - %(module)s:%(funcName)s:%(lineno)d - %(levelname)-8s %(message)s',
        # formatter = logging.Formatter('%(name)-12s: - %(module)s:%(funcName)s:%(lineno)d - %(levelname)-8s %(message)s')
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        return logging.getLogger(log_title)


    def get_all_hosts_names(self):
        self._hosts = []
        for hg in self._hosts_in_hostgroups.keys():
            self._hosts.extend(self._hosts_in_hostgroups[hg])
            self._logger.info('Retrieved list of hosts for hostgroup [%(hg)s]' % \
                               {'hg': hg})
            self._logger.debug('List of hosts in hostgroup [%(hg)s]: [%(hosts)s]' % \
                               {'hg': hg, 'hosts': self._hosts_in_hostgroups[hg]})


    def get_host_info(self, hostname):
        if hostname not in self._host_info.keys():
            self._host_info[hostname] = []
        cmd = 'ai-dump --json %(hostname)s 2>/dev/null' % {'hostname': hostname}
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
            self._logger.error('Ran [%(cmd)s]. Status [%(status)s]. Output[%(output)s]' \
                                   % {'cmd': cmd, 'status': str(status), 'output': output})
        else:
            self._logger.info('Fetched host info for [%(hostname)s]' % \
                               {'hostname': hostname})
            self._logger.debug('Host info for [%(hostname)s]: [%(hostinfo)s].'\
                               % {'hostname': hostname, 'hostinfo': output})
        self._host_info[hostname] = json.loads(output)


    def read_input_json(self):
        f = open(self._input_file, 'r')
        self._hosts_in_hostgroups = json.loads(f.read())
        f.close()


    def dump_output(self, filename=None, data=[]):
        if filename is not None:
            out_file = os.path.join(self._dir_output, filename)
        else:
            out_file = os.path.join(self._dir_output, self._logger_name + '.json')
        data_str = json.dumps(data, indent=2, sort_keys=True)
        f = open(out_file, 'w')
        f.write(data_str)
        f.close()
        msg = 'Output written into file ' + str(out_file) + '.'
        self._logger.info(msg)
        print msg


    def run(self):
#        ### Read input
#        self.read_input_json()
#        ### Get list of hosts in hostgroups
#        self.get_all_hosts_names()
        ### Get host info for all hosts
        for hostname in self._hosts:
            self.get_host_info(hostname)
        ### dump output for host info
        self.dump_output(data=self._host_info, filename='host_info.json')


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 1:
        hif = HostInfoFetcher(config_file=args[0])
    else:
        hif = HostInfoFetcher()
    hif.run()


