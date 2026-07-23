import json
import os
import logging
from typing import List, Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataVerifier:
    """
    Implements the Zero-Mock Policy for Festa Guide.
    Filters out records that lack critical identity fields or a valid source URL.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.min_required_fields = config.get('pipeline_settings', {}).get('stages', [{}])[1].get('min_required_fields', [])
        # Default if config is missing
        if not self.min_required_fields:
            self.min_required_fields = ["name_en", "source_url", "country"]
            
        self.output_dir = Path("/home/aiagent/hyeongryeol_workspace/festa_global_db/verified")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def verify_record(self, record: Dict[str, Any]) -> bool:
        """
        Checks if a record complies with the Zero-Mock Policy.
        Requirement: All min_required_fields must be present and non-empty.
        """
        for field in self.min_required_fields:
            value = record.get(field)
            if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
                logger.debug(f"Record failed verification: missing {field}. Record: {record.get('name_en', 'Unknown')}")
                return False
        
        # Zero-Mock Policy specifically requires source_url to be a physical evidence URL
        source_url = record.get('source_url')
        if not source_url or not source_url.startswith(('http://', 'https://')):
            logger.debug(f"Record failed Zero-Mock Policy: Invalid source_url for {record.get('name_en', 'Unknown')}")
            return False

        return True

    def process_batch(self, records: List[Dict[str, Any]], batch_id: str = "batch_001") -> List[Dict[str, Any]]:
        """
        Filters a batch of records and saves the verified subset to the truth lake.
        """
        verified_records = [rec for rec in records if self.verify_record(rec)]
        
        # Save verified records to L2 Truth Lake
        output_path = self.output_dir / f"verified_{batch_id}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(verified_records, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Verification complete. {len(verified_records)}/{len(records)} records passed. Saved to {output_path}")
        return verified_records

if __name__ == "__main__":
    # Simple test case
    mock_config = {
        'pipeline_settings': {
            'stages': [{}, {'min_required_fields': ["name_en", "source_url", "country"]}]
        }
    }
    verifier = DataVerifier(mock_config)
    test_data = [
        {"name_en": "Festival A", "source_url": "https://fest-a.com", "country": "USA"}, # Pass
        {"name_en": "Festival B", "source_url": "", "country": "JPN"},               # Fail (empty url)
        {"name_en": "Festival C", "source_url": "https://fest-c.com"},               # Fail (missing country)
        {"name_en": "Festival D", "source_url": "invalid_url", "country": "KOR"},    # Fail (invalid url format)
    ]
    result = verifier.process_batch(test_data)
    print(f"Verified: {result}")
