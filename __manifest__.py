{
    'name': 'Ship Lifecycle Management',
    'version': '1.0',
    'category': 'Operations',
    'summary': 'Manage full ship lifecycle from design to decommission',
    'author': 'Out of the Box Business Solutions Co.',
    'website': 'https://obbsco.com',
    'depends': ['base','mail','website','portal'],
    'data': [
        'security/ir.model.access.csv',
        'views/ship_views.xml',
        'views/templates.xml',
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
