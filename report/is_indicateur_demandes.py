# -*- coding: utf-8 -*-
from odoo import models,fields,tools

class is_indicateur_demandes(models.Model):
    _name = "is.indicateur.demandes"
    _description = "Indicateurs sur les demandes"
    _order = 'name'
    _auto = False

    name           = fields.Char('Application')
    application_id = fields.Many2one('is.gestion.demandes.application', 'Application concernée')
    commentaire    = fields.Char('Commentaire')
    tps_maxi_jour  = fields.Float('Temps prévu maxi (Jour)')
    tps_passe      = fields.Float('Temps passé (Jour)')
    tps_restant    = fields.Float('Temps restant')
    avancement     = fields.Float('Avancement')


    def init(self):
        cr = self._cr
        tools.drop_view_if_exists(cr, 'is_indicateur_demandes')
        cr.execute("""
                CREATE OR REPLACE view is_indicateur_demandes AS (
                    SELECT
                        ia.id as id,
                        ia.name as name,
                        ia.id as application_id,
                        ia.commentaire as commentaire,
                        ia.tps_maxi_jour as tps_maxi_jour,
                        sum(gd.tps_passe)/8 as tps_passe,
                        (ia.tps_maxi_jour - sum(gd.tps_passe)/8) as tps_restant,
                        (100*sum(gd.tps_passe)/ia.tps_maxi) as avancement
                    FROM is_gestion_demandes gd LEFT OUTER JOIN is_gestion_demandes_application ia ON gd.application_id=ia.id 
                    WHERE ia.id>0 and ia.tps_maxi>0
                    GROUP BY ia.id, ia.name
                    ORDER BY ia.name 
               )
        """)


