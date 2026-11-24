"""Single source of truth for the demo content.

build-content.py renders this into:
  * drafts/*.plain.html  (EDS-style markup for local `aem up --html-folder drafts`)
  * ../slf-eds-demo1-content/*.docx (Word documents to upload to SharePoint / Google Drive)

All people, phone numbers and emails are FICTIONAL.
"""

TEAM = 'Maple Ridge Wealth Partners'
PREVIEW_ORIGIN = 'https://main--slf-eds-demo1--michaelpereira78.aem.page'

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


def frag(path):
    """A link to an approved-content fragment. On its own line it is embedded automatically."""
    return ('p', [('a', PREVIEW_ORIGIN + path, path)])


DISCLOSURE_LINK = [frag('/fragments/disclosure')]


def compliance(status, by='', date='', cid=''):
    meta = {'Compliance Status': status}
    if by:
        meta['Approved By' if status == 'Approved' else 'Reviewer'] = by
    if date:
        meta['Approval Date' if status == 'Approved' else 'Review Date'] = date
    if cid:
        meta['Compliance ID'] = cid
    return meta

PAGES = {}

PAGES['index'] = {
    'metadata': {
        'Title': f'{TEAM} | Advisor Demo',
        'Description': 'Meet Maple Ridge Wealth Partners, a fictional Calgary advisor team built '
                       'to demonstrate Adobe Edge Delivery Services.',
        'Template': 'advisor-team',
        'Theme': 'Forest',
        **compliance('Approved', 'R. Castillo, Compliance', '2026-11-20', 'CR-2026-0412'),
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
        'Theme': 'Forest',
        **compliance('Approved', 'R. Castillo, Compliance', '2026-11-20', 'CR-2026-0413'),
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
                ('p', ['This is a demonstration website. Every firm, person, phone number and email address '
                       'shown is fictional. This site is not affiliated with, endorsed by or operated by '
                       'Sun Life or any of its affiliates.']),
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
            [('a', 'Platform demo', '/demo')],
        ])],
        [
            ('p', ['Demo, not affiliated with Sun Life']),
            ('p', ['Built on Adobe Edge Delivery Services. All names and contact details are fictional.']),
        ],
    ],
}


# =====================================================================
# PLATFORM DEMO: the seven business-user capabilities
# =====================================================================
def meta(rows):
    return ('block', 'Metadata', [[[('p', [k])], [('p', [v])]] for k, v in rows.items()])


def section_style(style):
    return ('block', 'Section Metadata', [[[('p', ['Style'])], [('p', [style])]]])


def link_p(text, href, kind='a'):
    return ('p', [(kind, text, href)])


# ---------------------------------------------------------------- second and third fictional firms
HARBOURVIEW = [
    {'slug': 'grace-macleod', 'name': 'Grace MacLeod, CFP', 'title': 'Senior Financial Advisor',
     'bio': 'Grace has helped Halifax families plan for retirement, education and everything in '
            'between for more than 20 years.',
     'email': 'grace.macleod@example.com', 'phone': '902-555-0114'},
    {'slug': 'omar-haddad', 'name': 'Omar Haddad, CIM', 'title': 'Investment Advisor',
     'bio': 'Omar builds portfolios for business owners and professionals, with a focus on '
            'tax-efficient investing and clear quarterly reviews.',
     'email': 'omar.haddad@example.com', 'phone': '902-555-0127'},
    {'slug': 'liam-obrien', 'name': 'Liam O\u2019Brien', 'title': 'Associate Advisor',
     'bio': 'Liam works with first-time investors and young families on TFSAs, RESPs and '
            'their first insurance plan.',
     'email': 'liam.obrien@example.com', 'phone': '902-555-0139'},
]

ELENA = {'slug': 'elena-park', 'name': 'Elena Park, CFP, CLU'}

