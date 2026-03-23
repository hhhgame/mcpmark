# [Task Title]

## Task
[1-2 sentence clear statement of the goal]

## Tools
IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a subprocess or manually start the MCP process.

### Step 1: Investigate [Page]
Navigate to `[URL]` and extract:
- field1
- field2

### Step N: Cross Analysis
Determine:

- FieldA
- FieldB

## Output Format

You MUST output EXACTLY:

<answer>
FieldA|value
FieldB|value
FieldC|number
</answer>

## Important Notes

- Only count required dependencies
- Values must be comma-separated
- Output ONLY the `<answer>` block
- Solve the task by yourself