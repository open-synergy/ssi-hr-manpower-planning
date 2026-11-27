# Print Manpower Planning Summary

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_planning`\
> **Menu:** Human Resource > Manpower Planning > Manpower Plannings\
> **Actor:** user in group _Manpower Planning: Viewer_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The planning exists. Any status can be printed.
- **Access:** User is in group _Manpower Planning: Viewer_ or higher.

## Flow

1. Open the **Human Resource > Manpower Planning > Manpower Plannings** menu.
2. Open the planning to print.
3. Click the **Print** menu in the control panel.
4. Select the report format:
   - **Manpower Planning Summary** opens the summary on screen as HTML.
   - **Manpower Planning Summary PDF** downloads the summary as a PDF file.
   - **Manpower Planning Summary XLSX** downloads the summary as an Excel workbook.

## Post-Condition

- The report lists the needed, filled and vacant manpower per job position, with the
  filled and vacant percentage of each row and a total.
- The report then lists the same figures and percentages per category (Category Recap).
- The report ends with the contract review lines and the percentage of contracts that
  are continued (review lines whose recommendation does not end the contract, divided by
  all review lines).
- The planning itself is not changed.
