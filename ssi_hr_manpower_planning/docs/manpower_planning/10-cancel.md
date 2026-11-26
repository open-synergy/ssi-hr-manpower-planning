# Cancel Manpower Planning

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_planning`\
> **Menu:** Human Resource > Manpower Planning > Manpower Plannings\
> **Actor:** user in group _Manpower Planning: Validator_\
> **State:** `draft` | `confirm` | `open` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, **On Progress** or
  **Done**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for state
  `that` to the actor's group.
- **Data:** At least one cancellation reason exists.
- **Access:** user in group _Manpower Planning: Validator_.

## Flow

1. Open the **Human Resource > Manpower Planning > Manpower Plannings** menu.
2. Open the planning to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
