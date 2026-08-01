---
name: capability-create
description: |
  Creates new capabilities for AET system including configuration files, agents, and skills. Automatically detects language and responds in the same language.
  Use this skill when creating new capability scenarios, extending existing capabilities, or setting up custom workflows.
---

# Capability 创建技能

Creates new capabilities for the AET (Agent Execution Toolkit) system based on user requirements. This skill helps users create custom capabilities by adjusting config.json and creating corresponding agents in the agents/ directory.

## 语言检测与响应

- Automatically detect the language of user input
- Respond in the same language as the user input

## 何时使用

Use this skill when:
- Creating a new capability scenario for AET
- Adding custom workflows to extend existing functionality
- Setting up specialized capabilities for specific domains
- Integrating new agents into the workflow system
- Creating capability templates for reuse

## 本技能做什么

This skill helps users create new capabilities based on their specific requirements:

### 1. User Requirement Analysis
- **Understand user needs** - Ask clarifying questions about desired capability
- **Identify specific functionality** - What should the new capability do?
- **Determine integration approach** - How to work with existing system?

### 2. Configuration Adjustment
- **Modify config.json** - Update .aet/config.json according to user needs
- **Create agent workflow** - Define appropriate workflow steps
- **Ensure project consistency** - Match existing patterns and conventions

### 3. Main Agent Creation
- **Create agent directory** - Set up corresponding agent in agents/{name}/
- **Follow project patterns** - Use established agent development standards
- **Implement proper structure** - Include index.js and prompts/main.md
- **Enable aet-capability-create** - Make sure it can be used as the main agent

### 3. Skill Integration
- **Leverages existing skills** where possible (agent-developing, skill-creator)
- **Creates new skills** if specialized functionality is needed
- **Enables skill discovery** and proper invocation
- **Provides extension points** for future enhancements

## 使用示例

### Example 1: User-Driven Capability Creation
```bash
# User specifies what they want the capability to do
# Skill asks clarifying questions about requirements
# Adjusts config.json based on user needs
# Creates corresponding agent in agents/ directory
```

### Example 2: Custom Integration
```bash
# User wants specific functionality
# Skill creates appropriate workflow steps
# Sets up main agent as aet-capability-create
# Ensures integration with existing skills
```

## Integration with Existing Skills

This skill leverages existing skills for capability creation:

- **agent-developing**: Follows established agent development patterns
- **skill-creator**: Uses when new specialized skills are needed
- **config-setup**: Helps with configuration management (if required)
- **project-analysis**: Understands current system architecture

## 输出结构

When creating a new capability based on user requirements, this skill generates:

```
.opencode/plugins/scenarios/<scenario_name>.json                    # Modified according to user needs
.opencode/plugins/agents/{capability-name}/           # Main agent directory created
├── index.js                        # Agent definition (aet-capability-create)
└── prompts/
    └── main.md                     # Agent instructions
skills/                             # Existing skills used as needed
docs/                               # Documentation for the capability
```

## 最佳实践

1. **User-Driven Design**: Base creation on user's specific requirements, not templates
2. **Main Agent Focus**: Create the main agent in agents/ directory as requested
3. **Project Consistency**: Follow established patterns from existing capabilities
4. **System Integration**: Ensure new capability works seamlessly with AET system
5. **Clear Communication**: Ask clarifying questions to understand user needs

## 常见创建能力

This skill has been used to create:

- **Code Development Workflow**: Standard feature development process
- **Bug Fix Workflow**: Systematic bug resolution process  
- **Plant Router**: IPD UML diagram generation
- **Agent Development**: Specialized agent creation workflow

## Troubleshooting

If capability creation encounters issues:

1. **Configuration Conflicts**: Check for syntax errors in config.json
2. **Agent Integration**: Verify agent definitions follow existing patterns
3. **Workflow Dependencies**: Ensure referenced agents exist and are properly configured
4. **Permission Issues**: Confirm write access to target directories

For advanced customization, consider using the underlying skills:
- Use `agent-developing` for detailed agent implementation guidance
- Use `skill-creator` for complex skill development requirements