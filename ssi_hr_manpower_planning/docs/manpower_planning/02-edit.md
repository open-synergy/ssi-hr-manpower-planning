# Edit Manpower Planning

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_planning`\
> **Menu:** Human Resource > Manpower Planning > Manpower Plannings\
> **Actor:** user in group _Manpower Planning: User_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** user in group _Manpower Planning: User_.

## Flow

1. Open the **Human Resource > Manpower Planning > Manpower Plannings** menu.
2. Find and open the planning to edit.
3. Change the required fields in the header, the **Formations** tab or the **Contract
   Reviews** tab.
4. Click **Save**.

## Post-Condition

- The planning is updated with the new values.
- **Quantity Needed**, **Quantity Filled** and **Quantity Vacant** are recomputed from
  the formation lines.
