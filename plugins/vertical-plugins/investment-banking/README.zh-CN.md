# 投资银行插件

面向股票研究、估值、演示文稿与交易材料的投行效率工具。

## 功能

- **交易材料**：CIM、teaser、process letter、buyer list
- **演示文稿**：strip profile、一键生成带品牌模板的 pitch deck
- **交易支持**：merger model、deal tracking、data pack

## 安装

```bash
claude --plugin-dir /path/to/investment-banking
```

或将本目录复制到你项目的 `.claude-plugin/` 目录中。

## Commands

| Command | 描述 |
|---------|-------------|
| `/one-pager [company]` | 为 pitch book 生成一页式 strip profile |
| `/cim [company]` | 起草保密信息备忘录（CIM） |
| `/teaser [company]` | 匿名的一页公司 teaser |
| `/buyer-list [company]` | 战略/财务买家清单 |
| `/merger-model [deal]` | 并购增厚/摊薄分析 |
| `/process-letter [deal]` | 投标说明与流程沟通材料 |
| `/deal-tracker` | 跟踪在途交易、里程碑与行动项 |

## Skills

### 交易材料
| Skill | 描述 |
|-------|-------------|
| **cim-builder** | 起草保密信息备忘录（CIM） |
| **teaser** | 匿名的一页公司 teaser |
| **process-letter** | 投标说明与流程沟通材料 |
| **buyer-list** | 战略/财务买家清单 |
| **datapack-builder** | 从 CIM 与披露文件构建数据包 |

### 演示文稿
| Skill | 描述 |
|-------|-------------|
| **strip-profile** | pitch book 用的高信息密度公司 profile |
| **pitch-deck** | 以数据填充 pitch deck 模板 |

### 交易支持
| Skill | 描述 |
|-------|-------------|
| **merger-model** | 并购增厚/摊薄分析 |
| **deal-tracker** | 跟踪在途交易、里程碑与行动项 |

## 示例工作流

### 一页式 Strip Profile
```
/one-pager Target

# 生成内容：
# - 使用 PPT 模板的一页公司 profile
# - 四象限：概览、业务、财务、股权/持股结构
# - 遵守模板边距与品牌规范
```

### CIM 起草
```
/cim Target

# 生成内容：
# - 完整 CIM 文档：执行摘要、业务概览、
#   财务分析与市场定位
```

### Merger Model
```
/merger-model Acquirer acquiring Target

# 生成内容：
# - 增厚/摊薄分析
# - 资金来源与用途、备考财务报表
# - 对收购价与协同的敏感性分析
```
