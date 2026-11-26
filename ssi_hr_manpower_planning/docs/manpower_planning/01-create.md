# Create Manpower Planning

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_planning`\
> **Menu:** Human Resource > Manpower Planning > Manpower Plannings\
> **Actor:** user in group _Manpower Planning: User_\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** The department the planning is made for exists, and every job position and
  employee that will be planned exists.
- **Data:** The contract recommendations that will be given exist (optional).
- **Access:** user in group _Manpower Planning: User_.

## Flow

1. Open the **Human Resource > Manpower Planning > Manpower Plannings** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the header fields:
   - **Responsible** _(required)_: Automatically filled with the current user. Change if
     needed.
   - **Department** _(required)_: Select the department the planning is made for.
   - **Date Start** _(required)_: First day of the planning period.
   - **Date End** _(required)_: Last day of the planning period. It cannot be earlier
     than **Date Start**.
4. On the **Formations** tab, click **Add a line**. Repeat the following steps as many
   times as needed:
   - **Job Position** _(required)_: Select the job position that is planned.
   - **Employee**: Select the employee who already fills the position. Leave empty when
     the position is vacant.
   - **Quantity Needed** _(required)_: Enter the number of people needed. It must be 1
     when an employee is selected.
5. On the **Contract Reviews** tab, click **Add a line**. Repeat the following steps as
   many times as needed:
   - **Employee** _(required)_: Select the employee whose contract is reviewed.
   - **Contract Start Date**: Automatically filled from **Employee**. Change if needed.
   - **Contract End Date**: Automatically filled from **Employee**. Change if needed.
   - **Recommendation**: Select the recommendation given for the contract.
   - **Notes**: Enter additional remarks.
6. Click **Save**.

## Post-Condition

- A new manpower planning is created in **Draft** status.
- **Quantity Needed**, **Quantity Filled** and **Quantity Vacant** are summed from the
  formation lines.
- The **Summary** tab shows the needed, filled and vacant manpower per job position.
