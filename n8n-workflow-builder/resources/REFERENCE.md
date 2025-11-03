# n8n Reference Guide

This document provides detailed technical reference information for working with n8n workflows.

## Expressions and Data Access

n8n uses a powerful expression system with `{{ }}` syntax to access dynamic data:

### Current Node Data
```javascript
{{ $json.fieldName }}          // Access field from current item's JSON data
{{ $json["field-with-dash"] }} // Access fields with special characters
{{ $json.nested.field }}       // Access nested fields
```

### Previous Node Data
```javascript
{{ $node["NodeName"].json.fieldName }}           // Access specific node's output
{{ $node["HTTP Request"].json.data[0].id }}      // Access arrays and nested data
```

### All Items and Iteration
```javascript
{{ $input.all() }}             // Get all items from input
{{ $itemIndex }}               // Current item index in the list
{{ $input.item.json }}         // Current item being processed
```

### Built-in Functions
```javascript
{{ $now.toISO() }}             // Current timestamp in ISO format
{{ $now.format('yyyy-MM-dd') }} // Formatted current date
{{ $jmespath(data, 'query') }} // Query JSON data with JMESPath
{{ $json.text.toLowerCase() }} // String manipulation methods
```

### Environment Variables
```javascript
{{ $env.VARIABLE_NAME }}       // Access environment variables
{{ $env.API_KEY }}             // Common pattern for API keys
{{ $env.DB_CONNECTION_STRING }} // Database connections
```

### Utility Variables
```javascript
{{ $workflow.name }}           // Current workflow name
{{ $workflow.id }}             // Current workflow ID
{{ $execution.id }}            // Current execution ID
{{ $execution.mode }}          // Execution mode (manual, trigger, etc.)
```

## Execution Modes

n8n workflows can run in different modes:

### Manual Execution
- Triggered by clicking "Execute Workflow" button
- Used for testing and development
- Runs immediately with current data
- Useful for debugging

### Webhook Trigger
- Triggered by incoming HTTP requests
- Can be synchronous (wait for response) or asynchronous
- URL is auto-generated or can be customized
- Supports GET, POST, PUT, DELETE methods

### Schedule Trigger
- Runs on a cron schedule
- Can be configured for specific times/dates
- Supports standard cron syntax
- Example: `0 9 * * 1-5` (9 AM on weekdays)

### Sub-workflow
- Called by other workflows using Execute Workflow node
- Can receive parameters from parent workflow
- Returns data back to parent
- Enables workflow reusability

### External Trigger
- Triggered by external services (email, chat, etc.)
- Depends on specific trigger node type
- Can be real-time or polling-based

## Credential Management

Always use n8n's built-in credential system for secure authentication:

### Credential Types

**OAuth2**: For services like Google, Twitter, etc.
- Automatic token refresh
- Redirect URL configuration
- Scope management

**API Key**: Simple token-based authentication
- Header-based or query parameter
- Can be static or rotating

**Basic Auth**: Username and password
- HTTP Basic Authentication
- Common for REST APIs

**Custom Auth**: For services with unique authentication
- Flexible configuration
- Can combine multiple auth methods

### Best Practices
- Never hardcode credentials in nodes
- Use credential sharing for team workflows
- Set appropriate credential permissions
- Regularly rotate API keys
- Use environment variables for sensitive data

## Node Categories

Understanding node types helps select the right tool:

### Trigger Nodes
Start workflows based on events:
- Webhook Trigger
- Schedule Trigger
- Manual Trigger
- Email Trigger (IMAP)
- Chat Trigger (Slack, Discord, etc.)

### Core Nodes
Data manipulation and logic:
- **Set**: Add/modify/remove fields
- **Code**: Execute JavaScript/Python
- **IF**: Conditional branching
- **Switch**: Multi-way branching
- **Merge**: Combine data from multiple sources
- **Split**: Divide data into separate paths
- **Loop**: Iterate over items
- **HTTP Request**: Make API calls

### Integration Nodes
Connect to external services:
- Database nodes (PostgreSQL, MongoDB, MySQL)
- Cloud storage (Google Drive, Dropbox, S3)
- Communication (Slack, Discord, Email)
- CRM (Salesforce, HubSpot)
- 400+ integrations available

### AI Nodes
Work with AI services:
- OpenAI
- LangChain
- Anthropic Claude
- Vector Store operations
- AI Agent workflows

## Data Structure

n8n passes data between nodes as an array of items:

```javascript
[
  {
    json: {
      // Your actual data
      field1: "value1",
      field2: "value2"
    },
    binary: {
      // Optional binary data (files, images)
      data: Buffer
    }
  },
  // More items...
]
```

### Working with Multiple Items
- Each node processes all items in the array
- Some nodes can loop over items individually
- Use Split node to process items separately
- Use Merge node to combine results

## Error Handling

Configure error handling at multiple levels:

### Node Level
- **Continue on Fail**: Keep workflow running if node fails
- **Retry on Fail**: Automatically retry failed operations
- **Retry Configuration**: Set retry count and delay

### Workflow Level
- **Error Trigger**: Catch errors from any workflow
- **Error Workflow**: Separate workflow for error handling
- **Error Output**: Access error details in subsequent nodes

### Best Practices
- Add error handling for external API calls
- Log errors to monitoring service
- Send notifications for critical failures
- Use try-catch in Code nodes

## Performance Considerations

### Rate Limiting
- Check API rate limits for external services
- Use Wait node to throttle requests
- Implement exponential backoff for retries

### Data Volume
- Consider pagination for large datasets
- Use streaming for large files
- Split processing into sub-workflows for heavy operations

### Execution Time
- Workflows timeout after configured duration
- Long-running tasks may need queue/batch processing
- Use webhooks for async operations

### Memory Usage
- Large binary data can consume memory
- Process files in chunks when possible
- Clean up temporary data
