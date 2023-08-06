# -*- coding: utf-8 -*-
import logging

from owo.connector import Connector, ConnectorException
from owo.settings import api_settings

logger = logging.getLogger(__name__)


class OwoHandler:
    """
        Handler to send shipping payload to Owo
    """

    def __init__(self, base_url=api_settings.OWO['BASE_URL'],
                 token=api_settings.OWO['TOKEN'],
                 email=api_settings.OWO['EMAIL'],
                 password=api_settings.OWO['PASSWORD'],
                 commerce_id=api_settings.SENDER['COMMERCE_ID'],
                 branch_office_id=api_settings.SENDER['BRANCH_OFFICE_ID'],
                 verify=True, **kwargs):

        self.base_url = kwargs.pop('base_url', base_url)
        self.email = kwargs.pop('email', email)
        self.password = kwargs.pop('password', password)
        self.token = kwargs.pop('token', token)
        self.verify = kwargs.pop('verify', verify)
        self.commerce_id = kwargs.pop('commerce_id', commerce_id)
        self.branch_office_id = kwargs.pop('branch_office_id', branch_office_id)
        self.connector = Connector(self._headers(), verify_ssl=self.verify)

    def _login(self):
        url = f'{self.base_url}auth/login'
        credentials = {'email': self.email, 'password': self.password}
        response = self.connector.post(url, credentials)
        return response

    def _headers(self):
        """
            Here define the headers for all connections with Owo.
        """
        return {
            'x-owo-token': self.token,
            'Content-Type': 'application/json',
        }

    def get_shipping_label(self):
        raise NotImplementedError(
            'get_shipping_label is not a method implemented for OwoHandler')

    def get_default_payload(self, instance):
        """
            This method generates by default all the necessary data with
            an appropriate structure for Owo courier.
        """

        payload = {
            'commerceId': self.commerce_id,
            'clientName': instance.customer.full_name,
            'clientPhone': instance.customer.phone,
            'clientEmail': instance.customer.email,
            'address': f'{instance.address}, {instance.commune.name}, {instance.region.name}',
            'lat': instance.lat if hasattr(instance, 'lat') else None,
            'lng': instance.lng if hasattr(instance, 'lng') else None,
            'number': instance.reference,
            'itemsCount': len(instance.items),
            'branchOfficeId': self.branch_office_id,
        }

        logger.debug(payload)
        return payload

    def create_shipping(self, data):
        """
            This method generate a Owo shipping.
            If the get_default_payload method returns data, send it here,
            otherwise, generate your own payload.
        """

        url = f'{self.base_url}orders/'
        logger.debug(data)

        try:
            response = self.connector.post(url, data)
            response.update({
                'tracking_number': response['id'],
            })
            return response

        except ConnectorException as error:
            logger.error(error)
            raise ConnectorException(error.message, error.description, error.code) from error

    def get_tracking(self, identifier):
        raise NotImplementedError(
            'get_tracking is not a method implemented for OwoHandler')

    def get_events(self, raw_data):
        """
            This method obtain array events.
            structure:
            {
                'tracking_number': 999999,
                'status': 'Entregado',
                'events': [{
                    'city': 'Santiago',
                    'state': 'RM',
                    'description': 'Llego al almacén',
                    'date': '12/12/2021'
                }]
            }
            return [{
                'city': 'Santiago',
                'state': 'RM',
                'description': 'Llego al almacén',
                'date': '12/12/2021'
            }]
        """
        return raw_data.get('events')

    def get_status(self, raw_data):
        """
            This method returns the status of the order and "is_delivered".
            structure:
            {
                'tracking_number': 999999,
                'status': 'Entregado',
                'events': [{
                    'city': 'Santiago'
                    'state': 'RM',
                    'description': 'Llego al almacén',
                    'date': '12/12/2021'
                }]
            }

            status: [
                'entregado', 'en camino entrega', 'en despacho',
                'error dirección', 'rechazado por cliente', 'devolución exitosa',
                'sin moradores', 'retiro cd cliente', 'recepción en bodega',
                'fuera de tiempo', 'extraviado en ruta',
            ]

            response: ('Entregado', True)
        """

        status = raw_data.get('status')
        is_delivered = False

        if status.capitalize() == 'Entregado':
            is_delivered = True

        return status, is_delivered
