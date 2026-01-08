# Task: Create Social Media Launch Posts

**Epic:** [launch-post-and-positioning.md](../epics/launch-post-and-positioning.md)
**Size:** `S`
**Status:** `Done`

## Context

Short-form social media posts help amplify the launch. Pre-written posts for Twitter/X and LinkedIn make it easy to share and get initial visibility.

## Acceptance Criteria

- [x] 3-5 Twitter/X posts written (280 char limit each)
- [x] 1-2 LinkedIn posts written (longer form)
- [x] Posts saved in `docs/SOCIAL_POSTS.md` for easy copy/paste
- [x] Each post has a distinct angle/hook
- [x] All posts link to the leaderboard

## Technical Notes

**Target File:**
- `docs/SOCIAL_POSTS.md` — Collection of ready-to-post content

**Twitter/X Post Angles:**
1. **Launch announcement**: "Introducing SA Bench..."
2. **Interesting finding**: "Claude Sonnet scores 95% on AWS practice exams but only 5% on CDK synthesis..."
3. **Question hook**: "Can AI pass the AWS Solutions Architect exam?"
4. **Methodology highlight**: "We built an LLM-as-judge scorer for architecture tasks..."
5. **Call to action**: "Run SA Bench on your favorite model..."

**LinkedIn Post Structure:**
- Hook line
- 2-3 short paragraphs explaining the benchmark
- Key finding or insight
- Call to action (try it, star repo, share thoughts)
- Link to leaderboard

**Example Twitter Post:**
```
🚀 Introducing SA Bench: measuring AI on AWS Solutions Architect work

We evaluated 5 LLMs across practice exams, architecture design, and CDK synthesis.

Surprising finding: models strong at MCQs often struggle with infrastructure code.

Live leaderboard: [link]
```

**Example LinkedIn Post:**
```
I've been curious about how well AI models actually perform at Solutions Architect work - not just chat, but real technical tasks.

So I built SA Bench, an open-source benchmark that evaluates LLMs on:
• AWS certification-style practice exams
• Architecture diagram analysis and design
• CDK infrastructure-as-code generation

Early results show interesting patterns. Claude Sonnet-4 leads overall, but the gap between exam performance and practical coding is striking.

The full methodology and live leaderboard: [link]

Would love feedback from the SA community. What tasks should we add?
```

**Approach:**
1. Draft posts with different angles
2. Include a surprising stat or finding if available
3. Keep Twitter posts punchy, LinkedIn more thoughtful
4. Include emoji sparingly for visual appeal
5. Always end with link to leaderboard

**Gotchas:**
- Twitter has 280 char limit (check each post)
- LinkedIn truncates after ~3 lines, so hook must be strong
- Avoid overly promotional language — focus on usefulness
- Tag relevant accounts if appropriate (AWS, AI researchers)

## Dependencies

- **Blocked by:** Task 001 (need blog post for context), Task 002 (need meta tags for good previews)
- **Blocks:** None (final task)

## Verification

```bash
# Check file exists
cat docs/SOCIAL_POSTS.md

# Check Twitter posts are under 280 chars
# Manual review of each post
```
