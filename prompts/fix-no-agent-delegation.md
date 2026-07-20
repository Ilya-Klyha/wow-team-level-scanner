# Fix: Eliminate Agent Delegation in wow-team-backlog-readiness Skill

## Problem Statement

During the 2026-07-17 scan execution, the main session delegated work to background agents (via the Agent tool) and then waited synchronously for their results. This created a pattern where:

1. Main session fetched team page HTML bodies (large responses, 10-30KB each)
2. Context window filled up with raw HTML content
3. Instead of offloading to disk and continuing, main launched an agent for "Build teams metadata"
4. Then launched another agent for "Execute backlog queries and full scan"
5. Then launched another agent for "Velocity and runway calculation"
6. Main session was idle during each agent execution, waiting for completion

## Why This Is Wrong

1. **No parallelism gain** - Main is blocked waiting for the agent. The total wall-clock time is: main work + agent spawn overhead + agent work. This is strictly slower than doing everything in main.

2. **Violates skill spec Rule #15** - The skill explicitly states: "This skill does NOT use the Agent tool. All MCP calls are made directly from the main session." and "This design saves ~300K+ tokens per run and reduces execution time by 60%."

3. **Token waste** - Each agent spawns with a fresh context that needs to be populated with instructions, mappings, and configuration. The 3 agents consumed ~362K subagent tokens total. The same work in main would have used the already-loaded context.

4. **Loss of accumulated state** - The main session already had team page HTML in context (needed for DoR extraction). By delegating to an agent, that content had to be re-fetched, doubling API calls.

## Root Cause

The executor (Claude) made a reactive decision when context grew large after fetching team page HTML. Instead of following the skill spec's prescribed solution (immediate file offloading), it chose the path of "fresh context via agent." This is a pattern recognition failure - the LLM associated "context getting large" with "delegate to agent" rather than "offload to disk."

Contributing factors to Rule #15 being ignored:
- Rule #15 is at position 15 of 16 rules - deep in the document, likely to fall out of active attention on long contexts
- The rule's original phrasing lacked "shock value" language strong enough to override the LLM's heuristic bias
- No early-in-the-document priming about this constraint before the first large context event occurs

## Required Fix

Update the skill spec with changes at **4 specific locations** to create layered defense against agent delegation:

1. **Early priming** - Add anti-pattern block in the Execution Model section (consumed before any MCP calls begin)
2. **Decision checkpoint** - Add a context checkpoint after Step 7 (the largest context accumulation point)
3. **Rule reinforcement** - Strengthen Rule #15 with explicit "NO EXCEPTIONS" language
4. **Post-run audit** - Add self-check to Step 13 that flags if the constraint was violated

## Specific Changes

### Change 1: Anti-Pattern Block in Execution Model Section

**Location:** Immediately after the existing "Execution Model - Sequential with Parallel MCP Calls" paragraph (before "Parallel MCP calls:")

**Insert:**

```
+------------------------------------------------------------------------+
| ANTI-PATTERN: DO NOT delegate to Agent tool.                            |
|                                                                         |
| If context feels large after MCP batch responses:                       |
| 1. Write a Python script that extracts needed fields from responses     |
| 2. Execute the script to save extracted data to OUTPUT_DIR              |
| 3. Continue in main session - the raw responses will be forgotten       |
|    naturally as conversation progresses                                  |
|                                                                         |
| NEVER launch Agent() as a "fresh context" workaround.                   |
| Main waiting for agent = pure overhead with zero benefit.               |
+------------------------------------------------------------------------+
```

**Rationale:** Placed early in the document (Execution Model is consumed before Step 1 begins), this primes the model BEFORE it encounters any large context events.

---

### Change 2: Context Checkpoint After Step 7

**Location:** After Step 7 (Fetch Team Names and Page Content), before Step 8 (Extract Board Metadata)

**Insert:**

