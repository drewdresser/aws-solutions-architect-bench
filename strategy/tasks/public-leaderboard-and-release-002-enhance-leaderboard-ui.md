# Task: Enhance Leaderboard UI with Category Scores and Mobile Support

**Epic:** [public-leaderboard-and-release.md](../epics/public-leaderboard-and-release.md)
**Size:** `M`
**Status:** `Done`

## Context

The current leaderboard page shows all score columns in a basic table. To make category-level performance visible and support mobile users, the UI needs to visually distinguish overall vs category scores and handle small screens gracefully.

## Acceptance Criteria

- [ ] Overall score column is visually prominent (bold, different background, or first column after model)
- [ ] Category columns (practice_exam, architecture_design, cdk_synth) are grouped/styled as secondary
- [ ] Table is horizontally scrollable on mobile (or uses card layout for small screens)
- [ ] Score cells use consistent color coding (green ≥80%, yellow ≥50%, red <50%)
- [ ] Model names are readable without truncation on mobile
- [ ] Tested on viewport widths: 375px (phone), 768px (tablet), 1024px+ (desktop)

## Technical Notes

**Relevant Files:**
- `docs/index.html` — Main leaderboard HTML/CSS/JS

**Approach:**
1. Reorder columns: Model → Overall → Categories (practice_exam, arch, cdk)
2. Add CSS class for overall column with bold/highlighted styling
3. Wrap table in `overflow-x: auto` container for mobile scrolling
4. Consider sticky first column (model name) on mobile
5. Add column headers with tooltips explaining each category

**CSS Patterns to Consider:**
```css
.overall-score { font-weight: bold; background: #f0f8ff; }
.table-container { overflow-x: auto; -webkit-overflow-scrolling: touch; }
@media (max-width: 768px) {
  .model-name { min-width: 150px; }
  .score { min-width: 80px; }
}
```

**Gotchas:**
- Bulma tables may have built-in responsive behavior — check before overriding
- Color-blind accessibility: use more than just color (bold, icons, patterns)
- Don't break existing page structure (keep methodology section below)

## Dependencies

- **Blocked by:** None (can start independently, but 001 adds timestamp to display)
- **Blocks:** None

## Verification

```bash
# Open in browser and test responsive behavior
open docs/index.html
# Or serve locally
python -m http.server 8000 -d docs
# Then resize browser window to test breakpoints
```
