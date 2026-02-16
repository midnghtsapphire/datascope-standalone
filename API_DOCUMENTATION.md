# DataScope Enhanced - API Documentation

## Overview

DataScope Enhanced provides a comprehensive REST API for programmatic access to multi-domain data collection and intelligence generation. The API supports real-time data collection, cached data retrieval, automated report generation, and browser automation for complex data sources.

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

Currently, the API uses basic authentication. In production, implement OAuth2 or JWT tokens.

```bash
# Basic authentication
curl -u username:password http://localhost:5000/api/v1/status
```

## Rate Limiting

- **Default**: 100 requests per minute per IP
- **Authenticated**: 1000 requests per minute per user
- **Browser Automation**: 10 requests per minute per user

## Response Format

All API responses follow this standard format:

```json
{
  "success": true,
  "data": {},
  "message": "Success",
  "timestamp": "2025-09-25T18:03:04.123456",
  "request_id": "req_123456789"
}
```

Error responses:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_DOMAIN",
    "message": "Domain 'invalid-domain' is not supported",
    "details": {}
  },
  "timestamp": "2025-09-25T18:03:04.123456",
  "request_id": "req_123456789"
}
```

## Endpoints

### System Status

#### GET /api/v1/status

Get system status and health information.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "operational",
    "version": "1.0.0",
    "uptime": 3600,
    "supported_domains": ["cybersecurity", "real-estate", "social-media", "healthcare"],
    "browser_automation_available": true,
    "cache_status": "healthy",
    "last_collection": "2025-09-25T17:30:00Z"
  }
}
```

### Data Collection

#### POST /api/v1/collect/{domain}

Collect data for a specific domain.

**Parameters:**
- `domain` (path): Domain to collect data for
- `location` (query, optional): Geographic location filter
- `use_cache` (query, optional): Use cached data if available (default: true)
- `max_items` (query, optional): Maximum items to collect (default: 100)

**Request Body:**
```json
{
  "filters": {
    "date_range": "7d",
    "severity": "high",
    "category": "malware"
  },
  "collection_params": {
    "max_scrolls": 5,
    "wait_time": 3
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "domain": "cybersecurity",
    "location": "federal",
    "collection_timestamp": "2025-09-25T18:03:02.299659",
    "total_items_collected": 1417,
    "sources_processed": 2,
    "data": [
      {
        "cveid": "CVE-2025-20362",
        "vendorproject": "Cisco",
        "product": "Secure Firewall",
        "vulnerabilityname": "Missing Authorization Vulnerability",
        "dateadded": "2025-09-25",
        "severity": "critical"
      }
    ],
    "available_filters": {
      "vendors": ["Cisco", "Microsoft", "Google"],
      "severities": ["critical", "high", "medium", "low"],
      "dates": ["2025-09-25", "2025-09-24"]
    },
    "cache_info": {
      "cached": false,
      "cache_age": null,
      "cache_expires": "2025-09-26T18:03:02Z"
    }
  }
}
```

#### GET /api/v1/collect/{domain}

Get cached data for a domain without triggering new collection.

**Parameters:**
- `domain` (path): Domain to get data for
- `max_age_hours` (query, optional): Maximum cache age in hours (default: 24)

### Browser Automation

#### POST /api/v1/browser/{platform}

Collect data using browser automation for platforms requiring JavaScript or login.

**Parameters:**
- `platform` (path): Platform to collect from (lemon8, instagram, linkedin)

**Request Body:**
```json
{
  "credentials": {
    "username": "your_username",
    "password": "your_password"
  },
  "collection_params": {
    "url": "https://www.lemon8-app.com/trending",
    "max_items": 50,
    "max_scrolls": 5,
    "search_query": "fashion trends"
  },
  "options": {
    "headless": true,
    "save_screenshots": false,
    "extract_images": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "platform": "lemon8",
    "data_count": 45,
    "cache_file": "/cache/lemon8_session_1695659784.json",
    "data": [
      {
        "platform": "lemon8",
        "content": "Amazing fall fashion trends! 🍂",
        "author": "fashionista_2025",
        "engagement": "1.2K",
        "collected_at": 1695659784,
        "url": "https://www.lemon8-app.com/post/123456",
        "images": ["https://img.lemon8.com/image1.jpg"],
        "links": ["https://shop.example.com"]
      }
    ],
    "collection_summary": {
      "total_posts": 45,
      "unique_authors": 23,
      "average_engagement": 856,
      "collection_duration": 120
    }
  }
}
```

### Report Generation

#### POST /api/v1/reports/{domain}

Generate a comprehensive report for collected domain data.

**Parameters:**
- `domain` (path): Domain to generate report for
- `report_type` (query): Type of report (operational, executive, public)
- `format` (query): Output format (markdown, pdf, json)

