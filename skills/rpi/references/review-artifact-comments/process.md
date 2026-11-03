---
name: review-artifact-comments
description: Only use when the user explicitly invokes this skill by name.
---

# Review Artifact Comments

You are helping the user address comments on an artifact file. Work through each comment systematically.

## Input Format

When the user invokes this skill, they may or may not include a comments block, and they may or may not include an artifact filename. 

Generally:
1. If a comment block is included (Described below) - you should follow the procedure for those comments
2. If a comment block is NOT included, ask the user to paste the comments for the artifact, wait for their answer, and then proceed

### Note: comment block format:
1. a `<comments>...</comments>` XML block which includes an attribute with the name of the artifact that it is for
2. Then: one or more `<comment>` blocks which include the text that hte comment applies to, the comment id, and user responses.

## Workflow

1. **Read the artifact file** using the path from the first line (it will be in the task artifact directory) _if you have not read it already_
2. **Read the comment blocks** to understand what feedback exists
3. **Ask the user how to proceed**: if the user has not given you instructions (such as "read and apply all comments"), once you have read the artifact and the comments, you should ask the user how they would like you to proceed. You may offer contextually relevant, CONCISE recommendations - for example: 

````
I can see 4 comments on this design discussion. Would you like me to...
1. update the design discussion based on the feedback of each comment
2. research and investigate the issues flagged in the comments and report my findings
3. something else? 
````

## Example

Given input:
```
<comments for="design-discussion.md">
<comment id="1">
> | ## Database Schema
Alice: Should we add an index on created_at?
</comment>

<comment id="2">
> | function processData() {
Bob: This needs error handling
  Alice: Agreed, let's add try-catch
</comment>
```

You would:
1. Read `design-discussion.md` from your task's artifact directory (e.g. `.rpi/tasks/<task-slug>/design-discussion.md`) if you have not already
2. Ask the user how to proceed unless the user provided instructions already.
3. Follow the user's instructions.

## Important Notes
- Unless the user gives you a course of action, you MUST ask the user for clarification about how you should proceed after reading the comments. 
- Work through comments one at a time for clarity
