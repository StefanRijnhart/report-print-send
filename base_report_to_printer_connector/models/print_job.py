# coding: utf-8
from openerp import api, fields, models
from openerp.addons.connector.queue.job import job
from openerp.tools.safe_eval import safe_eval
from .event import print_document_async


class PrintJob(models.TransientModel):
    """ Transient class to store print job data """
    _name = 'connector.print.job'

    job_context = fields.Char()
    job_ids = fields.Char()
    name = fields.Char('Report name')

    @api.multi
    def run(self):
        print 'Run'
        api.ensure_one()
        self.env['report'].with_context(
            safe_eval(self.job_context), queue_print_job=False).print_document(
            safe_eval(self.job_ids), self.name)


@job
def queue_print_job(session, model_name, record_id):
    print 'Queue'
    session.env[model_name].browse(record_id).run()


def delay_queue_print_job(session, model_name, record_id):
    print 'Delay'
    queue_print_job.delay(session, model_name, record_id)

print_document_async.subscribe(delay_queue_print_job)
