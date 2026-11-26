// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_hr_manpower_planning_recruitment.manpower_planning_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- Flow 1 of the work instruction: "Open the
    // Human Resource > Manpower Planning > Manpower Plannings menu."
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
                // Gate on the TARGET action, not on "some list view".
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

    // IK: docs/manpower_planning/16-create-recruitment-vacancy.md
    tour.register(
        "ssi_hr_manpower_planning_recruitment_manpower_planning_create_recruitment_vacancy",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Human Resource > Manpower Planning >
            // Manpower Plannings menu.
            openPlanningList(),
            [
                // Flow 2 -- Open the planning. Draft and open plannings
                // alike are told apart by the unique department name.
                {
                    content: "Open the manpower planning",
                    trigger: ".o_data_row:contains(Tour MPPR Dept) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 -- Click the Create Recruitment Vacancy button.
                {
                    content: "Click the Create Recruitment Vacancy button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_create_recruitment_vacancy']",
                    extra_trigger: ".o_form_view",
                },
                {
                    // In 14.0 an in-modal trigger must NOT be prefixed with
                    // ".modal". The proposed lines list only exists in the
                    // wizard, so it cannot match on the planning behind it.
                    content: "Wizard is open with the proposed line",
                    trigger:
                        ".o_field_x2many[name='line_ids'] .o_data_row:contains(Tour MPPR Job)",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- Fill in the Expected Join Date of the line.
                {
                    content: "Edit the Expected Join Date of the line",
                    trigger:
                        ".o_field_x2many[name='line_ids'] .o_data_row:first .o_data_cell:eq(2)",
                },
                {
                    content: "Fill in the Expected Join Date",
                    trigger:
                        ".o_selected_row .o_field_widget[name='expected_join_date'] input",
                    run: "text 12/31/2099",
                },

                // Flow 5 -- Click Create Vacancies. Clicking the label of
                // Date Start first leaves the row and commits its cell.
                {
                    content: "Leave the line",
                    trigger: ".o_form_label:contains(Date Start)",
                },
                {
                    content: "Click Create Vacancies",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Post-Condition -- the list of the created vacancies.
                {
                    content: "Recruitment Vacancies list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Recruitment Vacancies)",
                    extra_trigger: "body:not(:has(.modal)) .o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "The created vacancy is listed",
                    trigger: ".o_list_view .o_data_row",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );
});
