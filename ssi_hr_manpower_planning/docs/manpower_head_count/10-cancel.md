# Cancel Head Count Snapshot

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_head_count`\
> **Menu:** Human Resource > Manpower Planning > Head Count Snapshots\
> **Actor:** user in group _Manpower Head Count: Validator_\
> **State:** `draft` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft** or **Done**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for state
  `that` to the actor's group.
- **Data:** At least one cancellation reason exists.
- **Access:** user in group _Manpower Head Count: Validator_.

## Flow

1. Open the **Human Resource > Manpower Planning > Head Count Snapshots** menu.
2. Open the snapshot to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
