odoo.define(
    "ssi_hr_manpower_planning_school.manpower_planning_curriculum_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/manpower_planning_curriculum/01-create.md
        tour.register(
            "ssi_hr_manpower_planning_school_manpower_planning_curriculum_create",
            {
                test: true,
                url: "/web",
            },
            [
                // -- Flow 1 -- Open the Human Resource > Configuration > Manpower
                // Planning > Curriculums menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
                },
                {
                    // "Manpower Planning" is a grouping header without action;
                    // no step for it. Go straight to the leaf.
                    content: "Open the Curriculums menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr_manpower_planning_school.manpower_planning_curriculum_menu"]',
                },
                {
                    content: "Curriculums list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Curriculums)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // -- Flow 2 -- Click the New button (14.0: "Create").
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

                // -- Flow 3 -- Fill in the fields (Name, Code).
                {
                    content: "Enter the name",
                    trigger: ".o_form_view .o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR-MPPS-CUR-CREATE",
                },
                {
                    content: "Enter the code",
                    trigger: ".o_form_view .o_field_widget[name='code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR-MPPS-CUR-CREATE",
                },

                // -- Flow 4 -- Open the Curriculum tab.
                {
                    content: "Open the Curriculum tab",
                    trigger: ".o_notebook .nav-link:contains(Curriculum)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    content: "Curriculum tab is active",
                    trigger: ".o_notebook .nav-link.active:contains(Curriculum)",
                    run: function () {
                        // Assertion only.
                    },
                },

                // -- Flow 5 -- Fill in the curriculum details: Description.
                {
                    content: "Enter the description",
                    trigger: ".o_form_view .o_field_widget[name='description']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Tour MPPS curriculum description",
                },

                // -- Flow 6 -- Click Save.
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

                // -- Post-Condition -- the new record is created and listed.
                {
                    content: "Back to the list",
                    trigger: ".o_control_panel .breadcrumb-item:not(.active) a",
                },
                {
                    content: "The new record is listed",
                    trigger: ".o_list_view .o_data_row:contains(TOUR-MPPS-CUR-CREATE)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
