"""Search Index Sync - Elasticsearch, Algolia, Meilisearch."""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class SearchEngineType(Enum):
    ELASTICSEARCH = "elasticsearch"
    ALGOLIA = "algolia"
    MEILISEARCH = "meilisearch"

@dataclass
class SearchEngineConfig:
    name: str
    engine_type: SearchEngineType
    endpoint: str
    api_key: str

class SearchEngineConnector:
    def __init__(self, config: SearchEngineConfig):
        self.config = config
        self.connected = False
        self.last_sync: Optional[datetime] = None
        self.documents_indexed = 0
    
    async def connect(self) -> bool:
        logger.info(f"[{self.config.name}] Connecting to {self.config.engine_type.value}...")
        await asyncio.sleep(0.1)
        self.connected = True
        return True
    
    async def index_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not self.connected:
            raise Exception("Not connected")
        
        logger.info(f"[{self.config.name}] Indexing {len(documents)} documents...")
        await asyncio.sleep(0.1)
        
        self.last_sync = datetime.utcnow()
        self.documents_indexed += len(documents)
        
        return {
            "search_engine": self.config.name,
            "documents_indexed": len(documents),
            "total_indexed": self.documents_indexed,
            "timestamp": self.last_sync.isoformat()
        }

class SearchIndexSyncManager:
    def __init__(self):
        self.connectors: Dict[str, SearchEngineConnector] = {}
        self.sync_history: List[Dict[str, Any]] = []
        self.is_running = False
    
    def register_search_engine(self, config: SearchEngineConfig) -> None:
        self.connectors[config.name] = SearchEngineConnector(config)
        logger.info(f"Registered search engine: {config.name}")
    
    async def run_continuous_sync(self, check_interval: int = 25) -> None:
        self.is_running = True
        logger.info("\n" + "="*80)
        logger.info("SEARCH INDEX SYNC MANAGER STARTED")
        logger.info("="*80 + "\n")
        
        for connector in self.connectors.values():
            await connector.connect()
        
        try:
            iteration = 0
            while self.is_running:
                iteration += 1
                logger.info(f"[Cycle {iteration}] Indexing documents...")
                
                sample_docs = [{"id": i, "title": f"Doc {i}", "content": f"Content {i}"} for i in range(8)]
                
                tasks = [c.index_documents(sample_docs) for c in self.connectors.values()]
                results = await asyncio.gather(*tasks)
                
                for result in results:
                    self.sync_history.append(result)
                    logger.info(f"✓ {result['search_engine']}: {result['documents_indexed']} docs")
                
                await asyncio.sleep(check_interval)
        
        except KeyboardInterrupt:
            logger.info("Search sync stopped.")
        finally:
            self.is_running = False
            logger.info("Search Index Sync Manager Stopped")
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "running": self.is_running,
            "search_engines": list(self.connectors.keys()),
            "total_documents_indexed": sum(r.get("documents_indexed", 0) for r in self.sync_history)
        }
