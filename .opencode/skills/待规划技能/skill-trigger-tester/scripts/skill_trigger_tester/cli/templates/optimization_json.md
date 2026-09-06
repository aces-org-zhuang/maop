
基于测试结果，提供优化后的description。并使用脚本skill_trigger_tester fix进行SKILL.md的描述替换
记住 description 必须是中文 因为是中国人

**optimized_descriptions.json示例**
```json
{
    "docx": "Create, edit, or analyze .docx Word documents. Use for reports, letters, memos, and professional documents with tables, formatting, or tracked changes. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks.",
    "pdf": "Read, extract text from, or convert PDF files. Use for document analysis, text extraction, OCR, and PDF manipulation. Do NOT use for creating new PDFs from scratch or editing images.",
...
}
```