# Create Recruitment Vacancy from Manpower Planning

> **Module:** `ssi_hr_manpower_planning_recruitment`\
> **Model:** `manpower_planning`\
> **Menu:** Human Resource > Manpower Planning > Manpower Plannings\
> **Actor:** user in group _Recruitment Vacancy: User_\
> **Extends:** ssi_hr_manpower_planning — model `manpower_planning`\
> **State:** `open`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status of the planning is **On Progress**.
- **Data:** The planning has formation lines of a job position that are vacant (no
  employee selected). Job positions whose vacant quantity is already covered by the
  recruitment vacancies of the planning are not proposed.
- **Module:** `ssi_hr_manpower_planning_recruitment` is installed.
- **Access:** user in group _Recruitment Vacancy: User_.

## Flow

1. Open the **Human Resource > Manpower Planning > Manpower Plannings** menu.
2. Open the planning to recruit for.
3. Click the **Create Recruitment Vacancy** button.
4. In the wizard that appears, review **Date Start**. It is filled with today and is the
   start date of every created vacancy.
5. Review the proposed lines. One line is proposed per job position that still needs
   people. Edit, add or remove lines if needed. On each line:
   - **Job Position** _(required)_: The job position to recruit for.
   - **Quantity** _(required)_: The number of new employees. It is proposed as the
     vacant quantity that is not yet requested. It must be at least 1.
   - **Expected Join Date** _(required)_: Enter the date on which the new employees are
     expected to join. It must be on or after **Date Start**.
   - **Reason**: Enter why the vacancy is needed.
6. Click **Create Vacancies**.

## Post-Condition

- One recruitment vacancy is created in **Draft** for every line, with the job position,
  the number of expected new employees, the expected join date, the reason, and a link
  to the planning.
- The start date of each vacancy is **Date Start** and its end date is the **Expected
  Join Date** of the line.
- The list of the created vacancies is displayed.
- The **Vacancies** smart button of the planning counts the vacancies requested from it.
- Each vacancy then follows the standard approval of recruitment vacancies.

## Validation

- Creating the vacancies fails **if** the planning is not **On Progress**.
- Saving a line fails **if** the quantity is lower than 1 or the expected join date is
  before **Date Start**.
