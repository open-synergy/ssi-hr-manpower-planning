// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_hr_manpower_planning.manpower_head_count_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Steps shared by every tour: Flow "Open the Human Resource > Manpower
    // Planning > Head Count Snapshots menu".
    function openMenuSteps() {
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
                content: "Open the Head Count Snapshots menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_manpower_planning.manpower_head_count_menu"]',
            },
            {
                content: "Head Count Snapshots list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Head Count Snapshots)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    // IK: docs/manpower_head_count/01-create.md
    tour.register(
        "ssi_hr_manpower_planning_manpower_head_count_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Manpower Planning >
            // Head Count Snapshots menu.
            ...openMenuSteps(),

            // ── Flow 2 — Click the New button (14.0: "Create").
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

            // ── Flow 3 — Fill in the header fields. Responsible is filled
            // automatically with the current user, so it is left as is.
            {
                content: "Select the Department",
                trigger: ".o_field_many2one[name='department_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR HC Create Department",
            },
            {
                content: "Pick the Department from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR HC Create Department)",
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

            // ── Flow 4 — Click Save.
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

            // ── Flow 5 — Click Compute Lines in the form header to build the
            // lines on the Head Counts tab.
            {
                content: "Click the Compute Lines button",
                trigger: ".o_statusbar_buttons button[name='action_compute_line']",
                extra_trigger: ".o_form_view.o_form_readonly",
            },
            {
                // Gate: the job token exists only after the lines are built,
                // because a new snapshot has no lines before this click.
                content: "The head count lines are built",
                trigger:
                    ".o_field_widget[name='line_ids'] .o_data_row:contains(TOUR HC Create Job)",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Post-Condition — A new head count snapshot is created in
            // Draft status; each line shows the head count columns.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Head count line columns are displayed",
                trigger:
                    ".o_field_widget[name='line_ids'] th[data-name='closing_count']",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/manpower_head_count/09-finish.md
    tour.register(
        "ssi_hr_manpower_planning_manpower_head_count_finish",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Manpower Planning >
            // Head Count Snapshots menu.
            ...openMenuSteps(),

            // ── Flow 2 — Open the snapshot to finish.
            {
                content: "Open the snapshot to finish",
                trigger:
                    ".o_data_row:contains(TOUR HC Finish Department) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 3 — Click the Done button.
            {
                content: "Click the Done button",
                trigger: ".o_statusbar_buttons button[name='action_done']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — Status changes to Done and the document
            // number is generated.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Document number is generated",
                trigger: ".o_field_widget[name='display_name']:contains(MHC)",
                run: function () {
                    // Assertion only.
                },
            },
            // ── Post-Condition — The snapshot is locked: its lines cannot be
            // computed again.
            {
                content: "Compute Lines is NOT shown",
                trigger:
                    ".o_statusbar_buttons:not(:has(button[name='action_compute_line']:visible))",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/manpower_head_count/10-cancel.md
    tour.register(
        "ssi_hr_manpower_planning_manpower_head_count_cancel",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Manpower Planning >
            // Head Count Snapshots menu.
            ...openMenuSteps(),

            // ── Flow 2 — Open the snapshot to cancel.
            {
                content: "Open the snapshot to cancel",
                trigger:
                    ".o_data_row:contains(TOUR HC Cancel Department) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 3 — Click the Cancel button.
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — In the wizard that appears, select the
            // Cancellation Reason.
            {
                content: "Select the cancellation reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(TOUR HC Cancel Reason) input",
            },

            // ── Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // ── Flow 6 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
            },

            // ── Post-Condition — Status changes to Cancelled.
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
    );
});
