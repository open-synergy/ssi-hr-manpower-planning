# Generate Contract Reviews - Manpower Planning

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_planning`\
> **Menu:** Human Resource > Manpower Planning > Manpower Plannings\
> **Actor:** user in group _Manpower Planning: User_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** **Department** is filled.
- **Config:** The company of the planning has at least one **Contract Employment
  Statuses** value, set in **Settings > Human Resources > Manpower Planning**.
- **Data:** The employees of the department that are on a contract exist, are active,
  and have one of the contract employment statuses.
- **Access:** user in group _Manpower Planning: User_.

## Flow

1. Open the **Human Resource > Manpower Planning > Manpower Plannings** menu.
2. Open the draft planning to fill.
3. Click the **Generate Contract** button.
4. Open the **Contract Reviews** tab to check the new lines.

## Post-Condition

- The **Contract Reviews** tab has one line for each active employee of the planning
  company and department whose employment status is one of the contract employment
  statuses.
- Each new line holds the **Contract Start Date** and **Contract End Date** of the
  employee, and has no **Recommendation**.
- An employee that already has a line is skipped, so clicking the button again does not
  add the employee a second time and does not change the existing lines.
- When no employee matches, no line is added and no error is shown.
- When the company has no contract employment status, an error asks to configure the
  contract employment statuses first.
