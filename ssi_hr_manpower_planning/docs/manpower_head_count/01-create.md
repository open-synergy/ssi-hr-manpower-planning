# Create Head Count Snapshot

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_head_count`\
> **Menu:** Human Resource > Manpower Planning > Head Count Snapshots\
> **Actor:** user in group _Manpower Head Count: User_\
> **State:** `—` → `draft`\
> **Inline Actions:** `action_compute_line` (Compute Lines)

## Pre-Condition

- **Data:** Employees exist with their department, job position, join date and
  termination date.
- **Access:** user in group _Manpower Head Count: User_.

## Flow

1. Open the **Human Resource > Manpower Planning > Head Count Snapshots** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the header fields:
   - **Responsible** _(required)_: Automatically filled with the current user. Change if
     needed.
   - **Department**: Limit the snapshot to one department. Leave empty to count all
     departments.
   - **Date Start** _(required)_: First day of the period.
   - **Date End** _(required)_: Last day of the period. It cannot be earlier than **Date
     Start**.
4. Click **Save**.
5. Click **Compute Lines** in the form header to build the head count lines on the
   **Head Counts** tab from the current employee data. You can compute again as often as
   needed while the snapshot is a draft. **Done** is still allowed with no lines, but
   then the snapshot is empty.

## Post-Condition

- A new head count snapshot is created in **Draft** status.
- Each line shows the opening, joined, terminated and closing head count of one
  department and job position.