PAGES['harbourview/index'] = {
    'metadata': {
        'Title': 'Harbourview Financial Group | Advisor Demo',
        'Description': 'Harbourview Financial Group is a fictional Halifax advisor team, generated from the '
                       'approved Advisor team template with the Harbour brand theme.',
        'Template': 'advisor-team',
        'Theme': 'Harbour',
        'Nav': '/harbourview/nav',
        'Footer': '/harbourview/footer',
        **compliance('Pending review', 'R. Castillo, Compliance', '2026-11-23', 'CR-2026-0431'),
    },
    'sections': [
        [('block', 'Hero', [[[
            ('p', ['Halifax, Nova Scotia']),
            ('h1', 'Planning that sails through every season'),
            ('p', ['Harbourview Financial Group is a three-person team helping Nova Scotia families '
                   'and business owners save, invest and protect what matters, with one clear plan.']),
            link_p('Book a conversation', '/harbourview/#contact-us', 'b-a'),
            link_p('Meet the team', '/harbourview/#our-team', 'i-a'),
        ]]])],
        [
            ('h2', 'Our team'),
            ('p', ['Three advisors, one shared plan for every client.']),
            ('block', 'Team Cards', team_rows(HARBOURVIEW)),
            section_style('Light'),
        ],
        [
            ('h2', 'How we help'),
            ('p', ['The product descriptions below are approved content. They are shared with every '
                   'advisor site, so Compliance reviews them once.']),
            frag('/fragments/products/retirement-income'),
            frag('/fragments/products/tfsa-rrsp'),
        ],
        [
            ('h2', 'Contact us'),
            ('block', 'Contact', [
                [[('p', ['Office'])], [('p', ['Harbourview Financial Group']), ('p', ['200 Example Street, Suite 12']), ('p', ['Halifax, NS B3J 0A0'])]],
                [[('p', ['Main line'])], [('p', ['902-555-0100'])]],
                [[('p', ['Email'])], [('p', ['hello.harbourview@example.com'])]],
                [[('p', ['Hours'])], [('p', ['Monday to Friday, 9 a.m. to 5 p.m.'])]],
            ]),
        ],
        DISCLOSURE_LINK,
    ],
}

PAGES['harbourview/nav'] = {
    'metadata': {},
    'sections': [
        [('p', [('a', 'Harbourview', '/harbourview/')])],
        [('ul', [
            [('a', 'Home', '/harbourview/')],
            [('a', 'Our team', '/harbourview/#our-team')],
            [('a', 'Contact', '/harbourview/#contact-us')],
        ])],
        [link_p('Book a conversation', '/harbourview/#contact-us', 'b-a')],
    ],
}

PAGES['harbourview/footer'] = {
    'metadata': {},
    'sections': [
        [link_p('Harbourview', '/harbourview/'),
         ('p', ['Harbourview Financial Group, 200 Example Street, Suite 12, Halifax, NS B3J 0A0'])],
        [('ul', [[('a', 'Home', '/harbourview/')], [('a', 'Our team', '/harbourview/#our-team')],
                 [('a', 'Platform demo', '/demo')]])],
        [('p', ['Demo, not affiliated with Sun Life']),
         ('p', ['Generated from the Advisor team template with the Harbour theme. All names are fictional.'])],
    ],
}

PAGES['northstar/index'] = {
    'metadata': {
        'Title': 'Elena Park, CFP, CLU | Northstar Planning',
        'Description': 'Northstar Planning is a fictional one-advisor practice in Victoria, generated from the '
                       'approved Solo advisor template with the Slate brand theme.',
        'Template': 'solo-advisor',
        'Theme': 'Slate',
        'Nav': '/northstar/nav',
        'Footer': '/northstar/footer',
        **compliance('Changes requested', 'R. Castillo, Compliance', '2026-11-22', 'CR-2026-0428'),
    },
    'sections': [
        [('block', 'Hero (Profile)', [[
            [avatar('elena-park', 'Elena Park')],
            [
                ('p', ['Northstar Planning, Victoria, BC']),
                ('h1', 'Elena Park, CFP, CLU'),
                ('p', ['Independent advice for professionals and retirees on Vancouver Island, '
                       'from your first TFSA to your retirement paycheque.']),
                link_p('Book a meeting', 'mailto:elena.park@example.com', 'b-a'),
                link_p('How I work', '/northstar/#how-i-work', 'i-a'),
            ],
        ]])],
        [
            ('h2', 'How I work'),
            ('p', ['Every relationship starts with a one-hour conversation about what you want your money to do. '
                   'From there I build a written plan, review it with you every year and adjust it when life changes.']),
            ('h3', 'Services'),
            ('ul', [['Retirement income planning'], ['Investment and portfolio reviews'],
                    ['Life, disability and critical illness insurance'], ['Estate planning conversations']]),
            frag('/fragments/products/insurance-protection'),
            ('block', 'Contact (Card)', [
                [[('p', ['Phone'])], [('p', ['250-555-0175'])]],
                [[('p', ['Email'])], [('p', ['elena.park@example.com'])]],
                [[('p', ['Office'])], [('p', ['8 Example Lane']), ('p', ['Victoria, BC V8W 0A0'])]],
            ]),
            section_style('Sidebar'),
        ],
        [frag('/fragments/cta/book-a-review')],
        DISCLOSURE_LINK,
    ],
}

