# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 only SavepointCase prepares
# ``cls.env`` in ``setUpClass``, which is where every work instruction
# Pre-Condition below is built.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiManpowerPlanning(HttpSavepointCase):
    """Tour tests for the ``manpower_planning`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the master data and one planning per tour.

        ``base.user_admin`` belongs to the validator and the "All" data
        ownership groups of ``manpower_planning``, so it can run every
        tour below and sees every fixture. Each planning still gets an
        explicit ``user_id`` so that the internal user record rule
        cannot hide it from the tour session.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Pre-Condition 01-create.md: the department, job position,
        # employee and contract recommendation the tour picks from the
        # dropdowns already exist.
        cls.env["hr.department"].create({"name": "Tour MPP Create Dept"})
        cls.env["hr.job"].create({"name": "Tour MPP Create Job"})
        cls.env["hr.employee"].create({"name": "Tour MPP Create Employee"})
        cls.env["manpower_contract_recommendation"].create(
            {
                "name": "Tour MPP Create Recommendation",
                "code": "TOURMPPREC",
            }
        )

        # Pre-Condition 10-cancel.md: a reason exists and is global, so
        # the wizard lists it whatever the demo data holds.
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour MPP Cancel Reason",
                    "code": "TOURMPPCR",
                    "global_use": True,
                }
            )
        )

        # Pre-Condition 04-confirm.md: Draft.
        cls.planning_confirm = cls._create_planning("Confirm")

        # Pre-Condition 05-approve.md: Waiting for Approval, with
        # ``admin`` among the active approvers (validator group).
        cls.planning_approve = cls._create_planning("Approve")
        cls._run_transition(cls.planning_approve, "action_confirm")

        # Pre-Condition 09-finish.md: On Progress, reached by approving
        # a confirmed planning (the approval opens it automatically).
        cls.planning_finish = cls._create_planning("Finish")
        cls._run_transition(cls.planning_finish, "action_confirm")
        cls._run_transition(cls.planning_finish, "action_approve_approval")

        # Pre-Condition 10-cancel.md: Draft, one of the states the
        # cancel policy allows.
        cls.planning_cancel = cls._create_planning("Cancel")

        # Pre-Condition 16-generate-contract.md: Draft, the company has a
        # contract employment status and the department has one active
        # employee with that status. The employee is the delta the tour
        # waits for, because the planning has no review line before the
        # button is clicked.
        company = cls.admin.company_id
        cls.contract_status = cls.env["hr.employment_status"].create(
            {"name": "Tour MPP Contract Status", "code": "/"}
        )
        company.manpower_contract_employment_status_ids = [(4, cls.contract_status.id)]
        cls.planning_generate = cls._create_planning("Generate")
        cls.env["hr.employee"].create(
            {
                "name": "Tour MPP Generate Employee",
                "company_id": company.id,
                "department_id": cls.planning_generate.department_id.id,
                "employment_status_id": cls.contract_status.id,
                "date_contract_start": "2026-01-01",
                "date_contract_end": "2026-12-31",
            }
        )

    @classmethod
    def _create_planning(cls, label):
        """Create one Draft planning dedicated to a single tour.

        :param label: short scenario name, e.g. ``"Confirm"``
        :return: the new ``manpower_planning`` record, in Draft, whose
            department name is the key the tour uses to find its row
        """
        department = cls.env["hr.department"].create(
            {"name": "Tour MPP %s Dept" % label}
        )
        job = cls.env["hr.job"].create({"name": "Tour MPP %s Job" % label})
        return (
            cls.env["manpower_planning"]
            .with_user(cls.admin)
            .create(
                {
                    "department_id": department.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "user_id": cls.admin.id,
                    "formation_ids": [
                        (0, 0, {"job_id": job.id, "quantity": 2}),
                    ],
                }
            )
        )

    @classmethod
    def _run_transition(cls, planning, method):
        """Advance a fixture planning through one workflow method.

        The policy fields guarding each button are computed from
        ``policy.template`` against the state written by the previous
        transition, so the cache is dropped before every call.

        :param planning: the ``manpower_planning`` record to advance
        :param method: name of the workflow method, e.g.
            ``"action_confirm"``
        """
        planning.invalidate_cache()
        getattr(planning.with_user(cls.admin), method)()
        planning.invalidate_cache()

    def test_create(self):
        """Run the create tour for ``manpower_planning``.

        IK: docs/manpower_planning/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_manpower_planning_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``manpower_planning``.

        IK: docs/manpower_planning/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_manpower_planning_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``manpower_planning``.

        IK: docs/manpower_planning/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_manpower_planning_approve",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``manpower_planning``.

        IK: docs/manpower_planning/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_manpower_planning_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``manpower_planning``.

        IK: docs/manpower_planning/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_manpower_planning_cancel",
            login="admin",
        )

    def test_generate_contract(self):
        """Run the generate contract tour for ``manpower_planning``.

        IK: docs/manpower_planning/16-generate-contract.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_manpower_planning_generate_contract",
            login="admin",
        )
