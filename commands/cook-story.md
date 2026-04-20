You are creating a Shortcut story from a Notion specification page. You combine the `/story` skill's acceptance-criteria format with Notion fetching and Shortcut integration.

## Arguments

The user provides two arguments after the slash command:

```
/cook-story <notion-link> <iteration-name>
```

If either argument is missing, ask for it before proceeding.

## Steps

### 0. Check MCP availability

Before doing anything else, verify that both the **Notion** and **Shortcut** MCP integrations are reachable by using `ToolSearch` to look up a tool from each:

- `select:mcp__claude_ai_Notion__notion-fetch`
- `select:mcp__claude_ai_Shortcut__stories-create`

Run both searches in parallel. If either MCP is unavailable, tell the user which integration is missing and stop.

### 1. Fetch the Notion page

Use the `mcp__claude_ai_Notion__notion-fetch` tool with the provided Notion link to retrieve the page content. This content is the **specification** for the story.

### 2. Generate the story card

Using the Notion page content as the specification, generate a story card following these rules (same format as `/story`):

- Include the original spec verbatim in a `<details>` collapsible
- Write criteria from the end-user perspective
- Use **GIVEN** / **WHEN** / **AND** / **THEN** (bold, capitalised)
- Cover positive and negative paths; do not invent requirements
- Keep language precise and testable
- Flag ambiguities in **Open Questions** as **MANUAL REVIEW**
- Backend-only details go in Technical Notes (one line each)
- Keep each scenario to 3-5 lines
- Keep Open Questions brief (one sentence per item)

Output format:

```
# Title: <title>

<details>
<summary>Original Spec</summary>
<verbatim spec>
</details>

## Technical Notes
<bullet list or "None">

## Acceptance Criteria

### 1. <scenario name>
**GIVEN** ...
**WHEN** ...
**THEN** ...

## Open Questions
<ambiguities as **MANUAL REVIEW** — or "None">
```

### 3. Look up the Shortcut iteration

Use `mcp__claude_ai_Shortcut__iterations-list` to list iterations, then find the one whose name best matches the iteration name the user provided. Match flexibly — ignore case, whitespace differences, partial matches, and abbreviations. Pick the closest match confidently. Only ask the user to clarify if there are multiple equally plausible matches or genuinely no reasonable match; in that case show the available iteration names.

### 4. Get the default workflow

Use `mcp__claude_ai_Shortcut__workflows-get-default` to get the workspace default workflow.

### 5. Create the Shortcut story

Use `mcp__claude_ai_Shortcut__stories-create` with:

- **name**: The story title (without the "Title: " prefix)
- **description**: The full story card markdown content (everything generated in step 2)
- **iteration**: The iteration ID from step 3
- **workflow**: The workflow ID from step 4
- **type**: `feature`

Tell the user the Shortcut story was created and show them the story name and iteration.
