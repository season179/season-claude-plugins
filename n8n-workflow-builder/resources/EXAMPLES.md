# n8n Workflow Examples and Patterns

This document provides common workflow patterns and complete examples for building n8n automations.

## Common Workflow Patterns

### Pattern 1: Webhook-based Automation
**Use case**: Receive data via HTTP and process it

```
[Webhook Trigger] → [Validate/Transform Data] → [External Service Action] → [Webhook Response]
```

**Example: Form Submission Handler**
```
1. Webhook Trigger
   - HTTP Method: POST
   - Path: form-submit
   - Response Mode: Respond to Webhook

2. Code Node - Validate Data
   - Validate required fields
   - Clean/sanitize input
   - Transform data structure

3. HTTP Request - External API
   - Method: POST
   - URL: https://api.service.com/endpoint
   - Body: {{ $json }}

4. Set Node - Format Response
   - success: true
   - message: "Form submitted successfully"
   - id: {{ $json.id }}
```

**Sample Data Flow**:
```javascript
// Input (Webhook body)
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Hello!"
}

// After validation (Code node)
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Hello!",
  "timestamp": "2025-01-15T10:30:00Z",
  "valid": true
}

// After API call (HTTP Request)
{
  "id": "submission_123",
  "status": "created",
  "name": "John Doe"
}

// Response (Set node)
{
  "success": true,
  "message": "Form submitted successfully",
  "id": "submission_123"
}
```

---

### Pattern 2: Scheduled Data Sync
**Use case**: Periodically fetch data from one service and update another

```
[Schedule Trigger] → [Fetch from Source] → [Transform Data] → [Upsert to Destination] → [Log Results]
```

**Example: Daily Google Sheets to Airtable Sync**
```
1. Schedule Trigger
   - Mode: Every Day
   - Hour: 9
   - Minute: 0
   - Timezone: America/New_York

2. Google Sheets - Read Rows
   - Operation: Get Many
   - Range: A2:F
   - Sheet Name: Contacts

3. Code Node - Transform Structure
   const items = $input.all();
   return items.map(item => {
     const row = item.json;
     return {
       json: {
         Name: row[0],
         Email: row[1],
         Phone: row[2],
         Company: row[3],
         Status: row[4],
         Notes: row[5]
       }
     };
   });

4. Airtable - Create or Update
   - Operation: Upsert
   - Base: Customer Database
   - Table: Contacts
   - Unique Field: Email
   - Fields to Send: All

5. Set Node - Log Summary
   - timestamp: {{ $now.toISO() }}
   - records_synced: {{ $json.length }}
   - status: "completed"
```

**Sample Data Flow**:
```javascript
// Google Sheets output (raw rows)
[
  ["John Doe", "john@example.com", "555-0100", "Acme Corp", "Active", "VIP"],
  ["Jane Smith", "jane@example.com", "555-0101", "Beta Inc", "Prospect", ""]
]

// After transformation (Code node)
[
  {
    "Name": "John Doe",
    "Email": "john@example.com",
    "Phone": "555-0100",
    "Company": "Acme Corp",
    "Status": "Active",
    "Notes": "VIP"
  },
  {
    "Name": "Jane Smith",
    "Email": "jane@example.com",
    "Phone": "555-0101",
    "Company": "Beta Inc",
    "Status": "Prospect",
    "Notes": ""
  }
]

// Airtable response
{
  "created": 1,
  "updated": 1,
  "total": 2
}
```

---

### Pattern 3: AI-Powered Workflow
**Use case**: Use LLMs to process, analyze, or generate content

```
[Trigger] → [Prepare Context] → [AI Agent/LangChain] → [Process Result] → [Store/Send]
```

**Example: Content Moderation System**
```
1. Webhook Trigger
   - Path: moderate-content
   - Method: POST

2. Set Node - Prepare Prompt
   - content: {{ $json.text }}
   - prompt: "Analyze the following content for inappropriate material..."
   - max_tokens: 500

3. OpenAI Node
   - Resource: Chat
   - Model: gpt-4
   - System Message: "You are a content moderator..."
   - User Message: {{ $json.prompt }}\n\nContent: {{ $json.content }}

4. Code Node - Parse AI Response
   const response = $json.message.content;
   const approved = response.toLowerCase().includes('approved');

   return [{
     json: {
       original_content: $input.first().json.content,
       moderation_result: response,
       approved: approved,
       timestamp: new Date().toISOString()
     }
   }];

5. IF Node - Route Decision
   - Condition: {{ $json.approved }} equals true
   - True: [Approve Content Path]
   - False: [Flag for Review Path]
```

