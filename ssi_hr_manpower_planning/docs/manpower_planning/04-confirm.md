# Confirm Manpower Planning

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_planning`\
> **Menu:** Human Resource > Manpower Planning > Manpower Plannings\
> **Actor:** user in group _Manpower Planning: User_\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Department, **Date Start** and **Date End** are filled.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** user in group _Manpower Planning: User_.

## Flow

1. Open the **Human Resource > Manpower Planning > Manpower Plannings** menu.
2. Open the planning to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the approval template.
