"""
This module is a wrapper for the jira api
"""
import yaml
import requests
from requests.auth import HTTPBasicAuth


class JiraApi:
    """
    This class is a wrapper for the jira api
    """
    def __init__(self):
        self.url = None
        jira_info_stream = open('jira_info.yaml', 'r')
        jira_info = yaml.load(jira_info_stream, Loader=yaml.SafeLoader)
        self.url = jira_info['jira_url']
        self.token = jira_info['token']
        self.user_id = jira_info['user_id']
        self.headers = jira_info['headers']
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.user_id, self.token)

    def get_projects_json(self):
        projects_url = r'rest/api/3/project/search'
        projects_json = self.session.get(self.url + projects_url)
        return projects_json

    def get_issue(self, issue_id):
        issue_url = r'rest/api/2/issue/' + issue_id
        issue_json = self.session.get(self.url + issue_url)
        return issue_json

    def create_update_issue(self, issue_id=None):
        issue_url = r'rest/api/2/issue/'
        issue_input_stream = open('issue_input.yaml', 'r')
        issue_info = yaml.load(issue_input_stream, Loader=yaml.SafeLoader)
        header_json = self.headers
        if not issue_id:
            issue_response = self.session.post(self.url + issue_url, headers=header_json, json=issue_info)
        else:
            issue_response = self.session.put(self.url + issue_url + issue_id, headers=header_json, json=issue_info)
        return issue_response


jira_api = JiraApi()
projects_json_result = jira_api.get_projects_json()
issue_json_result = jira_api.get_issue('AD-2')
issue_result = jira_api.create_update_issue()
issue_result2 = jira_api.get_issue('AD-3')
print(issue_result)
