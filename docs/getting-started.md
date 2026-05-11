# PM Skills 新手上路指南

> 你不需要懂编程、不需要懂 AI。只要能跟着一步步点击，就能用。

## 这是什么？

PM Skills 是一个**产品经理助手**。你把需求、文档、想法告诉它，它帮你：

- 把乱七八糟的需求整理清楚
- 写出正式的 PRD（产品需求文档）
- 生成可跑的原型骨架代码

整个过程就像和一个很专业的产品经理聊天。

## 你需要什么

一台电脑（Windows 或 Mac），能上网。

下面 3 样东西按顺序装好就行，每样只需几分钟：

---

### 第 1 步：装 Node.js

Node.js 是一个运行环境，Claude Code 需要它。

1. 打开浏览器，访问 https://nodejs.org
2. 点击左边那个大按钮（写着 LTS 版本号），下载安装包
3. 双击下载的文件，一路点"下一步"装完
4. 装完后验证：打开**终端**（下面教你怎么打开），输入 `node --version`，看到版本号就说明装好了

**怎么打开终端？**

| 系统 | 操作 |
|------|------|
| Windows | 按 `Win + R`，输入 `cmd`，回车。或者搜索"终端" |
| Mac | 按 `Cmd + 空格`，输入 `Terminal`，回车 |

> 终端就是一个黑色（或白色）的窗口，你可以在里面输入命令。后面所有步骤都要用到它。

---

### 第 2 步：装 Claude Code

Claude Code 是你跟 AI 助手对话的工具，装在终端里。

1. 打开终端，输入下面这行命令然后回车：

```
npm install -g @anthropic-ai/claude-code
```

2. 等它装完（可能几十秒），然后验证：

```
claude --version
```

看到版本号就说明装好了。

3. 第一次运行需要登录：

```
claude
```

它会让你选登录方式。推荐选 **Anthropic API key**：
- 去 https://console.anthropic.com 注册账号
- 在 Settings → API Keys 页面创建一个 key
- 把 key 复制粘贴到终端里

> 如果你已经有 Claude 账号（claude.ai），也可以选那个方式登录。

---

### 第 3 步：装 PM Skills

PM Skills 就是产品经理助手的技能包。

1. 打开终端，输入：

```
npm install -g pm-skills
```

> 如果 npm 报错说找不到这个包，说明还没发布到 npm。改用下面的本地安装方式。

**本地安装（如果 npm 上没有这个包）：**

1. 打开浏览器，访问 https://github.com/EthanSMC/pm-skills
2. 点击绿色的 **Code** 按钮，选 **Download ZIP**
3. 解压下载的 zip 文件，放到你喜欢的地方（比如桌面）
4. 打开终端，进入你放项目的文件夹：

```
cd Desktop/pm-skills
```

> `cd` 是"切换目录"的意思。如果你放在别的地方，换成那个路径。

5. 在项目里装依赖：

```
npm install
```

---

### 第 4 步：连接 PM Skills 到 Claude Code

让 Claude Code 知道 PM Skills 在哪里。

在你打算做产品的项目文件夹里（比如你的 MSP 项目），创建一个配置文件：

1. 用终端进入你的项目文件夹：

```
cd 你的项目路径
```

2. 让 Claude Code 帮你创建配置：

```
claude
```

进入 Claude Code 后，输入：

```
帮我创建 .claude/settings.json 文件，内容是连接 pm-skills
```

Claude 会帮你生成这个文件。如果你用的是 npm 安装的 pm-skills，文件内容是：

```json
{
  "skills": {
    "sources": [
      { "type": "npm", "package": "pm-skills" }
    ]
  }
}
```

如果你用的是本地安装（解压 zip 的方式），改成：

```json
{
  "skills": {
    "sources": [
      { "type": "local", "path": "你解压pm-skills的路径/skills/pm-skills" }
    ]
  }
}
```

---

## 开始使用

现在一切都装好了。每次你要做产品工作时：

### 1. 打开终端，进入你的项目文件夹

```
cd 你的项目路径
```

### 2. 启动 Claude Code

```
claude
```

你会看到 Claude Code 的界面，可以开始对话了。

### 3. 调用产品经理助手

输入以下命令之一：

| 你想做什么 | 输入什么 |
|-----------|---------|
| 完整的产品经理流程 | `/pm-workflow 我要做xxx功能` |
| 只是讨论需求 | `/brainstorming xxx功能的设计` |
| 写 PRD | `/write-prd` |
| 合并多份 PRD | `/prd-reconcile` |
| 做原型验证 | `/prototyping` |

**最常用的是第一个**——输入 `/pm-workflow` 然后空格写一句你的需求描述，比如：

```
/pm-workflow 我需要设计一个任务管理系统，支持创建、分配、跟踪任务状态
```

然后 Claude 会引导你走完整个流程：
1. 先帮你整理已有知识
2. 跟你讨论需求，确认设计方向
3. 写出 PRD
4. 问你要不要做原型

每一步都会问你意见，你只需要回答问题就行。

### 4. 把文档给助手看

如果你有现成的文档（PDF、Word、Markdown），想让助手学习：

```
/pm-knowledge ingest 这份文档的路径
```

比如：

```
/pm-knowledge ingest raw/运营管理平台-PRD.docx
```

助手会读取文档，把里面的知识整理到知识库里。下次你提问时，它会自动参考这些知识。

### 5. 退出 Claude Code

对话结束后，按 `Ctrl + C`（Mac 也一样）退出。

---

## 产出文件在哪里？

助手帮你写的东西都保存在你项目文件夹里：

| 产出 | 位置 | 说明 |
|------|------|------|
| 设计文档 | `docs/pm/specs/` | brainstorming 产出的设计规格 |
| PRD | `docs/pm/prds/` | 正式的产品需求文档 |
| 原型 | `docs/prototype/<功能名>/` | 技术规格+实施计划+骨架代码 |
| 知识库 | `.pm-wiki/` | 自动积累的项目知识 |

你直接用文件管理器或 VS Code 打开这些文件夹就能看到产出。

---

## 常见问题

**问：终端里输入命令报错 "command not found"**

说明没装好。回去检查第 1-2 步，确认 `node --version` 和 `claude --version` 都能正常运行。

**问：Claude Code 启动后没有响应**

可能是网络问题。Claude Code 需要联网访问 Anthropic 的服务。检查网络连接，或者换个网络试试。

**问：PM Skills 的命令不生效**

检查 `.claude/settings.json` 文件是否在你当前项目文件夹里，路径是否正确。特别是本地安装时，路径要指向 `skills/pm-skills` 子目录，不是整个项目根目录。

**问：我想把几份不同的 PRD 合成一份**

输入 `/prd-reconcile`，然后把文档路径告诉它。助手会帮你找冲突、做决策、合并。

**问：助手说了"待审"，要我确认**

助手把分析性内容（比如竞品对比结论）标记为"待审"。你需要看一下它写的内容，告诉它"确认"或者"修改xxx部分"。

---

## 进阶（可选）

如果你用久了想更深入：

- **知识引擎配置**：安装 MinerU Document Explorer（`npm install mineru-document-explorer`），可以让知识检索更智能
- **个人知识库**：助手会在 `~/.pm-wiki/` 积累跨项目的通用知识，跟着你走
- **原型脚本**：`skills/pm-skills/scripts/` 下有 3 个 Python 工具（graph/lint/crystallize），需要 `pip install pyyaml pytest`

这些不影响基本使用，等你熟悉了再装。

---

## 一句话总结

装好 Node.js → 装好 Claude Code → 装好 PM Skills → 在项目里 `/pm-workflow 你的需求` → 跟着助手走就行。