**Request Body:**
```json
{
  "data_source": "latest",  // or specific collection ID
  "include_sections": [
    "executive_summary",
    "data_analysis",
    "recommendations",
    "appendix"
  ],
  "customization": {
    "title": "Custom Report Title",
    "logo_url": "https://example.com/logo.png",
    "footer_text": "Confidential Report"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "report_id": "cybersecurity_20250925_180304",
    "report_type": "operational",
    "format": "markdown",
    "file_path": "/reports/cybersecurity_20250925_180304_operational_report.md",
    "download_url": "/api/v1/reports/download/cybersecurity_20250925_180304_operational_report.md",
    "generated_at": "2025-09-25T18:03:04Z",
    "sections_included": [
      "executive_summary",
      "threat_analysis",
      "data_samples",
      "recommendations"
    ],
    "statistics": {
      "total_pages": 15,
      "word_count": 3420,
      "data_points": 1417
    }
  }
}
```

#### GET /api/v1/reports/download/{filename}

Download a generated report file.

**Parameters:**
- `filename` (path): Name of the report file to download

### Social Media Integration

#### POST /api/v1/social/generate-images

Generate social media summary images from collected data.

**Request Body:**
```json
{
  "domain": "cybersecurity",
  "data_source": "latest",
  "platforms": ["linkedin", "facebook", "instagram", "tiktok"],
  "style": {
    "theme": "professional",
    "color_scheme": "blue",
    "include_logo": true,
    "font_family": "Arial"
  },
  "content": {
    "title": "Daily Cyber Threat Intelligence",
    "key_stats": [
      "1,417 threats analyzed",
      "23 critical vulnerabilities",
      "5 new ransomware campaigns"
    ],
    "call_to_action": "Stay informed. Stay secure."
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "images": [
      {
        "platform": "linkedin",
        "dimensions": "1200x627",
        "file_path": "/images/linkedin_summary_20250925.png",
        "download_url": "/api/v1/images/download/linkedin_summary_20250925.png"
      },
      {
        "platform": "instagram",
        "dimensions": "1080x1080",
        "file_path": "/images/instagram_summary_20250925.png",
        "download_url": "/api/v1/images/download/instagram_summary_20250925.png"
      }
    ],
    "generation_time": 45,
    "total_images": 4
  }
}
```

### Automation & Scheduling

#### POST /api/v1/automation/schedule

Schedule automated data collection and reporting.

**Request Body:**
```json
{
  "name": "Daily Cyber Intelligence",
  "domains": ["cybersecurity", "healthcare"],
  "schedule": {
    "type": "cron",
    "expression": "0 6 * * *",
    "timezone": "UTC"
  },
  "collection_params": {
    "location": "federal",
    "max_items": 500
  },
  "reporting": {
    "generate_reports": true,
    "report_types": ["operational", "executive"],
    "email_recipients": ["admin@company.com"],
    "social_media_posting": {
      "enabled": true,
      "platforms": ["linkedin", "twitter"]
    }
  },
  "notifications": {
    "on_success": true,
    "on_failure": true,
    "webhook_url": "https://hooks.slack.com/services/..."
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "schedule_id": "sched_123456789",
    "name": "Daily Cyber Intelligence",
    "status": "active",
    "next_run": "2025-09-26T06:00:00Z",
    "created_at": "2025-09-25T18:03:04Z"
  }
}
```

#### GET /api/v1/automation/schedules

List all scheduled automation tasks.

**Response:**
```json
{
  "success": true,
  "data": {
    "schedules": [
      {
        "schedule_id": "sched_123456789",
        "name": "Daily Cyber Intelligence",
        "domains": ["cybersecurity", "healthcare"],
        "status": "active",
        "next_run": "2025-09-26T06:00:00Z",
        "last_run": "2025-09-25T06:00:00Z",
        "success_rate": 0.98
      }
    ],
    "total_schedules": 1,
    "active_schedules": 1
  }
}
```

### Cache Management

#### GET /api/v1/cache/status