PAGES['northstar/nav'] = {
    'metadata': {},
    'sections': [
        [link_p('Northstar Planning', '/northstar/')],
        [('ul', [[('a', 'Home', '/northstar/')], [('a', 'How I work', '/northstar/#how-i-work')]])],
        [link_p('Book a meeting', 'mailto:elena.park@example.com', 'b-a')],
    ],
}

PAGES['northstar/footer'] = {
    'metadata': {},
    'sections': [
        [link_p('Northstar Planning', '/northstar/'), ('p', ['8 Example Lane, Victoria, BC V8W 0A0'])],
        [('ul', [[('a', 'Home', '/northstar/')], [('a', 'Platform demo', '/demo')]])],
        [('p', ['Demo, not affiliated with Sun Life']),
         ('p', ['Generated from the Solo advisor template with the Slate theme. All names are fictional.'])],
    ],
}

# ---------------------------------------------------------------- campaign landing page (Campaign template)
PAGES['campaigns/retirement-checkup'] = {
    'metadata': {
        'Title': 'Free retirement check-up | Maple Ridge Wealth Partners',
        'Description': 'A fictional campaign landing page built from the approved Campaign template.',
        'Template': 'campaign',
        'Theme': 'Forest',
        **compliance('Pending review', 'R. Castillo, Compliance', '2026-11-24', 'CR-2026-0435'),
    },
    'sections': [
        [('block', 'Hero (Centered)', [[[
            ('p', ['Limited spots this December']),
            ('h1', 'Your free 30-minute retirement check-up'),
            ('p', ['Sit down with a Maple Ridge advisor and leave with three clear answers: when you can retire, '
                   'what your income will look like, and what to do next.']),
            link_p('Book my check-up', 'mailto:hello@example.com?subject=Retirement%20check-up', 'b-a'),
        ]]])],
        [
            ('h2', 'What we will cover'),
            ('block', 'Columns', [[
                [('h3', 'Your timeline'), ('p', ['When you can stop working, and what has to be true for that to happen.'])],
                [('h3', 'Your income'), ('p', ['Where each retirement paycheque comes from: pensions, RRIF, TFSA and government benefits.'])],
                [('h3', 'Your next step'), ('p', ['One or two practical moves to make this year, in plain language.'])],
            ]]),
            section_style('Centered'),
        ],
        [frag('/fragments/products/retirement-income')],
        [frag('/fragments/cta/book-a-review')],
        DISCLOSURE_LINK,
    ],
}

# ---------------------------------------------------------------- approved content (fragments)
def callout(name, body, approval, variant=''):
    title = f'Callout ({variant})' if variant else 'Callout'
    return {'metadata': {}, 'sections': [[('block', title, [[body], [[('p', ['Approved'])], [('p', [approval])]]])]]}


APPROVED = [
    ('Retirement income planning', '/fragments/products/retirement-income', 'AC-2026-031',
     'Approved product description for retirement income planning.'),
    ('TFSA and RRSP savings', '/fragments/products/tfsa-rrsp', 'AC-2026-018',
     'Approved plain-language comparison of TFSAs and RRSPs.'),
    ('Insurance protection', '/fragments/products/insurance-protection', 'AC-2026-022',
     'Approved description of life, disability and critical illness insurance.'),
    ('Book a review (call to action)', '/fragments/cta/book-a-review', 'AC-2026-040',
     'Approved call to action with compliant wording, for the end of any page.'),
    ('Regulatory disclosure', '/fragments/disclosure', 'AC-2026-001',
     'Required on every advisor page. Owned by Compliance.'),
]

PAGES['fragments/products/retirement-income'] = callout('Retirement income', [
    ('h3', 'Retirement income planning'),
    ('p', ['We help you turn your savings, pensions and government benefits into a steady retirement paycheque, '
           'and review the plan with you every year. Income amounts depend on your savings, investment returns '
           'and the choices you make; they are not guaranteed.']),
], 'AC-2026-031 \u00b7 Compliance \u00b7 Nov 2026')

PAGES['fragments/products/tfsa-rrsp'] = callout('TFSA and RRSP', [
    ('h3', 'TFSA or RRSP: which comes first?'),
    ('p', ['An RRSP lowers your taxes today and is taxed when you withdraw. A TFSA grows tax-free and withdrawals '
           'are not taxed. The right mix depends on your income now and later; your advisor will show you the '
           'numbers for your situation.']),
], 'AC-2026-018 \u00b7 Compliance \u00b7 Oct 2026')

PAGES['fragments/products/insurance-protection'] = callout('Insurance', [
    ('h3', 'Protecting your income and family'),
    ('p', ['Life, disability and critical illness insurance can replace income when you need it most. '
           'Coverage, exclusions and premiums depend on the policy and your health; read the policy contract '
           'for full details.']),
], 'AC-2026-022 \u00b7 Compliance \u00b7 Sep 2026')

