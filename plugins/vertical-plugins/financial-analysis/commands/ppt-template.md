---
description: Create a reusable PPT template skill from a PowerPoint template file
argument-hint: "[path to .pptx or .potx file]"
allowed-tools: ["Read", "Write", "Bash", "Glob"]
---

# PPT Template Creator Command

Create a self-contained PPT template skill from a user-provided PowerPoint template.

## Instructions

1. **Ask for the template file** if not provided:
   - "Please provide the path to your PowerPoint template file (.pptx or .potx)"
   - The template should contain the slide layouts and branding you want to use

2. **Load the ppt-template-creator skill**:
   - Use the `skill: "ppt-template-creator"` tool to load the full skill instructions
   - Follow the workflow in the skill to analyze the template and generate a new skill

3. **Gather additional info**:
   - Company/template name (for naming the skill)
   - Primary use cases (pitch decks, board materials, client presentations, etc.)

4. **Execute the skill workflow**:
   - Analyze template structure (layouts, placeholders, dimensions)
   - Generate skill directory with assets/ and SKILL.md
   - Create example presentation to validate
   - Package the skill

5. **Deliver the packaged skill** to the user
