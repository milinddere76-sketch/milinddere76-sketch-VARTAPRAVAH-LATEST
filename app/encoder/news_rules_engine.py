"""
VartaPravah News Generation Rules Engine
Enforces minimum/maximum news limits and breaking news thresholds
"""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class NewsGenerationRules:
    """
    News generation rule enforcement for VartaPravah bulletin system.
    
    Rules:
    - Minimum news per bulletin: 5
    - Maximum news per bulletin: 25
    - At 25 news: Automatically mark as Breaking News
    """
    
    # Rule constants
    MIN_NEWS = 5
    MAX_NEWS = 25
    BREAKING_NEWS_THRESHOLD = 25
    
    @staticmethod
    def validate_news_count(news_list: List[Dict]) -> Dict:
        """
        Validate news count against rules.
        
        Returns:
            {
                'valid': bool,
                'count': int,
                'is_breaking': bool,
                'warnings': [str],
                'errors': [str],
                'adjustments': [str]
            }
        """
        count = len(news_list)
        result = {
            'valid': True,
            'count': count,
            'is_breaking': False,
            'warnings': [],
            'errors': [],
            'adjustments': []
        }
        
        # Check minimum
        if count < NewsGenerationRules.MIN_NEWS:
            result['valid'] = False
            result['errors'].append(
                f"Insufficient news items: {count}. Minimum required: {NewsGenerationRules.MIN_NEWS}"
            )
        
        # Check maximum
        if count > NewsGenerationRules.MAX_NEWS:
            result['valid'] = False
            result['errors'].append(
                f"Too many news items: {count}. Maximum allowed: {NewsGenerationRules.MAX_NEWS}"
            )
        
        # Check breaking news threshold
        if count >= NewsGenerationRules.BREAKING_NEWS_THRESHOLD:
            result['is_breaking'] = True
            result['adjustments'].append(
                f"Breaking News trigger: {count} news items detected. Marking as breaking news."
            )
        
        # Warnings for edge cases
        if count == NewsGenerationRules.MIN_NEWS:
            result['warnings'].append(
                f"At minimum threshold: {count} items. Consider adding more news."
            )
        
        if count >= 20:
            result['warnings'].append(
                f"Approaching maximum threshold: {count}/{NewsGenerationRules.MAX_NEWS}"
            )
        
        return result
    
    @staticmethod
    def enforce_limits(news_list: List[Dict]) -> tuple[List[Dict], Dict]:
        """
        Enforce generation rules on news list.
        
        Returns:
            (adjusted_news_list, enforcement_report)
        """
        adjusted_list = news_list.copy()
        report = {
            'original_count': len(news_list),
            'final_count': len(adjusted_list),
            'changes_made': [],
            'is_breaking': False
        }
        
        # Truncate if exceeds maximum
        if len(adjusted_list) > NewsGenerationRules.MAX_NEWS:
            original_count = len(adjusted_list)
            adjusted_list = adjusted_list[:NewsGenerationRules.MAX_NEWS]
            report['changes_made'].append(
                f"Truncated from {original_count} to {NewsGenerationRules.MAX_NEWS} items"
            )
            logger.warning(
                f"News count exceeded maximum. Truncated {original_count} → {NewsGenerationRules.MAX_NEWS}"
            )
        
        # Set breaking news flag at threshold
        if len(adjusted_list) >= NewsGenerationRules.BREAKING_NEWS_THRESHOLD:
            report['is_breaking'] = True
            report['changes_made'].append(
                f"Breaking News flag activated ({len(adjusted_list)} items)"
            )
            logger.info(f"Breaking News trigger: {len(adjusted_list)} news items")
        
        # Minimum check (just warning if below)
        if len(adjusted_list) < NewsGenerationRules.MIN_NEWS:
            report['changes_made'].append(
                f"WARNING: Below minimum threshold ({len(adjusted_list)}/{NewsGenerationRules.MIN_NEWS})"
            )
            logger.warning(
                f"News count below minimum. Current: {len(adjusted_list)}, Minimum: {NewsGenerationRules.MIN_NEWS}"
            )
        
        report['final_count'] = len(adjusted_list)
        return adjusted_list, report
    
    @staticmethod
    def apply_breaking_news_format(news_item: Dict) -> Dict:
        """
        Apply breaking news formatting to a news item.
        
        Adds breaking news indicators/styling.
        """
        formatted = news_item.copy()
        
        # Add breaking news prefix
        if 'headline' in formatted:
            if not formatted['headline'].startswith('🔴'):
                formatted['headline'] = f"🔴 तातडीची बातमी: {formatted['headline']}"
        
        # Mark as breaking
        formatted['breaking'] = True
        formatted['priority'] = 'critical'
        
        # Add visual indicators
        formatted['display_style'] = 'breaking_news_banner'
        
        return formatted
    
    @staticmethod
    def categorize_news_volume(count: int) -> Dict:
        """
        Categorize news volume and provide handling recommendations.
        """
        categories = {
            'minimal': (1, 4),
            'standard': (5, 10),
            'extended': (11, 19),
            'comprehensive': (20, 24),
            'breaking': (25, 25)
        }
        
        category = None
        for cat_name, (min_val, max_val) in categories.items():
            if min_val <= count <= max_val:
                category = cat_name
                break
        
        recommendations = {
            'minimal': 'Below minimum. Add more news items.',
            'standard': 'Standard bulletin format.',
            'extended': 'Extended bulletin. Increase graphics complexity.',
            'comprehensive': 'Comprehensive bulletin. Consider multi-segment format.',
            'breaking': 'BREAKING NEWS. Activate special formatting and alerts.'
        }
        
        return {
            'count': count,
            'category': category or 'unknown',
            'recommendation': recommendations.get(category, 'Check count validity'),
            'bulletin_format': f"{category}_bulletin" if category else 'default'
        }
    
    @staticmethod
    def get_rule_summary() -> Dict:
        """Get summary of all news generation rules."""
        return {
            'minimum_news': NewsGenerationRules.MIN_NEWS,
            'maximum_news': NewsGenerationRules.MAX_NEWS,
            'breaking_news_threshold': NewsGenerationRules.BREAKING_NEWS_THRESHOLD,
            'valid_range': f"{NewsGenerationRules.MIN_NEWS}-{NewsGenerationRules.MAX_NEWS}",
            'rules': [
                f"Minimum {NewsGenerationRules.MIN_NEWS} news items per bulletin",
                f"Maximum {NewsGenerationRules.MAX_NEWS} news items per bulletin",
                f"At exactly {NewsGenerationRules.BREAKING_NEWS_THRESHOLD} items: Automatically mark as Breaking News",
                "Breaking News items receive special formatting and priority"
            ]
        }


