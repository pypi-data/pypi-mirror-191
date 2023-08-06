from clockify_api_client_adgstudios.factories.abstract_factory import AbstractFactory
from clockify_api_client_adgstudios.models.client import Client


class ClientFactory(AbstractFactory):
    class Meta:
        model = Client
