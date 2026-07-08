import json
import os
from typing import Any, Dict, Tuple, List

class QualityAuditor:
    """
    Quantitative Quality Auditor for the Global Festival Portal.
    Assigns a score (0.0 to 1.0) to each stage output based on heuristic and structural rules.
    """
    
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold

    def audit_processing(self, data: List[Dict]) -> Tuple[bool, float, str]:
        """
        Audits the AI Processing stage.
        """
        if not data:
            return False, 0.0, "No data provided for auditing."

        total_score = 0.0
        reasons = []
        
        sample_size = min(len(data), 5)
        sampled_data = data[:sample_size]
        
        sum_diversity = 0.0
        sum_richness = 0.0

        for item in sampled_data:
            hooks = item.rich_content.viral_hooks if hasattr(item, 'rich_content') else []
            
            # 1. Diversity Check
            diversity_score = min(len(hooks) / 4, 1.0) 
            sum_diversity += diversity_score
            
            # 2. Richness Check
            avg_len = sum(len(h) for h in hooks) / len(hooks) if hooks else 0
            richness_score = 1.0 if avg_len > 30 else (avg_len / 30)
            sum_richness += richness_score

        avg_diversity = sum_diversity / sample_size
        avg_richness = sum_richness / sample_size
        
        final_score = (avg_diversity * 0.6) + (avg_richness * 0.4)
        
        if final_score < self.threshold:
            return False, final_score, f"Low quality: Diversity({avg_diversity:.2f}), Richness({avg_richness:.2f})"
            
        return True, final_score, "Pass"

    def audit_scripting(self, scripts: List[Dict]) -> Tuple[bool, float, str]:
        """
        Audits the Script Generation stage.
        """
        if not scripts:
            return False, 0.0, "No scripts provided for auditing."

        formats = set(s.get('format') for s in scripts)
        format_score = min(len(formats) / 3, 1.0) 
        
        sample_size = min(len(scripts), 5)
        structure_score = 0.0
        for s in scripts[:sample_size]:
            scenes = s.get('blueprint', {}).get('scenes', [])
            if len(scenes) >= 4:
                structure_score += 1.0
            elif len(scenes) > 0:
                structure_score += 0.5
        
        avg_structure = structure_score / sample_size
        final_score = (format_score * 0.4) + (avg_structure * 0.6)

        if final_score < self.threshold:
            return False, final_score, f"Low quality: FormatVariety({format_score:.2f}), Structure({avg_structure:.2f})"
            
        return True, final_score, "Pass"
