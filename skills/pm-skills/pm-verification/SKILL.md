---
name: pm-verification
description: "PM 验证门控 — 在声称工作完成前必须运行验证命令并确认输出。证据先行，永远如此。在 prototyping 子阶段 5 使用。"
---

# Verification Before Completion (PM)

## Announcement

I'm using the pm-verification skill to verify this prototype.

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## PM Pipeline Context

This skill is used in the **prototyping Sub-phase 5 (验证)** of the PM workflow. It applies the Iron Law to prototype-specific claims:

- "Prototype compiles"
- "Prototype runs"
- "Walkthrough passes"
- "PRD covered"

Every prototype verification claim must be backed by a freshly run command and its output, just as every code completion claim must be backed by test output.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |
| Prototype compiles | Build command: exit 0 | "No compilation errors visible" |
| Prototype runs | Start command: no crash exit | "Looked at logs, seems fine" |
| Walkthrough passes | Scenario output log for each scenario | "Ran one scenario, others should work" |
| PRD covered | Line-by-line PRD→stub checklist | "Most requirements have stubs" |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"

**Regression tests (TDD Red-Green):**
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)

**Build:**
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)

**Requirements:**
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"

**Agent delegation:**
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report

**Prototype compilation:**
✅ [Run build command] [See: exit 0] "Prototype compiles"
❌ "No obvious errors"

**Prototype runtime:**
✅ [Run start command] [See: running without crash] "Prototype runs"
❌ "Should start fine"

**Scenario walkthrough:**
✅ [Execute scenario] [See: expected output] "Walkthrough scenario X passes"
❌ "Mock data should cover this"

**PRD coverage:**
✅ [Create PRD→stub checklist] [Verify each line] "PRD requirement Y has corresponding stub"
❌ "Most features covered"

## Knowledge Write-Back

Verification results are written back to `.pm-wiki/log.md` under a timestamped entry, recording:
- What was claimed
- What command was run
- What the output showed
- Whether the claim was confirmed or refuted

This creates an auditable trail of evidence for every verification gate in the prototyping phase.

## Why This Matters

From 24 failure memories:
- your human partner said "I don't believe you" - trust broken
- Undefined functions shipped - would crash
- Missing requirements shipped - incomplete features
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.