import urllib2
import json


class AlexandriaServices():

    def __init__(self, server):
        self.server = server

    def get_job_status(self, job_name, job_repository):
        url = "%s/job/status?job_name=%s&job_repository=%s" % (
            self.server, job_name, job_repository)
        content = self._get_url_content(url)
        return content

    def get_last_job_test_result_failures(self, job_name, job_repository):
        url = "%s/job/last_build_failed_test_results?job_name=%s&job_repository=%s" % (
            self.server, job_name, job_repository)
        content = self._get_url_content(url)
        test_result_list = self._decode_json_string(content)
        return test_result_list

    @staticmethod
    def _get_url_content(url):
        content = urllib2.urlopen(url).read()
        return content

    @staticmethod
    def _decode_json_string(content):
        return json.loads(content)