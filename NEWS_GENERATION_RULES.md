# VartaPravah News Generation Rules

## Overview

VartaPravah enforces strict rules on news generation to maintain professional broadcast standards and handle varying news volumes appropriately.

---

## Core Rules

### Rule 1: Minimum News Items
- **Minimum**: 5 news items per bulletin
- **Action**: Bulletin cannot be generated with fewer than 5 items
- **Solution**: Queue additional news or wait for more news items

### Rule 2: Maximum News Items
- **Maximum**: 25 news items per bulletin
- **Action**: Any bulletin exceeding 25 items is automatically truncated to 25
- **Solution**: Plan news distribution across multiple bulletins

### Rule 3: Breaking News Threshold
- **Threshold**: Exactly 25 news items
- **Action**: Automatically activates "Breaking News" mode
- **Format**: Special formatting applied (red emoji, priority handling)
- **Duration**: Extended bulletin time, in-depth coverage

---

## News Volume Categories

| Count | Category | Format | Recommendation |
|-------|----------|--------|-----------------|
| 1-4 | Minimal | N/A | Below minimum, rejected |
| 5-10 | Standard | Standard bulletin | Regular bulletin format |
| 11-19 | Extended | Extended bulletin | Longer segment, more detail |
| 20-24 | Comprehensive | Comprehensive bulletin | Multi-segment, detailed coverage |
| 25 | Breaking | Breaking News | Special alerts, extended duration |

---

## Usage Examples

### Example 1: Standard Bulletin (8 items)

```python
from encoder.news_rules_engine import validate_and_process_news

news_list = [
    {
        'headline': 'महाराष्ट्र में नई नीति',
        'content': 'नई नीति अगले सप्ताह से लागू होगी...',
        'category': 'राजनीति'
    },
    # ... 7 more items
]

report = validate_and_process_news(news_list)

# Output:
# {
#   'is_valid': True,
#   'input_count': 8,
#   'volume_category': 'standard',
#   'is_breaking': False,
#   'bulletin_format': 'standard_bulletin',
#   'processed_news': [...]
# }
```

### Example 2: Maximum with Breaking News (25 items)

```python
# 25 items submitted
news_list = [...]  # 25 items

report = validate_and_process_news(news_list)

# Output:
# {
#   'is_valid': True,
#   'input_count': 25,
#   'volume_category': 'breaking',
#   'is_breaking': True,
#   'bulletin_format': 'breaking_news_bulletin',
#   'recommendation': 'BREAKING NEWS. Activate special formatting and alerts.',
#   'processed_news': [...]  # All formatted with 🔴 emoji
# }
```

### Example 3: Below Minimum (3 items)

```python
news_list = [...]  # 3 items

report = validate_and_process_news(news_list)

# Output:
# {
#   'is_valid': False,
#   'input_count': 3,
#   'errors': [
#       'Item 1: Missing required field: category',
#       'Item 3: Content too short',
#       'Insufficient valid news items: 2. Minimum required: 5'
#   ],
#   'processed_news': []
# }
```

### Example 4: Exceeds Maximum (30 items)

```python
news_list = [...]  # 30 items

report = validate_and_process_news(news_list)

# Output:
# {
#   'is_valid': True,
#   'input_count': 30,
#   'enforcement': {
#       'original_count': 30,
#       'final_count': 25,
#       'changes_made': ['Truncated from 30 to 25 items']
#   },
#   'volume_category': 'breaking',
#   'is_breaking': True,
#   'processed_news': [...]  # First 25 items with breaking news formatting
# }
```

---

## API Integration

### New Endpoints for Rule Enforcement

#### 1. Get Rules Summary

```bash
GET /news/rules
```

**Response:**
```json
{
  "minimum_news": 5,
  "maximum_news": 25,
  "breaking_news_threshold": 25,
  "valid_range": "5-25",
  "rules": [
    "Minimum 5 news items per bulletin",
    "Maximum 25 news items per bulletin",
    "At 25 items: Automatically mark as Breaking News",
    "Breaking News items receive special formatting"
  ]
}
```

#### 2. Validate News Before Generation

```bash
POST /news/validate
```

**Request:**
```json
{
  "news_list": [
    {
      "headline": "बातमी मुख्य",
      "content": "विस्तृत विवरण...",
      "category": "सामान्य"
    },
    ...
  ]
}
```

**Response:**
```json
{
  "is_valid": true,
  "input_count": 15,
  "volume_category": "extended",
  "is_breaking": false,
  "bulletin_format": "extended_bulletin",
  "recommendation": "Extended bulletin. Increase graphics complexity.",
  "errors": [],
  "warnings": [],
  "processed_news": [...]
}
```

