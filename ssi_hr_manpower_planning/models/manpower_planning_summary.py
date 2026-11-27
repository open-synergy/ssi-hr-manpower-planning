# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ManpowerPlanningSummary(models.Model):
    """
    Read-only SQL view that summarizes the manpower lines of every
    manpower planning per job position and category: needed, filled
    and vacant manpower. The lines come from a union of sources;
    formation is the built-in one and other modules add their own by
    extending :meth:`_get_source_queries`. It feeds the summary tab of
    the planning form, the printed summary and the Manpower
    Fulfillment analysis.
    """

    _name = "manpower_planning_summary"
    _description = "Manpower Planning Summary"
    _auto = False
    _order = "planning_id, job_id"
    _rec_name = "job_id"
    # Models the view reads from, flushed before the view is searched.
    _depends = {
        "manpower_planning": [
            "company_id",
            "department_id",
            "user_id",
            "date_start",
            "date_end",
            "state",
        ],
        "manpower_planning_formation": [
            "planning_id",
            "job_id",
            "employee_id",
            "quantity",
        ],
    }

    planning_id = fields.Many2one(
        string="# Manpower Planning",
        comodel_name="manpower_planning",
        readonly=True,
        help="Manpower planning document the summary line belongs to.",
    )
    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
        readonly=True,
        help="Job position the manpower is summarized for.",
    )
    category = fields.Selection(
        string="Category",
        selection=[("formation", "Formation")],
        readonly=True,
        help="Source of the manpower lines the summary row is built from.",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        readonly=True,
        help="Company of the manpower planning.",
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        readonly=True,
        help="Department of the manpower planning.",
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        readonly=True,
        help="User responsible for the manpower planning.",
    )
    date_start = fields.Date(
        string="Date Start",
        readonly=True,
        help="Start date of the manpower planning period.",
    )
    date_end = fields.Date(
        string="Date End",
        readonly=True,
        help="End date of the manpower planning period.",
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
    quantity_needed = fields.Integer(
        string="Quantity Needed",
        readonly=True,
        help="Total manpower needed for the job position.",
    )
    quantity_filled = fields.Integer(
        string="Quantity Filled",
        readonly=True,
        help="Total manpower already filled for the job position.",
    )
    quantity_vacant = fields.Integer(
        string="Quantity Vacant",
        readonly=True,
        help="Total manpower still vacant for the job position.",
    )

    @property
    def _table_query(self):
        """Return the SQL query that backs this view model.

        :return: SQL string selecting one row per planning, job and
            category
        """
        return "%s %s %s" % (
            self._select(),
            self._from(),
            self._group_by(),
        )

    @api.model
    def _get_source_queries(self):
        """Return the SELECT queries the summary rows are built from.

        Every query must select, in this order, the columns
        ``planning_id``, ``job_id``, ``category``, ``quantity_needed``,
        ``quantity_filled`` and ``quantity_vacant``. Other modules add
        their own source by extending the returned list through
        ``super()``.

        :return: list of SQL SELECT strings, one per source
        :rtype: list
        """
        formation_query = """
        SELECT
            f.planning_id AS planning_id,
            f.job_id AS job_id,
            'formation' AS category,
            f.quantity AS quantity_needed,
            CASE WHEN f.employee_id IS NULL THEN 0 ELSE f.quantity END
                AS quantity_filled,
            CASE WHEN f.employee_id IS NULL THEN f.quantity ELSE 0 END
                AS quantity_vacant
        FROM manpower_planning_formation f
        """
        return [formation_query]

    @api.model
    def _select(self):
        """Return the SELECT clause of the summary view.

        :return: SQL fragment selecting one row per planning, job and
            category
        """
        select_str = """
        SELECT
            ROW_NUMBER() OVER (
                ORDER BY s.planning_id, s.category, s.job_id
            ) AS id,
            s.planning_id AS planning_id,
            s.job_id AS job_id,
            s.category AS category,
            p.company_id AS company_id,
            p.department_id AS department_id,
            p.user_id AS user_id,
            p.date_start AS date_start,
            p.date_end AS date_end,
            p.state AS state,
            SUM(s.quantity_needed) AS quantity_needed,
            SUM(s.quantity_filled) AS quantity_filled,
            SUM(s.quantity_vacant) AS quantity_vacant
        """
        return select_str

    @api.model
    def _from(self):
        """Return the FROM clause of the summary view.

        The source queries are wrapped as the union subquery ``s`` and
        joined to their planning, so header columns stay in the outer
        query.

        :return: SQL fragment joining the union of sources to plannings
        """
        from_str = """
        FROM (
            %s
        ) s
        JOIN manpower_planning p ON p.id = s.planning_id
        """ % (
            " UNION ALL ".join(self._get_source_queries())
        )
        return from_str

    @api.model
    def _group_by(self):
        """Return the GROUP BY clause of the summary view.

        :return: SQL fragment grouping per planning, job and category
        """
        group_by_str = """
        GROUP BY
            s.planning_id,
            s.job_id,
            s.category,
            p.company_id,
            p.department_id,
            p.user_id,
            p.date_start,
            p.date_end,
            p.state
        """
        return group_by_str
