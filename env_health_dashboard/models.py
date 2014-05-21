from django.db import models
import logging
from portlet_services import *


class Portlet(models.Model):
    serviceClass = models.CharField(max_length=200)

    def get_service_class(self):
        parts = self.serviceClass.split('.')
        initialModuleName = ".".join(parts[:-1])
        currentModuleOrClass = __import__(initialModuleName)
        for comp in parts[1:]:
            currentModuleOrClass = getattr(currentModuleOrClass, comp)
        return currentModuleOrClass


class PortletAssignment(models.Model):
    title = models.CharField(max_length=100)
    portlet = models.ForeignKey(Portlet)
    config = models.TextField()

    def gatherAndReturnPortletData(self):
        service = self.portlet.get_service_class()(self)
        service.execute()
        return service

    def returnPortletDataWithError(self, e):
        try:
            service = self.portlet.get_service_class()(self)
            service.set_error("An exception has occurred:" + str(e) + " - " + str(service))
            return service
        except Exception as ex:
            service = TextPortletService(PortletAssignment(title="ERROR", portlet=Portlet()))
            service.set_error("An exception has occurred:" + str(ex))
            return service
