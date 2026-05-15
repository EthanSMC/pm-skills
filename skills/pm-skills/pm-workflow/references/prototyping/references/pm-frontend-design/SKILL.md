---
name: pm-frontend-design
description: "前端设计（内部子 skill，由 prototyping 调度）— UI组件结构、视觉方向、交互模式"
---

# PM Frontend Design — 前端设计

为 PM 原型工作流提供前端设计能力。创建独特、高设计质量的前端界面，避免通用 "AI slop" 美学，产出可工作的代码并对美学细节和创意选择保持极致关注。

用户提供前端需求：组件、页面、应用或界面。可能包含关于用途、受众或技术约束的上下文。

## 当由 prototyping 调度时

prototyping 在子阶段 1.5（前端设计）使用 Skill 工具调用此 skill。仅当原型涉及前端 UI 时执行，后端纯 API 原型跳过。

### 交接参数

| 参数 | 值 |
|------|------|
| **Input** | docs/prototype/<feature>/spec.md（子阶段 1 产出）+ PRD 中 UI 相关描述 |
| **Output** | docs/prototype/<feature>/ui-spec.md |
| **PM 上下文** | 原型 scope：产出组件骨架 + CSS 变量定义 + 关键页面完整设计，不是生产级组件库 |
| **知识写回** | .pm-wiki/decisions/ + .pm-wiki/constraints/ + .pm-wiki/_working/ |

### 交接声明

```
我正在使用 pm-frontend-design skill 来设计这个原型的前端界面。

输入：docs/prototype/<feature>/spec.md + PRD UI 描述
输出：docs/prototype/<feature>/ui-spec.md

原型上下文：产出组件骨架 + CSS 变量 + 关键页面完整设计，不是生产级组件库。
```

## PM Pipeline Context

本 skill 在 prototyping 工作流中使用：

```
prototyping Sub-phase 1: 技术规格 (spec.md)
  ↓
prototyping Sub-phase 1.5: 前端设计 (ui-spec.md + 组件结构) ← 本 skill，仅前端原型时
  ↓
prototyping Sub-phase 2: 实施计划 (pm-writing-plans)
  ↓
prototyping Sub-phase 3: 骨架构建 (pm-executing-plans)
```

**触发条件**：当原型涉及 UI/前端界面时，在技术规格完成后、实施计划之前调用。后端纯 API 原型不需要本 skill。

**输入**：
- 技术规格 `docs/prototype/<feature>/spec.md`（prototyping Sub-phase 1 产出）
- PRD 中关于 UI/交互的描述

**输出**：
- `docs/prototype/<feature>/ui-spec.md` — UI 组件结构、视觉方向、交互模式
- 前端组件骨架代码（由 pm-executing-plans 在 Sub-phase 3 中构建）

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:

- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:

- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## ui-spec.md 结构

设计思考完成后，产出 UI 规格文档：

```markdown
# <Feature Name> UI Spec

**Aesthetic Direction:** [选定的视觉方向名称 + 一句话描述]
**Design Tone:** [极端选择的 tone]
**Key Differentiator:** [让人记住的那一点]

---

## Component Hierarchy
[组件树：哪些组件、层级关系、职责划分]

## Visual System
### Typography
- Display: <字体名> — <用途>
- Body: <字体名> — <用途>
- Monospace: <字体名> — <用途>

### Color Palette
- Primary: <色值> — <用途>
- Accent: <色值> — <用途>
- Background: <色值>
- Surface: <色值>
- Text: <色值> / <色值>
- Error/Warning/Success: <色值> / <色值> / <色值>

### Motion
- Page load: <动画策略>
- Micro-interactions: <交互模式>
- Transitions: <过渡策略>

### Spatial Layout
- Grid system: <布局方式>
- Key layouts: <主要页面布局描述>
- Negative space strategy: <空间策略>

## Interaction Patterns
| 状态 | 组件 | 表现 |
|------|------|------|
| 加载 | 全局 | <加载态设计> |
| 空态 | 列表/表格 | <空态设计> |
| 错误 | 表单 | <错误态设计> |
| Hover | 按钮/卡片 | <hover态设计> |
| Disabled | 按钮 | <禁用态设计> |

## CSS Variables
[提取关键变量定义，供骨架构建时直接使用]

## Source References
- spec.md Interfaces → <映射到哪些组件>
- spec.md Data Models → <映射到哪些展示逻辑>
- PRD requirements → <映射到哪些交互>
```

## 知识写回

- UI 设计决策 → `.pm-wiki/decisions/`（视觉方向选择 WHY）
- 交互模式发现 → `.pm-wiki/constraints/`（交互约束，如响应式断点、可访问性要求）
- 设计资源 → `.pm-wiki/_working/`（字体链接、色值参考、灵感截图路径）

## 原型范围适配

在原型 scope 内，前端设计产出的不是生产级 CSS/组件库，而是：
- **组件骨架 + CSS 变量定义** — 定义视觉系统骨架（字体、色值、间距变量）
- **关键页面的完整设计** — 核心交互页面做完整设计，次要页面用简化版
- **mock 数据驱动的交互演示** — 用 mock 数据展示交互模式，证明 UI 可行性

pm-writing-plans 在编写实施计划时，应参考 ui-spec.md 将前端组件拆为 bite-sized TDD 任务。