**Sample Data Flow**:
```javascript
// Input (Webhook)
{
  "text": "User comment to moderate",
  "author_id": "user123"
}

// After OpenAI (AI response)
{
  "message": {
    "content": "APPROVED. This content contains no policy violations."
  }
}

// After parsing (Code node)
{
  "original_content": "User comment to moderate",
  "moderation_result": "APPROVED. This content...",
  "approved": true,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

### Pattern 4: Error Handling Workflow
**Use case**: Catch and handle errors from any workflow

```
[Error Trigger] → [Parse Error Details] → [Determine Severity] → [Notify/Log]
```

**Example: Centralized Error Handler**
```
1. Error Trigger
   - Trigger On: Workflow Error

2. Code Node - Extract Error Info
   const error = $json.error;
   const workflow = $json.workflow;

   return [{
     json: {
       workflow_name: workflow.name,
       workflow_id: workflow.id,
       execution_id: $json.execution.id,
       error_message: error.message,
       error_node: error.node?.name,
       timestamp: new Date().toISOString(),
       severity: determineSeverity(error.message)
     }
   }];

3. Switch Node - Route by Severity
   - Mode: Rules
   - Rule 1: {{ $json.severity }} equals "critical"
   - Rule 2: {{ $json.severity }} equals "warning"
   - Fallback: Log only

4a. [Critical Path] Slack - Send Alert
   - Channel: #alerts-critical
   - Message: "🚨 Critical error in {{ $json.workflow_name }}"

4b. [Warning Path] Email - Send Notification
   - To: devteam@company.com
   - Subject: "Warning: {{ $json.workflow_name }}"

4c. [Fallback] HTTP Request - Log Service
   - Method: POST
   - URL: https://logging.service.com/logs
   - Body: {{ $json }}
```

---

## Complex Workflow Examples

### Example 1: E-commerce Order Processing
```
1. Webhook Trigger (Order received)
   ↓
2. IF Node (Check inventory)
   ├─ [In Stock] → Continue
   └─ [Out of Stock] → Notify & Stop
   ↓
3. HTTP Request (Charge payment)
   ↓
4. IF Node (Payment success?)
   ├─ [Yes] → Continue
   └─ [No] → Error workflow
   ↓
5. Merge Node (Combine order + payment data)
   ↓
6. Split In Batches (Process items)
   ↓
7. Loop Over Items
   ├─ Update inventory (Database)
   ├─ Generate shipping label (API)
   └─ Track shipment (Set)
   ↓
8. Email Node (Confirmation to customer)
   ↓
9. Slack Node (Notify fulfillment team)
```

### Example 2: Social Media Monitor & Response
```
1. Schedule Trigger (Every 5 minutes)
   ↓
2. HTTP Request (Twitter API - fetch mentions)
   ↓
3. IF Node (New mentions exist?)
   ├─ [No] → Stop
   └─ [Yes] → Continue
   ↓
4. Loop Over Mentions
   ↓
5. OpenAI (Analyze sentiment)
   ↓
6. Switch Node (Route by sentiment)
   ├─ [Positive] → Like & Thank
   ├─ [Negative] → Escalate to support
   └─ [Neutral] → Log only
   ↓
7. Merge paths
   ↓
8. Database (Log all interactions)
```

### Example 3: Document Processing Pipeline
```
1. Webhook Trigger (File upload notification)
   ↓
2. Google Drive (Download file)
   ↓
3. IF Node (Check file type)
   ├─ [PDF] → Extract text (PDF node)
   ├─ [Image] → OCR (Computer Vision)
   └─ [Other] → Error
   ↓
4. Merge paths
   ↓
5. OpenAI (Summarize & Extract entities)
   ↓
6. Code Node (Structure results)
   ↓
7. Split paths:
   ├─ Database (Store metadata)
   ├─ Airtable (Update records)
   └─ Slack (Notify team)
```

## Advanced Pattern: Sub-workflow Architecture

For complex systems, break workflows into reusable sub-workflows:

### Main Workflow
```
[Trigger] → [Validate Input] → [Execute Sub-workflows] → [Aggregate Results]
```

### Sub-workflow: Data Validation
```
Input: Raw data object
Process: Validate, clean, enrich
Output: Validated data + validation_status
```

### Sub-workflow: External API Call
```
Input: API parameters
Process: Call with retry logic & error handling
Output: API response + metadata
```

### Sub-workflow: Notification Router
```
Input: Notification data + priority
Process: Route to appropriate channel(s)
Output: Delivery confirmation
```

**Benefits**:
- **Reusability**: Use same sub-workflow in multiple workflows
- **Maintainability**: Update logic in one place
- **Testing**: Test sub-workflows independently
- **Organization**: Keep main workflows clean and readable

## Best Practices in Examples

When building your workflows, remember:

1. **Error Handling**: Add "Continue on Fail" where appropriate
2. **Data Validation**: Check inputs before processing
3. **Logging**: Track workflow execution for debugging
4. **Rate Limiting**: Add Wait nodes for API calls
5. **Credentials**: Always use credential system
6. **Testing**: Use Manual Trigger with test data first
7. **Documentation**: Add notes to complex nodes
8. **Performance**: Consider data volume and execution time
