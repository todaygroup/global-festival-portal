# 🌐 Global Festival Portal: System Architecture (v2.0 - Self-Evolving)

## 1. System Overview
The Global Festival Portal is an autonomous agentic ecosystem designed to discover, analyze, and market global festivals via short-form content. The system operates on a **Closed-Loop Feedback Mechanism**, where performance data directly informs the evolution of the system's rules and strategies.

## 2. Multi-Dimensional Flow Analysis

### 🔄 Work Flow (Event-Driven Autonomy)
- **Trigger:** Scheduled (Cron) or Event-based (Trend Discovery).
- **Process:** `Collect` $\rightarrow$ `Process` $\rightarrow$ `Ideate` $\rightarrow$ `Produce` $\rightarrow$ `Distribute` $\rightarrow$ `Analyze` $\rightarrow$ `Optimize`.
- **Self-Correction:** Each stage has a 'Quality Gate'. If the score is below threshold, the task is routed back to the previous stage with a "Reason for Failure".

### 👤 User Flow (Strategic Oversight)
- **User Role:** Strategic Director (sets high-level goals, approves major rule changes).
- **Interface:** High-level status dashboards and "Strategy Proposals" from the Chief Orchestrator.
- **Interaction:** User defines target regions or KPIs $\rightarrow$ System proposes execution plan $\rightarrow$ System executes and reports ROI.

### 💾 Data Flow (Feedback-Integrated)
- **Raw Layer:** Unfiltered festival data (Country Providers).
- **Enriched Layer:** Translated, viral-hooked, and scored data (AI Processor).
- **Asset Layer:** Final rendered videos and captions (Production Engine).
- **Insight Layer:** CTR, Conversion, View counts (Analytics).
- **Strategy Layer:** Dynamic weights and trigger blueprints (`active_strategy.json`, `SYSTEM_RULES.md`).

### 🛠️ Tech Flow (State-Managed Orchestration)
- **Control Plane:** `commander.py` (The Brain) manages the state and delegates tasks.
- **Execution Plane:** Specialized agents (Intelligence, Production, Audit teams).
- **Storage Plane:** Hybrid of JSON files for state and `.md` files for systemic rules.

## 3. The Self-Evolving Loop (Evolution Engine)
The system evolves through the following cycle:
1. **Sensing:** `PerformanceMonitor` and `GrowthOptimizer` track token usage and content ROI.
2. **Analyzing:** Identification of "High-Performing Patterns" (e.g., "FOMO triggers work best for Europe").
3. **Acting:** `GrowthOptimizer` updates `active_strategy.json` and proposes changes to `SYSTEM_RULES.md`.
4. **Learning:** The Chief Orchestrator applies the new rules, and the system measures the delta in performance.

## 4. Scaling Directions
- **Horizontal Scaling:** Adding new `CountryProviders` for worldwide coverage.
- **Vertical Scaling:** Integrating deeper AI layers (e.g., real-time trend analysis from X/TikTok API).
- **Quality Scaling:** Implementing a multi-agent debate system for script finalization.
