# Bright Data Proxy Setup Guide

This guide explains how to configure 9Scraper to use Bright Data's residential proxy network.

## Configuration Overview

The Bright Data proxy configuration has been added to your `.env` file with the following settings:

```env
# Proxy Configuration
USE_PROXIES=true
PROXY_PROVIDER=brightdata
PROXY_HOST=brd.superproxy.io
PROXY_PORT=33335
PROXY_USERNAME=brd-customer-hl_c2f94a5d-zone-residential_proxy1
PROXY_PASSWORD=9w2xx83lltkv
PROXY_SSL_CERT_PATH=/Users/b0s5/Downloads/brightdata_proxy_ca/New SSL certifcate - MUST BE USED WITH PORT 33335/BrightData SSL certificate (port 33335).crt
```

## Important Notes

1. **Port 33335 is Required**: As of September 2024, Bright Data requires using port 33335 with the new SSL certificate. The old port 22225 is deprecated.

2. **SSL Certificate**: The SSL certificate is located at:
   ```
   /Users/b0s5/Downloads/brightdata_proxy_ca/New SSL certifcate - MUST BE USED WITH PORT 33335/BrightData SSL certificate (port 33335).crt
   ```

3. **Proxy Authentication**: The proxy uses the following format:
   - Username: `brd-customer-hl_c2f94a5d-zone-residential_proxy1`
   - Password: `9w2xx83lltkv`

## Testing the Configuration

You can test the proxy configuration using the provided test script:

```bash
python test_proxy.py
```

This script will:
- Verify the configuration is loaded correctly
- Test the proxy connection using Playwright
- Display your proxied IP address

## Curl Command Reference

The original curl command for testing:
```bash
curl --proxy brd.superproxy.io:33335 \
     --proxy-user brd-customer-hl_c2f94a5d-zone-residential_proxy1:9w2xx83lltkv \
     -k "https://lumtest.com/myip.json"
```

## Integration Details

The proxy configuration has been integrated into the scraper base class at:
`backend/app/scraper/base.py`

Key changes:
1. Added proxy configuration fields to `backend/app/core/config.py`
2. Updated `_get_proxy_config()` method to return Bright Data proxy settings
3. Playwright will automatically use these proxy settings when `USE_PROXIES=true`

## Troubleshooting

### SSL Certificate Issues
- Ensure the certificate file exists at the specified path
- For development, Playwright typically handles SSL certificates automatically
- In production, you may need to configure certificate handling explicitly

### Connection Issues
- Verify your Bright Data account is active
- Check that you have sufficient proxy credits
- Ensure the proxy credentials are correct
- Confirm you're using port 33335 (not the old 22225)

### Testing Without SSL Verification
For quick testing, you can bypass SSL verification (not recommended for production):
```python
context_options["ignore_https_errors"] = True
```

## Security Considerations

1. **Never commit proxy credentials to version control**
2. Keep your `.env` file secure and private
3. Rotate proxy passwords regularly
4. Monitor proxy usage to detect any unauthorized access

## Additional Resources

- [Bright Data Documentation](https://docs.brightdata.com)
- [SSL Certificate Guide](https://docs.brightdata.com/general/account/ssl-certificate)
- [Proxy Integration Examples](https://github.com/luminati-io/luminati-proxy)