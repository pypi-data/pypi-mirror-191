from clockify_api_client_adgstudios.factories.abstract_factory import AbstractFactory
from clockify_api_client_adgstudios.models.user import User


class UserFactory(AbstractFactory):
    class Meta:
        model = User

    api_key = None
