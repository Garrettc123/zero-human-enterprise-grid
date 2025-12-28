#!/usr/bin/env python3
"""Run Mega Autonomous Sync System."""

import asyncio
import logging
import sys
from dotenv import load_dotenv
from mega_orchestrator import MegaOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point."""
    load_dotenv()
    
    logger.info("Starting Mega Autonomous Sync System...\n")
    
    orchestrator = MegaOrchestrator()
    
    try:
        asyncio.run(orchestrator.orchestrate_all_systems())
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        status = orchestrator.get_full_status()
        logger.info(f"Final Status: {status}")
        sys.exit(0)

if __name__ == "__main__":
    main()
