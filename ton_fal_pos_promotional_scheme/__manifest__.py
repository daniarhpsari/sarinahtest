# -*- coding: utf-8 -*-
{
    'name': "Generate Poss Promotional Scheme",

    'summary': """
       Generate Pos Promotional Scheme
       Add product to tree POS Promo Scheme
       """,

    'description': """
        Generate Pos Promotional Scheme
        Add product to tree POS Promo Scheme
    """,

    'author': "tono.awar@gmail.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['fal_pos_promotional_scheme'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}