{
    'name':
        "Test App",
    'author':
        "Kit Solutions",
    'category':
        'Uncategorized',
    'version':
        '17.0.0.0.0',
    'depends': ['base','sale_management','account_accountant', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/building_view.xml',
        'reports/property_report.xml',

    ],
    'application': True,
}