Get cache status and statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "cache_type": "file",
    "total_size": "245.7 MB",
    "total_entries": 156,
    "hit_rate": 0.87,
    "domains": {
      "cybersecurity": {
        "entries": 45,
        "size": "123.4 MB",
        "oldest_entry": "2025-09-20T10:30:00Z",
        "newest_entry": "2025-09-25T18:03:02Z"
      }
    }
  }
}
```

#### DELETE /api/v1/cache/{domain}

Clear cache for a specific domain.

**Parameters:**
- `domain` (path): Domain to clear cache for
- `older_than` (query, optional): Clear entries older than specified hours

### Analytics & Insights

#### GET /api/v1/analytics/summary

Get analytics summary across all domains.

**Parameters:**
- `period` (query): Time period (24h, 7d, 30d, 90d)
- `domains` (query): Comma-separated list of domains

**Response:**
```json
{
  "success": true,
  "data": {
    "period": "7d",
    "summary": {
      "total_collections": 42,
      "total_data_points": 15847,
      "unique_sources": 23,
      "reports_generated": 28
    },
    "by_domain": {
      "cybersecurity": {
        "collections": 7,
        "data_points": 9923,
        "avg_collection_time": 45,
        "top_sources": ["CISA KEV", "FBI IC3"]
      }
    },
    "trends": {
      "collection_frequency": [
        {"date": "2025-09-25", "count": 8},
        {"date": "2025-09-24", "count": 6}
      ],
      "data_volume": [
        {"date": "2025-09-25", "volume": 2847},
        {"date": "2025-09-24", "volume": 1923}
      ]
    }
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_DOMAIN` | Specified domain is not supported |
| `COLLECTION_FAILED` | Data collection failed |
| `BROWSER_AUTOMATION_ERROR` | Browser automation encountered an error |
| `AUTHENTICATION_FAILED` | Invalid credentials provided |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `CACHE_ERROR` | Cache operation failed |
| `REPORT_GENERATION_FAILED` | Report generation encountered an error |
| `INVALID_PARAMETERS` | Invalid request parameters |
| `RESOURCE_NOT_FOUND` | Requested resource not found |
| `INTERNAL_ERROR` | Internal server error |

## SDK Examples

### Python SDK

```python
import requests
from typing import Dict, Any

class DataScopeClient:
    def __init__(self, base_url: str, auth: tuple = None):
        self.base_url = base_url
        self.session = requests.Session()
        if auth:
            self.session.auth = auth
    
    def collect_domain_data(self, domain: str, location: str = None, 
                           filters: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/collect/{domain}"
        params = {}
        if location:
            params['location'] = location
        
        response = self.session.post(url, json={'filters': filters or {}}, params=params)
        return response.json()
    
    def generate_report(self, domain: str, report_type: str = 'operational') -> Dict[str, Any]:
        url = f"{self.base_url}/reports/{domain}"
        params = {'report_type': report_type}
        
        response = self.session.post(url, params=params)
        return response.json()

# Usage
client = DataScopeClient('http://localhost:5000/api/v1', auth=('user', 'pass'))
data = client.collect_domain_data('cybersecurity', location='federal')
report = client.generate_report('cybersecurity')
```

### JavaScript SDK

```javascript
class DataScopeClient {
    constructor(baseUrl, auth = null) {
        this.baseUrl = baseUrl;
        this.auth = auth;
    }
    
    async collectDomainData(domain, location = null, filters = {}) {
        const url = `${this.baseUrl}/collect/${domain}`;
        const params = new URLSearchParams();
        if (location) params.append('location', location);
        
        const response = await fetch(`${url}?${params}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(this.auth && { 'Authorization': `Basic ${btoa(`${this.auth.username}:${this.auth.password}`)}` })
            },
            body: JSON.stringify({ filters })
        });
        
        return response.json();
    }
    
    async generateReport(domain, reportType = 'operational') {
        const url = `${this.baseUrl}/reports/${domain}`;
        const params = new URLSearchParams({ report_type: reportType });
        
        const response = await fetch(`${url}?${params}`, {
            method: 'POST',
            headers: {
                ...(this.auth && { 'Authorization': `Basic ${btoa(`${this.auth.username}:${this.auth.password}`)}` })
            }
        });
        
        return response.json();
    }
}

// Usage
const client = new DataScopeClient('http://localhost:5000/api/v1', {
    username: 'user',
    password: 'pass'
});

const data = await client.collectDomainData('cybersecurity', 'federal');
const report = await client.generateReport('cybersecurity');
```

## Webhooks

DataScope Enhanced supports webhooks for real-time notifications:

### Webhook Events

- `collection.completed`: Data collection finished
- `collection.failed`: Data collection failed
- `report.generated`: Report generation completed
- `automation.executed`: Scheduled automation executed
- `cache.cleared`: Cache was cleared

### Webhook Payload

```json
{
  "event": "collection.completed",
  "timestamp": "2025-09-25T18:03:04Z",
  "data": {
    "domain": "cybersecurity",
    "collection_id": "col_123456789",
    "items_collected": 1417,
    "duration": 45,
    "sources": ["CISA KEV", "FBI IC3"]
  }
}
```

## Best Practices

1. **Rate Limiting**: Respect rate limits to avoid being blocked
2. **Caching**: Use cached data when possible to improve performance
3. **Error Handling**: Always handle API errors gracefully
4. **Authentication**: Use secure authentication methods in production
5. **Monitoring**: Monitor API usage and performance
6. **Data Validation**: Validate all input data before sending requests
7. **Pagination**: Use pagination for large datasets
8. **Compression**: Use gzip compression for large responses

## Support

For API support and questions:
- **Documentation**: [Full API Docs](https://docs.datascope-enhanced.com/api)
- **Issues**: [GitHub Issues](https://github.com/your-org/datascope-enhanced/issues)
- **Email**: api-support@datascope-enhanced.com

