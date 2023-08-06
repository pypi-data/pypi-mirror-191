from ..constants import PROJECT_TAG as PROJECT_TAG, TOPIC as TOPIC, TOPIC_PREFIX as TOPIC_PREFIX
from ..util import ProdClientError as ProdClientError, SerializableResultT as SerializableResultT, create_analytics_message_packet as create_analytics_message_packet
from .base_client import BaseClient as BaseClient
from _typeshed import Incomplete
from edgeiq._production_client.connection import IoTCoreConnection as IoTCoreConnection
from typing import Any

class AnalyticsCloudWriter(BaseClient):
    cloud_connection: Incomplete
    topic: Incomplete
    exit_event: Incomplete
    def __init__(self) -> None: ...
    def publish_analytics(self, results: SerializableResultT, type: str, base_service: str, tag: Any = ...): ...
    def publish(self, message: str, topic: str): ...
    def stop(self) -> None: ...
