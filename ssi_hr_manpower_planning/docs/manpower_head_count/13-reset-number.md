# Reset Document Number - Head Count Snapshot

> **Module:** `ssi_hr_manpower_planning`\
> **Model:** `manpower_head_count`\
> **Menu:** Human Resource > Manpower Planning > Head Count Snapshots\
> **Actor:** user in group _Manpower Head Count: Validator_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `sequence.template` exists for this model.
- **Config:** An active `policy.template` for this model grants `manual_number_ok` for
  state `draft` to the actor's group.
- **Access:** user in group _Manpower Head Count: Validator_.

## Flow

1. Open the **Human Resource > Manpower Planning > Head Count Snapshots** menu.
2. Open the snapshot whose document number will be reset.
3. Click the **Reset Document Number** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Document number returns to **/**.
- The snapshot receives an automatic number when it is done, according to the sequence
  template configuration.
