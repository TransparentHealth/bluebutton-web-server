import logging

from urllib.parse import urlencode
from rest_framework import exceptions
from rest_framework.response import Response

from apps.fhir.bluebutton.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from apps.fhir.bluebutton.utils import get_crosswalk
from apps.fhir.bluebutton.views.generic import FhirDataView

logger = logging.getLogger('hhs_server.%s' % __name__)

START_PARAMETER = 'startIndex'
SIZE_PARAMETER = 'count'


class SearchView(FhirDataView):

    def get(self, request, resource_type, *args, **kwargs):
        # Verify paging inputs. Casting an invalid int will throw a ValueError
        try:
            start_index = int(request.GET.get(START_PARAMETER, 0))
        except ValueError:
            raise exceptions.ParseError(detail='%s must be an integer between zero and the number of results' % START_PARAMETER)

        if start_index < 0:
            raise exceptions.ParseError()

        try:
            page_size = int(request.GET.get(SIZE_PARAMETER, DEFAULT_PAGE_SIZE))
        except ValueError:
            raise exceptions.ParseError(detail='%s must be an integer between 1 and %s' % (SIZE_PARAMETER, MAX_PAGE_SIZE))

        if page_size <= 0 or page_size > MAX_PAGE_SIZE:
            raise exceptions.ParseError()

        data = self.fetch_data(request, resource_type, *args, **kwargs)

        # TODO update to pagination class
        data['entry'] = data['entry'][start_index:start_index + page_size]
        replay_parameters = self.build_parameters()
        data['link'] = get_paging_links(request.build_absolute_uri('?'),
                                        start_index,
                                        page_size,
                                        data['total'],
                                        replay_parameters)

        return Response(data)

    def check_resource_permission(self, request, *args, **kwargs):
        crosswalk = get_crosswalk(request.resource_owner)

        # If the user isn't matched to a backend ID, they have no permissions
        if crosswalk is None:
            logger.info('Crosswalk for %s does not exist' % request.user)
            raise exceptions.PermissionDenied(
                'No access information was found for the authenticated user')

        patient_id = crosswalk.fhir_id

        if 'patient' in request.GET and request.GET['patient'] != patient_id:
            raise exceptions.PermissionDenied(
                'You do not have permission to access the requested patient\'s data')

        if 'beneficiary' in request.GET and patient_id not in request.GET['beneficiary']:
            raise exceptions.PermissionDenied(
                'You do not have permission to access the requested patient\'s data')
        return crosswalk

    def build_parameters(self, *args, **kwargs):
        patient_id = self.crosswalk.fhir_id
        resource_type = self.resource_type
        get_parameters = {
            '_format': 'application/json+fhir'
        }

        if resource_type == 'ExplanationOfBenefit':
            get_parameters['patient'] = patient_id
        elif resource_type == 'Coverage':
            get_parameters['beneficiary'] = 'Patient/' + patient_id
        elif resource_type == 'Patient':
            get_parameters['_id'] = patient_id
        return get_parameters

    def build_url(self, resource_router, resource_type, *args, **kwargs):
        return resource_router.fhir_url + resource_type + "/"


def get_paging_links(base_url, start_index, page_size, count, replay_parameters):

    if base_url[-1] != '/':
        base_url += '/'

    out = []
    replay_parameters[SIZE_PARAMETER] = page_size

    replay_parameters[START_PARAMETER] = start_index
    out.append({
        'relation': 'self',
        'url': base_url + '?' + urlencode(replay_parameters)
    })

    if start_index + page_size < count:
        replay_parameters[START_PARAMETER] = start_index + page_size
        out.append({
            'relation': 'next',
            'url': base_url + '?' + urlencode(replay_parameters)
        })

    if start_index - page_size >= 0:
        replay_parameters[START_PARAMETER] = start_index - page_size
        out.append({
            'relation': 'previous',
            'url': base_url + '?' + urlencode(replay_parameters)
        })

    if start_index > 0:
        replay_parameters[START_PARAMETER] = 0
        out.append({
            'relation': 'first',
            'url': base_url + '?' + urlencode(replay_parameters)
        })

    # This formula rounds count down to the nearest multiple of page_size
    # that's less than and not equal to count
    last_index = (count - 1) // page_size * page_size
    if start_index < last_index:
        replay_parameters[START_PARAMETER] = last_index
        out.append({
            'relation': 'last',
            'url': base_url + '?' + urlencode(replay_parameters)
        })

    return out
