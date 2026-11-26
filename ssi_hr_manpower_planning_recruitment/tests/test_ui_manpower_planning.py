# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 only SavepointCase prepares
# ``cls.env`` in ``setUpClass``, which is where the work instruction
# Pre-Condition below is built.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiManpowerPlanning(HttpSavepointCase):
    """Tour tests for the recruitment extension of ``manpower_planning``."""

    @classmethod
    def setUpClass(cls):
        """Create one open planning with a vacant position.

        ``base.user_admin`` belongs to the validator and the "All" data
        ownership groups of ``manpower_planning`` and to the vacancy
        validator group, so it can run the tour and sees the fixture.
        The planning gets an explicit ``user_id`` so that the internal
        user record rule cannot hide it from the tour session.
        """
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")
        department = cls.env["hr.department"].create({"name": "Tour MPPR Dept"})
        job = cls.env["hr.job"].create({"name": "Tour MPPR Job"})
        cls.planning = (
            cls.env["manpower_planning"]
            .with_user(admin)
            .create(
                {
                    "department_id": department.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "user_id": admin.id,
                    "formation_ids": [
                        (0, 0, {"job_id": job.id, "quantity": 2}),
                    ],
                }
            )
        )
        # The policy fields guarding each button are computed against the
        # state written by the previous transition, so the cache is
        # dropped before every call.
        for method in ("action_confirm", "action_approve_approval"):
            cls.planning.invalidate_cache()
            getattr(cls.planning.with_user(admin), method)()
            cls.planning.invalidate_cache()

    def test_create_recruitment_vacancy(self):
        """Run the create recruitment vacancy tour of the planning.

        IK: docs/manpower_planning/16-create-recruitment-vacancy.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_recruitment_manpower_planning_create_recruitment_vacancy",
            login="admin",
        )
