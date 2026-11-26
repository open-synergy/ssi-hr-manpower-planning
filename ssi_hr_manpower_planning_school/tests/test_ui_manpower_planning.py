# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase, not HttpCase: in 14.0 only SavepointCase prepares
# ``cls.env`` in ``setUpClass``, which is where the Pre-Condition below is
# built.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiManpowerPlanning(HttpSavepointCase):
    """Tour tests for the school extension of ``manpower_planning``."""

    @classmethod
    def setUpClass(cls):
        """Create the master data the create tour picks from dropdowns.

        The Pre-Condition of the create work instruction asks for a
        department, a school with a grade and a class, a subject taught
        on that grade, an academic year, a curriculum, a teacher and an
        assignment type. Master data codes are ``/`` (no unique code).
        """
        super().setUpClass()
        env = cls.env
        env["hr.department"].create({"name": "Tour MPPS Dept"})
        grade_type = env["school_grade_type"].create(
            {"name": "Tour MPPS Grade Type", "code": "/", "sequence": 10}
        )
        school = env["school"].create(
            {
                "name": "Tour MPPS School",
                "code": "/",
                "grade_type_id": grade_type.id,
            }
        )
        grade = env["school_grade"].create(
            {
                "name": "Tour MPPS Grade",
                "code": "/",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        env["school_grade_class"].create(
            {
                "name": "Tour MPPS Class",
                "code": "/",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        env["school_subject"].create(
            {
                "name": "Tour MPPS Subject",
                "code": "/",
                "grade_ids": [(6, 0, [grade.id])],
            }
        )
        env["school_academic_year"].create(
            {
                "name": "Tour MPPS Year",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        env["manpower_planning_curriculum"].create(
            {"name": "Tour MPPS Curriculum", "code": "/"}
        )
        env["hr.employee"].create({"name": "Tour MPPS Teacher"})
        env["manpower_planning_assignment_type"].create(
            {
                "name": "Tour MPPS Type",
                "code": "/",
                "category": "structural",
                "hour_basis": "week",
                "default_hours": 6,
            }
        )

    def test_create(self):
        """Run the create tour of the school tabs of the planning.

        IK: docs/manpower_planning/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_manpower_planning_school_manpower_planning_create",
            login="admin",
        )