PAGES['fragments/cta/book-a-review'] = callout('Book a review', [
    ('h2', 'Ready for a second opinion on your plan?'),
    ('p', ['Book a no-obligation review. We will look at where you are today and suggest next steps, '
           'with no pressure to buy anything.']),
    link_p('Book a review', 'mailto:hello@example.com?subject=Plan%20review', 'b-a'),
], 'AC-2026-040 \u00b7 Compliance \u00b7 Nov 2026', 'CTA')

PAGES['fragments/disclosure']['sections'][0][0][2].append(
    [[('p', ['Approved'])], [('p', ['AC-2026-001 \u00b7 Compliance \u00b7 Nov 2026'])]])

PAGES['approved-content'] = {
    'metadata': {
        'Title': 'Approved content library | Advisor Demo',
        'Description': 'Pre-approved product descriptions, calls to action and disclosures advisors can reuse.',
        'Theme': 'Forest',
        'Robots': 'noindex',
    },
    'sections': [
        [('block', 'Hero (Light)', [[[
            ('p', ['Capability 6: approved content']),
            ('h1', 'Approved content library'),
            ('p', ['Compliance writes and approves these blocks once. Advisors reuse them by pasting a link; '
                   'they cannot change the wording. When Compliance updates a block, every site that uses it '
                   'shows the new version on its next publish.']),
        ]]])],
        [
            ('h2', 'How advisors use it'),
            ('ol', [
                ['In the document, click Sidekick, then Library, then Approved content.'],
                ['Click Copy link next to the block you need.'],
                ['Paste it on its own line in your page and click Preview. The approved text appears.'],
            ]),
            ('p', ['No Sidekick handy? Type the link text shown under each block below on its own line '
                   'and make it a link. Both ways give the same result.']),
            section_style('Narrow'),
        ],
    ] + [
        [('h3', f'{name}'), ('p', [('i', f'{desc} Approval {aid}. Link to paste: {PREVIEW_ORIGIN}{path}')]), frag(path),
         section_style('Light' if i % 2 == 0 else 'Narrow')]
        for i, (name, path, aid, desc) in enumerate(APPROVED)
    ],
}

# ---------------------------------------------------------------- demo hub
CAPS = [
    ('1. Generate a new website', 'Fill in a short request form and pick a theme and template. The platform '
     'team turns it into a ready-to-edit folder of documents in minutes.', 'Open the site request form', '/new-site'),
    ('2. Make content changes', 'Edit the Word or Google Doc, click Preview, then Publish. Live worldwide in seconds.',
     'Open the Maple Ridge site', '/'),
    ('3. Make minor layout changes', 'Change a section style (Light, Dark, Centered, Sidebar) or a block '
     'variant by typing one word in the document.', 'See the layout gallery', '/layouts'),
    ('4. Use approved templates', 'Start every page from an approved template: Advisor team, Solo advisor '
     'or Campaign. Developers can add new ones without touching existing sites.', 'Browse approved templates', '/templates'),
    ('5. Apply a brand theme', 'Each site picks a theme with one metadata value. Same platform, different look.',
     'See Harbourview (Harbour theme)', '/harbourview/'),
    ('6. Reuse approved content', 'Product descriptions, calls to action and disclosures are written once by '
     'Compliance and reused everywhere.', 'Open the approved content library', '/approved-content'),
    ('7. Compliance review and approval', 'Authors request a review; Compliance approves or sends back changes. '
     'Only approvers can publish.', 'Open the compliance queue', '/compliance'),
]

PAGES['demo'] = {
    'metadata': {
        'Title': 'Platform demo | Advisor Demo',
        'Description': 'Seven things business users can do on the advisor web platform, without a developer.',
        'Theme': 'Forest',
        'Robots': 'noindex',
    },
    'sections': [
        [('block', 'Hero (Light, Centered)', [[[
            ('p', ['Advisor web platform demo']),
            ('h1', 'Seven things business users can do without a developer'),
            ('p', ['Everything on this demo is authored in ordinary documents and runs on Adobe Edge Delivery '
                   'Services. All firms, people and contact details are fictional.']),
        ]]])],
        [('h2', 'The seven capabilities'), ('block', 'Cards (Capabilities)', [
            [[('h3', t), ('p', [d]), link_p(lt, href)]] for t, d, lt, href in CAPS
        ])],
        [
            ('h2', 'Three sites, one platform'),
            ('p', ['Same code, same blocks, three different brands and templates.']),
            ('block', 'Cards (Sites)', [
                [[('h3', 'Maple Ridge Wealth Partners'), ('p', ['Calgary team site. Template: Advisor team. Theme: Forest.']), link_p('Open site', '/')]],
                [[('h3', 'Harbourview Financial Group'), ('p', ['Halifax team site. Template: Advisor team. Theme: Harbour.']), link_p('Open site', '/harbourview/')]],
                [[('h3', 'Northstar Planning'), ('p', ['Victoria solo practice. Template: Solo advisor. Theme: Slate.']), link_p('Open site', '/northstar/')]],
            ]),
            section_style('Light'),
        ],
    ],
}

