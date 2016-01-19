# coding: utf-8
from openerp import models, api
from openerp.addons.connector.session import ConnectorSession
from .event import print_document_async


class Report(models.Model):
    _inherit = 'report'

    @api.v7
    def print_document(
            self, cr, uid, ids, report_name, html=None, data=None,
            context=None):
        """ TODO: data and html arguments are ignored in
        base_report_to_printer. We do that here too. To be resolved.
        Call with context key queue_print_job=False to force synchronous
        printing.
        """
        if context and not context.get('queue_print_job', True):
            print 'Printing'
            return super(Report, self).print_document(
                cr, uid, ids, report_name, html=html, data=data,
                context=context)
        # serialize arguments
        job_id = self.pool['connector.print.job'].create(
            cr, uid, {
                'job_ids': str(ids),
                'job_context': unicode(context),
                'name': report_name}, context=context)
        print 'Firing'
        return print_document_async.fire(
            ConnectorSession(cr, uid, context),
            'connector.print.job', job_id)

    @api.v8
    def print_document(self, records, report_name, html=None, data=None):
        return self._model.print_document(
            self._cr, self._uid,
            records.ids, report_name,
            html=html, data=data, context=self._context)
