import asyncio
import logging
import sys
from festa_core.engine.pipeline_manager import PipelineManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def main():
    """
    Single entry point to trigger the full Festa Guide data pipeline.
    """
    CONFIG_PATH = "/home/aiagent/hyeongryeol_workspace/festa_core/config/config.yaml"
    
    try:
        logger.info("Starting Festa Guide Automation System...")
        manager = PipelineManager(CONFIG_PATH)
        
        # Run the pipeline for Tier 1 targets (Core Global Festivals)
        await manager.run_pipeline(tier=1)
        
        # Optionally run for Tier 2 (Expanded Global Festivals)
        # await manager.run_pipeline(tier=2)
        
        logger.info("Festa Guide Automation System completed successfully.")
        
    except Exception as e:
        logger.exception(f"Pipeline failed with an unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
