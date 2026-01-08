# Task: Add Social Media Meta Tags

**Epic:** [launch-post-and-positioning.md](../epics/launch-post-and-positioning.md)
**Size:** `S`
**Status:** `Done`

## Context

For the launch post to be shareable on social media (Twitter/X, LinkedIn, etc.), the HTML page needs proper Open Graph and Twitter Card meta tags for good link previews.

## Acceptance Criteria

- [x] Open Graph meta tags added to `docs/index.html`
- [x] Twitter Card meta tags added
- [x] Preview image created and referenced (`docs/og-image.svg`)
- [ ] Title, description, and image render correctly when shared
- [ ] Tested with social media preview validators

## Technical Notes

**Target File:**
- `docs/index.html` — Add meta tags to `<head>` section

**Required Meta Tags:**
```html
<!-- Open Graph -->
<meta property="og:title" content="SA Bench: AI Solutions Architect Benchmark">
<meta property="og:description" content="Measuring LLM performance on AWS Solutions Architect tasks. Compare models across practice exams, architecture design, and CDK synthesis.">
<meta property="og:image" content="https://drewdresser.github.io/aws-solutions-architect-bench/og-image.png">
<meta property="og:url" content="https://drewdresser.github.io/aws-solutions-architect-bench/">
<meta property="og:type" content="website">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="SA Bench: AI Solutions Architect Benchmark">
<meta name="twitter:description" content="Measuring LLM performance on AWS Solutions Architect tasks.">
<meta name="twitter:image" content="https://drewdresser.github.io/aws-solutions-architect-bench/og-image.png">
```

**Preview Image Requirements:**
- Size: 1200x630px (recommended for Twitter/LinkedIn)
- Format: PNG or JPG
- Content: SA Bench title, maybe a simple leaderboard preview or architecture diagram
- Save as: `docs/og-image.png`

**Image Design Ideas:**
- Simple: Dark background with "SA Bench" title and tagline
- Data-focused: Mini leaderboard visualization
- Technical: Architecture diagram silhouette with AWS icons

**Approach:**
1. Create a simple preview image (can use Figma, Canva, or generate programmatically)
2. Add meta tags to index.html head section
3. Test with validators

**Testing Tools:**
- Twitter Card Validator: https://cards-dev.twitter.com/validator
- LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/
- Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/

**Gotchas:**
- Image must be absolute URL (https://...)
- Some platforms cache previews; may need to re-scrape after changes
- Image should look good cropped (some platforms crop differently)

## Dependencies

- **Blocked by:** None (can run in parallel with Task 001)
- **Blocks:** Task 004 (social sharing)

## Verification

```bash
# Check meta tags exist in HTML
grep -E "og:|twitter:" docs/index.html

# Check image exists
ls -la docs/og-image.png

# Manual: Test with Twitter Card Validator
```
