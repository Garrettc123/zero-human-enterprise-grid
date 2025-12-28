"""Webhook Event Manager - Event-driven synchronization."""

import asyncio
import logging
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class EventType(Enum):
    DEPLOYMENT = "deployment"
    DATA_SYNC = "data_sync"
    INDEX_UPDATE = "index_update"
    MODEL_TRAINED = "model_trained"

@dataclass
class WebhookEvent:
    event_type: EventType
    source: str
    timestamp: datetime
    data: Dict[str, Any]

class WebhookManager:
    def __init__(self):
        self.event_handlers: Dict[EventType, List[Callable]] = {}
        self.event_history: List[WebhookEvent] = []
        self.is_running = False
    
    def register_handler(self, event_type: EventType, handler: Callable) -> None:
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        logger.info(f"Registered handler for {event_type.value}")
    
    async def emit_event(self, event: WebhookEvent) -> None:
        logger.info(f"[Event] {event.event_type.value} from {event.source}")
        self.event_history.append(event)
        
        handlers = self.event_handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Handler error: {e}")
    
    async def run_webhook_listener(self) -> None:
        self.is_running = True
        logger.info("\n" + "="*80)
        logger.info("WEBHOOK MANAGER STARTED")
        logger.info("="*80 + "\n")
        
        try:
            while self.is_running:
                await asyncio.sleep(10)
        except KeyboardInterrupt:
            logger.info("Webhook listener stopped.")
        finally:
            self.is_running = False
            logger.info("Webhook Manager Stopped")
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "running": self.is_running,
            "registered_event_types": len(self.event_handlers),
            "total_events": len(self.event_history)
        }
