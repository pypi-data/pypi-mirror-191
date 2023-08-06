from __future__ import annotations
import logging
from typing import List,Optional
from localstack.constants import APPLICATION_OCTET_STREAM
from localstack.http import Response
from localstack_ext.bootstrap.pods.server import persistence
from localstack_ext.bootstrap.pods.server.states import ServiceStateManager
from localstack_ext.bootstrap.pods.service_state.service_state import ServiceState
from localstack_ext.bootstrap.pods.utils.adapters import ServiceStateMarshaller
LOG=logging.getLogger(__name__)
def handle_get_state_request_in_memory(services=None):
	from localstack.services.plugins import SERVICE_PLUGINS as C;E=C.list_loaded_services();A=ServiceState()
	for B in services or E:
		F=C.get_service_container(B)
		if not F:LOG.debug("Can't get service container for service %s while calling handle_get_state_request_in_memory",B)
		try:G=ServiceStateManager(service=B);H=G.get_service_state();A.put_service_state(H)
		except Exception as I:LOG.debug('Unable to retrieve the state for service %s: %s - skipping',B,I)
	if A.is_empty():LOG.debug('Extracted state is empty')
	D=ServiceStateMarshaller.marshall(state=A,marshall_function=persistence.marshall_backend);J=A.get_services();K=Response(D,mimetype=APPLICATION_OCTET_STREAM,headers={'x-localstack-pod-services':','.join(J),'x-localstack-pod-size':len(D)});return K