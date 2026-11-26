# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase, not HttpCase: HttpCase has no cls.env in 14.0.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiManpowerHeadCount(HttpSavepointCase):
    """Tour tests for the ``manpower_head_count`` work instructions."""

    @classmethod
    def _create_department(cls, name):
        """Create a department and one employee on a job inside it.

        :param name: the unique name of the department
        :return: the new ``hr.department`` record
        """
        department = cls.env["hr.department"].create({"name": name})
        job = cls.env["hr.job"].create({"name": name.replace("Department", "Job")})
        for index in range(2):
            cls.env["hr.employee"].create(
                {
                    "name": "%s Employee %s" % (name, index),
                    "department_id": department.id,
                    "job_id": job.id,
                    "date_join": "2025-01-01",
                }
            )
        return department

    @classmethod
    def _create_head_count(cls, department):
        """Create a draft head count snapshot for a department.

        :param department: the ``hr.department`` to limit the snapshot to
        :return: the new ``manpower_head_count`` record
        """
        return cls.env["manpower_head_count"].create(
            {
                "department_id": department.id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
                # Explicit: cls.env runs as SUPERUSER and the record rule
                # would hide the snapshot from the admin tour session.
                "user_id": cls.admin.id,
            }
        )

    @classmethod
    def setUpClass(cls):
        """Create the departments, employees and snapshots for the tours."""
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.department_create = cls._create_department("TOUR HC Create Department")
        cls.department_finish = cls._create_department("TOUR HC Finish Department")
        cls.department_cancel = cls._create_department("TOUR HC Cancel Department")
        cls.head_count_finish = cls._create_head_count(cls.department_finish)
        cls.head_count_cancel = cls._create_head_count(cls.department_cancel)
        # global_use makes the reason visible in the cancel wizard.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR HC Cancel Reason",
                "code": "TOUR-HC-CANCEL",
                "global_use": True,
            }
        )

    def test_create(self):
        """Run the create tour for ``manpower_head_count``.

        IK: docs/manpower_head_count/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_manpower_head_count_create",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``manpower_head_count``.

        IK: docs/manpower_head_count/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_manpower_head_count_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``manpower_head_count``.

        IK: docs/manpower_head_count/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_manpower_head_count_cancel",
            login="admin",
        )
