# Task: Add Clickable Model Links to Leaderboard

**Epic**: [log-transparency-and-drilldown](../epics/log-transparency-and-drilldown.md)
**Task ID**: 003-add-leaderboard-links
**Status**: `Done`

## Objective

Modify the leaderboard UI to make model names clickable, linking to their detailed log viewer pages.

## Acceptance Criteria

- [ ] Model names in leaderboard are clickable links
- [ ] Links navigate to the corresponding model's log viewer
- [ ] Visual indication that names are clickable (hover style, cursor)
- [ ] Graceful handling if log viewer page doesn't exist (show tooltip or disable link)
- [ ] Mobile-friendly click targets

## Implementation Notes

### File to Modify

`docs/index.html`

### Proposed Changes

1. **Add Link Wrapper**: Wrap model names in `<a>` tags pointing to log viewer
2. **Add CSS Styles**: Style links to look integrated with the table
3. **Handle Missing Logs**: Either always link (404 if missing) or check log availability

### Example Code Changes

```javascript
// In the row rendering section
const modelCell = `<td class="model-name">
  <a href="logs/index.html#${encodeURIComponent(r.model)}"
     class="model-link"
     title="View detailed evaluation logs">
    ${r.model}
  </a>
</td>`;
```

```css
/* Add to styles */
.model-link {
  color: inherit;
  text-decoration: none;
  border-bottom: 1px dashed #666;
}
.model-link:hover {
  color: #3273dc;
  border-bottom-style: solid;
}
```

### URL Structure Options

Depending on how `inspect view bundle` organizes files:

1. **Fragment-based**: `logs/index.html#model-name` (if single-page app)
2. **Path-based**: `logs/{model-name}/index.html` (if separate pages)
3. **Query-based**: `logs/index.html?model={model-name}` (if parameterized)

## Dependencies

- Tasks 001 and 002 must be completed to know the URL structure of bundled logs
