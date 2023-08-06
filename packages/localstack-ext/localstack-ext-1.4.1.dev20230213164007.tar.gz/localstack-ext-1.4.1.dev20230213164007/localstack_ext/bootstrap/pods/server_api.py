_B='1.4.0'
_A='GET'
from typing import List
import localstack.constants
from localstack.config import is_env_true
from localstack.constants import ENV_PRO_ACTIVATED
from localstack.deprecations import deprecated_endpoint
from localstack.http import route
from werkzeug import Request
import localstack_ext.constants
from localstack_ext.constants import API_PATH_PODS,DEPRECATED_API_PATH_PODS
class CloudPodsPublicApi:
	def pods(I,request):
		A=request;from localstack_ext.bootstrap.pods.api_types import PodMeta as B,StateInjectRequest as C;from localstack_ext.bootstrap.pods.server.inject import handle_pod_state_injection as D
		if A.method=='OPTIONS':return
		E=A.values.get('pod_name');F=A.values.get('pod_version');G=A.values.get('merge_strategy','merge');H=C(pod_meta=B(pod_name=E,pod_version=F),merge_strategy=G,data=A.get_data());return D(H)
	pods_route=route(API_PATH_PODS,methods=['POST'])(pods);deprecated_pods_route=route(DEPRECATED_API_PATH_PODS,methods=['POST'])(deprecated_endpoint(endpoint=pods,deprecation_version=_B,previous_path=DEPRECATED_API_PATH_PODS,new_path=API_PATH_PODS))
	def pods_state(D,request):from localstack_ext.bootstrap.pods.server.extract import handle_get_state_request_in_memory as B;A=request.values.get('services','');C=A.split(',')if A else None;return B(C)
	pods_state_route=route(f"{API_PATH_PODS}/state",methods=[_A])(pods_state);deprecated_pods_state_route=route(f"{DEPRECATED_API_PATH_PODS}/state",methods=[_A])(deprecated_endpoint(endpoint=pods_state,deprecation_version=_B,previous_path=f"{DEPRECATED_API_PATH_PODS}/state",new_path=f"{API_PATH_PODS}/state"))
	def environment(B,request):from moto import __version__ as A;return{'localstack_version':localstack_ext.__version__,'localstack_ext_version':localstack.constants.VERSION,'moto_ext_version':A,'pro':is_env_true(ENV_PRO_ACTIVATED)}
	environment_route=route(f"{API_PATH_PODS}/environment",methods=[_A])(environment);deprecated_environment_route=route(f"{DEPRECATED_API_PATH_PODS}/environment",methods=[_A])(deprecated_endpoint(endpoint=environment,deprecation_version=_B,previous_path=f"{DEPRECATED_API_PATH_PODS}/environment",new_path=f"{API_PATH_PODS}/environment"))