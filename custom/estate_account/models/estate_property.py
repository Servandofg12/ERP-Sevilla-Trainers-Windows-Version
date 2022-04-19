from odoo import models, Command, fields

class EstatePropertyInherited(models.Model):
    _inherit = "estate.property"

    num_ejemplo = fields.Integer(default=1)

    def action_sold_estate(self):
        #print("ENTRA AQUIII")
        res = super().action_sold_estate()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        #journal = self.env['account.move'].with_context(move_type='out_invoice')._get_default_journal()
        #print("JOURNAL: " + str(journal.id))

        for record in self:
            self.env["account.move"].create(
                {
                    "partner_id": record.partner_id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": record.name,
                                "quantity": 1.0,
                                "price_unit": record.selling_price * 6.0 / 100.0,
                            }),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            },
                        ),
                    ],
                }
            )
        return res