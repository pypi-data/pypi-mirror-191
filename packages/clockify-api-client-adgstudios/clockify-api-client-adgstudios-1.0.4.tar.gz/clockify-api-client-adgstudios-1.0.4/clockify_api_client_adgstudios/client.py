from clockify_api_client_adgstudios.factories.project_factory import ProjectFactory
from clockify_api_client_adgstudios.factories.report_factory import ReportFactory
from clockify_api_client_adgstudios.factories.task_factory import TaskFactory
from clockify_api_client_adgstudios.factories.time_entry_factory import TimeEntryFactory
from clockify_api_client_adgstudios.factories.user_factory import UserFactory
from clockify_api_client_adgstudios.factories.workspace_factory import WorkspaceFactory
from clockify_api_client_adgstudios.factories.client_factory import ClientFactory
from clockify_api_client_adgstudios.utils import Singleton


class ClockifyAPIClient(metaclass=Singleton):
    def __init__(self):
        self.workspaces = None
        self.projects = None
        self.tasks = None
        self.time_entries = None
        self.users = None
        self.reports = None
        self.clients = None

    def build(self, api_key, api_url):
        """Builds services from available factories.
        :param api_key Clockify API key.
        :param api_url Clockify API url.
        """

        self.workspaces = WorkspaceFactory(api_key=api_key, api_url=api_url)
        self.projects = ProjectFactory(api_key=api_key, api_url=api_url)
        self.tasks = TaskFactory(api_key=api_key, api_url=api_url)
        self.time_entries = TimeEntryFactory(api_key=api_key, api_url=api_url)
        self.users = UserFactory(api_key=api_key, api_url=api_url)
        self.reports = ReportFactory(api_key=api_key, api_url=api_url)
        self.clients = ClientFactory(api_key=api_key, api_url=api_url)
        return self
