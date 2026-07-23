import os
import json
import logging
import subprocess
from typing import List, Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Publisher:
    """
    Handles the final stage of the pipeline: merging enriched data into the master file
    and publishing it to GitHub Pages via git.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.master_file_path = Path(config.get('pipeline_settings', {}).get('stages', [{}])[3].get('output_file', 'festivals_master.json'))
        # Correct for absolute path
        self.master_file_path = Path(config.get('system', {}).get('workspace_root', '/home/aiagent/hyeongryeol_workspace')) / self.master_file_path
        
        self.repo_path = Path(config.get('pipeline_settings', {}).get('stages', [{}])[4].get('repo_path', '/home/aiagent/hyeongryeol_workspace'))
        self.branch = config.get('pipeline_settings', {}).get('stages', [{}])[4].get('branch', 'main')

    def merge_to_master(self, enriched_records: List[Dict[str, Any]]) -> bool:
        """
        Merges newly enriched records into the festivals_master.json.
        Prevents duplicates based on 'identity.name_en'.
        """
        logger.info(f"Merging {len(enriched_records)} records into {self.master_file_path}...")
        
        master_data = []
        if self.master_file_path.exists():
            try:
                with open(self.master_file_path, 'r', encoding='utf-8') as f:
                    raw_master = json.load(f)
                    # Handle both formats: List of records OR Object with 'festivals' key
                    if isinstance(raw_master, dict) and 'festivals' in raw_master:
                        master_data = raw_master['festivals']
                    elif isinstance(raw_master, list):
                        master_data = raw_master
                    else:
                        logger.warning(f"Unexpected format in master file. Resetting to empty list.")
                        master_data = []
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error reading master file: {e}")
                master_data = []

        # Use a map for efficient merging (Key: name_en)
        master_map = {rec['identity']['name_en']: rec for rec in master_data}
        
        for rec in enriched_records:
            name_en = rec['identity']['name_en']
            master_map[name_en] = rec
            
        final_data = list(master_map.values())
        
        try:
            with open(self.master_file_path, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Successfully updated master file. Total records: {len(final_data)}")
            return True
        except IOError as e:
            logger.error(f"Failed to write to master file: {e}")
            return False

    def _run_git_command(self, args: List[str]) -> str:
        """
        Helper to run git commands via subprocess.
        """
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(args)}. Error: {e.stderr}")
            raise e

    def publish(self) -> bool:
        """
        Pushes changes to GitHub Pages (force-push to ensure master file sync).
        """
        try:
            logger.info(f"Publishing changes to GitHub branch {self.branch}...")
            
            # Add and commit
            self._run_git_command(["add", str(self.master_file_path.relative_to(self.repo_path))])
            
            # Check if there are changes to commit
            status = self._run_git_command(["status", "--porcelain"])
            if not status:
                logger.info("No changes to commit. Skipping push.")
                return True

            self._run_git_command(["commit", "-m", "🤖 Auto-update: Sync festivals_master.json from pipeline"])
            
            # Force push to GH Pages branch (as requested for deployment automation)
            self._run_git_command(["push", "-u", "origin", self.branch, "--force"])
            
            logger.info("Successfully published to GitHub Pages.")
            return True
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            return False

    def run(self, enriched_records: List[Dict[str, Any]]) -> bool:
        """
        Execution entry point for the publisher.
        """
        if not self.merge_to_master(enriched_records):
            return False
        return self.publish()
