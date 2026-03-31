---
description: Build DJ roster presentation for venue approval
allowed-tools: Read, Write, Glob, Bash(ls:*)
argument-hint: [output-format]
---

Build the DJ roster presentation for ABar management.

Output format: $1 (default: markdown)

## Instructions

1. Read all DJ profiles from `djs/profiles/`
2. Check for branding assets in `branding/`
3. Create presentation with DJ cards

## Presentation Structure

### Cover
- Title: "DJ Roster"
- Subtitle: "ABar"
- Bright Ears branding

### Per DJ Card
- Photo reference
- Stage name
- Music style
- Brief bio

### Summary
- Total DJs in roster
- Coverage plan

## Output
Save to `presentations/`
