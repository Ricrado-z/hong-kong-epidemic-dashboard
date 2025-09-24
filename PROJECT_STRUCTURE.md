# 📁 项目文件结构说明

## 🏗️ 整体架构
```
CASE-dashboard_epidemic/
├── 📁 src/                    # 源代码目录
│   ├── 📁 backend/            # 后端代码
│   │   └── app.py             # Flask主应用
│   └── 📁 frontend/           # 前端代码
│       ├── 📁 templates/      # HTML模板
│       │   └── dashboard.html # 主页面模板
│       ├── 📁 css/            # 样式文件
│       │   └── dashboard.css  # 主样式文件
│       ├── 📁 js/             # JavaScript文件
│       │   └── dashboard.js   # 主逻辑文件
│       └── 📁 images/         # 图片资源
│           └── favicon.ico     # 网站图标
├── 📁 data/                   # 数据文件
│   └── 香港各区疫情数据_20250322.xlsx  # 原始数据
├── 📁 scripts/               # 分析脚本
│   ├── analyze_epidemic_data.py      # 基础数据分析
│   ├── detailed_analysis.py          # 详细数据分析
│   ├── plot_daily_cases.py           # 每日趋势图表
│   └── plot_regional_comparison.py   # 区域对比图表
├── 📁 docs/                   # 文档和图片
│   └── *.png                  # 生成的图表
├── README.md                  # 项目说明
└── PROJECT_STRUCTURE.md       # 文件结构说明
```

## 📋 文件作用详解

### 🚀 启动文件
- **`src/backend/app.py`** - 🎯 **主启动文件**
  - Flask后端应用
  - 提供5个API接口
  - 处理数据请求和响应
  - 启动命令：`python3 src/backend/app.py`

### 🎨 前端文件
- **`src/frontend/templates/dashboard.html`** - 主页面模板
  - HTML结构定义
  - 5个统计卡片
  - 4个图表容器
  - 响应式布局

- **`src/frontend/css/dashboard.css`** - 样式文件
  - 渐变背景设计
  - 卡片动画效果
  - 响应式布局
  - Emoji字体支持

- **`src/frontend/js/dashboard.js`** - 交互逻辑
  - ECharts图表初始化
  - 数据加载和更新
  - 动画效果控制
  - 错误处理机制

### 📊 数据文件
- **`data/香港各区疫情数据_20250322.xlsx`** - 原始数据
  - 2022年1-6月香港疫情数据
  - 18个行政区 × 180天
  - 12个数据字段

### 🔧 分析脚本
- **`scripts/analyze_epidemic_data.py`** - 基础数据分析
  - 数据读取和基本统计
  - 前20行数据展示
  - 数据结构分析

- **`scripts/detailed_analysis.py`** - 详细数据分析
  - 完整的数据分析报告
  - 各区域统计对比
  - 疫情趋势分析

- **`scripts/plot_daily_cases.py`** - 每日趋势图表
  - 生成每日新增确诊趋势图
  - 保存为PNG文件

- **`scripts/plot_regional_comparison.py`** - 区域对比图表
  - 生成各区域对比图
  - 包含统计摘要

### 📚 文档文件
- **`README.md`** - 项目主要说明
- **`PROJECT_STRUCTURE.md`** - 文件结构说明
- **`docs/*.png`** - 生成的图表文件

## 🚀 启动说明

### 主要启动文件
**启动命令：**
```bash
python3 src/backend/app.py
```

**访问地址：**
- http://localhost:8080

### 其他脚本用途
- **数据分析脚本**：用于生成静态图表和分析报告
- **独立运行**：可以单独运行进行数据分析

## 🔧 技术栈
- **后端**：Flask (Python)
- **前端**：HTML5 + CSS3 + JavaScript
- **图表**：ECharts 5.4.3
- **数据处理**：pandas
- **数据格式**：Excel (.xlsx)

## 📱 功能特点
- ✅ 5个核心图表
- ✅ 实时数据更新
- ✅ 响应式设计
- ✅ 动画效果
- ✅ 错误处理
- ✅ Emoji支持
