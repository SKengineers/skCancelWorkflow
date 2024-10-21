# -*- coding: utf-8 -*-
{
    'name': "SK Cancel Work Flow",
    'summary': """
        Cancel Work Flow""",
    'description': """
        Cancel Work Flow of Sale, Purchase, Invoice, Bill and Picking
            """,
    'author': 'Sritharan K',
    'company': 'SK Engineer',
    'maintainer': 'SK ENgineer',
    'website': "https://www.skengineer.be/",
    'category': 'Tools',
    'version': '17.1',
    'depends': ['base', 'sale_purchase_stock'],
    'data': [
        'security/ir.model.access.csv',

        'views/stock_picking_view.xml',
        'views/purchase_order_view.xml',

        'data/action_server.xml',

        'wizard/wizard_cancel_work_flow_view.xml',
    ],
    "images": [
        "/static/description/icon.png"
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
