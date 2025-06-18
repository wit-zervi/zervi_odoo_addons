import logging
from collections import defaultdict

from odoo import fields, models
from odoo.tools import float_compare, float_is_zero

_logger = logging.getLogger(__name__)


class ProductLabelLayout(models.TransientModel):
    _inherit = "product.label.layout"

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        # This is what it look like after call super
        # xml_id = 'product.report_product_template_label_dymo'
        # data = {
        #     'active_model': 'product.product',
        #     'quantity_by_product': {2: 1}, # {productId: quantity}
        #     'layout_wizard': 18, # incremental integer
        #     'price_included': False,
        #     'custom_barcodes': defaultdict(<class 'list'>, {2: [('250605', 2), ('250604', 2)]})
        # }

        # _logger.info("Hello: this is wit trying to Debug")
        # _logger.info(xml_id)
        # _logger.info(data)

        # Logic that copy from addons\stock\wizard\product_label_layout.py but apply to move_quantity == 'custom'
        #       to print a specific amount of product label along with barcode of lot id
        # fmt: off
        if self.move_quantity == 'custom' and xml_id == 'product.report_product_template_label_dymo':
            if self.move_ids and all(float_is_zero(ml.quantity, precision_rounding=ml.product_uom_id.rounding) for ml in self.move_ids.move_line_ids):
                pass
            elif self.move_ids.move_line_ids:
                quantities = defaultdict(int)
                uom_unit = self.env.ref('uom.product_uom_categ_unit', raise_if_not_found=False)

                custom_barcodes = defaultdict(list)
                for line in self.move_ids.move_line_ids:
                    if line.product_uom_id.category_id == uom_unit:
                        if (line.lot_id or line.lot_name) and int(line.quantity):
                            custom_barcodes[line.product_id.id].append((line.lot_id.name or line.lot_name, int(self.custom_quantity)))
                            continue
                        quantities[line.product_id.id] += line.quantity
                    else:
                        quantities[line.product_id.id] = 1
                # Pass only products with some quantity done to the report
                data['quantity_by_product'] = {p: int(q) for p, q in quantities.items() if q}
                data['custom_barcodes'] = custom_barcodes

                # _logger.info("This is customization in custom_addons/zervi_stock/wizard/product_label_layout.py")
                # _logger.info(data)
        # fmt: on

        return xml_id, data
