"""Single source of truth for the demo content.

build-content.py renders this into:
  * drafts/*.plain.html  (EDS-style markup for local `aem up --html-folder drafts`)
  * ../slf-eds-demo1-content/*.docx (Word documents to upload to SharePoint / Google Drive)

All people, phone numbers and emails are FICTIONAL.
"""

TEAM = 'Maple Ridge Wealth Partners'

ADVISORS = [
    {
        'slug': 'jordan-lee', 'name': 'Jordan Lee, CFP, CLU',
        'title': 'Senior Financial Advisor and Team Lead',
        'bio': 'Jordan founded the practice in 2009 and helps families and business owners '
               'turn big goals into simple, step-by-step plans.',
        'email': 'jordan.lee@example.com', 'phone': '403-555-0142', 'profile': True,
    },
    {
        'slug': 'priya-nair', 'name': 'Priya Nair, CFP',
        'title': 'Financial Advisor',
        'bio': 'Priya specializes in retirement income planning and making sure clients '
               'know exactly where their paycheque will come from after work.',
        'email': 'priya.nair@example.com', 'phone': '403-555-0157',
    },
    {
        'slug': 'marc-tremblay', 'name': 'Marc Tremblay, FMA',
        'title': 'Investment Advisor',
        'bio': 'Marc builds diversified portfolios and explains the "why" behind every '
               'recommendation in plain language. Bilingual in English and French.',
        'email': 'marc.tremblay@example.com', 'phone': '403-555-0163',
    },
    {
        'slug': 'aisha-okafor', 'name': 'Aisha Okafor, CHS',
        'title': 'Insurance and Benefits Specialist',
        'bio': 'Aisha helps clients protect what matters most with life, disability and '
               'critical illness coverage, and designs group benefits for small businesses.',
        'email': 'aisha.okafor@example.com', 'phone': '403-555-0178',
    },
    {
        'slug': 'daniel-whitford', 'name': 'Daniel Whitford',
        'title': 'Associate Advisor',
        'bio': 'Daniel supports client reviews and RESP and TFSA planning for young '
               'families getting started on their financial journey.',
        'email': 'daniel.whitford@example.com', 'phone': '403-555-0181',
    },
    {
        'slug': 'sofia-martinez', 'name': 'Sofia Martinez',
        'title': 'Advisor Assistant',
        'bio': 'Sofia is often your first hello. She coordinates meetings, paperwork and '
               'follow-ups so nothing falls through the cracks.',
        'email': 'sofia.martinez@example.com', 'phone': '403-555-0190',
    },
]


def avatar(slug, name):
    short = name.split(',')[0]
    return ('img', slug, f'Placeholder avatar for {short}')


def team_rows(people):
    rows = []
    for a in people:
        name = ('p', [('a', a['name'], f"/advisors/{a['slug']}")]) if a.get('profile') else ('p', [a['name']])
        rows.append([
            [avatar(a['slug'], a['name'])],
            [name],
            [('p', [a['title']])],
            [('p', [a['bio']])],
            [('p', [a['email']])],
            [('p', [a['phone']])],
        ])
    return rows


DISCLOSURE_LINK = [('p', [('a', 'https://main--slf-eds-demo1--michaelpereira78.aem.page/fragments/disclosure',
                           '/fragments/disclosure')])]

PAGES = {}

PAGES['index'] = {
    'metadata': {
        'Title': f'{TEAM} | Advisor Demo',
        'Description': 'Meet Maple Ridge Wealth Partners, a fictional Calgary advisor team built '
                       'to demonstrate Adobe Edge Delivery Services.',
    },
    'sections': [
        [
            ('block', 'Hero', [[[
                ('p', ['Calgary, Alberta']),
                ('h1', f'Meet {TEAM}'),
                ('p', ['Trusted expertise for every stage of life. For more than 15 years our team has '
                       'helped families, business owners and retirees build plans they understand, '
                       'with advice on investments, retirement, insurance and estate planning, all under one roof.']),
                ('p', [('b-a', 'Book a meeting', '/#contact-us')]),
                ('p', [('i-a', 'Meet our team', '/#our-team')]),
            ]]]),
        ],
        [
            ('h2', 'Our team'),
            ('p', ['Six people, one plan. Every client works with a lead advisor and is supported by '
                   'specialists in investments, insurance and client service.']),
            ('block', 'Team Cards', team_rows(ADVISORS)),
            ('block', 'Section Metadata', [[[('p', ['Style'])], [('p', ['Light'])]]]),
        ],
        [
            ('h2', 'Contact us'),
            ('p', ['Visit us downtown, call the main line or email the team directly. '
                   'We usually reply within one business day.']),
            ('block', 'Contact', [
                [[('p', ['Office'])], [('p', ['Maple Ridge Wealth Partners']), ('p', ['Suite 400, 100 Example Avenue SW']), ('p', ['Calgary, AB T2P 0A0'])]],
                [[('p', ['Main line'])], [('p', ['403-555-0100'])]],
                [[('p', ['Email'])], [('p', ['hello@example.com'])]],
                [[('p', ['Hours'])], [('p', ['Monday to Friday, 8:30 a.m. to 5 p.m.']), ('p', ['Evenings by appointment'])]],
                [[('p', ['Directions'])], [('p', [('a', 'Get directions', 'https://www.google.com/maps/search/?api=1&query=Calgary%2C+AB')])]],
            ]),
        ],
        DISCLOSURE_LINK,
    ],
}

