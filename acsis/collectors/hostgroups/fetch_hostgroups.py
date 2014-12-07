"""
    fetch_hostgroups ... get list of possible hostgroups from git.
                     ... get list of hosts in a hostgroup (using mco).
    
"""
import commands
import ConfigParser
import json
import logging
import os
import re
import sys
from datetime import datetime


class HostgroupFetcher(object):
    ### configuration
    _config_file = '/tmp/ACSIS/collectors/settings/hostgroups.cfg'
    _ts = datetime.utcnow().strftime('%F.%H%M%S')
    _config = None
    _logger = None
    ### logger
    _logger_name = 'hostgroup_fetcher'
    _logger_level = 'INFO'
    _logger_file = '/tmp/ACSIS/collectors/logs/logger.' + _logger_name + '.log'
    ### hostgroups
    _config_hostgroups = {}
    _manifest_path = 'code/manifests'
    _hostgroups = []
    _hosts_in_hostgroups = {}


    def __init__(self, config_file=None):
        if config_file is not None:
            self._config_file = config_file
        self.configure()


    def configure(self):
        self._config = ConfigParser.ConfigParser()
        self._config.read(self._config_file)
        ### logging config
        self.configure_logger()
        ### hostgroups config
        self.configure_hostgroups()
        ### configure local file paths
        self.configure_local_paths()


    def configure_logger(self):
        self._logger_name = self._config.get("hostgroups", "log_name")
        self._logger_level = self._config.get("hostgroups", "log_level")
        self._logger_file = self._config.get("hostgroups", "log_file")
        self._logger = self.logger(self._logger_name, self._logger_level, self._logger_file)


    def configure_hostgroups(self):
        top_level_hostgroups = str(self._config.get("hostgroups", "hostgroups")).split(',')
        self._logger.debug('top_level_hostgroups: ' + str(top_level_hostgroups))
        for top_level_hostgroup in top_level_hostgroups:
            if top_level_hostgroup not in self._config_hostgroups:
                hg_name = None
                hg_git = None
                hg_branch = None
                hg_path = None
                self._config_hostgroups[top_level_hostgroup] = {}
                hg_name = self._config.get(top_level_hostgroup, "name")
                hg_git = self._config.get(top_level_hostgroup, "git")
                hg_branch = self._config.get(top_level_hostgroup, "branch")
                hg_path = self._config.get(top_level_hostgroup, "path")
                self._config_hostgroups[top_level_hostgroup]['name'] = hg_name
                self._config_hostgroups[top_level_hostgroup]['git'] = hg_git
                self._config_hostgroups[top_level_hostgroup]['branch'] = hg_branch
                self._config_hostgroups[top_level_hostgroup]['path'] = hg_path
                self._logger.debug('Activated top_level_hostgroup[' + top_level_hostgroup + \
                                   ']: ' + str(self._config_hostgroups[top_level_hostgroup]))


    def configure_local_paths(self):
        self._manifest_path = self._config.get("hostgroups", "manifest_path")
        self._dir_output = self._config.get("hostgroups", "dir_output")
        self._dir_git = self._config.get("hostgroups", "dir_git")
        ### make sure _dir_output and _dir_git exist
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
        try:
            cmd = 'mkdir -p %(dirname)s' % {'dirname': self._dir_git}
            status, output = commands.getstatusoutput(cmd)
            if status != 0:
                self._logger.error('Ran [%(cmd)s]. Status [%(status)s]. Output[%(output)s]' \
                                   % {'cmd': cmd, 'status': str(status), 'output': output})
            else:
                self._logger.debug('Dir for git exists: ' + str(self._dir_git))
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


    def walk_manifest_path(self, manifest_path=None):
        self._logger.debug('Will look for manifests in [' + str(manifest_path) + '].')
        hg_list=[]
        for root, dirs, files in os.walk(manifest_path):
            for file in files:
                if file.endswith(".pp"):
                     hg=os.path.join(root, file)
                     hg=re.sub(manifest_path, '', hg)
                     hg = re.sub('.pp', '', hg)
                     if hg.startswith('/'):
                        hg = hg[1:]
                     hg_list.append(hg)
        self._logger.info('Found ' + str(len(hg_list)) + ' manifests in [' + str(manifest_path) + '].')
        self._logger.debug('List of manifests in [' + str(manifest_path) + ']: ' + str(hg_list) + '.')
        return hg_list


    def clone_or_update_hostgroup_repo(self, hg_config=None):
        ###    clone/update git repo
        git_name = hg_config['name']
        git_root_dir = self._dir_git
        git_dir = os.path.join(self._dir_git, git_name)
        git_repo = hg_config['git']
        git_branch = hg_config['branch']
        if not os.path.isdir(git_dir):
            self._logger.info('Local git copy of ' + str(git_name) + ' does not exist. Will clone it.')
            cmd = 'cd %(git_root_dir)s ; git clone %(git_repo)s -b %(git_branch)s' % \
                {'git_root_dir': git_root_dir, 'git_repo': git_repo, 'git_branch': git_branch}
            status, output = commands.getstatusoutput(cmd)
            if status != 0:
                self._logger.error('Ran [%(cmd)s]. Status [%(status)s]. Output[%(output)s]' \
                                   % {'cmd': cmd, 'status': str(status), 'output': output})
            else:
                self._logger.info('Cloned git repo: [%(git_repo)s] to [%(git_dir)s]. Ran [%(cmd)s].' % \
                                  {'git_repo':git_repo, 'git_dir':git_dir, 'cmd': cmd})
        else:
            ### git repo exists, just update
            cmd = 'cd %(git_dir)s ; git pull' % {'git_dir': git_dir}
            status, output = commands.getstatusoutput(cmd)
            if status != 0:
                self._logger.error('Ran [%(cmd)s]. Status [%(status)s]. Output[%(output)s]' \
                                   % {'cmd': cmd, 'status': str(status), 'output': output})
            else:
                self._logger.info('Updated git repo: [' + str(git_repo) + \
                                   '] in [' + str(git_dir) + '].')
        return git_dir


    def process_a_hostgroup(self, hostgroupkey=None):
        try:
            hg_config = self._config_hostgroups[hostgroupkey]
        except:
            return None
        ###    clone/update git repo
        git_dir = self.clone_or_update_hostgroup_repo(hg_config)
        ###    get manifests for a hostgroup
        manifest_path = os.path.join(git_dir, self._manifest_path)
        hgs = self.walk_manifest_path(manifest_path)
        ### save hostgroups for this top level hostgroup
        if hostgroupkey not in self._hostgroups:
            hgs = ['%s/%s' % (hostgroupkey, x) for x in hgs ]
            self._hostgroups.extend(hgs)


    def get_hosts_in_a_hostgroup(self, hostgroup=None):
        hg_sections = []
        hosts = []
        if hostgroup is not None:
            hg_sections = hostgroup.split('/')
            #-F 'hostgroup_0=voatlasmisc' -F 'hostgroup_1=atlas'
        cmd = "mco find --dm puppetdb "
        for i in xrange(len(hg_sections)):
            cmd = "%(cmd)s -F 'hostgroup_%(hg_section_index)s=%(hg_section)s' "\
                % {'cmd': cmd, 'hg_section_index': i, 'hg_section': hg_sections[i] }
        cmd = "%s 2>/dev/null " % (cmd)
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
            self._logger.error('Ran [%(cmd)s]. Status [%(status)s]. Output[%(output)s]' \
                               % {'cmd': cmd, 'status': str(status), 'output': output})
        else:
            hosts = output.split('\n')
            self._logger.info('Got %(N)s hosts of hostgroup [%(hg)s].' % \
                                {'N':len(hosts), 'hg':hostgroup})
            self._logger.debug('Got %(N)s hosts of hostgroup [%(hg)s]: [%(output)s]. Ran [%(cmd)s].' % \
                                {'N':len(hosts), 'hg':hostgroup, \
                                 'output': output, 'cmd': cmd})
        if hostgroup not in self._hosts_in_hostgroups.keys():
            self._hosts_in_hostgroups[hostgroup] = []
        self._hosts_in_hostgroups[hostgroup] = hosts


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
        ### Get list of hostgroups
        ### loop through hostgroups
        for hg in self._config_hostgroups.keys():
            self.process_a_hostgroup(hg)
        ###    clone/update git repo
        ###    get manifests for a hostgroup
        ### dump output for list of hostgroups
        self.dump_output(data=self._hostgroups, filename='hostgroups.json')
        ### Get list of hosts in a hostgroup
        for hg in self._hostgroups:
            self.get_hosts_in_a_hostgroup(hg)
        ### dump output for list of hosts in hostgroups
        self.dump_output(data=self._hosts_in_hostgroups, filename='hosts_in_hostgroups.json')


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 1:
        hf = HostgroupFetcher(config_file=args[0])
    else:
        hf = HostgroupFetcher()
    hf.run()


