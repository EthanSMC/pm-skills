---
name: pm-tdd
description: 测试驱动开发（内部子 skill，由 pm-writing-plans/pm-executing-plans 引用）— Iron Law 执行纪律、合理化防御
---

# Test-Driven Development (PM Adaptation)

**Announce at start:** "I'm using the pm-tdd skill to drive this implementation."

## 调度路径

pm-tdd 不由 pm-workflow 或 prototyping 直接调度，而是由 pm-writing-plans 和 pm-executing-plans 内部引用：
- pm-workflow → prototyping → pm-writing-plans → pm-tdd（TDD 铁律）
- pm-workflow → prototyping → pm-executing-plans → pm-tdd（执行纪律）

pm-tdd 的 Iron Law 和合理化防御表在 pm-writing-plans 和 pm-executing-plans 执行时自动生效。

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask your human partner):**
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

**Prototype context note:** In PM prototyping flow, the GREEN phase produces stubs and mock returns (not production implementations). The Iron Law still applies: write the test first, watch it fail, then write the stub. The stub is the 'minimal implementation' in prototype scope — `return MOCK_DATA[request.id]` is a valid GREEN.

## PM Pipeline Context

This skill is used in two places in the PM workflow:

1. **pm-writing-plans** uses TDD to structure each plan task as Red → Verify Red → Green → Verify Green → Commit. The plan document itself is the TDD guide for execution.

2. **pm-executing-plans** uses TDD discipline when executing scaffold tasks. Each task step follows the TDD cycle exactly as defined in this skill.

In prototype scope, "minimal implementation" (GREEN phase) means stub/mock returns, not production logic. A `return MOCK_DATA[request.id]` is a perfectly valid GREEN-phase outcome when building a prototype scaffold.

**Pipeline position:**
```
pm-workflow → pm-brainstorming → write-prd → prototyping
  ├── Sub-phase 1: spec.md
  ├── Sub-phase 2: plan.md (pm-writing-plans uses pm-tdd) ← SKILL APPLIED HERE
  └── Sub-phase 3: scaffold execution (pm-executing-plans uses pm-tdd) ← SKILL APPLIED HERE
```

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## Red-Green-Refactor

```
    ┌─── RED ────────────────┐
    │ Write a failing test    │
    │ that describes desired  │
    │ behavior                │
    └────────────┬────────────┘
                 │
    ┌─── Verify RED ─────────┐
    │ Run the test            │
    │ Confirm it FAILS        │
    │ Confirm failure reason  │
    │ matches expectation     │
    └────────────┬────────────┘
                 │
    ┌─── GREEN ───────────────┐
    │ Write minimal code      │
    │ to make the test pass   │
    │ (prototype: stub/mock   │
    │  return is acceptable)  │
    └────────────┬────────────┘
                 │
    ┌─── Verify GREEN ───────┐
    │ Run the test            │
    │ Confirm it PASSES       │
    │ Confirm no other tests  │
    │ broke                   │
    └────────────┬────────────┘
                 │
    ┌─── REFACTOR ────────────┐
    │ Clean up code           │
    │ Remove duplication      │
    │ Improve names           │
    │ Better structure        │
    │ (prototype: skip if     │
    │  stub is temporary)     │
    └────────────┬────────────┘
                 │
                 ▼
              Repeat
```

### RED

Write a test that specifies the behavior you want. The test must fail because the behavior doesn't exist yet.

**Good:**
```python
def test_cart_adds_item():
    cart = Cart()
    cart.add(Item("widget", 9.99))
    assert cart.total() == 9.99
```

**Bad:**
```python
def test_cart_exists():
    # This tests nothing meaningful
    assert Cart() is not None
```

**Bad:**
```python
def test_cart_adds_item():
    cart = Cart()
    cart.add(Item("widget", 9.99))
    assert cart.total() == 9.99
    # Then wrote Cart implementation BEFORE running the test
```

### Verify RED

Run the test. It must fail. You must understand why it failed — the failure should be because the feature is missing, not because of a typo or import error.

**Good:**
```bash
$ pytest tests/test_cart.py::test_cart_adds_item -v
FAILED - NameError: name 'Cart' is not defined
# Expected failure: Cart class doesn't exist yet
```

**Bad:**
```bash
$ pytest tests/test_cart.py::test_cart_adds_item -v
FAILED - SyntaxError: invalid syntax
# Unexpected failure: typo in test, not missing feature
```

**Bad:** Not running the test at all.

### GREEN

Write the minimum code to make the test pass. No more, no less.

**Good:**
```python
class Cart:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def total(self):
        return sum(item.price for item in self._items)
```

**Bad (over-engineering):**
```python
class Cart:
    def __init__(self):
        self._items = []
        self._discounts = []  # No test for discounts yet
        self._tax_rate = 0.1  # No test for tax yet

    def add(self, item):
        self._items.append(item)

    def total(self):
        subtotal = sum(item.price for item in self._items)
        discount = sum(d.amount for d in self._discounts)  # Untested
        tax = subtotal * self._tax_rate  # Untested
        return subtotal - discount + tax  # Wrong: test expects just sum
```