# ---------------------------------------------------------------- templates gallery
TEMPLATES = [
    ('Advisor team', 'advisor-team', 'Teams of two or more advisors: hero, team cards, services, contact and disclosure.',
     '/', '/tools/sidekick/templates/advisor-team'),
    ('Solo advisor', 'solo-advisor', 'One-advisor practices: large portrait, story, services and a sticky contact card.',
     '/northstar/', '/tools/sidekick/templates/solo-advisor'),
    ('Campaign', 'campaign', 'Single-purpose landing pages: focused header, centred hero, one call to action, '
     'sticky booking button on phones.', '/campaigns/retirement-checkup', '/tools/sidekick/templates/campaign'),
]

PAGES['templates'] = {
    'metadata': {
        'Title': 'Approved templates | Advisor Demo',
        'Description': 'The approved page templates advisors can start from.',
        'Theme': 'Forest',
        'Robots': 'noindex',
    },
    'sections': [
        [('block', 'Hero (Light)', [[[
            ('p', ['Capability 4: templates']),
            ('h1', 'Approved templates'),
            ('p', ['Every page starts from a template that Brand and Compliance have already approved. '
                   'Authors copy a starter document; the Template value in its metadata controls the layout.']),
        ]]])],
        [('h2', 'Choose a template'), ('block', 'Cards (Templates)', [
            [[('h3', name), ('p', [desc]), ('p', [('b', 'Template value: '), key]),
              link_p('See an example', ex), link_p('Open the starter document', start)]]
            for name, key, desc, ex, start in TEMPLATES
        ])],
        [
            ('h2', 'Starting a page from a template'),
            ('ol', [
                ['Open the Approved templates folder in Drive (tools/sidekick/templates).'],
                ['Right-click the template and choose Make a copy, then move the copy to your site folder and rename it.'],
                ['Replace the text in square brackets, then click Preview in Sidekick.'],
                ['Or, inside any document: Sidekick, Library, Blocks, then pick a template and paste it.'],
            ]),
            ('h2', 'Adding a new approved template'),
            ('p', ['A developer adds a folder under templates/ in the code (a CSS file, and a JavaScript file if '
                   'needed), registers its name, and adds a starter document. Existing sites are not affected '
                   'until an author chooses the new template. See ADD-A-TEMPLATE.md in the repository.']),
            section_style('Narrow'),
        ],
    ],
}

# ---------------------------------------------------------------- layout gallery
PAGES['layouts'] = {
    'metadata': {
        'Title': 'Layout gallery | Advisor Demo',
        'Description': 'Section styles and block variants authors can switch by typing one word.',
        'Theme': 'Forest',
        'Robots': 'noindex',
    },
    'sections': [
        [('block', 'Hero (Light)', [[[
            ('p', ['Capability 3: layout changes']),
            ('h1', 'Layout gallery'),
            ('p', ['Each band below is the same kind of content with a different style. To change one, edit the '
                   'Style cell in that section\u2019s Section Metadata table, then Preview. No developer needed.']),
        ]]])],
        [('h2', 'Default'), ('p', ['No Section Metadata. White background, left-aligned text, full width.'])],
        [('h2', 'Style: Light'), ('p', ['A soft tinted band. Good for team lists and contact details.']), section_style('Light')],
        [('h2', 'Style: Dark'), ('p', ['The brand colour as a band, for a statement or call to action.']),
         link_p('A button on a dark band', '/demo', 'i-a'), section_style('Dark')],
        [('h2', 'Style: Accent'), ('p', ['A warm accent band that follows the site\u2019s theme.']), section_style('Accent')],
        [('h2', 'Style: Centered'), ('p', ['Centred headings and text, for short messages and campaign pages.']),
         section_style('Centered')],
        [('h2', 'Style: Dark, Centered'), ('p', ['Styles combine: separate them with a comma.']),
         link_p('Book a meeting', '/#contact-us', 'b-a'), section_style('Dark, Centered')],
        [('h2', 'Style: Narrow'), ('p', ['A reading width of about 70 characters for long articles and bios. '
                                         'Long lines are harder to read, so this style keeps them short.']),
         section_style('Narrow')],
        [
            ('h2', 'Style: Sidebar'),
            ('p', ['On a desktop, the last block in the section (here, a contact card) moves to a sticky column '
                   'on the right. On a phone, it stacks underneath.']),
            ('p', ['Use it for advisor profiles and service pages.']),
            ('block', 'Contact (Card)', [
                [[('p', ['Phone'])], [('p', ['403-555-0100'])]],
                [[('p', ['Email'])], [('p', ['hello@example.com'])]],
            ]),
            section_style('Sidebar'),
        ],
        [
            ('h2', 'Block variants'),
            ('p', ['Blocks change look with a word in brackets after the block name: Hero, Hero (Light), '
                   'Hero (Centered), Hero (Profile); Contact or Contact (Card); Callout or Callout (CTA); '
                   'Cards or Cards (Capabilities).']),
            ('block', 'Columns', [[
                [('h3', 'Columns'), ('p', ['Put content side by side by adding cells to a Columns table.'])],
                [('h3', 'Two or three'), ('p', ['On phones, columns stack automatically.'])],
                [('h3', 'Any content'), ('p', ['Text, images, lists and buttons all work inside columns.'])],
            ]]),
            section_style('Light'),
        ],
    ],
}

