import requests
import re

# unit in second
TIMEOUT = 1


class VersionService():

    def __init__(self, server_pool_list):
        self.server_pool_list = server_pool_list
        self.server_pool_version = dict()

    def get_pool_list_version(self):
        for each_pool in self.server_pool_list:
            self._get_server_list_version(each_pool)
        self._format_order_server_pool()

    def _get_server_list_version(self, pool):
        server_dict = dict()
        server_list = self.server_pool_list[pool]
        for server in server_list:
            server_dict = self._get_server_version(server, server_dict)
        self._add_server_dict_to_pool_dict(server_dict, pool)

    def _format_order_server_pool(self):
        ordered_dict = dict()
        for version, content in self.server_pool_version.items():
            item_list = content.split(",")
            server_or_pool = dict()
            hosts_list, pools_list = self._determine_server_or_pool(item_list)
            server_or_pool['hosts'] = ", ".join(sorted(hosts_list)) if hosts_list else ""
            server_or_pool['pools'] = ", ".join(sorted(pools_list)) if pools_list else ""
            ordered_dict[version] = server_or_pool
        self.server_pool_version = ordered_dict

    def _determine_server_or_pool(self, item_list):
        hosts_list = []
        pools_list = []
        for item in item_list:
            if item.find("host-") != -1:
                hosts_list.append(item.replace("host-", ""))
            if item.find("pool-") != -1:
                pools_list.append(item.replace("pool-", ""))
        return hosts_list, pools_list

    def _get_server_version(self, server, server_dict):
        url = "http://%s/VERSION" % server['host']
        server_name = self._get_server_display_name(url)
        content = self._get_url_content(url)
        if content:
            server_dict = self._add_to_dict(content, server_name, server_dict, key="host")
        else:
            server_dict = self._add_to_dict('unknown', server_name, server_dict, key="host")
        return server_dict

    def _add_server_dict_to_pool_dict(self, server_dict, pool):
        if len(server_dict) == 1:
            version = server_dict.keys()[0]
            self.server_pool_version = self._add_to_dict(version, pool, self.server_pool_version, key="pool")
        else:
            for server_version_list_key, server_version_list in server_dict.iteritems():
                self.server_pool_version = self._add_to_dict(server_version_list_key, server_version_list, self.server_pool_version, key="host")

    @staticmethod
    def _add_to_dict(version, server_or_pool, dict, key):
        if version in dict.keys():
            dict[version] = dict[version] + ", " + key + "-" + server_or_pool
        else:
            dict[version] = key + "-" + server_or_pool
        return dict


    @staticmethod
    def _get_server_display_name(url):
        name = url.split('.')[0]
        name = name.replace("http://", "")
        return name

    def _get_url_content(self, url):
        content = ""
        try:
            r = requests.get(url, timeout=TIMEOUT)
            if r.status_code == 200:
                content = self._get_content_from_response(r)
            else:
                raise Exception("Unsuccessful status")
        except:
            pass
        return str(content)

    @staticmethod
    def _get_content_from_response(success_response):
        text = success_response.text
        is_match = False
        if re.match("^main.*", text):
            is_match = True
        elif re.match("1[0-9]\..*", text):
            is_match = True

        if is_match:
            first_line = text.splitlines()[0]
            second_part_of_first_line = first_line.split()[2]
            return second_part_of_first_line
        else:
            raise Exception("Incorrect Page.")


