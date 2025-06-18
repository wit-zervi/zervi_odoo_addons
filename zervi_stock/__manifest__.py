{
    "name": "Zervi Inventory Customization",
    "version": "17.0.1.0.3",
    "category": "Inventory",
    "summary": "A customization module for inventory.",
    "description": """
Features
==========
1. Add barcode of the lot number to "Print product label" feature at stock.picking page 
when select Quantity to print = Custom. This allow user to print less copy 
and avoid odoo hang due to huge number of receipt qty.
    """,
    "author": "Wit",
    "website": "http://www.zervi.com",
    "depends": ["stock"],
    "data": [
        # 'security/ir.model.access.csv', # Uncomment if you have security rules
        # 'views/my_model_views.xml',    # Uncomment if you have views
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "MIT",
}
