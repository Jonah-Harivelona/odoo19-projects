{
    'name': 'Quality Check',
    'category': 'Inventory',
    'version': '19.0.1.0.0',
    'description': "Gérer les contrôles de qualité lors de la réception des produits",
    'depends': ['stock', 'purchase', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        #'security/quality_check_groups.xml',
        # 'security/quality_check_record_rules.xml',
        
        'data/quality_check_sequence.xml'
        
    ],
    'installable': True,
    'license': 'LGPL-3',
    'author': 'Jonah'
}