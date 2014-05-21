from jenkinsapi.jenkins import Jenkins
import re
import croniter
import datetime
from xml.dom import minidom


class JenkinsService():

    def __init__(self, server):
        self.jenkins = Jenkins(server)

    def get_job_with_name(self, jobname):
        return self.jenkins[jobname]

    def get_job_next_scheduled_build(self, jobname):
        job = self.jenkins[jobname]
        conf_content = job.get_config()

        cron_schedule_list = self.grab_cron_time(conf_content)
        nextbuild = "Unknown"
        if cron_schedule_list:
            nextbuild = self.get_next_time(cron_schedule_list)
        return nextbuild

    def grab_cron_time(self, conf_content):
        def getText(nodelist):
            rc = []
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)
            return ''.join(rc)
        xmldoc = minidom.parseString(conf_content)
        itemlist = xmldoc.getElementsByTagName('spec')
        cron_content = getText(itemlist[0].childNodes)
        cron_content_list = cron_content.split('\n')
        return cron_content_list

    def get_next_time(self, schedule_list):
        now = datetime.datetime.now()
        nextbuild_list = map(lambda schedule: croniter.croniter(schedule, now).get_next(
            datetime.datetime), schedule_list)
        return min(nextbuild_list)

    def get_changelist_detail(self, jobname):
        job = self.jenkins[jobname]
        actions = job.get_last_build().get_actions()
        items = actions.items()
        changelist = self.get_changelist_dict_from_items(items)
        return changelist

    def get_changelist_dict_from_items(self, items):
        changelist = {}
        for item in items:
            if item[0] == 'parameters':
                parameters = item[1]
                for param in parameters:
                    if param['name'] == 'VERSION':
                        changelist['version'] = param['value']
                    if param['name'] == 'CLIST':
                        changelist['cl'] = param['value']
                    if param['name'] == 'BRANCH':
                        changelist['branch'] = param['value']
        return changelist

    def get_last_build_timestamp(self, jobname):
        job = self.get_job_with_name(jobname)
        last_build = job.get_last_build()
        last_build_timestamp = last_build.get_timestamp()
        return last_build_timestamp
