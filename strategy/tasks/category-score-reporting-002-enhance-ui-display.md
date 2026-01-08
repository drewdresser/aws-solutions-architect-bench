# Task: Enhance Leaderboard UI Category Display

**Epic:** [category-score-reporting.md](../epics/category-score-reporting.md)
**Size:** `M`
**Status:** `Done`

## Context

The leaderboard UI currently shows category scores in table columns but doesn't prominently display category definitions or help users understand what each category measures. This task enhances the UI to make category information more accessible.

## Acceptance Criteria

- [x] Category column headers show weight badge (e.g., "34%")
- [x] Hovering on category header shows tooltip with description
- [x] Category descriptions pulled from JSON metadata (not hardcoded)
- [x] Sample count shown in methodology section or tooltips
- [x] Mobile-friendly tooltip/popover implementation
- [x] No visual regression on existing leaderboard

## Technical Notes

**Target File:**
- `docs/index.html`

**Current Category Headers:**
```html
<th class="category-header">Practice Exam</th>
```

**Enhanced Headers:**
```html
<th class="category-header" title="AWS certification-style MCQ questions (50 items)">
  Practice Exam <span class="weight-badge">34%</span>
</th>
```

**Or with custom tooltip:**
```html
<th class="category-header has-tooltip">
  Practice Exam <span class="weight-badge">34%</span>
  <div class="tooltip">
    <strong>Practice Exam</strong>
    <p>AWS certification-style MCQ questions</p>
    <small>50 items · Binary scoring</small>
  </div>
</th>
```

**CSS Additions:**
```css
.weight-badge {
  background: #3273dc;
  color: white;
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  font-size: 0.7em;
  margin-left: 0.3rem;
  vertical-align: middle;
}

.has-tooltip {
  position: relative;
  cursor: help;
}

.tooltip {
  display: none;
  position: absolute;
  /* ... positioning styles ... */
}

.has-tooltip:hover .tooltip {
  display: block;
}
```

**JavaScript Changes:**
- Read category metadata from `_metadata.categories`
- Build headers dynamically with descriptions and weights
- Handle missing metadata gracefully (fallback to current behavior)

**Approach:**
1. Add CSS for weight badges and tooltips
2. Update header rendering to include weight badges
3. Add tooltip div for each category header
4. Populate tooltips from JSON metadata
5. Test on mobile (touch-friendly tooltips)

**Gotchas:**
- Tooltips should work without JavaScript for basic functionality
- Consider using native `title` attribute as fallback
- Don't make headers too wide on mobile
- Handle case where metadata is missing (old JSON format)

## Dependencies

- **Blocked by:** Task 001 (needs category metadata in JSON)
- **Blocks:** None

## Verification

```bash
# Start local server
python -m http.server 8000 --directory docs

# Manual verification:
# 1. Open http://localhost:8000
# 2. Hover over category headers
# 3. Verify tooltips show description
# 4. Verify weight badges visible
# 5. Test on mobile viewport
```
