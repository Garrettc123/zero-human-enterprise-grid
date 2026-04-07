"""Tests for sync system instantiation and status reporting."""

import pytest
import asyncio

from sync_engine import AutonomousSyncEngine, CloudProvider, SyncConfig
from database_sync import (
    DatabaseSyncManager, DatabaseConfig, DatabaseType, SyncDirection,
)
from storage_sync import StorageSyncManager, StorageConfig, StorageType
from cache_sync import CacheSyncManager, CacheConfig, CacheType
from message_sync import MessageQueueSyncManager, MessageQueueConfig, MessageQueueType
from search_sync import SearchIndexSyncManager, SearchEngineConfig, SearchEngineType
from ml_pipeline_sync import MLPipelineSyncManager, MLPlatformConfig, MLPlatformType
from graphql_sync import GraphQLSyncManager, GraphQLEndpointConfig
from webhook_sync import WebhookManager, EventType, WebhookEvent
from monitoring import MonitoringSystem, HealthStatus


def test_cloud_sync_register_provider():
    engine = AutonomousSyncEngine()
    config = SyncConfig("AWS", CloudProvider.AWS, "aws.com", "key")
    engine.register_provider(config)
    status = engine.get_status()
    assert "AWS" in status["providers"]
    assert status["running"] is False


def test_database_sync_register_and_pair():
    mgr = DatabaseSyncManager()
    mgr.register_database(DatabaseConfig("pg", DatabaseType.POSTGRESQL, "pg://localhost"))
    mgr.register_database(DatabaseConfig("mongo", DatabaseType.MONGODB, "mongo://localhost"))
    mgr.add_sync_pair("pg", "mongo", SyncDirection.SOURCE_TO_TARGET)
    status = mgr.get_status()
    assert len(status["databases"]) == 2
    assert status["sync_pairs"] == 1


def test_storage_sync_register():
    mgr = StorageSyncManager()
    config = StorageConfig("S3", StorageType.S3, "s3.amazonaws.com", "bucket", {})
    mgr.register_storage(config)
    status = mgr.get_status()
    assert "S3" in status["storage_providers"]


def test_cache_sync_register():
    mgr = CacheSyncManager()
    config = CacheConfig("Redis", CacheType.REDIS, "localhost", 6379)
    mgr.register_cache(config)
    status = mgr.get_status()
    assert "Redis" in status["cache_providers"]


def test_message_queue_register():
    mgr = MessageQueueSyncManager()
    config = MessageQueueConfig("Kafka", MessageQueueType.KAFKA, ["localhost:9092"])
    mgr.register_queue(config)
    status = mgr.get_status()
    assert "Kafka" in status["message_queues"]


def test_search_engine_register():
    mgr = SearchIndexSyncManager()
    config = SearchEngineConfig("ES", SearchEngineType.ELASTICSEARCH, "localhost:9200", "key")
    mgr.register_search_engine(config)
    status = mgr.get_status()
    assert "ES" in status["search_engines"]


def test_ml_platform_register():
    mgr = MLPipelineSyncManager()
    config = MLPlatformConfig("MLflow", MLPlatformType.MLFLOW, "localhost:5000", {})
    mgr.register_platform(config)
    status = mgr.get_status()
    assert "MLflow" in status["ml_platforms"]


def test_graphql_register():
    mgr = GraphQLSyncManager()
    config = GraphQLEndpointConfig("Prod", "https://api.example.com/graphql", "token")
    mgr.register_endpoint(config)
    status = mgr.get_status()
    assert "Prod" in status["graphql_endpoints"]


def test_webhook_register_handler():
    mgr = WebhookManager()
    mgr.register_handler(EventType.DEPLOYMENT, lambda e: None)
    status = mgr.get_status()
    assert status["registered_event_types"] == 1


def test_monitoring_status():
    mon = MonitoringSystem()
    status = mon.get_status()
    assert status["running"] is False
    assert status["total_checks"] == 0


@pytest.mark.asyncio
async def test_cloud_connector_deploy():
    engine = AutonomousSyncEngine()
    config = SyncConfig("AWS", CloudProvider.AWS, "aws.com", "key")
    engine.register_provider(config)
    connector = engine.providers["AWS"]
    await connector.connect()
    result = await connector.deploy([{"name": "test.bin", "size": 100}])
    assert result["files_deployed"] == 1
    assert result["provider"] == "AWS"


@pytest.mark.asyncio
async def test_monitoring_health_check():
    mon = MonitoringSystem()
    status = await mon.check_component_health("test_component")
    assert status == HealthStatus.HEALTHY
