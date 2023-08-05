from sapiopylib.rest.DashboardManager import DashboardManager
from sapiopylib.rest.DataTypeService import DataTypeManager

from sapiopylib.rest.AccessionService import AccessionManager
from sapiopylib.rest.CustomReportService import CustomReportManager
from sapiopylib.rest.DataRecordManagerService import DataRecordManager
from sapiopylib.rest.ELNService import ElnManager
from sapiopylib.rest.PicklistService import PicklistManager
from sapiopylib.rest.User import SapioUser


class DataMgmtServer:
    """
    Contains all service points for the current API.
    """

    @staticmethod
    def get_dashboard_manager(user: SapioUser) -> DashboardManager:
        """
        Get the dashboard manager service for the current context.
        :param user The user auth context.
        """
        return DashboardManager(user)

    @staticmethod
    def get_data_record_manager(user: SapioUser) -> DataRecordManager:
        """
        Get the data record manager service for the current context.
        :param user The user auth context.
        """
        return DataRecordManager(user)

    @staticmethod
    def get_accession_manager(user: SapioUser) -> AccessionManager:
        """
        Get the accession service manager for the current context.
        :param user: The user auth context.
        """
        return AccessionManager(user)

    @staticmethod
    def get_custom_report_manager(user: SapioUser) -> CustomReportManager:
        """
        Get the custom report manager for the current context.
        :param user: The user auth context.
        """
        return CustomReportManager(user)

    @staticmethod
    def get_eln_manager(user: SapioUser) -> ElnManager:
        """
        Get the ELN (Notebook Experiment) manager for the current context.
        :param user:The user auth context.
        """
        return ElnManager(user)

    @staticmethod
    def get_picklist_manager(user: SapioUser) -> PicklistManager:
        """
        Get the picklist manager for the current context.
        :param user: The user auth context.
        """
        return PicklistManager(user)

    @staticmethod
    def get_data_type_manager(user: SapioUser) -> DataTypeManager:
        """
        Get the data type manager for the current context.
        :param user: The user auth context.
        """
        return DataTypeManager(user)