# ---------------------------------------------------------------- new site request (capability 1)
PAGES['new-site'] = {
    'metadata': {
        'Title': 'Request a new advisor site | Advisor Demo',
        'Description': 'Request a new advisor website: pick a brand theme and an approved template.',
        'Theme': 'Forest',
        'Robots': 'noindex',
    },
    'sections': [
        [('block', 'Hero (Light)', [[[
            ('p', ['Capability 1: new websites']),
            ('h1', 'Request a new advisor site'),
            ('p', ['Answer five questions. Pick a theme and watch this page change to match. '
                   'The platform team generates the site\u2019s starter documents from your answers.']),
        ]]])],
        [('block', 'Site Request', [[[('p', ['Form'])]]])],
        [
            ('h2', 'What happens after you submit'),
            ('ol', [
                ['The platform team runs the site generator with your answers. It creates the home page, '
                 'navigation and footer documents, already set to your theme and template.'],
                ['They create a Drive (or SharePoint) folder for the site, share it with you, and upload the documents.'],
                ['They create the site with one call to the platform\u2019s admin service. No new code, no new hosting.'],
                ['You edit the documents, Preview, request a compliance review, and Compliance publishes.'],
            ]),
            ('p', ['Examples generated this way: ', ('a', 'Harbourview Financial Group', '/harbourview/'),
                   ' and ', ('a', 'Northstar Planning', '/northstar/'), '.']),
            section_style('Narrow'),
        ],
    ],
}

# ---------------------------------------------------------------- compliance queue (capability 7)
PAGES['compliance'] = {
    'metadata': {
        'Title': 'Compliance review queue | Advisor Demo',
        'Description': 'Review, approve or send back advisor page changes before they are published.',
        'Theme': 'Forest',
        'Robots': 'noindex',
    },
    'sections': [
        [('block', 'Hero (Light)', [[[
            ('p', ['Capability 7: compliance review']),
            ('h1', 'Compliance review queue'),
            ('p', ['Pages waiting for review, with their preview links. Approving a page lets it be published; '
                   'requesting changes sends it back to the advisor with a note.']),
        ]]])],
        [('block', 'Compliance Queue', [[[('p', ['Review queue'])]]])],
        [
            ('h2', 'How it works in production'),
            ('ol', [
                ['The advisor edits the page and clicks Preview. The preview shows a status bar: Not yet approved.'],
                ['The advisor clicks Request review (in the status bar or in Sidekick). Using Sidekick\u2019s '
                 'Review button, the page goes into a review snapshot, which locks that exact version.'],
                ['Compliance opens the review link, checks the page and clicks Approve or Reject in the snapshot '
                 'tool. Approve publishes that locked version; Reject unlocks it with notes for the advisor.'],
                ['Only people in the Compliance publisher role can publish. Advisors can edit and preview, '
                 'but the Publish button is not available to them.'],
            ]),
            ('p', [('i', 'In this demo, Approve and Request changes are saved in this browser only, so you can '
                         'click through the flow safely. Reset the demo with the button above the queue.')]),
            section_style('Narrow'),
        ],
    ],
}

# ---------------------------------------------------------------- approved templates (starter docs for the Library)
def library_meta(name, desc, kind='template'):
    rows = [[[('p', ['name'])], [('p', [name])]], [[('p', ['description'])], [('p', [desc])]]]
    if kind:
        rows.append([[('p', ['type'])], [('p', [kind])]])
    return [('block', 'Library Metadata', rows)]


