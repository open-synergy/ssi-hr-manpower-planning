# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ManpowerPlanningWorkload(models.Model):
    """
    Read-only SQL view that recaps the workload of every employee in
    every school manpower planning: the teaching hours, the number of
    co-teaching lines, the additional assignment hours per week and per
    day, and the total weekly hours. Lines without an employee are left
    out. It feeds the workload tab of the planning form and the workload
    analysis.
    """

    _name = "manpower_planning_workload"
    _description = "Manpower Planning Workload"
    _auto = False
    _order = "planning_id, employee_id"
    _rec_name = "employee_id"
    # Models the view reads from, flushed before the view is searched.
    _depends = {
        "manpower_planning": ["company_id", "user_id", "school_id", "state"],
        "manpower_planning_teaching": [
            "planning_id",
            "employee_id",
            "co_employee_id",
            "total_weekly_hours",
        ],
        "manpower_planning_assignment": [
            "planning_id",
            "employee_id",
            "hour_basis",
            "hours",
        ],
    }

    planning_id = fields.Many2one(
        string="# Manpower Planning",
        comodel_name="manpower_planning",
        readonly=True,
        help="Manpower planning document the workload belongs to.",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        readonly=True,
        help="Employee the workload is recapped for.",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        readonly=True,
        help="Company of the manpower planning.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        readonly=True,
        help="School of the manpower planning.",
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        readonly=True,
        help="User responsible for the manpower planning.",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("reject", "Rejected"),
            ("open", "On Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        readonly=True,
        help="State of the manpower planning.",
    )
    teaching_hours = fields.Integer(
        string="Teaching Hours",
        readonly=True,
        help="Weekly hours of the teaching lines the employee teaches.",
    )
    co_teaching_count = fields.Integer(
        string="Co-Teaching Lines",
        readonly=True,
        help="Number of teaching lines the employee assists as co-teacher.",
    )
    assignment_weekly_hours = fields.Integer(
        string="Assignment Hours per Week",
        readonly=True,
        help="Hours of the additional assignments counted per week.",
    )
    assignment_daily_hours = fields.Integer(
        string="Assignment Hours per Day",
        readonly=True,
        help="Hours of the additional assignments counted per day.",
    )
    total_weekly_hours = fields.Integer(
        string="Total Weekly Hours",
        readonly=True,
        help="Teaching hours plus the additional assignment hours " "counted per week.",
    )

    @property
    def _table_query(self):
        """Return the SQL query that backs this view model.

        :return: SQL string selecting one row per planning and employee
        """
        return "%s %s %s" % (
            self._select(),
            self._from(),
            self._group_by(),
        )

    @api.model
    def _select(self):
        """Return the SELECT clause of the workload view.

        :return: SQL fragment selecting the hours summed per employee
        """
        select_str = """
        SELECT
            ROW_NUMBER() OVER (
                ORDER BY w.planning_id, w.employee_id
            ) AS id,
            w.planning_id AS planning_id,
            w.employee_id AS employee_id,
            p.company_id AS company_id,
            p.school_id AS school_id,
            p.user_id AS user_id,
            p.state AS state,
            SUM(w.teaching_hours) AS teaching_hours,
            SUM(w.co_teaching_count) AS co_teaching_count,
            SUM(w.assignment_weekly_hours) AS assignment_weekly_hours,
            SUM(w.assignment_daily_hours) AS assignment_daily_hours,
            SUM(w.teaching_hours) + SUM(w.assignment_weekly_hours)
                AS total_weekly_hours
        """
        return select_str

    @api.model
    def _from(self):
        """Return the FROM clause of the workload view.

        The inner query unions the teaching lines (as teacher and as
        co-teacher) and the assignment lines, one row per line and
        employee, so the outer query only has to sum them.

        :return: SQL fragment joining the union to its planning
        """
        from_str = """
        FROM (
            SELECT
                t.planning_id AS planning_id,
                t.employee_id AS employee_id,
                COALESCE(t.total_weekly_hours, 0) AS teaching_hours,
                0 AS co_teaching_count,
                0 AS assignment_weekly_hours,
                0 AS assignment_daily_hours
            FROM manpower_planning_teaching t
            WHERE t.employee_id IS NOT NULL
            UNION ALL
            SELECT
                t.planning_id AS planning_id,
                t.co_employee_id AS employee_id,
                0 AS teaching_hours,
                1 AS co_teaching_count,
                0 AS assignment_weekly_hours,
                0 AS assignment_daily_hours
            FROM manpower_planning_teaching t
            WHERE t.co_employee_id IS NOT NULL
            UNION ALL
            SELECT
                a.planning_id AS planning_id,
                a.employee_id AS employee_id,
                0 AS teaching_hours,
                0 AS co_teaching_count,
                CASE WHEN a.hour_basis = 'week'
                    THEN COALESCE(a.hours, 0) ELSE 0
                END AS assignment_weekly_hours,
                CASE WHEN a.hour_basis = 'day'
                    THEN COALESCE(a.hours, 0) ELSE 0
                END AS assignment_daily_hours
            FROM manpower_planning_assignment a
            WHERE a.employee_id IS NOT NULL
        ) w
        JOIN manpower_planning p ON p.id = w.planning_id
        """
        return from_str

    @api.model
    def _group_by(self):
        """Return the GROUP BY clause of the workload view.

        :return: SQL fragment grouping per planning and employee
        """
        group_by_str = """
        GROUP BY
            w.planning_id,
            w.employee_id,
            p.company_id,
            p.school_id,
            p.user_id,
            p.state
        """
        return group_by_str
