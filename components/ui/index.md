# Dumbwork UI Component Contract
## Core
- Button (`.dw-btn .dw-btn-primary|secondary`) min height 44px
- Input (`.dw-input`) min height 44px + visible focus
- Card (`.dw-card`) tokenized border/bg/radius/padding
- Badge (`.dw-badge`) includes status text, not color-only

## Layout
- PublicShell (`components/layout/PublicShell.html`)
- AdminShell (`components/layout/AdminShell.html`)
- Sidebar width uses `--dw-sidebar-width`

## Planned reusable component inventory
- PageHeader, SectionHeader
- Textarea, Select, Checkbox, Radio
- StatusBadge, MetricCard, ActionPanel
- EmptyState, BlockedState, ProgressBar
- SidebarNav, Table, Tabs, Toast, Modal

## Empty/Blocked state rule
- clear headline
- 1 short explanation
- 1 primary action max
- no fake metrics or fake customer data
