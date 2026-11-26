# Edit Head Count Snapshot

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_head_count`\
> **Menu:** Human Resource > Manpower Planning > Head Count Snapshots\
> **Actor:** user in group _Manpower Head Count: User_\
> **Requires:** `01-create`\
> **Inline Actions:** `action_compute_line` (Compute Lines)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** user in group _Manpower Head Count: User_.

## Flow

1. Open the **Human Resource > Manpower Planning > Head Count Snapshots** menu.
2. Find and open the snapshot to edit.
3. Change the department or the period.
4. Click **Save**.
5. Click **Compute Lines** in the form header to rebuild the lines after changing the
   department or the period. The old lines are replaced, and the lines no longer match
   the new period if you skip this step.

## Post-Condition

- The snapshot is updated with the new values.