**Good (prototype scope):**
```python
class Cart:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def total(self):
        return 9.99  # Stub: returns hardcoded value for test case
```

### Verify GREEN

Run the test again. It must pass. Run ALL tests to confirm nothing broke.

**Good:**
```bash
$ pytest tests/test_cart.py::test_cart_adds_item -v
PASSED
$ pytest -v
4 passed  # All existing tests still pass
```

**Bad:**
```bash
$ pytest tests/test_cart.py::test_cart_adds_item -v
PASSED
$ pytest -v
3 passed, 1 FAILED  # Broke an existing test — must fix before proceeding
```

### REFACTOR

Clean up while tests pass. Remove duplication, improve names, simplify structure. Tests remain green throughout.

**Good:**
- Rename `self._items` to `self.items` for clarity
- Extract `sum(item.price for item in self.items)` into `self._calculate_subtotal()`
- Remove dead code discovered during cleanup

**Bad:**
- Adding new behavior without a test (that's a new RED cycle)
- Changing test assertions to match refactored code (tests define behavior)
- Skipping refactor because "it works" (debt accumulates)

**Prototype note:** In prototype scope, if the GREEN implementation is a stub (hardcoded return), refactoring may be skipped — the stub is temporary scaffolding, not production code. Only refactor if the stub will persist into production.

### Repeat

Pick the next smallest behavior. Write a test for it. Watch it fail. Make it pass. Refactor. Repeat until the feature is complete.

## Good Tests

| Property | Description |
|----------|-------------|
| Fast | Run in milliseconds, not seconds |
| Isolated | No shared state between tests |
| Repeatable | Same result every time |
| Self-validating | Assert outcomes, not return values to check manually |
| Small | One behavior per test |
| Named by behavior | `test_cart_adds_item_increases_total`, not `test_cart_01` |
| No mocks by default | Use real code. Mock only external dependencies that are slow/flaky/unavailable |

## Why Order Matters

1. **Test-first forces you to think about what you want before how to do it.** Writing code first means you're testing what you built, not what you intended. The test captures the intent; the code serves it.

2. **Watching the test fail proves it can fail.** If a test passes immediately, it either tests existing behavior (redundant) or has a bug (never catches anything). A test that can't fail is a test that doesn't test.

3. **The failure message tells you what to implement.** A good failing test tells you exactly what's missing — `NameError: 'Cart' is not defined` means "create Cart class." `AssertionError: expected 9.99, got 0` means "implement total()." This is your roadmap.

4. **Minimal implementation prevents over-engineering.** Without a test forcing you to stop, you'll add "just in case" features, caching layers, error handling for paths that don't exist yet. TDD constrains you to what's needed now.

5. **Refactoring is safe with passing tests.** Tests lock behavior. Change structure without fear. Without tests, refactoring is guessing — "I think this still works" isn't engineering.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Example: Bug Fix

**Bug:** `Cart.total()` returns 0 when cart has items with price 0.

**Step 1 — RED: Write failing test**
```python
def test_cart_total_with_zero_price_items():
    cart = Cart()
    cart.add(Item("sample", 0))
    cart.add(Item("widget", 9.99))
    assert cart.total() == 9.99  # Bug: returns 0 because 0 + 9.99 filtered out
```

Run test:
```bash
$ pytest tests/test_cart.py::test_cart_total_with_zero_price_items -v
FAILED - AssertionError: expected 9.99, got 0
```

**Step 2 — GREEN: Fix the bug**
```python
def total(self):
    return sum(item.price for item in self.items)
    # Bug was: filter(item.price) removed zero-price items
    # Fix: include all items regardless of price
```

Run test:
```bash
$ pytest tests/test_cart.py::test_cart_total_with_zero_price_items -v
PASSED
$ pytest -v
5 passed  # All tests still pass
```

**Step 3 — REFACTOR:** No duplication found, names are clear. Move on.

**Step 4 — Commit**
```bash
git add tests/test_cart.py src/cart.py
git commit -m "fix: Cart.total() includes zero-price items"
```

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.

Never fix bugs without a test.

## Testing Anti-Patterns

When adding mocks or test utilities, read @testing-anti-patterns.md to avoid common pitfalls.

## Knowledge Write-Back

During TDD cycles, discoveries and insights emerge. Capture them:

- **Test discoveries** (new constraints, edge cases, unexpected behaviors) → `.pm-wiki/constraints/`
  - Example: "API returns null for empty results, not empty array — test revealed this constraint"
  - Example: "Library X v3.2 has race condition on concurrent access — test caught it"

- **Temporary notes** during testing (scratch observations, hypothesis, trial results) → `.pm-wiki/_working/`
  - These are ephemeral — refine into constraints or synthesis later

- **Testing insights** (design lessons, patterns that worked, anti-patterns caught) → `.pm-wiki/synthesis/`
  - Example: "Dependency injection pattern makes Cart testable without mocking — generalizable insight"
  - Example: "Stub-first GREEN in prototype scope reveals interface contracts faster than full implementation"

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without your human partner's permission.