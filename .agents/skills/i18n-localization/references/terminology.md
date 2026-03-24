# AstronRPA Terminology (Glossary)

When translating user-facing copy, always prefer the translations here to keep naming consistent across frontend, engine, and backend.

## Product Names

| Source | Preferred | Notes |
|--------|----------|------|
| AstronRPA | AstronRPA | Do not translate |
| 星辰RPA | AstronRPA | Use the product name in English UI |
| Astron Agent | Astron Agent | Do not translate |

## UI Naming (Client/Frontend)

| 中文（现名称） | English | Notes |
|--------------|---------|------|
| 应用 | Application | Previously “机器人” in some UI text |
| 控制台 | Console | Previously “卓越中心”; do not use “Control Center/Controller/Manager” |
| 设计器 | Studio | UI module name |
| 执行器 | Robot | UI module name |

## Core Concepts

| Term | Preferred | Notes |
|------|----------|------|
| Application | Application | Abstract concept; includes Workflow and Agent |
| Workflow | Workflow | Predefined process with clear structure |
| Agent | Agent | AI-driven planning and decisioning |
| 流程 | Process | Includes main/sub processes |
| 主流程 | Main Process | Core process |
| 子流程 | Sub Process | Called by main or runs standalone |
| 流程参数 | Process Parameters | Process-level parameter definitions |
| 元素 | Elements | Objects referenced by processes |
| 原子能力 | Actions / Atomic Actions | Built-in atomic operations |
| 组件 | Components | Composed from Actions, reusable |
| 智能组件 | Smart Component | Higher-level intelligent component |

## Engine-side Naming

Engine terms may differ from UI naming.

| 中文 | English/Identifier | Notes |
|------|---------------------|------|
| 机器人（引擎侧） | robot | Refers to the project/application bundle (not the UI “应用”) |
| 设计器 | studio | Engine naming |
| 控制台 | console | Legacy “卓越中心” is deprecated |
| 模块 | module | Engine naming |
| 调度模式 | dispatch mode | Engine naming |

## Services

| 中文 | English/Identifier | Notes |
|------|---------------------|------|
| 执行器 | executor | Service name |
| 调度器 | scheduler | Service name |
| 拾取器 | picker | Service name |
| 图像拾取器 | vision_picker | Previously “cv_picker” |
| 触发器 | trigger | Service name |
| 远程监控 | monitor | Service name |
| 浏览器插件通信 | browser_bridge | Previously “browser_connector” |

## Libraries and Packages

Prefer code identifiers as-is unless translating explanatory text.

| Old | New |
|-----|-----|
| rpaai | astronverse.ai |
| rpabrowser | astronverse.browser |
| rpacv | astronverse.vision |
| rpadialog | astronverse.dialog |
| rpadocx | astronverse.word |
| rpagui | astronverse.input |
| rpahelper | astronverse.workflowlib |
| rpawindow | astronverse.window |
| rpasystem | astronverse.system |
| rpawinele | astronverse.winelement |
| rpasoftware | astronverse.software |
| rpanetwork | astronverse.network |
| rpaencrypt | astronverse.encrypt |

## Translation Rules

- Prefer the glossary translations above.
- Do not translate product names and code identifiers.
- Use “控制台 / Console” consistently everywhere.
