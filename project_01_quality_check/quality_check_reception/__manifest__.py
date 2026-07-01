{
    'name': 'Quality Check',
    'category': 'Inventory',
    'version': '19.0.1.0.0',
    'description': "Gérer les contrôles de qualité lors de la réception des produits",
    'depends': ['stock', 'purchase', 'mail'],
    'data': [
        'security/quality_check_groups.xml',
        'security/ir.model.access.csv',
        # 'security/quality_check_record_rules.xml',
        
        'data/quality_check_sequence.xml',
        'views/quality_check_views.xml',
        'views/quality_check_menus.xml',
        'views/quality_check_template_views.xml',
        
        
    ],
    'installable': True,
    'license': 'LGPL-3',
    'author': 'Jonah'
}