#### 3. Generate with Rule Enforcement

```bash
POST /bulletin/generate-with-rules
```

**Request:**
```json
{
  "news_list": [...],
  "bulletin_type": "evening"
}
```

**Response:**
```json
{
  "status": "success",
  "bulletin": "evening",
  "news_count": 25,
  "is_breaking": true,
  "message": "Breaking news bulletin generated with 25 items"
}
```

---

## Implementation in main.py

### Update generate_news Function

```python
from encoder.news_rules_engine import validate_and_process_news

def generate_news(news_data=None, custom_path=None, bulletin_type=None):
    """Generate news with rule enforcement."""
    global news_queue, video_list
    
    # Validate news before processing
    if news_data:
        # Single item - wrap in list
        if isinstance(news_data, dict):
            news_data = [news_data]
        
        # Apply rules
        report = validate_and_process_news(news_data)
        
        if not report['is_valid']:
            logger.error(f"News validation failed: {report['errors']}")
            return {
                'status': 'error',
                'message': 'News validation failed',
                'errors': report['errors']
            }
        
        # Use processed news
        news_data = report['processed_news']
        is_breaking = report['is_breaking']
    else:
        # ... rest of logic
```

### Add API Endpoint

```python
@app.post("/news/validate")
def validate_news(request: Dict):
    """Validate news before generation."""
    from encoder.news_rules_engine import validate_and_process_news
    
    try:
        report = validate_and_process_news(request['news_list'])
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/news/rules")
def get_news_rules():
    """Get current news generation rules."""
    from encoder.news_rules_engine import NewsGenerationRules
    return NewsGenerationRules.get_rule_summary()
```

---

## Breaking News Handling

### What Happens at 25 Items?

1. **Automatic Detection**: System detects 25+ items
2. **Formatting Applied**: Each headline gets 🔴 (red circle) emoji
3. **Priority Escalation**: News marked as critical/high-priority
4. **Extended Duration**: Bulletin length increased
5. **Visual Indicators**: Special graphics/banners displayed
6. **Alerts**: May trigger notification systems
7. **Archive**: Marked with breaking_news tag for records

### Example Breaking News Processing

```python
news_item = {
    'headline': 'महत्वपूर्ण घोषणा की गई है',
    'content': 'विस्तृत जानकारी...',
    'category': 'महत्वपूर्ण'
}

formatted = NewsGenerationRules.apply_breaking_news_format(news_item)

# Result:
# {
#   'headline': '🔴 तातडीची बातमी: महत्वपूर्ण घोषणा की गई है',
#   'content': 'विस्तृत जानकारी...',
#   'category': 'महत्वपूर्ण',
#   'breaking': True,
#   'priority': 'critical',
#   'display_style': 'breaking_news_banner'
# }
```

---

## Error Handling

### Minimum Threshold Error

```
Error: Insufficient news items: 3. Minimum required: 5

Solution:
1. Add more news items (need 2 more)
2. Queue pending news
3. Wait for additional items
```

### Maximum Threshold Enforcement

```
Warning: News count exceeded maximum. Truncated 35 → 25

Impact:
- First 25 items kept
- Items 26-35 discarded
- Breaking News flag activated
- Check truncated items separately
```

### Invalid News Item

```
Error: Item 5: Content too short (minimum 10 characters)

Solution:
1. Add more detail to content
2. Review headline for clarity
3. Ensure all required fields present
```

---

## Best Practices

### ✅ DO:
- Queue news items as they arrive
- Batch queue when you have 5+ items
- Use bulletin endpoints for bulk news
- Check validation before generation
- Monitor breaking news bulletins
- Archive processing reports

### ❌ DON'T:
- Submit fewer than 5 items (will be rejected)
- Submit more than 25 items (will be truncated)
- Submit incomplete news items (will be filtered)
- Ignore validation errors
- Submit duplicate headlines
- Mix different bulletin types in queue

---

## Monitoring

### Check Current Rules

```bash
curl http://localhost:8000/news/rules
```

### Validate News Batch

```bash
curl -X POST http://localhost:8000/news/validate \
  -H "Content-Type: application/json" \
  -d '{
    "news_list": [...]
  }'
```

### View Generation Logs

```bash
docker-compose logs app | grep -i "news\|validation\|breaking"
```

---

## Summary

| Rule | Min | Max | Action |
|------|-----|-----|--------|
| News Count | 5 | 25 | Validate & truncate |
| Breaking News | - | 25 | Auto-format & flag |
| Item Validation | - | - | Check fields & length |
| Volume Category | 1 | 25 | Categorize & recommend |

**VartaPravah News Rules Engine ensures professional, consistent, and safe broadcast news generation! 📺**