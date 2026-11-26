# Finish Head Count Snapshot

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_head_count`\
> **Menu:** Human Resource > Manpower Planning > Head Count Snapshots\
> **Actor:** user in group _Manpower Head Count: User_\
> **State:** `draft` → `done`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `done_ok` for state
  `draft` to the actor's group.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** user in group _Manpower Head Count: User_.

## Flow

1. Open the **Human Resource > Manpower Planning > Head Count Snapshots** menu.
2. Open the snapshot to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done** and the document number is generated.
- The snapshot is locked: its lines cannot be computed again.
