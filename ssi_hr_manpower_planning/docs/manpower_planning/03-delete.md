# Delete Manpower Planning

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_planning`\
> **Menu:** Human Resource > Manpower Planning > Manpower Plannings\
> **Actor:** user in group _Manpower Planning: User_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Document number is still **/** (not yet generated).
- **Access:** user in group _Manpower Planning: User_.

## Flow

1. Open the **Human Resource > Manpower Planning > Manpower Plannings** menu.
2. Select one or more plannings to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected plannings, with their formation and contract review lines, are
  permanently removed from the system.
