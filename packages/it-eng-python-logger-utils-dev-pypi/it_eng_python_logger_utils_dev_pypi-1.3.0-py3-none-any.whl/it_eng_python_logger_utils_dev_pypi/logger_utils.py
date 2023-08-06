import logging
import json
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace import config_integration
import requests
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace import config_integration
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
config_integration.trace_integrations(["requests"])


class LoggerHelper:
    def __init__(
        self, logger_name, app_insights_token="", basic_config_level="INFO", send_to_azure=True
    ):
        self.logger_name = logger_name
        self.__app_insights_token = app_insights_token
        self.basic_config_level = basic_config_level
        self.logger = logging.getLogger(self.logger_name)
        if send_to_azure and app_insights_token:
            try:
                self.logger.addHandler(
                    AzureLogHandler(
                        connection_string=f"InstrumentationKey={self.__app_insights_token}"
                    )
                )
            except Exception as e:
                print("Azure Add Handler error: ", e)
                raise e
        level = eval("logging." + self.basic_config_level.upper())
        logging.basicConfig(level=level)

    def trace(self):
        """
        Trace your API calls and send them to Azure App Insights.
        """
        if self.__app_insights_token:
            try:
                return Tracer(
                    exporter=AzureExporter(
                        connection_string=f"InstrumentationKey={self.__app_insights_token}"
                    ),
                    sampler=ProbabilitySampler(1.0),
                )
            except Exception as e:
                print("Tracer Error: ", e)
                raise e
        return

    def info(
        self,
        message: dict | str,
        structured=True,
    ):

        """Acts like a typical logging instance but has ability to send to Azure App Insights and defaulted structured logging"""

        if structured:
            if isinstance(message, dict):
                
                message = json.dumps(
                    json.loads(
                        f'{{"App": "{self.logger_name}", "Severity": "Info", "Message": {json.dumps(message)}}}'
                    )
                )

            else:
                message = json.dumps(
                    json.loads(
                        f'{{"App": "{self.logger_name}", "Severity": "Info", "Message": "{(message)}"}}'
                    )
                )
        if not structured:
            if isinstance(message, dict):
                
                message = json.dumps(json.loads(message))

        return self.logger.info(message)

    def debug(
        self,
        message: dict | str,
        structured=True,
    ):
        """Acts like a typical logging instance but has ability to send to Azure App Insights and defaulted structured logging"""

        if structured:
            if isinstance(message, dict):
                
                message = json.dumps(
                    json.loads(
                        f'{{"App": "{self.logger_name}", "Severity": "Debug", "Message": {json.dumps(message)}}}'
                    )
                )

            else:
                message = json.dumps(
                    json.loads(
                        f'{{"App": "{self.logger_name}", "Severity": "Debug", "Message": "{(message)}"}}'
                    )
                )
        if not structured:
            if isinstance(message, dict):
                
                message = json.dumps(json.loads(message))

        return self.logger.debug(message)

    def warning(
        self,
        message: dict | str,
        structured=True,
    ):
        """Acts like a typical logging instance but has ability to send to Azure App Insights and defaulted structured logging"""
        if structured:
            if isinstance(message, dict):
                
                message = json.dumps(
                    json.loads(
                        f'{{"App": "{self.logger_name}", "Severity": "Warning", "Message": {json.dumps(message)}}}'
                    )
                )

            else:
                message = json.dumps(
                    json.loads(
                        f'{{"App": "{self.logger_name}", "Severity": "Warning", "Message": "{(message)}"}}'
                    )
                )
        if not structured:
            if isinstance(message, dict):
                
                message = json.dumps(json.loads(message))

        return self.logger.warning(message)

    def critical(
        self,
        message: dict | str,
        structured=True,
    ):
        """Acts like a typical logging instance but has ability to send to Azure App Insights and defaulted structured logging"""
        if structured:
            if isinstance(message, dict):
                
                message = json.dumps(
                    json.loads(
                        f'{{"App": "{self.logger_name}", "Severity": "Critical", "Message": {json.dumps(message)}}}'
                    )
                )

            else:
                message = json.dumps(
                    json.loads(
                        f'{{"App": "{self.logger_name}", "Severity": "Critical", "Message": "{(message)}"}}'
                    )
                )
        if not structured:
            if isinstance(message, dict):
                
                message = json.dumps(json.loads(message))

        return self.logger.critical(message)

    def error(
        self,
        message: dict | str,
        structured=True,
    ):
        """Acts like a typical logging instance but has ability to send to Azure App Insights and defaulted structured logging"""
        if structured:
            if isinstance(message, dict):
                
                message = json.dumps(
                    json.loads(
                        f'{{"App": "{self.logger_name}", "Severity": "Error", "Message": {json.dumps(message)}}}'
                    )
                )

            else:
                message = json.dumps(
                    json.loads(
                        f'{{"App": "{self.logger_name}", "Severity": "Error", "Message": "{(message)}"}}'
                    )
                )
        if not structured:
            if isinstance(message, dict):
                
                message = json.dumps(json.loads(message))

        return self.logger.error(message)

    def basicConfig(self, level=logging.INFO):
        """Sets basic config logging level
        NOTE: Only use if you want to set basicConfig multiple times during execution (not sure when you'd want to do this but it's here). Else set during Class init.
        """
        level = str(level)
        level = eval(level)
        self.logging.getLogger()
        return self.logging.basicConfig(level=level)
