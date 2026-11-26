# Activate Contract Recommendation

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_contract_recommendation`\
> **Menu:** Human Resource > Configuration > Manpower Planning > Contract
> Recommendations\
> **Actor:** user in group _Manpower Planning: Manpower Contract Recommendation_\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** user in group _Manpower Planning: Manpower Contract Recommendation_.

## Flow

1. Open the **Human Resource > Configuration > Manpower Planning > Contract
   Recommendations** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more recommendations to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected in new contract review lines.
