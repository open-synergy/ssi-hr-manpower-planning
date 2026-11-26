# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=C8101
{
    "name": "HR - Manpower Planning - Recruitment",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_hr_manpower_planning",
        "ssi_hr_recruitment",
        "web_tour",
    ],
    "data": [
        "security/ir_model_access/create_recruitment_vacancy_from_manpower_planning.xml",
        "security/ir_model_access/create_recruitment_vacancy_from_manpower_planning_line.xml",
        "views/recruitment_vacancy.xml",
        "views/manpower_planning.xml",
        "wizards/create_recruitment_vacancy_from_manpower_planning.xml",
        "views/assets.xml",
    ],
    "demo": [],
}
