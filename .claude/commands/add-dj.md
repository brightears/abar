---
description: Create a DJ profile from provided info and organize their image
allowed-tools: Read, Write, Edit, Bash(cp:*), Bash(mv:*), Bash(ls:*)
argument-hint: [dj-name]
---

Create a DJ profile for: $1

## Instructions

1. Read the template from `djs/profiles/_TEMPLATE.md`
2. Ask the user for DJ information if not provided:
   - Stage name and real name
   - Music genres/specialties
   - Bio (2-3 sentences)
   - Contact info (phone, LINE, Instagram)
   - Photo file location
3. Create profile file at `djs/profiles/[dj-name].md`
4. Copy/move photo to `djs/images/` with consistent naming
