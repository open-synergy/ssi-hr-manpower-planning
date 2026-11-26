# Deactivate Contract Recommendation

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_contract_recommendation`\
> **Menu:** Human Resource > Configuration > Manpower Planning > Contract
> Recommendations\
> **Actor:** user in group _Manpower Planning: Manpower Contract Recommendation_\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** user in group _Manpower Planning: Manpower Contract Recommendation_.

## Flow

1. Open the **Human Resource > Configuration > Manpower Planning > Contract
   Recommendations** menu.
2. Select one or more recommendations to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected in new contract review lines.
- Contract review lines that already use this record can still be viewed.