PAGES['tools/sidekick/templates/advisor-team'] = {
    'metadata': {'Title': '[Firm name] | [City]', 'Description': '[One sentence about the team]',
                 'Template': 'advisor-team', 'Theme': 'Forest', 'Compliance Status': 'Draft', 'Robots': 'noindex'},
    'sections': [
        library_meta('Advisor team', 'Team home page: hero, team cards, contact, disclosure.'),
        [('block', 'Hero', [[[
            ('p', ['[City, Province]']),
            ('h1', 'Meet [Firm name]'),
            ('p', ['[Two or three sentences about who you help and how.]']),
            link_p('Book a meeting', '/#contact-us', 'b-a'),
        ]]])],
        [('h2', 'Our team'), ('p', ['[One sentence about the team.]']),
         ('block', 'Team Cards', team_rows([ADVISORS[0], ADVISORS[1]])), section_style('Light')],
        [('h2', 'Contact us'), ('block', 'Contact', [
            [[('p', ['Office'])], [('p', ['[Street address]']), ('p', ['[City, Province, Postal code]'])]],
            [[('p', ['Main line'])], [('p', ['[555 number]'])]],
            [[('p', ['Email'])], [('p', ['[team@example.com]'])]],
        ])],
        DISCLOSURE_LINK,
    ],
}

PAGES['tools/sidekick/templates/solo-advisor'] = {
    'metadata': {'Title': '[Advisor name] | [Practice name]', 'Description': '[One sentence about the advisor]',
                 'Template': 'solo-advisor', 'Theme': 'Slate', 'Compliance Status': 'Draft', 'Robots': 'noindex'},
    'sections': [
        library_meta('Solo advisor', 'One-advisor home page: portrait hero, story, services, sticky contact card.'),
        [('block', 'Hero (Profile)', [[
            [avatar('elena-park', 'Advisor')],
            [('p', ['[Practice name, City]']), ('h1', '[Advisor name, credentials]'),
             ('p', ['[Who you help, in one sentence.]']), link_p('Book a meeting', 'mailto:advisor@example.com', 'b-a')],
        ]])],
        [('h2', 'How I work'), ('p', ['[Your story and approach.]']),
         ('ul', [['[Service one]'], ['[Service two]'], ['[Service three]']]),
         ('block', 'Contact (Card)', [[[('p', ['Phone'])], [('p', ['[555 number]'])]],
                                      [[('p', ['Email'])], [('p', ['[advisor@example.com]'])]]]),
         section_style('Sidebar')],
        DISCLOSURE_LINK,
    ],
}

PAGES['tools/sidekick/templates/campaign'] = {
    'metadata': {'Title': '[Campaign name] | [Firm name]', 'Description': '[One sentence offer]',
                 'Template': 'campaign', 'Theme': 'Forest', 'Compliance Status': 'Draft', 'Robots': 'noindex'},
    'sections': [
        library_meta('Campaign', 'Landing page: centred hero, three benefits, approved call to action.'),
        [('block', 'Hero (Centered)', [[[
            ('p', ['[Short eyebrow]']), ('h1', '[The offer in one line]'),
            ('p', ['[Why it matters, in two sentences.]']), link_p('Book now', 'mailto:hello@example.com', 'b-a'),
        ]]])],
        [('h2', 'What you get'), ('block', 'Columns', [[
            [('h3', '[Benefit one]'), ('p', ['[One sentence.]'])],
            [('h3', '[Benefit two]'), ('p', ['[One sentence.]'])],
            [('h3', '[Benefit three]'), ('p', ['[One sentence.]'])],
        ]]), section_style('Centered')],
        [frag('/fragments/cta/book-a-review')],
        DISCLOSURE_LINK,
    ],
}

# ---------------------------------------------------------------- block library docs (Sidekick Library > Blocks)
PAGES['tools/sidekick/blocks/hero'] = {
    'metadata': {'Robots': 'noindex'},
    'sections': [
        [('block', 'Hero', [[[('p', ['Eyebrow']), ('h1', 'Heading'), ('p', ['Intro text.']),
                              link_p('Primary button', '/', 'b-a'), link_p('Secondary button', '/', 'i-a')]]]),
         ('block', 'Library Metadata', [[[('p', ['name'])], [('p', ['Hero'])]],
                                        [[('p', ['description'])], [('p', ['Brand-colour hero band.'])]]])],
        [('block', 'Hero (Light, Centered)', [[[('p', ['Eyebrow']), ('h1', 'Heading'), ('p', ['Intro text.'])]]]),
         ('block', 'Library Metadata', [[[('p', ['name'])], [('p', ['Hero (Light, Centered)'])]],
                                        [[('p', ['description'])], [('p', ['Pale, centred hero for landing pages.'])]]])],
    ],
}

