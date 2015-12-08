# -*- coding: utf-8 -*-

from openerp import models, fields, api
from suds.client import Client


class Wizard(models.TransientModel):
    _name = 'maarch.wizard'

    filesubject = fields.Char(string=u"Objet du document / courrier", required=True)
    document_ids = fields.One2many('maarch.document', 'document_id', string=u"Documents")

    @api.multi
    def add_maarchdoc_in_odoo(self):
        # TODO
        """
        return {
            'name': 'Recherche d\'un document dans Maarch',
            'type': 'ir.actions.act_window',
            'res_model': 'maarch.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            # 'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
        """

    @api.onchange('filesubject')
    # @api.constrains('filesubject')
    def on_filesubject_change(self):

        # TODO : replace the test data
        _client_maarch = Client("http://10.0.0.195/maarch15/ws_server.php?WSDL", username="bblier", password="maarch")

        param = _client_maarch.factory.create('customizedSearchParams')
        param.subject = self.filesubject
        response = _client_maarch.service.customizedSearchResources(param)
        final_docs_list = []
        if response:
            maarchdoc = response[0]
            # if there is more than 1 result we handle a list
            if isinstance(maarchdoc, list):
                for doc in maarchdoc:
                    result = {}
                    result.update({'maarch_id': doc.res_id})
                    result.update({'subject': doc.subject.encode('utf8')})
                    result.update({'doc_date': doc.doc_date})
                    final_docs_list.append(result)
            # if there is exactly one result we get directly the document instance
            else:
                result = {}
                result.update({'maarch_id': maarchdoc.res_id})
                result.update({'subject': maarchdoc.subject.encode('utf8')})
                result.update({'doc_date': maarchdoc.doc_date})
                final_docs_list.append(result)
        self.document_ids = final_docs_list


class DocumentWizard(models.TransientModel):
    _name = 'maarch.document'

    maarch_id = fields.Char(string=u"id", readonly=True)
    subject = fields.Char(string=u"objet", readonly=True)
    doc_date = fields.Date(string=u"date", readonly=True)
    document_id = fields.Many2one('maarch.wizard')