PAGES['advisors/jordan-lee'] = {
    'metadata': {
        'Title': 'Jordan Lee, CFP, CLU | Maple Ridge Wealth Partners',
        'Description': 'Jordan Lee is a fictional senior financial advisor at Maple Ridge Wealth Partners, '
                       'used to demonstrate Adobe Edge Delivery Services.',
    },
    'sections': [
        [
            ('block', 'Hero (Profile)', [[
                [avatar('jordan-lee', 'Jordan Lee')],
                [
                    ('p', ['Senior Financial Advisor and Team Lead']),
                    ('h1', 'Jordan Lee, CFP, CLU'),
                    ('p', ['Helping Calgary families and business owners turn big goals into simple, '
                           'step-by-step plans since 2009.']),
                    ('p', [('b-a', 'Book a meeting', 'mailto:jordan.lee@example.com')]),
                    ('p', [('i-a', 'Back to our team', '/#our-team')]),
                ],
            ]]),
        ],
        [
            ('h2', 'About Jordan'),
            ('p', ['Jordan started Maple Ridge Wealth Partners with one idea: financial advice should be '
                   'easy to understand. Today Jordan leads a team of six and works closely with families, '
                   'incorporated professionals and small business owners across southern Alberta.']),
            ('p', ['Outside the office, Jordan coaches youth soccer, volunteers with a local food bank '
                   'and is always up for a weekend hike in Kananaskis.']),
            ('h3', 'How I can help'),
            ('ul', [
                ['Retirement and retirement income planning'],
                ['Investment planning and portfolio reviews'],
                ['Life, disability and critical illness insurance'],
                ['Business owner and succession planning'],
                ['Estate planning conversations, with your lawyer and accountant'],
            ]),
            ('h3', 'Credentials'),
            ('ul', [
                ['Certified Financial Planner (CFP)'],
                ['Chartered Life Underwriter (CLU)'],
                ['Licensed for life and health insurance in Alberta'],
            ]),
            ('block', 'Contact (Card)', [
                [[('p', ['Phone'])], [('p', ['403-555-0142'])]],
                [[('p', ['Email'])], [('p', ['jordan.lee@example.com'])]],
                [[('p', ['Office'])], [('p', ['Suite 400, 100 Example Avenue SW']), ('p', ['Calgary, AB T2P 0A0'])]],
                [[('p', ['Hours'])], [('p', ['Monday to Friday, 8:30 a.m. to 5 p.m.'])]],
                [[('p', ['Directions'])], [('p', [('a', 'Get directions', 'https://www.google.com/maps/search/?api=1&query=Calgary%2C+AB')])]],
            ]),
            ('block', 'Section Metadata', [[[('p', ['Style'])], [('p', ['Sidebar'])]]]),
        ],
        [
            ('h2', 'Working with Jordan'),
            ('p', ['Jordan is supported by the whole Maple Ridge team.']),
            ('block', 'Team Cards', team_rows([a for a in ADVISORS if a['slug'] in ('priya-nair', 'aisha-okafor', 'sofia-martinez')])),
            ('block', 'Section Metadata', [[[('p', ['Style'])], [('p', ['Light'])]]]),
        ],
        DISCLOSURE_LINK,
    ],
}

PAGES['fragments/disclosure'] = {
    'metadata': {},
    'sections': [
        [
            ('block', 'Disclosure', [[[
                ('h2', 'Important information'),
                ('p', ['This is a demonstration website. Maple Ridge Wealth Partners and every person, phone '
                       'number and email address shown are fictional. This site is not affiliated with, '
                       'endorsed by or operated by Sun Life or any of its affiliates.']),
                ('p', ['In a real advisor site, this box would hold the regulatory disclosure, for example the '
                       'legal names of the advisors\u2019 dealer and insurance distributor and the products each '
                       'person is licensed to offer. It is authored once as a shared fragment, so Compliance '
                       'can update the wording in one place and every advisor site picks it up on the next publish.']),
            ]]]),
        ],
    ],
}

PAGES['nav'] = {
    'metadata': {},
    'sections': [
        [('p', [('a', 'Advisor Demo', '/')])],
        [('ul', [
            [('a', 'Home', '/')],
            [('a', 'Our team', '/#our-team')],
            [('a', 'Contact', '/#contact-us')],
        ])],
        [('p', [('b-a', 'Book a meeting', '/#contact-us')])],
    ],
}

PAGES['footer'] = {
    'metadata': {},
    'sections': [
        [
            ('p', [('a', 'Advisor Demo', '/')]),
            ('p', ['Maple Ridge Wealth Partners, Suite 400, 100 Example Avenue SW, Calgary, AB T2P 0A0']),
        ],
        [('ul', [
            [('a', 'Home', '/')],
            [('a', 'Our team', '/#our-team')],
            [('a', 'Jordan Lee', '/advisors/jordan-lee')],
            [('a', 'Contact', '/#contact-us')],
        ])],
        [
            ('p', ['Demo, not affiliated with Sun Life']),
            ('p', ['Built on Adobe Edge Delivery Services. All names and contact details are fictional.']),
        ],
    ],
}
