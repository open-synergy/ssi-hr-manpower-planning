odoo.define("ssi_hr_manpower_planning.manpower_contract_recommendation_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/manpower_contract_recommendation/01-create.md
    tour.register(
        "ssi_hr_manpower_planning_manpower_contract_recommendation_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Configuration > Manpower
            // Planning > Contract Recommendations menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
            },
            {
                // "Manpower Planning" is a grouping header without action;
                // no step for it. Go straight to the leaf.
                content: "Open the Contract Recommendations menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_manpower_planning.manpower_contract_recommendation_menu"]',
            },
            {
                content: "Contract Recommendations list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Contract Recommendations)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

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

            // ── Flow 3 — Fill in the fields (Name, Code).
            {
                content: "Enter the name",
                trigger: ".o_form_view .o_field_widget[name='name']",
                run: "text TOUR-REC-CREATE",
            },
            {
                content: "Enter the code",
                trigger: ".o_form_view .o_field_widget[name='code']",
                run: "text TOUR-REC-CREATE",
            },

            // ── Flow 4 — Open the Contract tab.
            {
                content: "Open the Contract tab",
                trigger: ".o_notebook .nav-link:contains(Contract)",
            },
            {
                content: "Contract tab is active",
                trigger: ".o_notebook .nav-link.active:contains(Contract)",
                extra_trigger: ".o_field_widget[name='is_terminate']",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 5 — Set the contract options: Terminate Contract.
            {
                content: "Check Terminate Contract",
                trigger: ".o_field_widget[name='is_terminate'] input",
            },

            // ── Flow 6 — Click Save.
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

            // ── Post-Condition — A new contract recommendation is created.
            {
                content: "Back to the list",
                trigger: ".o_control_panel .breadcrumb-item:not(.active) a",
            },
            {
                content: "The new recommendation is listed",
                trigger: ".o_list_view .o_data_row:contains(TOUR-REC-CREATE)",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});
