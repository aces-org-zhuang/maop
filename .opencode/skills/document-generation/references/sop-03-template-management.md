# SOP-03 Template Management

## Goal

支持文档模板（元数据、YAML头部、标题格式、占位符、MarkdownTable/ASCII图）、CLI 支持更新模板。

## Steps

1. 创建或更新模板：`.aces/features/<k-case>/doc-templates/template.md`。
2. CLI 支持 `template` 子命令更新模板，并拒绝缺少 YAML 头部分隔符的模板。
3. 模板必须包含 YAML 头部和占位符。

## Output

模板文件 + 更新记录。
