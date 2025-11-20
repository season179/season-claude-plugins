# Security & Privacy Guidelines

This skill visits live websites and captures screenshots. Follow these guidelines to use it responsibly and safely.

## Before Using This Skill

### Data Handling

**Screenshots may contain sensitive information:**
- Delete analysis outputs after theme generation if not needed for reference

**Local storage only:**
- All analysis data is stored on your local machine
- No data is sent to third-party services (except the target website)
- Analysis outputs remain private unless you share them

## Browser Security

Playwright runs a real Chromium browser with these characteristics:

**What happens during analysis:**
- JavaScript execution is enabled (required for accurate design extraction)
- Network requests are made to the target site and its resources
- Cookies and local storage are created during the session
- Browser resources (fonts, images, CSS) are downloaded

**Security measures in place:**
- Browser runs in an isolated context
- Cookies and storage are ephemeral (not persisted between runs)
- Browser instance is closed after analysis completes
- No persistent browsing state is maintained

**Potential risks:**
- Malicious sites could attempt browser exploits (Playwright mitigates this)
- JavaScript on the site executes in the browser context
- Network requests reveal your IP address to the target site

## Rate Limiting & Ethical Scraping

### Responsible Usage

**Don't abuse this skill:**
- Don't run batch analyses on hundreds of sites from one domain
- Respect server resources and bandwidth

**Network considerations:**
- Each analysis makes dozens of network requests
- Downloads all CSS, fonts, and images on the page
- Can use significant bandwidth on large sites
- Be mindful of site performance impact

## Recommendations Summary

✅ **DO:**
- Analyze public marketing and landing pages
- Use themes for inspiration and learning
- Delete screenshots containing sensitive information
- Respect rate limits

❌ **DON'T:**
- Batch-analyze hundreds of sites
