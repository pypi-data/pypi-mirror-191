from clockify_api_client_adgstudios.factories.abstract_factory import AbstractFactory
from clockify_api_client_adgstudios.models.task import Task


class TaskFactory(AbstractFactory):
    class Meta:
        model = Task

    api_key = None
