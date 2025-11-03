# n8n Troubleshooting Guide

This guide helps diagnose and resolve common issues when building n8n workflows.

## Systematic Troubleshooting Approach

When encountering issues, follow these steps in order:

### 1. Check Official Documentation First
Always verify against the latest n8n documentation:
- Use `WebSearch` to find: `"n8n [node-name] documentation 2025"`
- Use `WebFetch` to read specific doc pages: `https://docs.n8n.io/integrations/builtin/[node-type]/`
- Use `mcp__deepwiki__ask_question` with repo `"n8n-io/n8n"` for technical details

### 2. Verify Node Configuration
- Check all required fields are filled
- Verify field types match expectations (string vs number vs boolean)
- Confirm authentication/credentials are set correctly
- Review expression syntax for dynamic values

### 3. Test Data Flow
- Use manual trigger to test with sample data
- Inspect output of each node using "Execute Node" button
- Check data structure matches what downstream nodes expect
- Verify field names are spelled correctly (case-sensitive)

### 4. Examine Error Messages
n8n provides detailed error messages:
- Read the full error message carefully
- Check the specific node that failed
- Look for API error codes and messages
- Review execution logs for additional context

### 5. Consider Alternative Approaches
If a node isn't working as expected:
- Check if there's a different node for the task
- Try using HTTP Request node as a fallback
- Consider splitting complex operations into multiple nodes
- Look for community workflows with similar patterns

## Common Issues and Solutions

### Issue: "Cannot read property 'X' of undefined"

**Cause**: Trying to access data that doesn't exist

**Solutions**:
```javascript
// ❌ Bad - will fail if field doesn't exist
{{ $json.user.email }}

// ✅ Good - with null check
{{ $json.user?.email || 'default@example.com' }}

// ✅ Good - with conditional
{{ $json.user && $json.user.email ? $json.user.email : 'N/A' }}
```

### Issue: "Expression evaluates to undefined"

**Cause**: Wrong expression syntax or incorrect node reference

**Solutions**:
- Verify node names match exactly (case-sensitive)
- Check if referencing the correct output property (`json`, `binary`, `error`)
- Use the expression editor to test expressions
- Review available data using "Show available data" option

### Issue: Workflow doesn't trigger on schedule

**Cause**: Workflow not activated or incorrect cron syntax

**Solutions**:
1. Ensure workflow is **activated** (toggle in top-right)
2. Verify cron expression using a cron validator
3. Check n8n instance timezone settings
4. Review execution history for errors

### Issue: API authentication fails

**Cause**: Incorrect credentials or expired tokens

**Solutions**:
1. Test credentials using "Test" button in credential modal
2. Check if API key/token is still valid in external service
3. Verify OAuth tokens haven't expired
4. Review API rate limits (may appear as auth errors)
5. Check if IP allowlist is configured on external service

### Issue: Data not passing between nodes

**Cause**: Data structure mismatch or empty output

**Solutions**:
1. Execute each node individually to see output
2. Use Set node to transform data structure
3. Check for empty arrays or null values
4. Verify node connections are correct
5. Review "Continue on Fail" settings

### Issue: "Request failed with status code 4XX/5XX"

**Cause**: HTTP request issues

**4XX Errors** (Client-side):
- `400 Bad Request`: Check request body format
- `401 Unauthorized`: Verify authentication credentials
- `403 Forbidden`: Check API permissions and scopes
- `404 Not Found`: Verify URL and endpoint exist
- `429 Too Many Requests`: Implement rate limiting

**5XX Errors** (Server-side):
- `500 Internal Server Error`: External service issue
- `502 Bad Gateway`: Service temporarily unavailable
- `503 Service Unavailable`: Service down or overloaded
- `504 Gateway Timeout`: Increase timeout or use async

**Solutions**:
- Enable "Continue on Fail" and handle errors
- Add Wait node for rate limiting
- Implement retry logic with exponential backoff
- Check external service status page

### Issue: Expression not working in Code node

**Cause**: Different syntax in Code node vs expression fields

**Note**: Code nodes use pure JavaScript/Python, not n8n expression syntax

```javascript
// ❌ Wrong - n8n expression syntax doesn't work in Code node
const data = {{ $json.field }};

// ✅ Correct - use Code node API
const data = $input.item.json.field;

// ✅ Access all items
const items = $input.all();

// ✅ Return data
return items.map(item => ({
  json: {
    processed: item.json.field
  }
}));
```

### Issue: Binary data (files) not transferring

**Cause**: Binary data handling misconfigured

**Solutions**:
1. Ensure "Binary Property" field is set correctly
2. Check upstream node outputs binary data
3. Verify property name matches (case-sensitive)
4. Use Read Binary File node for local files
5. Check file size limits (some nodes have restrictions)

### Issue: Loop node iterating incorrectly

**Cause**: Loop configuration or exit condition issues

**Solutions**:
1. Verify loop exit condition is reachable
2. Check iteration count/limit settings
3. Ensure data structure is compatible with loop
4. Add debug outputs to track loop progress
5. Consider using Code node for complex iteration

### Issue: Merge node not combining data as expected

**Cause**: Merge mode or input timing issues

**Solutions**:
- Choose correct merge mode:
  - **Append**: Add all items together
  - **Merge By Index**: Combine items at same position
  - **Merge By Key**: Match items by field value
  - **Multiplex**: Create combinations
- Ensure all input nodes execute before merge
- Check data structure compatibility

### Issue: Credentials not available in execution

**Cause**: Credential permissions or workflow settings

**Solutions**:
1. Check workflow has permission to use credential
2. Verify credential is saved and active
3. For self-hosted: check credential encryption key
4. Review credential sharing settings
5. Test credential in different workflow

## Debugging Best Practices

### Enable Detailed Execution Logging
1. Go to Settings → Execution Data
2. Enable "Save Execution Progress"
3. Review step-by-step execution in workflow history

### Use Test Data
1. Create sample data that covers edge cases
2. Use Manual Trigger for controlled testing
3. Test with empty values, null, and missing fields
4. Verify type handling (strings vs numbers)

### Add Debug Outputs
Insert Set or Code nodes to output debug information:
```javascript
// Debug node to inspect data
return items.map(item => ({
  json: {
    debug: {
      originalData: item.json,
      dataType: typeof item.json.field,
      timestamp: new Date().toISOString()
    }
  }
}));
```

### Isolate Problems
1. Disable nodes to isolate failing section
2. Test problematic node in separate workflow
3. Use simple static data first, then real data
4. Add one complexity at a time

### Check Version Compatibility
1. Note your n8n version (Settings → About)
2. Check if node has version-specific features
3. Review changelog for breaking changes
4. Update n8n if using outdated version

## When to Ask for Help

If troubleshooting doesn't resolve the issue:

1. **Search n8n Community Forum**: https://community.n8n.io/
2. **Check GitHub Issues**: https://github.com/n8n-io/n8n/issues
3. **Review n8n Discord**: Active community support
4. **Consult Documentation**: May have updated examples

When asking for help, provide:
- n8n version
- Node configuration (sanitized credentials)
- Error message (full text)
- Sample data structure
- What you've already tried