class NewsValidator:
    """Validator for news items before bulletin generation."""
    
    @staticmethod
    def validate_news_item(news: Dict) -> tuple[bool, List[str]]:
        """
        Validate individual news item.
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields
        required_fields = ['headline', 'content', 'category']
        for field in required_fields:
            if field not in news or not news[field]:
                errors.append(f"Missing or empty required field: {field}")
        
        # Check field types
        if 'headline' in news and not isinstance(news['headline'], str):
            errors.append("Headline must be a string")
        
        if 'content' in news and not isinstance(news['content'], str):
            errors.append("Content must be a string")
        
        # Check minimum length
        if 'headline' in news and len(str(news['headline'])) < 3:
            errors.append("Headline too short (minimum 3 characters)")
        
        if 'content' in news and len(str(news['content'])) < 10:
            errors.append("Content too short (minimum 10 characters)")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_news_list(news_list: List[Dict]) -> tuple[bool, List[str], List[Dict]]:
        """
        Validate entire news list.
        
        Returns:
            (is_valid, error_messages, validated_news_items)
        """
        errors = []
        valid_items = []
        
        for idx, news in enumerate(news_list):
            is_valid, item_errors = NewsValidator.validate_news_item(news)
            
            if is_valid:
                valid_items.append(news)
            else:
                for error in item_errors:
                    errors.append(f"Item {idx+1}: {error}")
        
        # Check count after validation
        if len(valid_items) < NewsGenerationRules.MIN_NEWS:
            errors.append(
                f"Insufficient valid news items: {len(valid_items)}. "
                f"Minimum required: {NewsGenerationRules.MIN_NEWS}"
            )
        
        return len(errors) == 0, errors, valid_items


def validate_and_process_news(news_list: List[Dict]) -> Dict:
    """
    Complete validation and processing pipeline for news generation.
    
    Returns comprehensive report with validation results and processed list.
    """
    report = {
        'input_count': len(news_list),
        'validation': {},
        'enforcement': {},
        'processed_news': [],
        'is_valid': False,
        'is_breaking': False,
        'errors': [],
        'warnings': []
    }
    
    # Step 1: Validate individual items
    is_list_valid, list_errors, valid_items = NewsValidator.validate_news_list(news_list)
    report['validation'] = {
        'is_valid': is_list_valid,
        'valid_count': len(valid_items),
        'errors': list_errors
    }
    report['errors'].extend(list_errors)
    
    if not is_list_valid:
        logger.error(f"News validation failed: {len(list_errors)} errors")
        return report
    
    # Step 2: Apply generation rules
    adjusted_news, enforcement = NewsGenerationRules.enforce_limits(valid_items)
    report['enforcement'] = enforcement
    report['processed_news'] = adjusted_news
    report['is_breaking'] = enforcement['is_breaking']
    
    # Step 3: Apply breaking news formatting if needed
    if report['is_breaking']:
        report['processed_news'] = [
            NewsGenerationRules.apply_breaking_news_format(news) 
            for news in report['processed_news']
        ]
    
    # Step 4: Categorize
    volume_info = NewsGenerationRules.categorize_news_volume(len(report['processed_news']))
    report['volume_category'] = volume_info['category']
    report['bulletin_format'] = volume_info['bulletin_format']
    report['recommendation'] = volume_info['recommendation']
    
    report['is_valid'] = True
    
    logger.info(
        f"News processing complete: {report['input_count']} → {len(report['processed_news'])} "
        f"({report['volume_category']}, breaking={report['is_breaking']})"
    )
    
    return report
