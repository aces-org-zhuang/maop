# Security Configuration Guide for WeChat Article Extractor

## URL Validation Policy

### Allowed Domains
**Whitelist Only**: Strictly limited to WeChat official account domains
- Primary: `mp.weixin.qq.com`
- Format: `https://mp.weixin.qq.com/s/[article_id]`

### URL Validation Regex
```python
import re

WECHAT_URL_PATTERN = r'https?://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+'

def validate_wechat_url(url: str) -> bool:
    """Validate URL is from WeChat official account."""
    return bool(re.match(WECHAT_URL_PATTERN, url))
```

### Rejection Criteria
Immediately reject URLs containing:
- Other domains (even subdomains)
- IP addresses
- Localhost or 127.0.0.1
- Suspicious characters or patterns
- URL shorteners or redirects

## Browser Sandbox Configuration

### Chromium Launch Arguments
```python
# Required for container compatibility
browser_args = [
    '--no-sandbox',           # Disable Chromium sandbox
    '--disable-setuid-sandbox', # Disable setuid sandbox
    '--disable-dev-shm-usage',  # Avoid /dev/shm issues
    '--disable-accelerated-2d-canvas', # Disable GPU acceleration
    '--no-first-run',         # Skip first run wizard
    '--no-zygote',           # Disable zygote process
    '--single-process',      # Run in single process mode
]
```

### Security Implications
**Risk Level**: Low (when accessing trusted domains only)
- **Container Isolation**: Primary security boundary
- **Domain Restriction**: Only trusted WeChat domains
- **No Plugin Access**: Disabled Flash, Java, etc.
- **Network Isolation**: Browser runs in isolated context

## Anti-Detection Strategies

### User-Agent Configuration
```python
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
]
```

### Browser Context Settings
```python
context_settings = {
    'user_agent': random.choice(USER_AGENTS),
    'locale': 'zh-CN',
    'timezone_id': 'Asia/Shanghai',
    'viewport': {'width': 1920, 'height': 1080},
    'device_scale_factor': 1.0,
    'is_mobile': False,
    'has_touch': False,
}
```

### Interaction Patterns
- **Random Delays**: 1-3 seconds between actions
- **Human-like Scrolling**: Variable speed and direction
- **Mouse Movement Simulation**: Optional coordinate tracking
- **Type Speed Variation**: Natural typing patterns

## Resource Management

### Browser Lifecycle
```python
class SecureBrowserManager:
    def __init__(self):
        self.browser = None
        self.context = None
        self.pages = set()
    
    async def __aenter__(self):
        await self.setup_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
    
    async def cleanup(self):
        """Ensure all resources are properly released."""
        for page in self.pages:
            try:
                await page.close()
            except:
                pass
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
```

### Timeout Configuration
```python
TIMEOUT_CONFIG = {
    'page_load': 15000,      # 15 seconds
    'navigation': 30000,     # 30 seconds
    'element_wait': 5000,    # 5 seconds
    'script execution': 10000, # 10 seconds
    'total_operation': 60000,  # 60 seconds max
}
```

## Network Security

### Request Interception
```python
async def setup_request_interception(page):
    """Block unnecessary resources for security and performance."""
    await page.route("**/*", lambda route: asyncio.create_task(route.continue_()))
    
    # Block specific resource types
    blocked_resources = [
        'image', 'media', 'font', 'stylesheet',
        'websocket', 'manifest', 'other'
    ]
    
    for resource_type in blocked_resources:
        try:
            await page.route(f"**/*", lambda route, rtype=resource_type: 
                asyncio.create_task(route.abort()) if route.request.resource_type == rtype else route.continue_())
        except:
            pass
```

### Domain Whitelisting
```python
ALLOWED_DOMAINS = ['mp.weixin.qq.com', 'res.wx.qq.com']

async def validate_request(request):
    """Validate all requests against whitelist."""
    url = request.url
    if not any(domain in url for domain in ALLOWED_DOMAINS):
        await request.abort()
        return False
    return True
```

## Error Handling and Logging

### Security Event Logging
```python
import logging

security_logger = logging.getLogger('weixin_extractor.security')

def log_security_event(event_type: str, details: dict):
    """Log security-related events."""
    security_logger.info(f"Security Event: {event_type}", extra=details)
    
    # Alert on suspicious activities
    if event_type in ['invalid_url', 'blocked_request', 'timeout_exceeded']:
        security_logger.warning(f"Security Alert: {event_type} - {details}")
```

### Exception Handling
```python
class SecurityException(Exception):
    """Base security exception."""
    pass

class InvalidURLError(SecurityException):
    """Raised when URL validation fails."""
    pass

class DomainNotAllowedError(SecurityException):
    """Raised when accessing non-whitelisted domain."""
    pass

class ExtractionTimeoutError(SecurityException):
    """Raised when extraction exceeds time limit."""
    pass
```

## Best Practices

### Pre-Execution Checks
1. **URL Validation**: Must pass whitelist check
2. **Resource Availability**: Verify browser can start
3. **Network Connectivity**: Check internet access
4. **Domain Resolution**: Verify domain resolves correctly

### Runtime Security
1. **Monitor Timeouts**: Kill long-running operations
2. **Resource Limits**: Constrain memory and CPU usage
3. **Network Monitoring**: Track all outgoing requests
4. **Error Recovery**: Graceful failure handling

### Post-Execution Cleanup
1. **Close All Pages**: Ensure no browser tabs remain
2. **Clear Context**: Remove browsing data
3. **Browser Termination**: Completely close browser
4. **Resource Release**: Free all system resources

## Emergency Procedures

### Immediate Actions on Security Issue
1. **Stop All Operations**: Terminate current extraction
2. **Close Browser**: Force-close all browser instances
3. **Log Incident**: Record all relevant details
4. **Alert Administrator**: Notify security team
5. **Isolate Environment**: Prevent further execution

### Recovery Steps
1. **Review Logs**: Analyze what happened
2. **Update Policies**: Adjust security rules
3. **Test Fixes**: Verify solution works
4. **Resume Operations**: Carefully restart service

## Compliance and Auditing

### Audit Trail
All operations should log:
- Timestamp of extraction
- Source URL
- User who initiated request
- Execution time
- Resource usage
- Success/failure status
- Any security events

### Compliance Checklist
- [ ] URL validation performed on all requests
- [ ] Domain whitelisting enforced
- [ ] Resource limits configured
- [ ] Timeout policies implemented
- [ ] Error handling in place
- [ ] Security logging enabled
- [ ] Regular security reviews scheduled