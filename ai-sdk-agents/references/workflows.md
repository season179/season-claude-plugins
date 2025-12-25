# Workflow Patterns Reference

Comprehensive guide to structured workflows using AI SDK core functions with OpenRouter.

## Table of Contents

- [Setup](#setup)
- [Choosing Your Approach](#choosing-your-approach)
- [Sequential Processing](#sequential-processing)
- [Routing](#routing)
- [Parallel Processing](#parallel-processing)
- [Orchestrator-Worker](#orchestrator-worker)
- [Evaluator-Optimizer](#evaluator-optimizer)
- [Combining Patterns](#combining-patterns)

## Setup

```ts
import { createOpenRouter } from '@openrouter/ai-sdk-provider';
import { generateText, generateObject, streamText } from 'ai';
import { z } from 'zod';

const openrouter = createOpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});

const model = openrouter.chat('openai/gpt-oss-120b:nitro');
```

## Choosing Your Approach

| Factor | Agent Class | Workflow Patterns |
|--------|-------------|-------------------|
| **Control** | LLM decides flow | You define explicit flow |
| **Predictability** | Non-deterministic | Deterministic |
| **Flexibility** | High | Structured |
| **Error Handling** | Built-in retry | Custom handling |
| **Best For** | Open-ended tasks | Reliable pipelines |

### Decision Framework

```
Is the task well-defined with clear steps?
├─ YES → Use Workflow Patterns
│   ├─ Single linear flow? → Sequential Processing
│   ├─ Different paths based on input? → Routing
│   ├─ Independent subtasks? → Parallel Processing
│   ├─ Complex multi-part task? → Orchestrator-Worker
│   └─ Quality-critical output? → Evaluator-Optimizer
└─ NO → Use Agent Class with tools
```

---

## Sequential Processing

Execute steps in order where each output becomes input for the next.

### When to Use

- Content generation pipelines
- Data transformation processes
- Multi-stage analysis
- Document processing workflows

### Basic Chain

```ts
async function basicChain(input: string) {
  // Step 1: Extract key information
  const { object: extracted } = await generateObject({
    model,
    schema: z.object({
      topics: z.array(z.string()),
      entities: z.array(z.string()),
      sentiment: z.enum(['positive', 'neutral', 'negative']),
    }),
    prompt: `Extract key information from: ${input}`,
  });

  // Step 2: Expand on topics
  const { text: expanded } = await generateText({
    model,
    prompt: `Provide detailed analysis of these topics: ${extracted.topics.join(', ')}
    
    Context: The original text had ${extracted.sentiment} sentiment and mentioned: ${extracted.entities.join(', ')}`,
  });

  // Step 3: Generate summary
  const { text: summary } = await generateText({
    model,
    prompt: `Summarize this analysis in 2-3 sentences: ${expanded}`,
  });

  return { extracted, expanded, summary };
}
```

### Chain with Quality Gates

```ts
async function chainWithQualityGates(input: string) {
  // Step 1: Generate initial content
  const { text: draft } = await generateText({
    model,
    prompt: `Write marketing copy for: ${input}`,
  });

  // Step 2: Quality evaluation
  const { object: quality } = await generateObject({
    model,
    schema: z.object({
      score: z.number().min(1).max(10),
      hasCallToAction: z.boolean(),
      isOnBrand: z.boolean(),
      issues: z.array(z.string()),
      suggestions: z.array(z.string()),
    }),
    prompt: `Evaluate this marketing copy:
    
    ${draft}
    
    Score 1-10, check for call-to-action and brand alignment.`,
  });

  // Step 3: Conditional improvement
  if (quality.score < 7 || !quality.hasCallToAction || !quality.isOnBrand) {
    const { text: improved } = await generateText({
      model,
      prompt: `Improve this marketing copy based on feedback:
      
      Original: ${draft}
      
      Issues: ${quality.issues.join(', ')}
      Suggestions: ${quality.suggestions.join(', ')}
      
      Requirements:
      ${!quality.hasCallToAction ? '- Add a clear call to action' : ''}
      ${!quality.isOnBrand ? '- Improve brand alignment' : ''}
      ${quality.score < 7 ? '- Improve overall quality' : ''}`,
    });

    return { content: improved, quality, wasImproved: true };
  }

  return { content: draft, quality, wasImproved: false };
}
```

### Document Processing Pipeline

```ts
async function documentProcessingPipeline(document: string) {
  // Step 1: Structure extraction
  const { object: structure } = await generateObject({
    model,
    schema: z.object({
      title: z.string(),
      sections: z.array(z.object({
        heading: z.string(),
        content: z.string(),
        type: z.enum(['introduction', 'body', 'conclusion', 'reference']),
      })),
      metadata: z.object({
        wordCount: z.number(),
        readingLevel: z.enum(['basic', 'intermediate', 'advanced']),
        language: z.string(),
      }),
    }),
    prompt: `Parse this document into structured sections: ${document}`,
  });

  // Step 2: Content analysis per section
  const analyzedSections = [];
  for (const section of structure.sections) {
    const { object: analysis } = await generateObject({
      model,
      schema: z.object({
        keyPoints: z.array(z.string()),
        sentiment: z.enum(['positive', 'neutral', 'negative']),
        actionItems: z.array(z.string()),
        questions: z.array(z.string()),
      }),
      prompt: `Analyze this section:
      
      Heading: ${section.heading}
      Content: ${section.content}`,
    });

    analyzedSections.push({ ...section, analysis });
  }

  // Step 3: Generate executive summary
  const { text: executiveSummary } = await generateText({
    model,
    prompt: `Generate an executive summary from this analysis:
    
    Document: ${structure.title}
    
    Key points by section:
    ${analyzedSections.map(s => `- ${s.heading}: ${s.analysis.keyPoints.join(', ')}`).join('\n')}
    
    Action items:
    ${analyzedSections.flatMap(s => s.analysis.actionItems).join('\n')}`,
  });

  // Step 4: Generate recommendations
  const { object: recommendations } = await generateObject({
    model,
    schema: z.object({
      priorities: z.array(z.object({
        item: z.string(),
        urgency: z.enum(['high', 'medium', 'low']),
        rationale: z.string(),
      })),
      nextSteps: z.array(z.string()),
    }),
    prompt: `Based on this document analysis, provide prioritized recommendations:
    
    ${executiveSummary}`,
  });

  return {
    structure,
    analyzedSections,
    executiveSummary,
    recommendations,
  };
}
```

---

## Routing

Model classifies input and routes to appropriate handler with optimized configuration.

### When to Use

- Customer support systems
- Multi-domain assistants
- Adaptive response systems
- Resource optimization (model selection)

### Basic Router

```ts
async function basicRouter(query: string) {
  // Classification step
  const { object: classification } = await generateObject({
    model,
    schema: z.object({
      category: z.enum(['technical', 'billing', 'general', 'urgent']),
      confidence: z.number().min(0).max(1),
      reasoning: z.string(),
    }),
    prompt: `Classify this customer query:
    
    "${query}"
    
    Categories:
    - technical: Product issues, bugs, how-to questions
    - billing: Payments, invoices, subscriptions
    - general: General inquiries, feedback
    - urgent: Security issues, data concerns, critical problems`,
  });

  // Route based on classification
  const handlers = {
    technical: handleTechnicalQuery,
    billing: handleBillingQuery,
    general: handleGeneralQuery,
    urgent: handleUrgentQuery,
  };

  const handler = handlers[classification.category];
  const response = await handler(query, classification);

  return { classification, response };
}

async function handleTechnicalQuery(query: string, classification: any) {
  return generateText({
    model,
    system: `You are a technical support specialist.
    
    Guidelines:
    - Provide step-by-step troubleshooting
    - Include relevant documentation links
    - Offer to escalate if needed`,
    prompt: query,
  });
}

async function handleBillingQuery(query: string, classification: any) {
  return generateText({
    model,
    system: `You are a billing support specialist.
    
    Guidelines:
    - Never share sensitive payment details
    - Explain charges clearly
    - Offer payment options when appropriate`,
    prompt: query,
  });
}

async function handleGeneralQuery(query: string, classification: any) {
  return generateText({
    model,
    system: 'You are a helpful customer service representative.',
    prompt: query,
  });
}

async function handleUrgentQuery(query: string, classification: any) {
  // Urgent queries get priority handling
  return generateText({
    model,
    system: `You are handling an URGENT customer issue.
    
    Priority guidelines:
    - Acknowledge the urgency immediately
    - Provide immediate mitigation steps
    - Escalate to human support
    - Document everything`,
    prompt: query,
  });
}
```

### Multi-Level Router

```ts
async function multiLevelRouter(input: string) {
  // Level 1: Domain classification
  const { object: domain } = await generateObject({
    model,
    schema: z.object({
      domain: z.enum(['sales', 'support', 'product', 'legal']),
      confidence: z.number(),
    }),
    prompt: `Classify the domain: ${input}`,
  });

  // Level 2: Sub-category classification based on domain
  const subCategories = {
    sales: ['inquiry', 'demo_request', 'pricing', 'negotiation'],
    support: ['bug', 'feature_request', 'how_to', 'complaint'],
    product: ['feedback', 'suggestion', 'question', 'documentation'],
    legal: ['privacy', 'terms', 'compliance', 'contract'],
  };

  const { object: subCategory } = await generateObject({
    model,
    schema: z.object({
      subCategory: z.enum(subCategories[domain.domain] as [string, ...string[]]),
      priority: z.enum(['low', 'medium', 'high', 'critical']),
      sentiment: z.enum(['positive', 'neutral', 'negative']),
    }),
    prompt: `Further classify this ${domain.domain} query:
    
    "${input}"
    
    Sub-categories: ${subCategories[domain.domain].join(', ')}`,
  });

  // Level 3: Generate response with appropriate context
  const { text: response } = await generateText({
    model,
    system: getSystemPrompt(domain.domain, subCategory.subCategory, subCategory.priority),
    prompt: input,
  });

  return {
    routing: { domain, subCategory },
    response,
  };
}

function getSystemPrompt(domain: string, subCategory: string, priority: string): string {
  const prompts = {
    sales: {
      inquiry: 'You are a sales representative. Be helpful and informative.',
      demo_request: 'You are scheduling product demos. Collect requirements.',
      pricing: 'You are discussing pricing. Be transparent about options.',
      negotiation: 'You are in sales negotiations. Be professional and flexible.',
    },
    support: {
      bug: 'You are handling bug reports. Collect details and provide workarounds.',
      feature_request: 'You are collecting feature requests. Understand the use case.',
      how_to: 'You are providing technical guidance. Be clear and step-by-step.',
      complaint: 'You are handling a complaint. Be empathetic and solution-focused.',
    },
    // ... more prompts
  };

  let prompt = prompts[domain]?.[subCategory] || 'You are a helpful assistant.';
  
  if (priority === 'critical') {
    prompt += '\n\nThis is a CRITICAL priority issue. Respond with urgency.';
  }

  return prompt;
}
```

---

## Parallel Processing

Execute independent tasks simultaneously for efficiency.

### When to Use

- Multi-aspect analysis
- Batch processing
- Independent evaluations
- Data gathering from multiple sources

### Basic Parallel Execution

```ts
async function parallelAnalysis(content: string) {
  const [sentimentResult, topicsResult, entitiesResult, summaryResult] = await Promise.all([
    // Sentiment analysis
    generateObject({
      model,
      schema: z.object({
        sentiment: z.enum(['positive', 'neutral', 'negative']),
        confidence: z.number(),
        emotionalTone: z.array(z.string()),
      }),
      prompt: `Analyze sentiment: ${content}`,
    }),

    // Topic extraction
    generateObject({
      model,
      schema: z.object({
        mainTopics: z.array(z.string()),
        subTopics: z.array(z.string()),
        categories: z.array(z.string()),
      }),
      prompt: `Extract topics: ${content}`,
    }),

    // Entity recognition
    generateObject({
      model,
      schema: z.object({
        people: z.array(z.string()),
        organizations: z.array(z.string()),
        locations: z.array(z.string()),
        dates: z.array(z.string()),
      }),
      prompt: `Extract entities: ${content}`,
    }),

    // Summary generation
    generateText({
      model,
      prompt: `Summarize in 2-3 sentences: ${content}`,
    }),
  ]);

  return {
    sentiment: sentimentResult.object,
    topics: topicsResult.object,
    entities: entitiesResult.object,
    summary: summaryResult.text,
  };
}
```

### Parallel Code Review

```ts
async function comprehensiveCodeReview(code: string, language: string) {
  const reviewers = [
    {
      name: 'security',
      system: 'You are a security expert. Focus on vulnerabilities, injection risks, authentication issues, and data exposure.',
      schema: z.object({
        vulnerabilities: z.array(z.object({
          severity: z.enum(['critical', 'high', 'medium', 'low']),
          type: z.string(),
          location: z.string(),
          description: z.string(),
          fix: z.string(),
        })),
        overallRisk: z.enum(['critical', 'high', 'medium', 'low', 'none']),
      }),
    },
    {
      name: 'performance',
      system: 'You are a performance engineer. Focus on bottlenecks, memory leaks, inefficient algorithms, and optimization opportunities.',
      schema: z.object({
        issues: z.array(z.object({
          impact: z.enum(['critical', 'high', 'medium', 'low']),
          type: z.string(),
          location: z.string(),
          description: z.string(),
          optimization: z.string(),
        })),
        complexity: z.object({
          time: z.string(),
          space: z.string(),
        }),
      }),
    },
    {
      name: 'maintainability',
      system: 'You are a code quality expert. Focus on readability, structure, documentation, and best practices.',
      schema: z.object({
        issues: z.array(z.object({
          category: z.enum(['naming', 'structure', 'documentation', 'complexity', 'duplication']),
          location: z.string(),
          description: z.string(),
          suggestion: z.string(),
        })),
        scores: z.object({
          readability: z.number().min(1).max(10),
          modularity: z.number().min(1).max(10),
          documentation: z.number().min(1).max(10),
        }),
      }),
    },
    {
      name: 'testing',
      system: 'You are a QA engineer. Focus on testability, edge cases, and test coverage suggestions.',
      schema: z.object({
        testability: z.enum(['excellent', 'good', 'fair', 'poor']),
        suggestedTests: z.array(z.object({
          type: z.enum(['unit', 'integration', 'e2e']),
          description: z.string(),
          scenario: z.string(),
        })),
        edgeCases: z.array(z.string()),
      }),
    },
  ];

  // Run all reviews in parallel
  const reviewPromises = reviewers.map(reviewer =>
    generateObject({
      model,
      system: reviewer.system,
      schema: reviewer.schema,
      prompt: `Review this ${language} code:\n\n${code}`,
    }).then(result => ({
      reviewer: reviewer.name,
      findings: result.object,
    }))
  );

  const reviews = await Promise.all(reviewPromises);

  // Synthesize all reviews
  const { text: synthesis } = await generateText({
    model,
    system: 'You are a technical lead synthesizing multiple code reviews.',
    prompt: `Synthesize these code review findings into a prioritized action plan:

${JSON.stringify(reviews, null, 2)}

Provide:
1. Critical issues requiring immediate attention
2. Recommended improvements in priority order
3. Overall code health assessment`,
  });

  return {
    reviews: Object.fromEntries(reviews.map(r => [r.reviewer, r.findings])),
    synthesis,
  };
}
```

### Batch Processing with Concurrency Control

```ts
async function batchProcessWithConcurrency<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  concurrency: number = 5
): Promise<R[]> {
  const results: R[] = [];
  const executing: Promise<void>[] = [];

  for (const item of items) {
    const promise = processor(item).then(result => {
      results.push(result);
    });

    executing.push(promise);

    if (executing.length >= concurrency) {
      await Promise.race(executing);
      // Remove completed promises
      executing.splice(0, executing.findIndex(p => p === promise) + 1);
    }
  }

  await Promise.all(executing);
  return results;
}

// Usage
async function analyzeDocuments(documents: string[]) {
  return batchProcessWithConcurrency(
    documents,
    async (doc) => {
      const { object } = await generateObject({
        model,
        schema: z.object({
          summary: z.string(),
          topics: z.array(z.string()),
          sentiment: z.enum(['positive', 'neutral', 'negative']),
        }),
        prompt: `Analyze: ${doc}`,
      });
      return object;
    },
    5 // Process 5 at a time
  );
}
```

---

## Orchestrator-Worker

A primary model coordinates specialized workers for complex tasks.

### When to Use

- Complex multi-part projects
- Tasks requiring different expertise
- Hierarchical problem decomposition
- Project management workflows

### Basic Orchestrator-Worker

```ts
async function orchestratedTask(request: string) {
  // Orchestrator: Analyze and plan
  const { object: plan } = await generateObject({
    model,
    system: 'You are a project manager breaking down complex tasks.',
    schema: z.object({
      understanding: z.string(),
      subtasks: z.array(z.object({
        id: z.string(),
        description: z.string(),
        type: z.enum(['research', 'analysis', 'creation', 'review']),
        dependencies: z.array(z.string()),
        priority: z.number(),
      })),
      expectedOutputs: z.array(z.string()),
    }),
    prompt: `Break down this request into subtasks:
    
    "${request}"`,
  });

  // Sort tasks by priority and dependencies
  const sortedTasks = topologicalSort(plan.subtasks);

  // Worker execution
  const results: Record<string, any> = {};

  for (const task of sortedTasks) {
    // Check dependencies are complete
    const dependencyResults = task.dependencies.map(dep => results[dep]);

    // Select appropriate worker based on task type
    const workerResult = await executeWorker(task, dependencyResults);
    results[task.id] = workerResult;
  }

  // Orchestrator: Synthesize results
  const { text: finalOutput } = await generateText({
    model,
    system: 'You are synthesizing work from multiple specialists.',
    prompt: `Combine these results into a cohesive response:
    
    Original request: ${request}
    
    Completed work:
    ${Object.entries(results).map(([id, result]) => `${id}: ${JSON.stringify(result)}`).join('\n')}`,
  });

  return { plan, results, finalOutput };
}

async function executeWorker(task: any, dependencyResults: any[]) {
  const workerConfigs = {
    research: {
      system: 'You are a research specialist. Gather comprehensive information.',
      schema: z.object({
        findings: z.array(z.string()),
        sources: z.array(z.string()),
        confidence: z.number(),
      }),
    },
    analysis: {
      system: 'You are an analyst. Provide deep insights and patterns.',
      schema: z.object({
        insights: z.array(z.string()),
        patterns: z.array(z.string()),
        recommendations: z.array(z.string()),
      }),
    },
    creation: {
      system: 'You are a content creator. Produce high-quality output.',
      schema: z.object({
        content: z.string(),
        format: z.string(),
        quality: z.number(),
      }),
    },
    review: {
      system: 'You are a reviewer. Evaluate and improve work.',
      schema: z.object({
        assessment: z.string(),
        issues: z.array(z.string()),
        improvements: z.array(z.string()),
      }),
    },
  };

  const config = workerConfigs[task.type];

  const { object: result } = await generateObject({
    model,
    system: config.system,
    schema: config.schema,
    prompt: `Task: ${task.description}
    
    ${dependencyResults.length > 0 ? `Previous work:\n${JSON.stringify(dependencyResults)}` : ''}`,
  });

  return result;
}

function topologicalSort(tasks: any[]): any[] {
  const sorted: any[] = [];
  const visited = new Set<string>();

  function visit(task: any) {
    if (visited.has(task.id)) return;
    visited.add(task.id);

    for (const depId of task.dependencies) {
      const depTask = tasks.find(t => t.id === depId);
      if (depTask) visit(depTask);
    }

    sorted.push(task);
  }

  const byPriority = [...tasks].sort((a, b) => b.priority - a.priority);
  byPriority.forEach(visit);

  return sorted;
}
```

### Feature Implementation Orchestrator

```ts
async function implementFeature(featureRequest: string, codebase: string) {
  // Orchestrator: Architecture planning
  const { object: architecture } = await generateObject({
    model,
    system: 'You are a senior software architect.',
    schema: z.object({
      approach: z.string(),
      components: z.array(z.object({
        name: z.string(),
        purpose: z.string(),
        type: z.enum(['new_file', 'modification', 'test', 'documentation']),
        dependencies: z.array(z.string()),
      })),
      testingStrategy: z.string(),
      risks: z.array(z.string()),
    }),
    prompt: `Design architecture for this feature:
    
    Feature: ${featureRequest}
    
    Existing codebase structure:
    ${codebase}`,
  });

  // Workers: Implement each component
  const implementations = await Promise.all(
    architecture.components.map(async (component) => {
      const workerPrompts = {
        new_file: 'You are implementing a new component. Follow project conventions.',
        modification: 'You are modifying existing code. Maintain compatibility.',
        test: 'You are writing comprehensive tests. Cover edge cases.',
        documentation: 'You are writing clear documentation. Include examples.',
      };

      const { object: implementation } = await generateObject({
        model,
        system: workerPrompts[component.type],
        schema: z.object({
          code: z.string(),
          explanation: z.string(),
          notes: z.array(z.string()),
        }),
        prompt: `Implement: ${component.name}
        
        Purpose: ${component.purpose}
        
        Feature context: ${featureRequest}
        
        Architecture context: ${architecture.approach}`,
      });

      return { component, implementation };
    })
  );

  // Orchestrator: Integration review
  const { object: integrationReview } = await generateObject({
    model,
    system: 'You are reviewing code integration.',
    schema: z.object({
      isConsistent: z.boolean(),
      integrationIssues: z.array(z.string()),
      suggestedChanges: z.array(z.object({
        component: z.string(),
        change: z.string(),
      })),
    }),
    prompt: `Review these implementations for integration issues:
    
    ${JSON.stringify(implementations, null, 2)}`,
  });

  return {
    architecture,
    implementations,
    integrationReview,
  };
}
```

---

## Evaluator-Optimizer

Iterative quality improvement through evaluation and refinement loops.

### When to Use

- Quality-critical content
- Translation and localization
- Creative writing
- Code generation
- Any output requiring polish

### Basic Evaluation Loop

```ts
async function evaluateAndOptimize(
  task: string,
  maxIterations: number = 3,
  qualityThreshold: number = 8
) {
  let currentOutput = '';
  let iteration = 0;
  let evaluation: any = null;

  // Initial generation
  const { text: initial } = await generateText({
    model,
    prompt: task,
  });

  currentOutput = initial;

  // Evaluation-optimization loop
  while (iteration < maxIterations) {
    // Evaluate current output
    const { object: newEvaluation } = await generateObject({
      model,
      schema: z.object({
        qualityScore: z.number().min(1).max(10),
        strengths: z.array(z.string()),
        weaknesses: z.array(z.string()),
        suggestions: z.array(z.string()),
        meetsRequirements: z.boolean(),
      }),
      prompt: `Evaluate this output against the original task:
      
      Task: ${task}
      
      Output: ${currentOutput}`,
    });

    evaluation = newEvaluation;

    // Check if quality threshold is met
    if (evaluation.qualityScore >= qualityThreshold && evaluation.meetsRequirements) {
      break;
    }

    // Optimize based on feedback
    const { text: improved } = await generateText({
      model,
      prompt: `Improve this output based on feedback:
      
      Original task: ${task}
      
      Current output: ${currentOutput}
      
      Weaknesses to address:
      ${evaluation.weaknesses.join('\n')}
      
      Improvement suggestions:
      ${evaluation.suggestions.join('\n')}`,
    });

    currentOutput = improved;
    iteration++;
  }

  return {
    finalOutput: currentOutput,
    iterations: iteration + 1,
    finalEvaluation: evaluation,
  };
}
```

### Multi-Criteria Evaluation

```ts
async function multiCriteriaOptimization(content: string, criteria: string[]) {
  let currentContent = content;
  let iteration = 0;
  const maxIterations = 5;

  while (iteration < maxIterations) {
    // Evaluate against all criteria in parallel
    const evaluations = await Promise.all(
      criteria.map(criterion =>
        generateObject({
          model,
          schema: z.object({
            criterion: z.string(),
            score: z.number().min(1).max(10),
            met: z.boolean(),
            feedback: z.string(),
            improvements: z.array(z.string()),
          }),
          prompt: `Evaluate against criterion "${criterion}":
          
          Content: ${currentContent}`,
        }).then(r => r.object)
      )
    );

    // Check if all criteria are met
    const allMet = evaluations.every(e => e.met);
    const avgScore = evaluations.reduce((sum, e) => sum + e.score, 0) / evaluations.length;

    if (allMet && avgScore >= 8) {
      return {
        content: currentContent,
        iterations: iteration + 1,
        evaluations,
        averageScore: avgScore,
      };
    }

    // Prioritize improvements by lowest scores
    const prioritized = [...evaluations].sort((a, b) => a.score - b.score);
    const focusAreas = prioritized.slice(0, 2);

    // Optimize
    const { text: improved } = await generateText({
      model,
      prompt: `Improve this content focusing on these criteria:
      
      Content: ${currentContent}
      
      Priority improvements needed:
      ${focusAreas.map(e => `${e.criterion}: ${e.feedback}\n${e.improvements.join('\n')}`).join('\n\n')}`,
    });

    currentContent = improved;
    iteration++;
  }

  return { content: currentContent, iterations: maxIterations };
}
```

### Translation with Back-Translation Verification

```ts
async function verifiedTranslation(
  text: string,
  sourceLang: string,
  targetLang: string
) {
  let currentTranslation = '';
  let iteration = 0;
  const maxIterations = 3;

  // Initial translation
  const { text: initial } = await generateText({
    model,
    system: `You are an expert translator from ${sourceLang} to ${targetLang}.`,
    prompt: `Translate, preserving meaning, tone, and cultural nuances:
    
    ${text}`,
  });

  currentTranslation = initial;

  while (iteration < maxIterations) {
    // Back-translate to source language
    const { text: backTranslation } = await generateText({
      model,
      system: `You are an expert translator from ${targetLang} to ${sourceLang}.`,
      prompt: `Translate back to ${sourceLang}:
      
      ${currentTranslation}`,
    });

    // Compare original with back-translation
    const { object: comparison } = await generateObject({
      model,
      schema: z.object({
        semanticSimilarity: z.number().min(0).max(1),
        preservedMeaning: z.boolean(),
        preservedTone: z.boolean(),
        lostElements: z.array(z.string()),
        addedElements: z.array(z.string()),
        suggestions: z.array(z.string()),
      }),
      prompt: `Compare these texts for translation accuracy:
      
      Original (${sourceLang}): ${text}
      
      Back-translation (${sourceLang}): ${backTranslation}`,
    });

    // Check quality
    if (comparison.semanticSimilarity > 0.95 && 
        comparison.preservedMeaning && 
        comparison.preservedTone) {
      return {
        translation: currentTranslation,
        iterations: iteration + 1,
        quality: comparison,
      };
    }

    // Improve translation based on comparison
    const { text: improved } = await generateText({
      model,
      system: `You are refining a ${sourceLang} to ${targetLang} translation.`,
      prompt: `Improve this translation based on back-translation analysis:
      
      Original: ${text}
      
      Current translation: ${currentTranslation}
      
      Issues found:
      - Lost elements: ${comparison.lostElements.join(', ')}
      - Added elements: ${comparison.addedElements.join(', ')}
      
      Suggestions: ${comparison.suggestions.join('\n')}`,
    });

    currentTranslation = improved;
    iteration++;
  }

  return { translation: currentTranslation, iterations: maxIterations };
}
```

---

## Combining Patterns

Real-world applications often combine multiple patterns.

### Research Pipeline (Sequential + Parallel + Evaluator)

```ts
async function researchPipeline(topic: string) {
  // Step 1: Sequential - Define research questions
  const { object: researchPlan } = await generateObject({
    model,
    schema: z.object({
      mainQuestion: z.string(),
      subQuestions: z.array(z.string()),
      methodology: z.string(),
    }),
    prompt: `Create a research plan for: ${topic}`,
  });

  // Step 2: Parallel - Research each question
  const findings = await Promise.all(
    researchPlan.subQuestions.map(question =>
      generateObject({
        model,
        schema: z.object({
          question: z.string(),
          findings: z.array(z.string()),
          confidence: z.number(),
          gaps: z.array(z.string()),
        }),
        prompt: `Research: ${question}`,
      }).then(r => r.object)
    )
  );

  // Step 3: Evaluator - Synthesize with quality check
  let synthesis = '';
  let quality = 0;
  let iteration = 0;

  while (quality < 8 && iteration < 3) {
    const { text: draft } = await generateText({
      model,
      prompt: `Synthesize research findings into a comprehensive answer:
      
      Main question: ${researchPlan.mainQuestion}
      
      Findings:
      ${JSON.stringify(findings, null, 2)}
      
      ${synthesis ? `Previous attempt (improve on this): ${synthesis}` : ''}`,
    });

    const { object: evaluation } = await generateObject({
      model,
      schema: z.object({
        score: z.number().min(1).max(10),
        isComprehensive: z.boolean(),
        addressesMainQuestion: z.boolean(),
        feedback: z.string(),
      }),
      prompt: `Evaluate this research synthesis:
      
      Main question: ${researchPlan.mainQuestion}
      
      Synthesis: ${draft}`,
    });

    synthesis = draft;
    quality = evaluation.score;
    iteration++;
  }

  return {
    researchPlan,
    findings,
    synthesis,
    iterations: iteration,
  };
}
```

### Customer Service System (Routing + Orchestrator + Evaluator)

```ts
async function customerServiceSystem(customerMessage: string, customerHistory: any) {
  // Routing: Classify and route
  const { object: routing } = await generateObject({
    model,
    schema: z.object({
      intent: z.enum(['support', 'sales', 'billing', 'feedback', 'escalation']),
      urgency: z.enum(['low', 'medium', 'high', 'critical']),
      sentiment: z.enum(['positive', 'neutral', 'negative', 'angry']),
      requiresHuman: z.boolean(),
    }),
    prompt: `Classify this customer message:
    
    Message: ${customerMessage}
    
    Customer history: ${JSON.stringify(customerHistory)}`,
  });

  if (routing.requiresHuman) {
    return {
      routing,
      response: 'Connecting you with a human agent...',
      escalated: true,
    };
  }

  // Orchestrator: Plan response
  const { object: plan } = await generateObject({
    model,
    schema: z.object({
      steps: z.array(z.object({
        action: z.string(),
        type: z.enum(['lookup', 'generate', 'calculate']),
      })),
      tone: z.string(),
      keyPoints: z.array(z.string()),
    }),
    prompt: `Plan response for ${routing.intent} request with ${routing.sentiment} sentiment:
    
    ${customerMessage}`,
  });

  // Workers: Execute plan steps
  const stepResults = await Promise.all(
    plan.steps.map(step => executeStep(step, customerMessage, customerHistory))
  );

  // Generate response
  let response = '';
  let quality = 0;
  let iteration = 0;

  // Evaluator: Quality loop
  while (quality < 8 && iteration < 2) {
    const { text: draft } = await generateText({
      model,
      system: `You are a customer service agent. Tone: ${plan.tone}`,
      prompt: `Respond to customer:
      
      Message: ${customerMessage}
      
      Key points to address: ${plan.keyPoints.join(', ')}
      
      Information gathered: ${JSON.stringify(stepResults)}
      
      ${response ? `Improve on: ${response}` : ''}`,
    });

    const { object: evaluation } = await generateObject({
      model,
      schema: z.object({
        score: z.number().min(1).max(10),
        isHelpful: z.boolean(),
        isEmpathetic: z.boolean(),
        addressesConcern: z.boolean(),
      }),
      prompt: `Evaluate this customer service response:
      
      Customer sentiment: ${routing.sentiment}
      Response: ${draft}`,
    });

    response = draft;
    quality = evaluation.score;
    iteration++;
  }

  return { routing, plan, response, iterations: iteration };
}

async function executeStep(step: any, message: string, history: any) {
  return { step: step.action, result: 'Step completed' };
}
```