```
**CONTEXT CHECKPOINT after Step 7:**
At this point, N team page HTML bodies have been fetched (where N = number of teams
found in Step 6). This is the largest context accumulation point in the entire skill.

DO NOT delegate remaining work to agents. This is the expected behavior:
1. The HTML content is NEEDED in subsequent steps (Step 8 extracts board metadata
   from URLs already in context, Step 9A extracts DoR sections from the HTML)
2. After each processing step, write results to files via Python scripts
3. Raw HTML leaves context naturally as new MCP responses push it out of the window
4. If context pressure is felt, offload intermediate results to disk -
   NEVER spawn Agent() as a "fresh context" workaround

The pattern "context feels large -> launch Agent" is ALWAYS wrong here.
The pattern "context feels large -> offload to files, continue in main" is ALWAYS correct.
```

**Rationale:** This is the exact decision point where the 2026-07-17 failure occurred. The checkpoint explains WHY the context is large (it's supposed to be), WHY the data is needed in subsequent steps, and WHAT to do instead of agent delegation. It does not prescribe specific filenames or actions that duplicate later steps - it reinforces the principle.

---

### Change 3: Strengthen Rule #15

**Location:** Replace existing Rule #15 in the "Important Rules" section

**Replace current:**
```
15. **No Background Agents:**
    - This skill does NOT use the Agent tool
    - All MCP calls are made directly from the main session
    - Parallel MCP calls (multiple in one message) provide concurrency without agent overhead
    - Python scripts handle ALL data processing
    - This design saves ~300K+ tokens per run and reduces execution time by 60%
```

**With:**
```
15. **No Background Agents (STRICT - NO EXCEPTIONS):**
    - This skill NEVER uses the Agent tool - not for "fresh context", not for
      "parallel work", not for any reason
    - If context feels full: offload to files via Python, then continue
    - The pattern "launch agent -> wait for result -> continue" is ALWAYS
      slower than "offload to disk -> continue in main"
    - All MCP calls are made directly from the main session
    - Parallel MCP calls (multiple in one message) provide concurrency
    - Python scripts handle ALL data processing
    - This design saves ~300K+ tokens per run and reduces execution time by 60%
    - VIOLATION OF THIS RULE invalidates the entire scan run
```

**Rationale:** Adds explicit counter-conditioning against the specific rationalization the model used ("fresh context"), includes the direct comparison of the two patterns, and adds a consequence statement.

---

### Change 4: Post-Run Self-Check in Step 13

**Location:** Add to Step 13 (Report Completion), after the final console output block

**Insert:**

```
### Execution Integrity Check

If at any point during this execution, the Agent tool was invoked:
- Append to console output: `[ERROR] Agent delegation detected. This violates Rule #15. Scan results may be incomplete or duplicated.`
- Add to teams.json metadata: `"rule_violations": ["agent_delegation"]`

If no Agent tool was invoked (expected path):
- Append to console output: `[OK] Single-session execution confirmed (no agent delegation)`
```

**Rationale:** Creates an audit trail. Even if the model breaks the rule, the violation is surfaced in the output rather than silently producing potentially corrupted results.

---

## Expected Outcome After Fix

- Single-session execution from start to finish
- No Agent tool invocations
- Context managed via Python file offloading after each MCP batch
- Zero subagent tokens consumed
- Total execution tokens reduced by 40-60% compared to agent-delegated run (baseline: ~400K)
- Fewer API calls (no re-fetching data that was already in context)
- Self-reporting of execution integrity in output

## Validation

After implementing the fix, run the skill and verify:
1. Zero Agent tool calls in the execution trace
2. All teams (dynamic count from Step 6) processed in main session
3. All project backlog queries run in main session
4. All velocity queries run in main session
5. Reports generated in main session
6. `[OK] Single-session execution confirmed` message in final output
7. Zero subagent tokens in session summary
8. Total token usage reduced 40-60% vs agent-delegated baseline (~400K)

## Optional Structural Reinforcement

If this problem recurs after implementing the above prompt-level fixes, add a pre-tool hook in `.claude/settings.local.json` that intercepts Agent tool calls during skill execution:

```json
{
  "hooks": {
    "preToolUse": [
      {
        "matcher": "Agent",
        "command": "echo 'BLOCKED: Agent tool is prohibited during wow-team-backlog-readiness execution' && exit 1"
      }
    ]
  }
}
```

This provides a hard structural guarantee that no amount of context pressure can override. However, this blocks Agent for ALL skills in the project, so it should only be applied if the prompt-level fix proves insufficient.
