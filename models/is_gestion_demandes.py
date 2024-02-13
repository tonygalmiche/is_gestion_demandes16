# -*- coding: utf-8 -*-
from odoo import models,fields,api
from datetime import datetime, date


class is_gestion_demandes_application(models.Model):
    _name = 'is.gestion.demandes.application'
    _description = "Application"
    

    name          = fields.Char('Application', required=True)
    tps_mini      = fields.Float('Temps mini prévu (H)')
    tps_maxi      = fields.Float('Temps maxi prévue (H)')
    tps_mini_jour = fields.Float('Temps mini (Jour)' , compute="_compute", store=True)
    tps_maxi_jour = fields.Float('Temps maxi (Jour)' , compute="_compute", store=True)
    cout_horaire = fields.Float('Coût horaire', default=45)
    cout_mini    = fields.Float('Coût mini prévu'    , compute="_compute", store=True)
    cout_maxi    = fields.Float('Coût maxi prévue'   , compute="_compute", store=True)
    commentaire  = fields.Text('Commentaire')

   

    @api.depends('tps_mini','tps_maxi','cout_horaire')
    def _compute(self):
        for obj in self:
            obj.cout_mini = obj.tps_mini * obj.cout_horaire
            obj.cout_maxi = obj.tps_maxi * obj.cout_horaire
            obj.tps_mini_jour = obj.tps_mini/8
            obj.tps_maxi_jour = obj.tps_maxi/8


    

class is_gestion_demandes(models.Model):
    _name = 'is.gestion.demandes'
    # _inherit=['mail.thread']
    _description = "Gestion des demandes pour Plastigray"
    _order='name desc'

    name             = fields.Char('N°demande', readonly=True)
    createur_id      = fields.Many2one('res.users', 'Créateur' , readonly=True, default=lambda self: self.env.uid)
    demandeur_id     = fields.Many2one('res.users', 'Demandeur', required=True, default=lambda self: self.env.uid)
    date_demande     = fields.Date('Date demande', default=lambda *a: fields.datetime.now())
    application_id   = fields.Many2one('is.gestion.demandes.application', 'Application concernée')
    demande          = fields.Text('Demande', required=True)
    etude            = fields.Text('Étude')
    tps_prevu        = fields.Float('Temps prévu (H)')
    date_validation  = fields.Date('Date validation')
    date_prevue      = fields.Date('Date prévue')
    date_realisation = fields.Date('Date réalisation')
    tps_passe        = fields.Float('Temps passé (H)')
    tps_passe_jour   = fields.Float('Temps passé (Jour)', compute="_compute", store=True)
    taux_horaire     = fields.Float('Taux horaire', default=45)
    montant_facture  = fields.Float('Montant à facturer', compute="_compute", store=True)
    facture          = fields.Char('Facture')
    state            = fields.Selection([
        ('a_chiffrer' , u'A Chiffrer'),
        ('a_valider'  , u'A Valider'),
        ('a_realiser' , u'A Réaliser'),
        ('a_facturer' , u'A Facturer'),
        ('facture'    , u'Facturé')
    ], 'Etat', index=True, default="a_chiffrer")


    @api.depends('tps_passe','taux_horaire')
    def _compute(self):
        for obj in self:
            obj.montant_facture = obj.tps_passe*obj.taux_horaire
            obj.tps_passe_jour=obj.tps_passe/8


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('is.gestion.demandes')
        return super().create(vals_list)

