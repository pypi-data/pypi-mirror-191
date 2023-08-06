import logging

from clockify_api_client_adgstudios.abstract_clockify import AbstractClockify


class Workspace(AbstractClockify):

    def __init__(self, api_key, api_url):
        super(Workspace, self).__init__(api_key=api_key, api_url=api_url)

    def get_workspaces(self):
        """Returns all workspaces.
        :return List of Workspaces in dictionary representation.
        """
        try:
            url = self.base_url + '/workspaces/'
            return self.get(url)
        except Exception as e:
            logging.error("API error: {0}".format(e))
            raise e

    def AddUser(self, workspace_id, user_id):
        """Add user to workspace.
        :param workspace_id Id of workspace.
        :param user_id      Id of user.
        """
        try:
            url = self.base_url + '/workspaces/' + workspace_id + '/users/' + user_id
            return self.post(url)
        except Exception as e:
            logging.error("API error: {0}".format(e))
            raise e