PAGES['tools/sidekick/blocks/callout'] = {
    'metadata': {'Robots': 'noindex'},
    'sections': [
        [('block', 'Callout', [[[('h3', 'Heading'), ('p', ['Text.'])]]]),
         ('block', 'Library Metadata', [[[('p', ['name'])], [('p', ['Callout'])]],
                                        [[('p', ['description'])], [('p', ['Highlighted box. Approved content uses this block.'])]]])],
        [('block', 'Callout (CTA)', [[[('h2', 'Heading'), ('p', ['Text.']), link_p('Button', '/', 'b-a')]]]),
         ('block', 'Library Metadata', [[[('p', ['name'])], [('p', ['Callout (CTA)'])]],
                                        [[('p', ['description'])], [('p', ['Brand-colour call to action.'])]]])],
    ],
}

PAGES['tools/sidekick/blocks/contact'] = {
    'metadata': {'Robots': 'noindex'},
    'sections': [
        [('block', 'Contact (Card)', [[[('p', ['Phone'])], [('p', ['403-555-0100'])]],
                                      [[('p', ['Email'])], [('p', ['hello@example.com'])]]]),
         ('block', 'Library Metadata', [[[('p', ['name'])], [('p', ['Contact (Card)'])]],
                                        [[('p', ['description'])], [('p', ['Compact contact card for sidebars.'])]]])],
    ],
}

# ---------------------------------------------------------------- spreadsheets
SHEETS = {
    'tools/sidekick/library': {
        'helix-blocks': [
            {'name': 'Hero', 'path': '/tools/sidekick/blocks/hero'},
            {'name': 'Callout', 'path': '/tools/sidekick/blocks/callout'},
            {'name': 'Contact', 'path': '/tools/sidekick/blocks/contact'},
            {'name': 'Template: Advisor team', 'path': '/tools/sidekick/templates/advisor-team'},
            {'name': 'Template: Solo advisor', 'path': '/tools/sidekick/templates/solo-advisor'},
            {'name': 'Template: Campaign', 'path': '/tools/sidekick/templates/campaign'},
        ],
        'helix-approved-content': [
            {'name': name, 'path': path, 'approval': aid, 'description': desc}
            for name, path, aid, desc in APPROVED
        ],
    },
    'compliance-queue': {
        'Sheet1': [
            {'Page': '/campaigns/retirement-checkup', 'Title': 'Free retirement check-up (campaign)',
             'Site': 'Maple Ridge Wealth Partners', 'Submitted By': 'Priya Nair', 'Submitted': '2026-11-24',
             'Status': 'Pending review', 'Reviewer': 'R. Castillo', 'Decision Date': '',
             'Notes': 'New December campaign. Uses approved retirement income wording.', 'Snapshot': 'retirement-checkup-2026'},
            {'Page': '/harbourview/', 'Title': 'Harbourview Financial Group home',
             'Site': 'Harbourview Financial Group', 'Submitted By': 'Grace MacLeod', 'Submitted': '2026-11-23',
             'Status': 'Pending review', 'Reviewer': 'R. Castillo', 'Decision Date': '',
             'Notes': 'New site launch.', 'Snapshot': 'harbourview-launch'},
            {'Page': '/northstar/', 'Title': 'Northstar Planning home', 'Site': 'Northstar Planning',
             'Submitted By': 'Elena Park', 'Submitted': '2026-11-21', 'Status': 'Changes requested',
             'Reviewer': 'R. Castillo', 'Decision Date': '2026-11-22',
             'Notes': 'Use the approved insurance wording (AC-2026-022) instead of custom text.', 'Snapshot': ''},
            {'Page': '/', 'Title': 'Maple Ridge Wealth Partners home', 'Site': 'Maple Ridge Wealth Partners',
             'Submitted By': 'Jordan Lee', 'Submitted': '2026-11-19', 'Status': 'Approved',
             'Reviewer': 'R. Castillo', 'Decision Date': '2026-11-20', 'Notes': 'Approved as submitted.', 'Snapshot': ''},
            {'Page': '/advisors/jordan-lee', 'Title': 'Jordan Lee profile', 'Site': 'Maple Ridge Wealth Partners',
             'Submitted By': 'Jordan Lee', 'Submitted': '2026-11-19', 'Status': 'Approved',
             'Reviewer': 'R. Castillo', 'Decision Date': '2026-11-20', 'Notes': '', 'Snapshot': ''},
        ],
    },
}
