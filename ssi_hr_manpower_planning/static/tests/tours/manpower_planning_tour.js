// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_hr_manpower_planning.manpower_planning_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- Flow 1 of every manpower_planning work
    // instruction: "Open the Human Resource > Manpower Planning >
    // Manpower Plannings menu."
    //
    // The Manpower Planning section sits at level 2 and has children, so
    // it is rendered as a clickable <a class="dropdown-toggle"
    // data-menu-xmlid> by Menu.sections; the leaf is the third step.
    function openPlanningList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Manpower Planning menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_manpower_planning.manpower_planning_menu"]',
            },
            {
                content: "Open the Manpower Plannings menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_manpower_planning.manpower_planning_menu_item"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted, not just
                // for "some list view" -- the landing action of the app is
                // also a .o_list_view.
                content: "Manpower Plannings list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Manpower Plannings)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Opens the row identified by the department name set by setUpClass.
    // Draft plannings share the placeholder number "/", so the unique
    // department name is the only stable row key.
    function openPlanningByDepartment(departmentName) {
        return [
            {
                content: "Open the manpower planning",
                trigger:
                    ".o_data_row:contains(" + departmentName + ") .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    // IK: docs/manpower_planning/01-create.md
    tour.register(
        "ssi_hr_manpower_planning_manpower_planning_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Human Resource > Manpower Planning >
            // Manpower Plannings menu.
            openPlanningList(),
            [
                // Flow 2 -- Click the New button (14.0: "Create").
                {
                    content: "Click Create",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 -- Fill in the header fields. Responsible is
                // filled automatically with the current user and the IK
                // only asks to change it "if needed", so it is left as-is.
                {
                    content: "Fill in the Department",
                    trigger: ".o_field_many2one[name='department_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Tour MPP Create Dept",
                },
                {
                    content: "Pick the Department from the dropdown",
                    trigger:
                        ".ui-autocomplete:visible .ui-menu-item a:contains(Tour MPP Create Dept)",
                    in_modal: false,
                },
                {
                    content: "Fill in Date Start",
                    trigger: ".o_field_widget[name='date_start'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 01/01/2026",
                },
                {
                    content: "Fill in Date End",
                    trigger: ".o_field_widget[name='date_end'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 12/31/2026",
                },

                // Flow 4 -- On the Formations tab, click Add a line and
                // fill in Job Position, Employee and Quantity Needed.
                {
                    content: "Open the Formations tab",
                    trigger: ".o_notebook .nav-link:contains(Formations)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    content: "Add a formation line",
                    trigger:
                        ".o_field_x2many[name='formation_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    content: "Fill in the Job Position",
                    trigger: ".o_selected_row .o_field_many2one[name='job_id'] input",
                    run: "text Tour MPP Create Job",
                },
                {
                    content: "Pick the Job Position from the dropdown",
                    trigger:
                        ".ui-autocomplete:visible .ui-menu-item a:contains(Tour MPP Create Job)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Employee",
                    trigger:
                        ".o_selected_row .o_field_many2one[name='employee_id'] input",
                    run: "text Tour MPP Create Employee",
                },
                {
                    content: "Pick the Employee from the dropdown",
                    trigger:
                        ".ui-autocomplete:visible .ui-menu-item a:contains(Tour MPP Create Employee)",
                    in_modal: false,
                },
                {
                    // Quantity is 1 because an employee is selected.
                    content: "Fill in the Quantity Needed",
                    trigger: ".o_selected_row .o_field_widget[name='quantity']",
                    run: "text 1",
                },

                // Flow 5 -- On the Contract Reviews tab, click Add a line
                // and fill in Employee, Recommendation and Notes. The
                // contract dates are filled automatically from Employee
                // and the IK only asks to change them "if needed".
                {
                    // Clicking the tab also leaves the formation row, which
                    // commits it into the record.
                    content: "Open the Contract Reviews tab",
                    trigger: ".o_notebook .nav-link:contains(Contract Reviews)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    content: "Add a contract review line",
                    trigger:
                        ".o_field_x2many[name='contract_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    content: "Fill in the contract Employee",
                    trigger:
                        ".o_selected_row .o_field_many2one[name='employee_id'] input",
                    run: "text Tour MPP Create Employee",
                },
                {
                    content: "Pick the contract Employee from the dropdown",
                    trigger:
                        ".ui-autocomplete:visible .ui-menu-item a:contains(Tour MPP Create Employee)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Recommendation",
                    trigger:
                        ".o_selected_row .o_field_many2one[name='recommendation_id'] input",
                    run: "text Tour MPP Create Recommendation",
                },
                {
                    content: "Pick the Recommendation from the dropdown",
                    trigger:
                        ".ui-autocomplete:visible .ui-menu-item a:contains(Tour MPP Create Recommendation)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Notes",
                    trigger: ".o_selected_row .o_field_widget[name='notes']",
                    run: "text Tour MPP contract review notes",
                },
                {
                    // Leaving the row commits the last cell; "press Tab"
                    // would open a new empty row and leave the form dirty.
                    content: "Open the Summary tab to commit the review line",
                    trigger: ".o_notebook .nav-link:contains(Summary)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },

                // Flow 6 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Post-Condition -- a new manpower planning is created in
                // Draft status. The summed quantities and the rows of the
                // Summary tab are values and belong to the unit test.
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/manpower_planning/04-confirm.md
    tour.register(
        "ssi_hr_manpower_planning_manpower_planning_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Human Resource > Manpower Planning >
            // Manpower Plannings menu.
            openPlanningList(),
            // Flow 2 -- Open the planning to confirm.
            openPlanningByDepartment("Tour MPP Confirm Dept"),
            [
                // Flow 3 -- Click the Confirm button.
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Waiting for Approval.
                // The approval records created behind it are data, not a
                // user-visible surface, so they are left to the unit test.
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/manpower_planning/05-approve.md
    tour.register(
        "ssi_hr_manpower_planning_manpower_planning_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Human Resource > Manpower Planning >
            // Manpower Plannings menu.
            openPlanningList(),
            // Flow 2 -- Open the planning to approve.
            openPlanningByDepartment("Tour MPP Approve Dept"),
            [
                // Flow 3 -- Click the Approve button.
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- the standard approval template has a
                // single level, so the planning opens automatically and
                // its status changes to On Progress (there is no Start
                // button). The document number is a value and belongs to
                // the unit test.
                {
                    content: "Status is On Progress",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/manpower_planning/09-finish.md
    tour.register(
        "ssi_hr_manpower_planning_manpower_planning_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Human Resource > Manpower Planning >
            // Manpower Plannings menu.
            openPlanningList(),
            // Flow 2 -- Open the planning to finish.
            openPlanningByDepartment("Tour MPP Finish Dept"),
            [
                // Flow 3 -- Click the Done button.
                {
                    content: "Click the Done button",
                    trigger: ".o_statusbar_buttons button[name='action_done']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Done.
                {
                    content: "Status is Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/manpower_planning/10-cancel.md
    tour.register(
        "ssi_hr_manpower_planning_manpower_planning_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Human Resource > Manpower Planning >
            // Manpower Plannings menu.
            openPlanningList(),
            // Flow 2 -- Open the planning to cancel.
            openPlanningByDepartment("Tour MPP Cancel Dept"),
            [
                // Flow 3 -- Click the Cancel button. The button is
                // type="action", so its name= is resolved to a numeric
                // window action id at render time; the label is the only
                // stable handle.
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:contains(Cancel)",
                    extra_trigger: ".o_form_view",
                },
                {
                    // Wizard gate. In 14.0 an in-modal trigger must NOT be
                    // prefixed with ".modal". Gating on the
                    // cancel_reason_id widget rather than ".o_form_view"
                    // matters: the planning form behind the wizard would
                    // satisfy ".o_form_view" even if the wizard never
                    // opened.
                    content: "Wizard is open",
                    trigger: ".o_field_widget[name='cancel_reason_id']",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- In the wizard, select the Cancellation
                // Reason. The field is a radio, picked by its label.
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] label:contains(Tour MPP Cancel Reason)",
                },

                // Flow 5 -- Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Flow 6 -- Click OK on the confirmation dialog. The
                // wizard's Confirm button carries confirm="Are you sure?",
                // so this dialog is stacked on top of the wizard.
                {
                    content: "Confirm the stacked dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Cancelled.
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/manpower_planning/16-generate-contract.md
    tour.register(
        "ssi_hr_manpower_planning_manpower_planning_generate_contract",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Human Resource > Manpower Planning >
            // Manpower Plannings menu.
            openPlanningList(),
            // Flow 2 -- Open the draft planning to fill.
            openPlanningByDepartment("Tour MPP Generate Dept"),
            [
                // Flow 3 -- Click the Generate Contract button.
                {
                    content: "Click the Generate Contract button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_generate_contract']",
                    extra_trigger: ".o_form_view",
                },
                {
                    // The button sits in the statusbar, so it stays
                    // disabled while the action and the reload run.
                    content: "Generate Contract has finished",
                    trigger:
                        ".o_statusbar_buttons button[name='action_generate_contract']:enabled",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- Open the Contract Reviews tab. The row of the
                // fixture employee only exists once the lines are
                // generated, so it cannot match earlier.
                {
                    content: "Open the Contract Reviews tab",
                    trigger: ".o_notebook .nav-link:contains(Contract Reviews)",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition -- a review line exists for the
                // employee on a contract status. The copied dates and the
                // skipped employees are values and belong to the unit test.
                {
                    content: "The contract review line is generated",
                    trigger:
                        ".o_field_x2many[name='contract_ids'] .o_data_row:contains(Tour MPP Generate Employee)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );
});
