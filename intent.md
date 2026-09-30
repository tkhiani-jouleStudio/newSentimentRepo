# Feedback Sentiment Analysis Agent

AI agent for analyzing and classifying customer feedback sentiment.

## Business challenge

Build an AI agent that receives customer feedback, classifies each item as positive, negative, or neutral with 96% accuracy, and provides a concise summary of the feedback.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Sentiment classification accuracy | — | 96% | At go-live | Feedback sentiment analysis | user |

## Key Milestones

1. **Feedback Ingestion** — Agent receives raw feedback input (text) from the user or a calling system.
2. **Sentiment Classification** — Agent classifies each feedback item as positive, negative, or neutral.
3. **Summary Generation** — Agent produces a concise, human-readable summary of the overall feedback.
4. **Result Delivery** — Agent returns structured results (classification + summary) to the requester.
5. **Accuracy Validation** — Agent output is validated against the 96% accuracy target.

## Business Architecture (RBA)

### End-to-End Process

B2C Omnichannel Commerce (physical products)

### Process Hierarchy

```
B2C Omnichannel Commerce (physical products)
└── Marketing to Insight (B2C)
    └── Market products and services (B2C) [BPS-368_002]
        └── Analyze and respond to customer insight
└── Manage Customers and Channels (B2C)
    └── Manage customers (B2C) [BPS-370_003]
        └── Manage customer experience
```

### Summary

The challenge maps to "Manage Customer Experience" and "Analyze and Respond to Customer Insight" within the B2C Omnichannel Commerce E2E process. No standard SAP product covers AI-driven sentiment analysis end-to-end; a custom AI agent is required.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|--------------------|--------------------|---------------------|------|---------------------|
| Classify feedback as positive/negative/neutral | No Recommendation (Customer Experience Management) | — | — | — | — | — | Yes | No SAP API or MCP server for sentiment classification; custom LLM-based agent required |
| Summarize feedback content | No Recommendation | — | — | — | — | — | Yes | Custom agent LLM capability needed |
| Achieve 96% classification accuracy | SAP AI Core (runtime) | — | — | — | — | — | Maybe | Accuracy depends on model and prompt engineering; SAP AI Core provides the runtime |

### Key findings

- No standard SAP API or MCP server was found for sentiment analysis or feedback summarization.
- SAP AI Core provides the LLM runtime for the custom agent.
- SAP Customer Data Platform and SAP Emarsys cover adjacent customer analytics but not NLP sentiment classification.
- A pro-code Python agent (A2A protocol) is the recommended approach.
- Accuracy target of 96% is achievable with a well-prompted LLM; no fine-tuning assumed at this stage.

## Recommendations

### Feedback Sentiment Analysis AI Agent

#### Executive Summary

Python A2A agent for feedback classification and summarization via LLM.

#### Recommended Solution

A pro-code Python AI agent built on the A2A protocol, deployed on SAP AI Core. The agent accepts free-text feedback as input, uses an LLM to classify sentiment (positive, negative, neutral) and generate a summary, then returns structured results. No external SAP API integration is required at this stage.

#### Recommended solution category

AI Agent

#### Intent fit
95%
