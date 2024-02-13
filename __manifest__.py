# -*- coding: utf-8 -*-
{
    "name"     : "Module Odoo 16 de gestion des demandes pour Plastigray",
    "version"  : "1.0",
    "author"   : "InfoSaône",
    "category" : "InfoSaône\Plastigray",
    "description": """
Module Odoo 16 de gestion des demandes pour Plastigray
""",
    "maintainer": "InfoSaône",
    "website": "http://www.infosaone.com",
    "depends": [
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/is_gestion_demandes_view.xml",
        "report/is_indicateur_demandes.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}

