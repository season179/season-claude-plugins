# Loop Control Reference

Comprehensive guide to controlling agent execution flow with `stopWhen` and `prepareStep`.

## Table of Contents

- [Understanding the Agent Loop](#understanding-the-agent-loop)
- [Stop Conditions](#stop-conditions)
- [Built-in Conditions](#built-in-conditions)
- [Custom Stop Conditions](#custom-stop-conditions)
- [Combining Conditions](#combining-conditions)
- [prepareStep Callback](#preparestep-callback)
- [Dynamic Model Selection](#dynamic-model-selection)
- [Context Management](#context-management)
- [Tool Selection](#tool-selection)
- [Message Modification](#message-modification)
- [Step Information Access](#step-information-access)
- [Manual Loop Control](#manual-loop-control)

## Understanding the Agent Loop

The agent loop is the core execution cycle:

```
┌─────────────────────────────────────────────────────────┐
│                     Agent Loop                          │
├─────────────────────────────────────────────────────────┤
│  1. prepareStep() called (if defined)                   │
│  2. Model generates response (text or tool call)        │
│  3. If tool call → execute tool, add result to context  │
│  4. Check stopWhen conditions                           │
│  5. If not stopped → return to step 1                   │
│  6. If stopped → return final result                    │
└─────────────────────────────────────────────────────────┘
```

### Default Behavior

By default, agents run for a single step (`stopWhen: stepCountIs(1)`):

```ts
const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  // Implicit: stopWhen: stepCountIs(1)
});

// Single generation - no looping
const result = await agent.generate({ prompt: 'Hello' });
```

### Multi-Step Behavior

Configure `stopWhen` to enable multiple steps:

```ts
const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  tools: { /* ... */ },
  stopWhen: stepCountIs(20), // Allow up to 20 steps
});
```

Each step represents one model generation. The loop continues until:
- The model generates text instead of calling a tool, OR
- A stop condition is met

## Stop Conditions

Stop conditions determine when to end the agent loop after tool execution.

### How Stop Conditions Work

```ts
// Stop condition signature
type StopCondition<TOOLS extends ToolSet> = (args: {
  steps: StepResult<TOOLS>[];
  stepNumber: number;
}) => boolean | Promise<boolean>;
```

- Returns `true` → stop the loop
- Returns `false` → continue to next step
- Evaluated AFTER each tool execution

## Built-in Conditions

### stepCountIs

Stop after a maximum number of steps:

```ts
import { stepCountIs } from 'ai';

const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  tools: { /* ... */ },
  stopWhen: stepCountIs(20), // Stop after 20 steps max
});
```

### hasToolCall

Stop when a specific tool has been called:

```ts
import { hasToolCall } from 'ai';

const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  tools: {
    search: searchTool,
    submitAnswer: submitAnswerTool,
  },
  stopWhen: hasToolCall('submitAnswer'), // Stop when submitAnswer is called
});
```

## Custom Stop Conditions

Create conditions for specific requirements.

### Basic Custom Condition

```ts
import { StopCondition, ToolSet } from 'ai';

const tools = {
  search: searchTool,
  analyze: analyzeTool,
} satisfies ToolSet;

// Stop when model outputs specific text
const hasAnswer: StopCondition<typeof tools> = ({ steps }) => {
  return steps.some(step => step.text?.includes('FINAL ANSWER:')) ?? false;
};

const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  tools,
  stopWhen: hasAnswer,
});
```

### Token Budget Condition

```ts
const tokenBudgetExceeded: StopCondition<typeof tools> = ({ steps }) => {
  const totalTokens = steps.reduce((acc, step) => {
    return acc + (step.usage?.totalTokens ?? 0);
  }, 0);
  
  return totalTokens > 10000; // Stop if over 10k tokens
};
```

### Cost Budget Condition

```ts
const costBudgetExceeded: StopCondition<typeof tools> = ({ steps }) => {
  const totalUsage = steps.reduce(
    (acc, step) => ({
      inputTokens: acc.inputTokens + (step.usage?.inputTokens ?? 0),
      outputTokens: acc.outputTokens + (step.usage?.outputTokens ?? 0),
    }),
    { inputTokens: 0, outputTokens: 0 }
  );

  // Estimate cost (example rates)
  const inputCost = totalUsage.inputTokens * 0.01 / 1000;
  const outputCost = totalUsage.outputTokens * 0.03 / 1000;
  const totalCost = inputCost + outputCost;

  return totalCost > 0.50; // Stop if cost exceeds $0.50
};
```

### Tool Result Condition

```ts
const foundSufficientData: StopCondition<typeof tools> = ({ steps }) => {
  const searchResults = steps
    .flatMap(step => step.toolResults)
    .filter(result => result.toolName === 'search');
  
  // Stop when we have at least 5 search results
  return searchResults.length >= 5;
};
```

### Quality Threshold Condition

```ts
const qualityThresholdMet: StopCondition<typeof tools> = ({ steps }) => {
  const analysisResults = steps
    .flatMap(step => step.toolResults)
    .filter(result => result.toolName === 'analyze');
  
  // Stop when analysis confidence exceeds threshold
  return analysisResults.some(result => {
    const data = result.result as { confidence: number };
    return data.confidence > 0.95;
  });
};
```

### Time-Based Condition

```ts
const createTimeoutCondition = (maxSeconds: number): StopCondition<typeof tools> => {
  const startTime = Date.now();
  
  return () => {
    const elapsedSeconds = (Date.now() - startTime) / 1000;
    return elapsedSeconds > maxSeconds;
  };
};

const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  tools,
  stopWhen: createTimeoutCondition(30), // 30 second timeout
});
```

### Async Condition

```ts
const externalValidation: StopCondition<typeof tools> = async ({ steps }) => {
  const lastResult = steps.at(-1)?.toolResults?.at(-1);
  
  if (!lastResult) return false;
  
  // Check with external service
  const isValid = await validationService.check(lastResult.result);
  return isValid;
};
```

## Combining Conditions

Use an array to combine multiple conditions (stops when ANY is met):

```ts
const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  tools,
  stopWhen: [
    stepCountIs(20),                    // Max 20 steps
    hasToolCall('submitFinalAnswer'),   // Stop on final submission
    tokenBudgetExceeded,                // Stop if tokens exceeded
    costBudgetExceeded,                 // Stop if cost exceeded
  ],
});
```

### Create Condition Combinator

```ts
// All conditions must be true
const allConditions = (...conditions: StopCondition<typeof tools>[]): StopCondition<typeof tools> => {
  return async (args) => {
    const results = await Promise.all(conditions.map(c => c(args)));
    return results.every(r => r === true);
  };
};

// At least N conditions must be true
const atLeastN = (n: number, ...conditions: StopCondition<typeof tools>[]): StopCondition<typeof tools> => {
  return async (args) => {
    const results = await Promise.all(conditions.map(c => c(args)));
    return results.filter(r => r === true).length >= n;
  };
};
```

## prepareStep Callback

Modify agent settings before each step in the loop.

### Signature

```ts
prepareStep: async (args: {
  model: LanguageModel;
  stepNumber: number;
  steps: StepResult<TOOLS>[];
  messages: ModelMessage[];
}) => Promise<PrepareStepResult> | PrepareStepResult;
```

### Return Values

Return an object with any settings to override:

```ts
interface PrepareStepResult {
  model?: LanguageModel;           // Switch model
  messages?: ModelMessage[];       // Modify messages
  activeTools?: string[];          // Subset of tools to enable
  toolChoice?: ToolChoice;         // Force tool behavior
  // ... other generateText options
}
```

Return empty object `{}` to use default settings.

## Dynamic Model Selection

Switch models based on step requirements.

### Escalate to Stronger Model

```ts
const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'), // Default
  tools: { /* ... */ },
  prepareStep: async ({ stepNumber, messages }) => {
    // Use stronger model for complex reasoning after initial steps
    if (stepNumber > 2 && messages.length > 10) {
      return {
        model: openrouter.chat('openai/gpt-oss-120b:nitro'),
      };
    }
    return {};
  },
  stopWhen: stepCountIs(20),
});
```

### Task-Based Model Selection

```ts
prepareStep: async ({ steps }) => {
  const lastToolCall = steps.at(-1)?.toolCalls?.at(-1);
  
  // Use specialized model for code tasks
  if (lastToolCall?.toolName === 'writeCode') {
    return {
      model: openrouter.chat('openai/gpt-oss-120b:nitro'),
    };
  }
  
  // Use fast model for simple lookups
  if (lastToolCall?.toolName === 'lookup') {
    return {
      model: openrouter.chat('openai/gpt-oss-120b:nitro'),
    };
  }
  
  return {};
}
```

## Context Management

Manage growing conversation history in long-running loops.

### Sliding Window

```ts
prepareStep: async ({ messages }) => {
  // Keep only recent messages to stay within context limits
  if (messages.length > 20) {
    return {
      messages: [
        messages[0],           // Keep system message
        ...messages.slice(-10), // Keep last 10 messages
      ],
    };
  }
  return {};
}
```

### Summarize Old Context

```ts
prepareStep: async ({ messages, stepNumber }) => {
  if (messages.length > 30 && stepNumber % 5 === 0) {
    // Every 5 steps, summarize old messages
    const oldMessages = messages.slice(1, -10);
    const summary = await summarizeMessages(oldMessages);
    
    return {
      messages: [
        messages[0],                                    // System message
        { role: 'assistant', content: `Context summary: ${summary}` },
        ...messages.slice(-10),                         // Recent messages
      ],
    };
  }
  return {};
}
```

### Token-Aware Truncation

```ts
prepareStep: async ({ messages }) => {
  const estimatedTokens = messages.reduce((acc, msg) => {
    return acc + estimateTokens(msg.content);
  }, 0);
  
  const MAX_CONTEXT_TOKENS = 100000;
  
  if (estimatedTokens > MAX_CONTEXT_TOKENS) {
    // Remove oldest non-system messages until under limit
    const truncated = [messages[0]]; // Keep system
    let currentTokens = estimateTokens(messages[0].content);
    
    for (const msg of messages.slice(1).reverse()) {
      const msgTokens = estimateTokens(msg.content);
      if (currentTokens + msgTokens < MAX_CONTEXT_TOKENS) {
        truncated.unshift(msg);
        currentTokens += msgTokens;
      }
    }
    
    return { messages: truncated };
  }
  return {};
}
```

## Tool Selection

Control which tools are available at each step.

### Phase-Based Tools

```ts
const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  tools: {
    search: searchTool,
    analyze: analyzeTool,
    summarize: summarizeTool,
  },
  prepareStep: async ({ stepNumber }) => {
    // Search phase (steps 0-2)
    if (stepNumber <= 2) {
      return {
        activeTools: ['search'],
        toolChoice: 'required',
      };
    }
    
    // Analysis phase (steps 3-5)
    if (stepNumber <= 5) {
      return {
        activeTools: ['analyze'],
      };
    }
    
    // Summary phase (step 6+)
    return {
      activeTools: ['summarize'],
      toolChoice: 'required',
    };
  },
  stopWhen: stepCountIs(10),
});
```

### Conditional Tool Access

```ts
prepareStep: async ({ steps }) => {
  const hasSearched = steps.some(step => 
    step.toolCalls?.some(call => call.toolName === 'search')
  );
  
  // Only allow analyze after searching
  if (!hasSearched) {
    return { activeTools: ['search'] };
  }
  
  return { activeTools: ['search', 'analyze', 'report'] };
}
```

### Force Specific Tool

```ts
prepareStep: async ({ stepNumber }) => {
  if (stepNumber === 0) {
    // Force search tool first
    return {
      toolChoice: { type: 'tool', toolName: 'search' },
    };
  }
  
  if (stepNumber === 5) {
    // Force summarize after analysis
    return {
      toolChoice: { type: 'tool', toolName: 'summarize' },
    };
  }
  
  return {};
}
```

### Progressive Tool Unlocking

```ts
prepareStep: async ({ steps }) => {
  const toolsUsed = new Set(
    steps.flatMap(s => s.toolCalls?.map(c => c.toolName) ?? [])
  );
  
  // Start with basic tools
  const availableTools = ['search', 'read'];
  
  // Unlock analysis after search
  if (toolsUsed.has('search')) {
    availableTools.push('analyze');
  }
  
  // Unlock report after analysis
  if (toolsUsed.has('analyze')) {
    availableTools.push('generateReport');
  }
  
  // Unlock submission after report
  if (toolsUsed.has('generateReport')) {
    availableTools.push('submit');
  }
  
  return { activeTools: availableTools };
}
```

## Message Modification

Transform messages before sending to the model.

### Summarize Tool Results

```ts
prepareStep: async ({ messages }) => {
  const processedMessages = messages.map(msg => {
    if (msg.role === 'tool' && msg.content.length > 1000) {
      return {
        ...msg,
        content: summarizeToolResult(msg.content),
      };
    }
    return msg;
  });
  
  return { messages: processedMessages };
}
```

### Inject Context

```ts
prepareStep: async ({ messages, stepNumber }) => {
  // Add step-specific context
  const contextMessage = {
    role: 'system' as const,
    content: `Current step: ${stepNumber}. Remember to stay focused on the task.`,
  };
  
  return {
    messages: [...messages, contextMessage],
  };
}
```

### Filter Sensitive Data

```ts
prepareStep: async ({ messages }) => {
  const sanitized = messages.map(msg => ({
    ...msg,
    content: typeof msg.content === 'string' 
      ? redactSensitiveInfo(msg.content)
      : msg.content,
  }));
  
  return { messages: sanitized };
}
```

## Step Information Access

Both `stopWhen` and `prepareStep` receive detailed step information.

### Available Information

```ts
interface StepResult<TOOLS> {
  text?: string;                    // Generated text (if any)
  toolCalls?: ToolCall[];           // Tools called in this step
  toolResults?: ToolResult[];       // Results from tool executions
  usage?: {
    inputTokens: number;
    outputTokens: number;
    totalTokens: number;
  };
  response: {
    messages: ModelMessage[];       // Messages from this step
  };
}
```

### Accessing Previous Results

```ts
prepareStep: async ({ steps }) => {
  // Get all previous tool calls
  const allToolCalls = steps.flatMap(step => step.toolCalls ?? []);
  
  // Get all previous tool results
  const allResults = steps.flatMap(step => step.toolResults ?? []);
  
  // Get specific tool's results
  const searchResults = allResults.filter(r => r.toolName === 'search');
  
  // Check total token usage
  const totalTokens = steps.reduce((acc, step) => 
    acc + (step.usage?.totalTokens ?? 0), 0
  );
  
  // Make decisions based on history
  if (searchResults.length > 3) {
    return { activeTools: ['analyze'] };
  }
  
  return {};
}
```

## Manual Loop Control

For complete control, implement your own loop with core functions.

### Basic Manual Loop

```ts
import { generateText, ModelMessage } from 'ai';
import { createOpenRouter } from '@openrouter/ai-sdk-provider';

const openrouter = createOpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});

async function manualAgentLoop(prompt: string) {
  const messages: ModelMessage[] = [{ role: 'user', content: prompt }];
  let step = 0;
  const maxSteps = 10;

  while (step < maxSteps) {
    const result = await generateText({
      model: openrouter.chat('openai/gpt-oss-120b:nitro'),
      messages,
      tools: {
        // your tools
      },
    });

    // Add response to message history
    messages.push(...result.response.messages);

    // Stop if model generated text (not a tool call)
    if (result.text) {
      return { text: result.text, steps: step + 1, messages };
    }

    step++;
  }

  return { text: null, steps: maxSteps, messages };
}
```

### Advanced Manual Loop with Custom Logic

```ts
async function advancedAgentLoop(prompt: string) {
  const messages: ModelMessage[] = [{ role: 'user', content: prompt }];
  const results: any[] = [];
  let step = 0;
  let totalCost = 0;

  while (step < 20) {
    // Custom pre-step logic
    const currentModel = step < 3 
      ? openrouter.chat('openai/gpt-oss-120b:nitro')
      : openrouter.chat('openai/gpt-oss-120b:nitro');

    // Custom tool selection
    const activeTools = step < 2 
      ? { search: searchTool }
      : { search: searchTool, analyze: analyzeTool };

    const result = await generateText({
      model: currentModel,
      messages,
      tools: activeTools,
    });

    messages.push(...result.response.messages);

    // Track costs
    if (result.usage) {
      totalCost += calculateCost(result.usage);
    }

    // Custom stop conditions
    if (result.text) break;
    if (totalCost > 1.00) break;
    if (results.length > 5) break;

    // Store results for analysis
    if (result.toolResults) {
      results.push(...result.toolResults);
    }

    step++;
  }

  return { messages, results, totalCost, steps: step };
}
```

### Streaming Manual Loop

```ts
import { streamText } from 'ai';

async function* streamingAgentLoop(prompt: string) {
  const messages: ModelMessage[] = [{ role: 'user', content: prompt }];
  let step = 0;

  while (step < 10) {
    const stream = streamText({
      model: openrouter.chat('openai/gpt-oss-120b:nitro'),
      messages,
      tools: { /* ... */ },
    });

    // Yield text chunks as they arrive
    for await (const chunk of stream.textStream) {
      yield { type: 'text', content: chunk };
    }

    const result = await stream;
    messages.push(...result.response.messages);

    // Yield tool calls
    if (result.toolCalls?.length) {
      yield { type: 'tools', calls: result.toolCalls };
    }

    if (result.text) break;
    step++;
  }
}

// Usage
for await (const event of streamingAgentLoop('Research AI trends')) {
  if (event.type === 'text') {
    process.stdout.write(event.content);
  } else {
    console.log('Tool calls:', event.calls);
  }
}
```
