from clockify_api_client_adgstudios.factories.abstract_factory import AbstractFactory
from clockify_api_client_adgstudios.models.report import Report


class ReportFactory(AbstractFactory):
    class Meta:
        model = Report

    api_key = None
