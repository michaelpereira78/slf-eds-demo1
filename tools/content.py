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


# Stock photos in /images/photos (Pexels licence, credits in docs/PHOTO-CREDITS.md).
# The people in the photos are models; the names and bios on the demo sites are fictional.
PHOTOS = {'jordan-lee', 'priya-nair', 'marc-tremblay', 'aisha-okafor', 'daniel-whitford', 'sofia-martinez',
          'grace-macleod', 'omar-haddad', 'liam-obrien', 'elena-park'}


def photo(name, alt):
    """A photo from /images/photos (embedded in the Word document, so Drive uploads it as page media)."""
    return ('photo', name, alt)


def avatar(slug, name):
    short = name.split(',')[0]
    if slug in PHOTOS:
        return photo(slug, short)
    return ('img', slug, f'Placeholder avatar for {short}')


def meta(rows):
    return ('block', 'Metadata', [[[('p', [k])], [('p', [v])]] for k, v in rows.items()])


def section_style(style):
    return ('block', 'Section Metadata', [[[('p', ['Style'])], [('p', [style])]]])


def link_p(text, href, kind='a'):
    return ('p', [(kind, text, href)])


def icon_p(name):
    """An icon on its own line. Authors type :name: in the document; EDS turns it into /icons/name.svg."""
    return ('p', [('icon', name)])


def action_rows(items):
    """Cards (Actions) rows: (icon, title, text, link text, href)."""
    return [[[icon_p(ic), ('h3', t), ('p', [d]), link_p(lt, href)]] for ic, t, d, lt, href in items]


def kv_block(name, rows):
    return ('block', name, [[[('p', [k])], [('p', [v])]] for k, v in rows])


def service_rows(items):
    """Cards (Services) rows: (icon, title, text)."""
    return [[[icon_p(ic), ('h3', t), ('p', [d])]] for ic, t, d in items]


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
            ('block', 'Hero', [
                [[photo('hero-calgary', 'The Peace Bridge over the Bow River in Calgary on a sunny day')]],
                [[
                    ('p', ['Calgary, Alberta \u00b7 Since 2009']),
                    ('h1', 'Clear financial plans for every stage of life'),
                    ('p', [f'{TEAM} is a team of six advisors and specialists helping families, business owners '
                           'and retirees build plans they understand, with advice on investments, retirement, '
                           'insurance and estate planning under one roof.']),
                    ('p', [('b-a', 'Book a meeting', '/#contact-us')]),
                    ('p', [('i-a', 'Meet our team', '/#our-team')]),
                ]],
            ]),
        ],
        [
            ('block', 'Stats', [
                [[('p', ['15+'])], [('p', ['years helping Calgary families and business owners'])]],
                [[('p', ['6'])], [('p', ['advisors and specialists working on one shared plan'])]],
                [[('p', ['Yearly'])], [('p', ['full plan reviews, at no extra cost'])]],
                [[('p', ['1 day'])], [('p', ['typical reply time on business days'])]],
            ]),
        ],
        [
            ('h2', 'How we help'),
            ('p', ['Most clients come to us with one question and leave with a complete plan. '
                   'Here is where we spend most of our time.']),
            ('block', 'Cards (Services)', service_rows([
                ('retirement', 'Retirement income', 'When you can retire and where each paycheque will come from: pensions, RRIFs, TFSAs and government benefits.'),
                ('invest', 'Investment planning', 'Diversified portfolios built around your goals, with plain-language reviews of what changed and why.'),
                ('shield', 'Insurance and protection', 'Life, disability and critical illness coverage sized to your family and your mortgage.'),
                ('family', 'Families and education', 'RESPs, TFSAs and first-home savings for young families getting started.'),
                ('business', 'Business owners', 'Paying yourself, group benefits for your staff and a plan for the day you sell or step back.'),
                ('estate', 'Estate conversations', 'Wills, beneficiaries and powers of attorney, coordinated with your lawyer and accountant.'),
            ])),
        ],
        [
            ('block', 'Columns', [[
                [photo('advisor-meeting', 'An advisor reviewing a plan on a tablet with a retired couple at home')],
                [
                    ('p', [('b', 'Our approach')]),
                    ('h2', 'A plan you can explain to your family'),
                    ('p', ['We start with what you want your money to do, not with products. Every client gets a '
                           'written plan in plain language, one lead advisor who knows their story, and a team '
                           'of specialists behind them.']),
                    ('ul', [
                        ['One written plan that covers investments, insurance and retirement together'],
                        ['A yearly review, plus a call whenever life changes'],
                        ['Clear fees, explained before you sign anything'],
                    ]),
                ],
            ]]),
        ],
        [
            ('h2', 'Our team'),
            ('p', ['Six people, one plan. Every client works with a lead advisor and is supported by '
                   'specialists in investments, insurance and client service.']),
            ('block', 'Team Cards', team_rows(ADVISORS)),
            ('block', 'Section Metadata', [[[('p', ['Style'])], [('p', ['Light'])]]]),
        ],
        [
            ('h2', 'How working with us works'),
            ('p', ['Four steps, no surprises. Most clients have a written plan within three weeks.']),
            ('block', 'Cards (Steps)', [
                [[('h3', 'Get to know you'), ('p', ['A one-hour conversation about your goals, worries and timeline. No cost, no obligation.'])]],
                [[('h3', 'Build your plan'), ('p', ['We map out your retirement, investments and protection in one written plan.'])]],
                [[('h3', 'Put it in motion'), ('p', ['We open the accounts and policies you need and handle the paperwork.'])]],
                [[('h3', 'Review every year'), ('p', ['We meet once a year, and any time life changes, to keep the plan on track.'])]],
            ]),
            section_style('Dark'),
        ],
        [
            ('h2', 'What our clients say'),
            ('block', 'Testimonials', [
                [[('p', ['For the first time we know exactly when we can retire and what our income will be. '
                         'Jordan explained every number until it made sense.'])],
                 [('p', ['Karen and Doug M.'])], [('p', ['Clients since 2014, Calgary'])]],
                [[('p', ['Aisha set up group benefits for my eight employees in two weeks, and walked each of '
                         'them through their coverage.'])],
                 [('p', ['Ravi S.'])], [('p', ['Business owner, Airdrie'])]],
                [[('p', ['Priya turned three old pensions and a pile of statements into one simple '
                         'retirement paycheque.'])],
                 [('p', ['Linda T.'])], [('p', ['Retired teacher, Cochrane'])]],
            ]),
            ('p', [('i', 'Client stories on this demo site are fictional. On a real advisor site, testimonials are '
                         'regulated advertising and go through Compliance review like every other change.')]),
        ],
        [
            ('block', 'Banner', [
                [[photo('retirement-walk', 'A retired couple walking along a sunny beach')]],
                [[
                    ('h2', 'Ready for a second opinion on your plan?'),
                    ('p', ['Book a free one-hour review. We will look at where you are today and suggest next '
                           'steps, with no pressure to buy anything.']),
                    ('p', [('b-a', 'Book a review', 'mailto:hello@example.com?subject=Plan%20review')]),
                    ('p', [('i-a', 'Call 403-555-0100', 'tel:4035550100')]),
                ]],
            ]),
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
        [('p', [('a', 'Maple Ridge', '/')])],
        [('ul', [
            [('a', 'How we help', '/#how-we-help')],
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
            ('p', [('a', 'Maple Ridge Wealth Partners', '/')]),
            ('p', ['Clear financial plans for Calgary families, business owners and retirees since 2009.']),
        ],
        [('p', [('b', 'Explore')]), ('ul', [
            [('a', 'How we help', '/#how-we-help')],
            [('a', 'Our team', '/#our-team')],
            [('a', 'Jordan Lee', '/advisors/jordan-lee')],
            [('a', 'Retirement check-up', '/campaigns/retirement-checkup')],
        ])],
        [('p', [('b', 'Visit')]),
         ('p', ['Suite 400, 100 Example Avenue SW']), ('p', ['Calgary, AB T2P 0A0']),
         ('p', [('a', '403-555-0100', 'tel:4035550100')]), ('p', [('a', 'hello@example.com', 'mailto:hello@example.com')])],
        [('p', [('b', 'Platform demo')]), ('ul', [
            [('a', 'Demo hub', '/demo')],
            [('a', 'Advisor workspace', '/advisor')],
            [('a', 'Supervisor console', '/admin')],
        ])],
        [
            ('p', ['Demo, not affiliated with Sun Life']),
            ('p', ['Built on Adobe Edge Delivery Services. All names and contact details are fictional. '
                   'Photos: Pexels (see docs/PHOTO-CREDITS.md).']),
        ],
    ],
}


# =====================================================================
# PLATFORM DEMO: the seven business-user capabilities
# =====================================================================


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
        [('block', 'Hero', [
            [[photo('hero-halifax', 'Georges Island lighthouse in Halifax Harbour')]],
            [[
                ('p', ['Halifax, Nova Scotia']),
                ('h1', 'Planning that sails through every season'),
                ('p', ['Harbourview Financial Group is a three-person team helping Nova Scotia families '
                       'and business owners save, invest and protect what matters, with one clear plan.']),
                link_p('Book a conversation', '/harbourview/#contact-us', 'b-a'),
                link_p('Meet the team', '/harbourview/#our-team', 'i-a'),
            ]],
        ])],
        [('block', 'Stats', [
            [[('p', ['20+'])], [('p', ['years helping Nova Scotia families plan ahead'])]],
            [[('p', ['3'])], [('p', ['advisors, one shared plan for every client'])]],
            [[('p', ['1 hour'])], [('p', ['first conversation, free and with no obligation'])]],
        ])],
        [
            ('h2', 'What we do'),
            ('p', ['From your first TFSA to your retirement paycheque, we keep every part of your plan working together.']),
            ('block', 'Cards (Services)', service_rows([
                ('retirement', 'Retirement planning', 'A clear date, a clear income and a plan to get there, reviewed every year.'),
                ('invest', 'Tax-smart investing', 'Portfolios for professionals and business owners, with quarterly reviews in plain language.'),
                ('family', 'First-time investors', 'TFSAs, RESPs and your first insurance plan, explained step by step.'),
                ('shield', 'Protecting your family', 'Life, disability and critical illness coverage that fits your budget.'),
            ])),
        ],
        [
            ('h2', 'Our team'),
            ('p', ['Three advisors, one shared plan for every client.']),
            ('block', 'Team Cards', team_rows(HARBOURVIEW)),
            section_style('Light'),
        ],
        [
            ('block', 'Columns', [[
                [
                    ('p', [('b', 'Plain answers')]),
                    ('h2', 'How we help'),
                    ('p', ['The product descriptions here are approved content. They are shared with every '
                           'advisor site, so Compliance reviews them once and every site stays consistent.']),
                    link_p('Book a conversation', '/harbourview/#contact-us', 'b-a'),
                ],
                [photo('couple-planning', 'A young couple signing documents with their financial advisor')],
            ]]),
        ],
        [
            frag('/fragments/products/retirement-income'),
            frag('/fragments/products/tfsa-rrsp'),
            section_style('Narrow'),
        ],
        [
            ('h2', 'Clients on working with us'),
            ('block', 'Testimonials', [
                [[('p', ['Grace took a box of old statements and turned it into a plan we actually look forward '
                         'to reviewing every spring.'])],
                 [('p', ['Margaret and Ian R.'])], [('p', ['Clients since 2011, Dartmouth'])]],
                [[('p', ['Omar explained the tax side of my practice better than anyone had in ten years.'])],
                 [('p', ['Dr. Nadia K.'])], [('p', ['Dentist and practice owner, Halifax'])]],
                [[('p', ['Liam helped us open our first RESP the week our daughter was born. Simple and quick.'])],
                 [('p', ['Chris and Alex P.'])], [('p', ['New parents, Bedford'])]],
            ]),
            ('p', [('i', 'Client stories on this demo site are fictional. Real testimonials go through Compliance review.')]),
            section_style('Light'),
        ],
        [
            ('block', 'Banner', [
                [[photo('hero-halifax', 'Halifax Harbour on a calm evening')]],
                [[
                    ('h2', 'Let\u2019s talk about your plan'),
                    ('p', ['One hour, no cost, no obligation. Bring your questions; we will bring coffee.']),
                    link_p('Book a conversation', '/harbourview/#contact-us', 'b-a'),
                ]],
            ]),
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
            [('a', 'What we do', '/harbourview/#what-we-do')],
            [('a', 'Our team', '/harbourview/#our-team')],
            [('a', 'Contact', '/harbourview/#contact-us')],
        ])],
        [link_p('Book a conversation', '/harbourview/#contact-us', 'b-a')],
    ],
}

PAGES['harbourview/footer'] = {
    'metadata': {},
    'sections': [
        [link_p('Harbourview Financial Group', '/harbourview/'),
         ('p', ['Retirement, investment and insurance planning for Nova Scotia families and business owners.'])],
        [('p', [('b', 'Explore')]), ('ul', [[('a', 'What we do', '/harbourview/#what-we-do')],
                                             [('a', 'Our team', '/harbourview/#our-team')],
                                             [('a', 'Contact', '/harbourview/#contact-us')]])],
        [('p', [('b', 'Visit')]), ('p', ['200 Example Street, Suite 12']), ('p', ['Halifax, NS B3J 0A0']),
         ('p', [('a', '902-555-0100', 'tel:9025550100')])],
        [('p', [('b', 'Platform demo')]), ('ul', [[('a', 'Demo hub', '/demo')], [('a', 'Advisor workspace', '/advisor')]])],
        [('p', ['Demo, not affiliated with Sun Life']),
         ('p', ['Generated from the Advisor team template with the Harbour theme. All names are fictional. Photos: Pexels.'])],
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
        [('block', 'Stats', [
            [[('p', ['12'])], [('p', ['years as a Certified Financial Planner'])]],
            [[('p', ['1:1'])], [('p', ['you always work directly with Elena'])]],
            [[('p', ['Yearly'])], [('p', ['plan reviews, in person or by video'])]],
        ])],
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
        [
            ('h2', 'Working together'),
            ('block', 'Cards (Steps)', [
                [[('h3', 'A first conversation'), ('p', ['One hour, at my office or by video. You talk, I listen.'])]],
                [[('h3', 'Your written plan'), ('p', ['A clear plan with numbers you can check, delivered within three weeks.'])]],
                [[('h3', 'Every year after'), ('p', ['We review the plan together and adjust it whenever life changes.'])]],
            ]),
            section_style('Light'),
        ],
        [
            ('h2', 'Kind words'),
            ('block', 'Testimonials', [
                [[('p', ['Elena made retirement feel like a plan instead of a guess. We finally stopped worrying.'])],
                 [('p', ['Susan and Mark L.'])], [('p', ['Retired, Oak Bay'])]],
                [[('p', ['As a physician with no time, I needed someone who would just tell me what to do next. '
                         'Elena does exactly that.'])],
                 [('p', ['Dr. Amir H.'])], [('p', ['Physician, Saanich'])]],
            ]),
            ('p', [('i', 'Client stories on this demo site are fictional. Real testimonials go through Compliance review.')]),
        ],
        [('block', 'Banner', [
            [[photo('hero-victoria', 'Victoria\u2019s Inner Harbour on a sunny day')]],
            [[
                ('h2', 'Meeting clients across Vancouver Island'),
                ('p', ['In my Victoria office, at your kitchen table, or by video. Whatever is easiest for you.']),
                link_p('Book a meeting', 'mailto:elena.park@example.com', 'b-a'),
            ]],
        ])],
        [frag('/fragments/cta/book-a-review')],
        DISCLOSURE_LINK,
    ],
}

PAGES['northstar/nav'] = {
    'metadata': {},
    'sections': [
        [link_p('Northstar Planning', '/northstar/')],
        [('ul', [[('a', 'How I work', '/northstar/#how-i-work')], [('a', 'Working together', '/northstar/#working-together')]])],
        [link_p('Book a meeting', 'mailto:elena.park@example.com', 'b-a')],
    ],
}

PAGES['northstar/footer'] = {
    'metadata': {},
    'sections': [
        [link_p('Northstar Planning', '/northstar/'),
         ('p', ['Independent financial planning for professionals and retirees on Vancouver Island.'])],
        [('p', [('b', 'Visit')]), ('p', ['8 Example Lane']), ('p', ['Victoria, BC V8W 0A0']),
         ('p', [('a', '250-555-0175', 'tel:2505550175')])],
        [('p', [('b', 'Platform demo')]), ('ul', [[('a', 'Demo hub', '/demo')], [('a', 'Advisor workspace', '/advisor')]])],
        [('p', ['Demo, not affiliated with Sun Life']),
         ('p', ['Generated from the Solo advisor template with the Slate theme. All names are fictional. Photos: Pexels.'])],
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
    ('1. Generate a new website', 'From the supervisor console, pick a template and a look. The starter pages for '
     'the new practice are ready to edit in minutes.', 'Open the new site form', '/admin/new-site'),
    ('2. Make content changes', 'Advisors open a document, make a change and preview it privately. After approval a supervisor '
     'publishes, and it is live worldwide in seconds.', 'Open the advisor workspace', '/advisor'),
    ('3. Make minor layout changes', 'Change a section style (Light, Dark, Centered, Sidebar) or a block '
     'variant by typing one word in the document.', 'See the layout gallery', '/layouts'),
    ('4. Use approved templates', 'Start every page from an approved template: Advisor team, Solo advisor '
     'or Campaign. Developers can add new ones without touching existing sites.', 'Browse approved templates', '/templates'),
    ('5. Apply a brand theme', 'Each site picks a theme with one metadata value. Same platform, different look.',
     'See Harbourview (Harbour theme)', '/harbourview/'),
    ('6. Reuse approved content', 'Product descriptions, calls to action and disclosures are written once by '
     'Compliance and reused everywhere.', 'Open the approved content library', '/approved-content'),
    ('7. Compliance review and approval', 'Advisors submit a short note from their workspace; supervisors approve or send back '
     'changes from the console and then publish. Every step is logged.', 'Open the approval queue', '/admin/approvals'),
]

PAGES['demo'] = {
    'metadata': {
        'Title': 'Platform demo | Advisor Demo',
        'Description': 'Two workspaces, one platform: advisors update their own sites and supervisors stay in control, with no developer in the loop.',
        'Theme': 'Forest',
        'Robots': 'noindex',
    },
    'sections': [
        [('block', 'Hero (Light, Centered)', [[[
            ('p', ['Advisor web platform demo']),
            ('h1', 'Two workspaces. One platform. No developer required.'),
            ('p', ['Advisors update their own websites in ordinary documents. Supervisors review, approve and '
                   'launch new sites. Everything you will see is fictional, and this is not a Sun Life website.']),
        ]]])],
        [
            ('h2', 'Two workspaces, two roles'),
            ('p', ['Each role has its own home, its own menu, and only the tools that belong there.']),
            ('block', 'Cards (Actions)', action_rows([
                ('edit', 'Advisor workspace', 'A simple home for advisors: update a page, add a page, use approved wording, '
                 'send a change for review and follow its progress. Advisors cannot publish.',
                 'Open the advisor workspace', '/advisor'),
                ('approve', 'Supervisor console', 'A dashboard for supervisors: the review queue, advisor sites, new site launches, '
                 'layout changes, Figma imports and the audit log. Supervisors publish.',
                 'Open the supervisor console', '/admin'),
            ])),
            section_style('Light'),
        ],
        [('h2', 'What you can do, without a developer'), ('block', 'Cards (Capabilities)', [
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
                ['The advisor clicks Request review (in the status bar, in Sidekick, or on the advisor workspace). '
                 'The page joins this queue and the submission is written to the audit log.'],
                ['The supervisor and Compliance check the preview and click Approve or Request changes. For a '
                 'locked, exact-version approval the supervisor can add the page to a review snapshot '
                 '(Sidekick > Review), which needs the publish role.'],
                ['Only supervisors (the publish role) can publish. Advisors have the author role: they can edit and '
                 'preview, and Sidekick shows Publish greyed out. The platform rejects a publish from an author '
                 'account, so this is enforced, not just hidden.'],
                ['Each submission, approval, request for changes and publish is added to the compliance-audit-log '
                 'Google Sheet for audits.'],
            ]),
            ('p', [('i', 'In this demo, Approve and Request changes are saved in this browser only, so you can '
                         'click through the flow safely. Reset the demo with the button above the queue.')]),
            section_style('Narrow'),
        ],
    ],
}

# =====================================================================
# WORKSPACES: advisor and supervisor consoles (dashboard + subpages)
# =====================================================================
DRIVE_AUDIT_LOG = 'https://drive.google.com/drive/search?q=compliance-audit-log'


def workspace_meta(title, description, nav, footer):
    return {
        'Title': title,
        'Description': description,
        'Theme': 'Forest',
        'Template': 'workspace',
        'Nav': nav,
        'Footer': footer,
        'Robots': 'noindex',
    }


# ---- Advisor workspace ------------------------------------------------

PAGES['advisor/nav'] = {
    'metadata': {},
    'sections': [
        [link_p('Advisor workspace', '/advisor')],
        [('ul', [
            [('a', 'Dashboard', '/advisor')],
            [('a', 'My website', '/advisor/my-website')],
            [('a', 'Edit content', '/advisor/edit')],
            [('a', 'Approved content', '/advisor/approved-content')],
            [('a', 'Submissions', '/advisor/submissions')],
            [('a', 'Help', '/advisor/help')],
        ])],
        [link_p('Submit a change', '/advisor/submit-review?modal', 'b-a')],
    ],
}

PAGES['advisor/footer'] = {
    'metadata': {},
    'sections': [
        [link_p('Advisor workspace', '/advisor'),
         ('p', ['Update your website in ordinary documents. Your supervisor puts approved changes live.'])],
        [('p', [('b', 'In this workspace')]), ('ul', [
            [('a', 'Dashboard', '/advisor')],
            [('a', 'My website', '/advisor/my-website')],
            [('a', 'Submissions', '/advisor/submissions')],
            [('a', 'Help', '/advisor/help')],
        ])],
        [('p', [('b', 'Platform demo')]), ('ul', [
            [('a', 'Demo hub', '/demo')],
            [('a', 'Supervisor console', '/admin')],
        ])],
        [('p', ['Demo, not affiliated with Sun Life']),
         ('p', ['All names and contact details are fictional.'])],
    ],
}

PAGES['advisor'] = {
    'metadata': workspace_meta(
        'Advisor workspace | Advisor Demo',
        'Your website, updated in minutes, no tech skills needed.',
        '/advisor/nav', '/advisor/footer'),
    'sections': [
        [('block', 'Hero (Light)', [[[
            ('p', ['Advisor workspace']),
            ('h1', 'Your website, updated in minutes'),
            ('p', ['No tech skills needed. Change a photo, tweak your bio or start a new page in a familiar '
                   'document, then send it for a quick review. Your supervisor puts it live once it is approved.']),
            link_p('Update my site', '/advisor/edit', 'b-a'),
            link_p('Submit a change for review', '/advisor/submit-review?modal', 'i-a'),
        ]]])],
        [
            ('h2', 'At a glance'),
            ('p', ['How your recent changes are doing. Open any card to see the details.']),
            ('block', 'Compliance Queue (Mine, Summary)', [
                [[('p', ['View all'])], [link_p('View my submissions', '/advisor/submissions')]],
            ]),
        ],
        [
            ('h2', 'What would you like to do?'),
            ('block', 'Cards (Actions)', action_rows([
                ('edit', 'Edit a page',
                 'Open the page in a document, make your change, and preview it privately before anyone else sees it.',
                 'How to edit', '/advisor/edit'),
                ('add', 'Add a new page',
                 'Start from an approved template, fill in the blanks, and you have a new page ready for review.',
                 'Add a page', '/advisor/add-page'),
                ('library', 'Use approved wording',
                 'Drop in product descriptions, invitations and the legal disclosure that Compliance has already signed off.',
                 'Browse approved content', '/advisor/approved-content'),
                ('preview', 'See my website',
                 'Your private preview updates in seconds. Nothing goes public until your supervisor publishes it.',
                 'Open my website', '/advisor/my-website'),
                ('layout', 'Request a layout change',
                 'Ask for a new section, a different arrangement, or anything you cannot switch yourself.',
                 'Request a change', '/advisor/layout-change?modal'),
                ('review', 'Submit for review',
                 'Tell Compliance what you changed in a short note. You will get a reference number straight away.',
                 'Submit a change', '/advisor/submit-review?modal'),
                ('status', 'Track my submissions',
                 'See what is with Compliance, what was approved, and what came back with a note.',
                 'My submissions', '/advisor/submissions'),
                ('help', 'Get help',
                 'Short answers to common questions, and who to call when you are stuck.',
                 'Help and FAQ', '/advisor/help'),
            ])),
        ],
        [
            ('h2', 'How an update goes live'),
            ('block', 'Cards (Steps)', [
                [[('h3', 'Open the page'), ('p', ['In your site folder, open the document for the page you want to change. The home page is called index.'])]],
                [[('h3', 'Make the change'), ('p', ['Edit the text, replace a photo, or paste a piece of approved wording.'])]],
                [[('h3', 'Preview and send'), ('p', ['Preview is private, and ready in a few seconds. Then send a short note so Compliance can take a look.'])]],
                [[('h3', 'It goes live'), ('p', ['Once it is approved, your supervisor publishes it and your live website updates worldwide.'])]],
            ]),
            section_style('Dark'),
        ],
        [
            ('block', 'Columns', [[
                [('h3', 'You can'), ('ul', [
                    ['Edit your own pages in a document'],
                    ['Preview changes on a private address'],
                    ['Use approved wording and approved templates'],
                    ['Switch a section style yourself'],
                    ['Send pages for compliance review'],
                ])],
                [('h3', 'Your supervisor does'), ('ul', [
                    ['Reviews your changes with Compliance'],
                    ['Publishes approved pages to your live site'],
                    ['Handles bigger layout and brand changes'],
                    ['Sets up new advisor websites'],
                ])],
            ]]),
            ('p', [('i', 'You will notice the Publish button is unavailable on your account. That is by design: '
                         'only a supervisor can put a page live, so nothing reaches the public site before it is approved.')]),
            section_style('Light'),
        ],
    ],
}

PAGES['advisor/my-website'] = {
    'metadata': workspace_meta(
        'My website | Advisor workspace',
        'Open your private preview or your live website.',
        '/advisor/nav', '/advisor/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['My website']),
            ('h1', 'Your site, in preview and live'),
            ('p', ['Preview is your private copy: it shows your latest edits in a few seconds, and visitors cannot '
                   'see it. The live site is what the public sees, and it only changes when your supervisor publishes.']),
        ]]])],
        [
            ('h2', 'Open a site'),
            ('p', ['In this demo you can look at any of the sample firms. On a real workspace, this list would show only your site.']),
            ('block', 'Cards (Sites)', [
                [[('p', [('b', 'Approved')]), ('h3', 'Maple Ridge Wealth Partners'),
                  ('p', ['Calgary team site. The public version is already approved.']),
                  link_p('Open preview', '/'), link_p('Jordan Lee’s profile', '/advisors/jordan-lee')]],
                [[('p', [('b', 'Pending review')]), ('h3', 'Harbourview Financial Group'),
                  ('p', ['Halifax team site. A new home page is waiting for review.']),
                  link_p('Open preview', '/harbourview/')]],
                [[('p', [('b', 'Changes requested')]), ('h3', 'Northstar Planning'),
                  ('p', ['Victoria solo practice. Compliance asked for a wording change.']),
                  link_p('Open preview', '/northstar/')]],
            ]),
        ],
    ],
}

PAGES['advisor/edit'] = {
    'metadata': workspace_meta(
        'Edit content | Advisor workspace',
        'Change your website in a familiar document, then preview it privately.',
        '/advisor/nav', '/advisor/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Edit content']),
            ('h1', 'Change a page in a few minutes'),
            ('p', ['You work in an ordinary document, the same way you would edit a letter. Save, preview, and '
                   'you will see your update on a private copy of the page.']),
        ]]])],
        [
            ('h2', 'The steps'),
            ('block', 'Cards (Steps)', [
                [[('h3', 'Open the document'), ('p', ['In your site folder, open the document for that page. The home page is the one named index.'])]],
                [[('h3', 'Make the change'), ('p', ['Edit a heading, replace a photo, or add a sentence. For product wording, paste a piece of approved content instead of writing your own.'])]],
                [[('h3', 'Preview'), ('p', ['Click Preview in the toolbar on the document. Your private preview updates in about three seconds.'])]],
                [[('h3', 'Send for review'), ('p', ['When you are happy with it, submit the page so Compliance can take a look.'])]],
            ]),
            link_p('Submit a change for review', '/advisor/submit-review?modal', 'b-a'),
            link_p('Browse approved wording', '/advisor/approved-content', 'i-a'),
        ],
        [
            ('h2', 'Things you can do yourself'),
            ('ul', [
                ['Change names, titles, phone numbers and short biographies'],
                ['Replace a photo: click the picture, insert a new one, then preview'],
                ['Switch a section’s look by changing one word (for example Light to Dark)'],
                ['Paste approved product wording and the legal disclosure'],
            ]),
            ('p', ['Bigger changes, such as a new section or a different page layout, can be requested from your supervisor.']),
            link_p('Request a layout change', '/advisor/layout-change?modal', 'i-a'),
            section_style('Light'),
        ],
    ],
}

PAGES['advisor/approved-content'] = {
    'metadata': workspace_meta(
        'Approved content | Advisor workspace',
        'Reuse wording Compliance has already signed off, so you never have to write it from scratch.',
        '/advisor/nav', '/advisor/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Approved content']),
            ('h1', 'Wording you can trust, ready to paste'),
            ('p', ['Product descriptions, invitations and the legal disclosure are written once by Compliance. '
                   'You place them on your pages; you cannot edit the words, and that is the point: every site stays accurate.']),
            link_p('Open the full library', '/approved-content', 'b-a'),
        ]]])],
        [
            ('h2', 'How to add a piece to a page'),
            ('ol', [
                ['Open the library and copy the link for the piece you need.'],
                ['In your page document, paste the link on its own line.'],
                ['Preview. The approved wording appears, badge and all.'],
            ]),
            ('p', ['When Compliance updates a piece, every site that uses it picks up the new wording the next time the page is published.']),
        ],
    ],
}

PAGES['advisor/add-page'] = {
    'metadata': workspace_meta(
        'Add a page | Advisor workspace',
        'Start a new page from an approved template.',
        '/advisor/nav', '/advisor/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Add a page']),
            ('h1', 'Start from a template, not a blank page'),
            ('p', ['Every new page begins with a layout Brand and Compliance have already approved. '
                   'Copy one, fill in the brackets, preview, and send it for review.']),
        ]]])],
        [
            ('h2', 'Choose a starting point'),
            ('block', 'Cards (Templates)', [
                [[('h3', name), ('p', [desc]), link_p('See an example', ex)]]
                for name, key, desc, ex, _start in TEMPLATES
            ]),
        ],
        [
            ('h2', 'Then do this'),
            ('ol', [
                ['Open the templates folder in your site’s document library and make a copy of the one you want.'],
                ['Move the copy into your site folder and give it a clear name.'],
                ['Replace the text in square brackets, add your photo, and click Preview.'],
                ['Submit the new page for review when you are happy with it.'],
            ]),
            link_p('Submit a new page for review', '/advisor/submit-review?modal', 'b-a'),
            link_p('Browse all templates', '/templates', 'i-a'),
            section_style('Light'),
        ],
    ],
}

PAGES['advisor/submit-review'] = {
    'metadata': workspace_meta(
        'Submit for review | Advisor workspace',
        'Send a page to Compliance with a short note. You will get a reference number straight away.',
        '/advisor/nav', '/advisor/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Submit for review']),
            ('h1', 'Tell us what you changed'),
            ('p', ['A short note is enough. The page joins the review queue, and a row is added to the audit log '
                   'with the date, your name, the site and a summary.']),
        ]]])],
        [
            ('block', 'Request Form', [[[('p', ['Form'])], [('p', ['compliance-review'])]]]),
            ('p', [('i', 'You can also start a review from the status bar at the bottom of any preview page.')]),
        ],
    ],
}

PAGES['advisor/layout-change'] = {
    'metadata': workspace_meta(
        'Request a layout change | Advisor workspace',
        'Ask your supervisor for a layout change you cannot make yourself.',
        '/advisor/nav', '/advisor/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Layout change']),
            ('h1', 'Ask for a layout change'),
            ('p', ['Use this when you need a new section, a different arrangement, or something you cannot switch '
                   'with a section style. Your supervisor will pick it up, or pass it on if it needs a designer.']),
        ]]])],
        [
            ('block', 'Request Form', [[[('p', ['Form'])], [('p', ['layout-change'])]]]),
        ],
    ],
}

PAGES['advisor/submissions'] = {
    'metadata': workspace_meta(
        'My submissions | Advisor workspace',
        'Follow the pages you have sent for compliance review.',
        '/advisor/nav', '/advisor/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Submissions']),
            ('h1', 'Follow your reviews'),
            ('p', ['See what is with Compliance, what was approved, and what came back with a note. '
                   'If changes were requested, edit the page, preview it, and submit it again.']),
            link_p('Submit a change', '/advisor/submit-review?modal', 'b-a'),
        ]]])],
        [
            ('block', 'Compliance Queue (Mine)', [[[('p', ['My submissions'])]]]),
        ],
    ],
}

PAGES['advisor/help'] = {
    'metadata': workspace_meta(
        'Help | Advisor workspace',
        'Answers to common questions about updating your website.',
        '/advisor/nav', '/advisor/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Help']),
            ('h1', 'Questions, answered quickly'),
            ('p', ['A short list of the things advisors ask most often. If you are still stuck, your supervisor is the first call.']),
        ]]])],
        [
            ('block', 'Accordion', [
                [[('p', ['Why can’t I publish?'])],
                 [('p', ['Advisor accounts can edit and preview only. Publishing is reserved for supervisors, '
                         'so only approved content reaches the live site. This is a platform rule, not a hidden button.'])]],
                [[('p', ['How do I change my photo?'])],
                 [('p', ['In the team table, click the photo in the first column, replace it with your new picture, then preview.'])]],
                [[('p', ['How do I add approved product wording?'])],
                 [('p', ['Copy the link from the approved content library and paste it on its own line in your page.']),
                  link_p('Approved content', '/advisor/approved-content')]],
                [[('p', ['My change is not showing on the preview'])],
                 [('p', ['Wait five seconds and click Preview again; documents save in the background. '
                         'Still stuck? Check you edited the document in your own site folder.'])]],
                [[('p', ['Who do I contact?'])],
                 [('p', ['Your supervisor for content and layout questions; the platform team '
                         '(martech-engineering@example.com) for anything technical.'])]],
            ]),
            section_style('Narrow'),
        ],
    ],
}


# ---- Supervisor / admin console ---------------------------------------

PAGES['admin/nav'] = {
    'metadata': {},
    'sections': [
        [link_p('Supervisor console', '/admin')],
        [('ul', [
            [('a', 'Dashboard', '/admin')],
            [('a', 'Approvals', '/admin/approvals')],
            [('a', 'Sites', '/admin/sites')],
            [('a', 'New site', '/admin/new-site')],
            [('a', 'Layouts', '/admin/layouts')],
            [('a', 'Figma import', '/admin/figma-import')],
            [('a', 'Audit log', '/admin/audit-log')],
            [('a', 'Roles', '/admin/roles')],
        ])],
        [link_p('Review queue', '/admin/approvals', 'b-a')],
    ],
}

PAGES['admin/footer'] = {
    'metadata': {},
    'sections': [
        [link_p('Supervisor console', '/admin'),
         ('p', ['Review advisor updates, publish what is approved, and launch new advisor websites.'])],
        [('p', [('b', 'In this console')]), ('ul', [
            [('a', 'Dashboard', '/admin')],
            [('a', 'Approvals', '/admin/approvals')],
            [('a', 'New site', '/admin/new-site')],
            [('a', 'Audit log', '/admin/audit-log')],
        ])],
        [('p', [('b', 'Platform demo')]), ('ul', [
            [('a', 'Demo hub', '/demo')],
            [('a', 'Advisor workspace', '/advisor')],
        ])],
        [('p', ['Demo, not affiliated with Sun Life']),
         ('p', ['All names and contact details are fictional.'])],
    ],
}

PAGES['admin'] = {
    'metadata': workspace_meta(
        'Supervisor console | Advisor Demo',
        'Keep every advisor site on brand and on track: reviews, new sites, and custom designs.',
        '/admin/nav', '/admin/footer'),
    'sections': [
        [('block', 'Hero (Light)', [[[
            ('p', ['Supervisor console']),
            ('h1', 'Keep every advisor site on brand and on track'),
            ('p', ['See what is waiting for your review, publish approved updates, and launch a new advisor '
                   'website whenever someone joins the team. Custom designs go to the design-and-build team as a short request.']),
            link_p('Review submissions', '/admin/approvals', 'b-a'),
            link_p('Launch a new site', '/admin/new-site', 'i-a'),
        ]]])],
        [
            ('h2', 'At a glance'),
            ('p', ['What is in the review queue right now. Open a card to work through it.']),
            ('block', 'Compliance Queue (Summary)', [
                [[('p', ['View all'])], [link_p('Open the approval queue', '/admin/approvals')]],
            ]),
        ],
        [
            ('h2', 'What would you like to do?'),
            ('block', 'Cards (Actions)', action_rows([
                ('approve', 'Review and approve',
                 'Approve a page or send it back with a note. Every decision is added to the audit log.',
                 'Open the queue', '/admin/approvals'),
                ('publish', 'Publish approved updates',
                 'Once a page is approved, publish it and the live site updates worldwide in seconds.',
                 'How to publish', '/admin/approvals#how-to-publish'),
                ('users', 'See advisor sites',
                 'Open any advisor website, check its review status, and jump to its preview.',
                 'View sites', '/admin/sites'),
                ('template', 'Launch a new website',
                 'Pick a template and a look; the starter pages are created for the new advisor practice.',
                 'Start a new site', '/admin/new-site'),
                ('layout', 'Advanced layout updates',
                 'Themes, navigation, footers and new sections for any advisor site, plus requests from advisors.',
                 'Layout tools', '/admin/layouts'),
                ('figma', 'Import a design from Figma',
                 'Send a Figma file to the design-and-build team. They turn it into pages that match your approved look.',
                 'Start an import', '/admin/figma-import'),
                ('audit', 'Compliance audit log',
                 'Every submission, approval and publish, in one spreadsheet you can hand to an auditor.',
                 'View the log', '/admin/audit-log'),
                ('lock', 'Roles and permissions',
                 'Advisors edit and preview; supervisors publish; platform admins manage the setup.',
                 'View roles', '/admin/roles'),
            ])),
        ],
        [
            ('h2', 'Recent activity'),
            ('p', ['The latest rows from this browser and the sample log. The spreadsheet in Drive is the official record.']),
            ('block', 'Submissions', [
                [[('p', ['Form'])], [('p', ['compliance-audit'])]],
                [[('p', ['Sheet'])], [('p', [('a', 'compliance-audit-log', DRIVE_AUDIT_LOG)])]],
            ]),
            link_p('Open the full audit log', '/admin/audit-log', 'i-a'),
            section_style('Light'),
        ],
    ],
}

PAGES['admin/approvals'] = {
    'metadata': workspace_meta(
        'Approvals | Supervisor console',
        'Review pages advisors have submitted, approve them or send them back, then publish.',
        '/admin/nav', '/admin/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Approvals']),
            ('h1', 'Review what advisors have sent'),
            ('p', ['Approve a page or send it back with a short note. Each decision is written to the audit log. '
                   'When a page is approved, you publish it and the live site updates.']),
        ]]])],
        [
            ('block', 'Compliance Queue', [[[('p', ['Review queue'])]]]),
        ],
        [
            ('h2', 'How to publish'),
            ('ol', [
                ['Open the approved page’s preview (Open preview in the queue).'],
                ['Click Publish in the toolbar. It is only available on a supervisor account; advisors see it unavailable.'],
                ['The live site updates worldwide in a few seconds, and a Published row is added to the audit log.'],
            ]),
            ('p', ['Publishing many pages at once, for example a new site launch: select the documents in the folder and use bulk Publish.']),
            ('p', [('i', 'This is enforced by the platform: a publish from an account that is not a supervisor is rejected, '
                         'whether it comes from the toolbar, a script or a bookmark.')]),
            section_style('Light'),
        ],
    ],
}

PAGES['admin/sites'] = {
    'metadata': workspace_meta(
        'Advisor sites | Supervisor console',
        'Every advisor website on this platform, with its current review status.',
        '/admin/nav', '/admin/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Sites']),
            ('h1', 'Every advisor website, in one place'),
            ('p', ['Open a preview, check review status, or start a brand-new site from an approved template.']),
            link_p('Launch a new site', '/admin/new-site', 'b-a'),
        ]]])],
        [
            ('block', 'Cards (Sites)', [
                [[('p', [('b', 'Approved')]), ('h3', 'Maple Ridge Wealth Partners'),
                  ('p', ['Calgary. Advisor team template, Forest look.']),
                  link_p('Open preview', '/'), link_p('Team lead profile', '/advisors/jordan-lee')]],
                [[('p', [('b', 'Pending review')]), ('h3', 'Harbourview Financial Group'),
                  ('p', ['Halifax. Advisor team template, Harbour look. New home page waiting for review.']),
                  link_p('Open preview', '/harbourview/'), link_p('Open in the queue', '/admin/approvals')]],
                [[('p', [('b', 'Changes requested')]), ('h3', 'Northstar Planning'),
                  ('p', ['Victoria. Solo advisor template, Slate look. Compliance asked for a wording change.']),
                  link_p('Open preview', '/northstar/'), link_p('Open in the queue', '/admin/approvals')]],
            ]),
        ],
    ],
}

PAGES['admin/new-site'] = {
    'metadata': workspace_meta(
        'New advisor website | Supervisor console',
        'Launch a new advisor website from an approved template and look.',
        '/admin/nav', '/admin/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['New site']),
            ('h1', 'Launch a new advisor website'),
            ('p', ['Pick a template and a look. The starter pages are created for the new practice, ready to edit, '
                   'preview and send for review.']),
        ]]])],
        [
            ('h2', 'Pick a template'),
            ('block', 'Cards (Templates)', [
                [[('h3', name), ('p', [desc]), link_p('See an example', ex),
                  link_p('Use this template', f'/admin/new-site?template={key}')]]
                for name, key, desc, ex, _start in TEMPLATES
            ]),
        ],
        [
            ('h2', 'Tell us about the practice'),
            ('p', ['The form below prepares the starter documents and the one-step setup command. '
                   'Harbourview and Northstar were created this way.']),
            ('block', 'Site Request', [[[('p', ['New site'])]]]),
            section_style('Light'),
        ],
    ],
}

PAGES['admin/layouts'] = {
    'metadata': workspace_meta(
        'Layouts | Supervisor console',
        'Advanced layout updates for advisor websites, and requests from advisors.',
        '/admin/nav', '/admin/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Layouts']),
            ('h1', 'Bigger layout changes, still in documents'),
            ('p', ['Themes, navigation, footers and new sections are all edited in documents, so they are previewed '
                   'and approved like any other change.']),
            link_p('See every section style', '/layouts', 'i-a'),
        ]]])],
        [
            ('h2', 'What you can change'),
            ('block', 'Cards (Services)', service_rows([
                ('layout', 'Switch the look or template', 'Change the Theme or Template value in a page’s details, or for a whole site at once.'),
                ('template', 'Navigation and footer', 'Edit the site’s menu, contact details and footer links in their documents.'),
                ('add', 'Add a section', 'Facts, testimonials, banners and service cards can be added from the content library.'),
                ('figma', 'Something entirely new', 'Need a new kind of section? Send it to the design-and-build team as a Figma import.'),
            ])),
        ],
        [
            ('h2', 'Requests from advisors'),
            ('p', ['Layout changes advisors have asked for. Nothing submitted from this browser yet will show the sample row below.']),
            ('block', 'Submissions', [[[('p', ['Form'])], [('p', ['layout-change'])]]]),
            section_style('Light'),
        ],
    ],
}

PAGES['admin/figma-import'] = {
    'metadata': workspace_meta(
        'Import a design from Figma | Supervisor console',
        'Send a Figma file to the design-and-build team to turn into an advisor website.',
        '/admin/nav', '/admin/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Figma import']),
            ('h1', 'Turn a Figma file into an advisor website'),
            ('p', ['Send the file to the design-and-build team. They map it to the approved sections you already use, '
                   'build anything new, and send you a preview to review and publish.']),
            link_p('Back to the console', '/admin', 'i-a'),
        ]]])],
        [
            ('block', 'Request Form', [[[('p', ['Form'])], [('p', ['figma-import'])]]]),
        ],
        [
            ('h2', 'What happens next'),
            ('block', 'Cards (Steps)', [
                [[('h3', 'Intake'), ('p', ['Your request lands in the team’s intake sheet with a reference number.'])]],
                [[('h3', 'Scope and timeline'), ('p', ['The team checks the file and replies by email with the scope and a date.'])]],
                [[('h3', 'Build'), ('p', ['The team turns frames into the approved sections and drafts anything new. A person reviews every change.'])]],
                [[('h3', 'Your review'), ('p', ['You get a preview link. Compliance reviews the content; you publish.'])]],
            ]),
            section_style('Light'),
        ],
        [
            ('h2', 'Recent requests'),
            ('block', 'Submissions', [[[('p', ['Form'])], [('p', ['figma-import'])]]]),
        ],
    ],
}

PAGES['admin/audit-log'] = {
    'metadata': workspace_meta(
        'Audit log | Supervisor console',
        'Every compliance submission, approval and publish, in one place.',
        '/admin/nav', '/admin/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Audit log']),
            ('h1', 'A complete record of every review'),
            ('p', ['Each submission, approval, request for changes and publish is added to a spreadsheet: '
                   'when it happened, who did it, which site and page, and the decision.']),
        ]]])],
        [
            ('block', 'Submissions', [
                [[('p', ['Form'])], [('p', ['compliance-audit'])]],
                [[('p', ['Sheet'])], [('p', [('a', 'compliance-audit-log', DRIVE_AUDIT_LOG)])]],
            ]),
            ('p', [('i', 'Rows from this browser appear at the top. The spreadsheet in Drive is the official record, '
                         'once the forms have been connected (see the setup guide).')]),
        ],
    ],
}

PAGES['admin/roles'] = {
    'metadata': workspace_meta(
        'Roles and permissions | Supervisor console',
        'Advisors edit and preview; supervisors publish; platform admins manage the setup.',
        '/admin/nav', '/admin/footer'),
    'sections': [
        [('block', 'Hero (Light, Page)', [[[
            ('p', ['Roles']),
            ('h1', 'Who can do what'),
            ('p', ['Advisors look after their own pages. Supervisors decide what goes live. '
                   'The platform team looks after the setup. These rules are enforced, not just hidden in the toolbar.']),
        ]]])],
        [
            ('block', 'Cards (Services)', service_rows([
                ('users', 'Advisor', 'Edit, preview, delete drafts and request reviews. Cannot publish or change site settings.'),
                ('approve', 'Supervisor', 'Everything an advisor can do, plus publish, unpublish, review locked versions and publish many pages at once.'),
                ('lock', 'Platform admin', 'Site setup, roles, new sites and connections. The platform team and the owner.'),
            ])),
            ('p', [('i', 'Roles are set once in the site’s access configuration and checked on every publish. '
                         'The /admin and /advisor pages themselves are ordinary pages; the real control is who is allowed to publish.')]),
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
        library_meta('Advisor team', 'Team home page: photo hero, key facts, services, team, call to action, contact, disclosure.'),
        [('block', 'Hero', [
            [[photo('hero-calgary', '[Describe your photo]')]],
            [[
                ('p', ['[City, Province]']),
                ('h1', '[One line about who you help]'),
                ('p', ['[Two or three sentences about who you help and how.]']),
                link_p('Book a meeting', '/#contact-us', 'b-a'),
                link_p('Meet our team', '/#our-team', 'i-a'),
            ]],
        ])],
        [('block', 'Stats', [
            [[('p', ['[15+]'])], [('p', ['[years serving your community]'])]],
            [[('p', ['[6]'])], [('p', ['[advisors and specialists]'])]],
            [[('p', ['[1 day]'])], [('p', ['[typical reply time]'])]],
        ])],
        [('h2', 'How we help'), ('p', ['[One sentence about your services.]']),
         ('block', 'Cards (Services)', service_rows([
             ('retirement', '[Service one]', '[One sentence.]'),
             ('invest', '[Service two]', '[One sentence.]'),
             ('shield', '[Service three]', '[One sentence.]'),
         ]))],
        [('h2', 'Our team'), ('p', ['[One sentence about the team.]']),
         ('block', 'Team Cards', team_rows([ADVISORS[0], ADVISORS[1]])), section_style('Light')],
        [('block', 'Banner', [
            [[photo('retirement-walk', '[Describe your photo]')]],
            [[('h2', '[Your call to action]'), ('p', ['[One sentence.]']), link_p('Book a meeting', '/#contact-us', 'b-a')]],
        ])],
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
        library_meta('Solo advisor', 'One-advisor home page: portrait hero, key facts, story, sticky contact card, steps, call to action.'),
        [('block', 'Hero (Profile)', [[
            [avatar('elena-park', 'Advisor')],
            [('p', ['[Practice name, City]']), ('h1', '[Advisor name, credentials]'),
             ('p', ['[Who you help, in one sentence.]']), link_p('Book a meeting', 'mailto:advisor@example.com', 'b-a')],
        ]])],
        [('block', 'Stats', [
            [[('p', ['[12]'])], [('p', ['[years in practice]'])]],
            [[('p', ['[1:1]'])], [('p', ['[you always work with me]'])]],
        ])],
        [('h2', 'How I work'), ('p', ['[Your story and approach.]']),
         ('ul', [['[Service one]'], ['[Service two]'], ['[Service three]']]),
         ('block', 'Contact (Card)', [[[('p', ['Phone'])], [('p', ['[555 number]'])]],
                                      [[('p', ['Email'])], [('p', ['[advisor@example.com]'])]]]),
         section_style('Sidebar')],
        [('h2', 'Working together'), ('block', 'Cards (Steps)', [
            [[('h3', '[Step one]'), ('p', ['[One sentence.]'])]],
            [[('h3', '[Step two]'), ('p', ['[One sentence.]'])]],
            [[('h3', '[Step three]'), ('p', ['[One sentence.]'])]],
        ]), section_style('Light')],
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

def lib_doc(block, name, desc):
    return [block, ('block', 'Library Metadata', [[[('p', ['name'])], [('p', [name])]],
                                                   [[('p', ['description'])], [('p', [desc])]]])]


PAGES['tools/sidekick/blocks/stats'] = {
    'metadata': {'Robots': 'noindex'},
    'sections': [lib_doc(('block', 'Stats', [[[('p', ['15+'])], [('p', ['years serving our community'])]],
                                             [[('p', ['6'])], [('p', ['advisors and specialists'])]],
                                             [[('p', ['1 day'])], [('p', ['typical reply time'])]]]),
                         'Stats', 'Key facts strip: a value and a label per row. Avoid performance or return claims.')],
}

PAGES['tools/sidekick/blocks/testimonials'] = {
    'metadata': {'Robots': 'noindex'},
    'sections': [lib_doc(('block', 'Testimonials', [[[('p', ['Quote.'])], [('p', ['Client name'])], [('p', ['Client since 2015'])]],
                                                    [[('p', ['Quote.'])], [('p', ['Client name'])], [('p', ['City'])]]]),
                         'Testimonials', 'Client quotes: quote | name | context. Regulated: needs Compliance approval.')],
}

PAGES['tools/sidekick/blocks/banner'] = {
    'metadata': {'Robots': 'noindex'},
    'sections': [lib_doc(('block', 'Banner', [[[photo('retirement-walk', 'Describe the photo')]],
                                              [[('h2', 'Call to action heading'), ('p', ['One sentence.']), link_p('Button', '/', 'b-a')]]]),
                         'Banner', 'Full-width call to action over a photo. Replace the photo; keep one or two buttons.')],
}

PAGES['tools/sidekick/blocks/cards'] = {
    'metadata': {'Robots': 'noindex'},
    'sections': [
        lib_doc(('block', 'Cards (Services)', service_rows([('retirement', 'Service', 'One sentence.'),
                                                            ('invest', 'Service', 'One sentence.'),
                                                            ('shield', 'Service', 'One sentence.')])),
                'Cards (Services)', 'Service cards with icons. Icons: type :retirement:, :invest:, :shield:, :family:, :business:, :estate:.'),
        lib_doc(('block', 'Cards (Steps)', [[[('h3', 'Step'), ('p', ['One sentence.'])]], [[('h3', 'Step'), ('p', ['One sentence.'])]],
                                            [[('h3', 'Step'), ('p', ['One sentence.'])]]]),
                'Cards (Steps)', 'Numbered process steps.'),
    ],
}

# ---------------------------------------------------------------- spreadsheets
SHEETS = {
    'tools/sidekick/library': {
        'helix-blocks': [
            {'name': 'Hero', 'path': '/tools/sidekick/blocks/hero'},
            {'name': 'Callout', 'path': '/tools/sidekick/blocks/callout'},
            {'name': 'Contact', 'path': '/tools/sidekick/blocks/contact'},
            {'name': 'Stats', 'path': '/tools/sidekick/blocks/stats'},
            {'name': 'Testimonials', 'path': '/tools/sidekick/blocks/testimonials'},
            {'name': 'Banner', 'path': '/tools/sidekick/blocks/banner'},
            {'name': 'Cards (Services, Steps)', 'path': '/tools/sidekick/blocks/cards'},
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


# ---------------------------------------------------------------- form sheets (Forms Submission Service targets)
# Each workbook: `shared-aem` = form definition (public as /forms/<name>.json, no personal data),
# `incoming` = where submissions are appended (never exposed), `README` = setup notes (never exposed).
AUDIT_COLUMNS = ['timestamp', 'event', 'advisor', 'site', 'pagePath', 'changeSummary', 'submittedBy', 'status',
                 'reviewer', 'decisionDate', 'notes', 'reference', 'source']
FIGMA_COLUMNS = ['submittedAt', 'reference', 'figmaUrl', 'siteName', 'requester', 'email', 'deadline', 'theme',
                 'pages', 'notes', 'requestType', 'status', 'page']
LAYOUT_COLUMNS = ['submittedAt', 'reference', 'site', 'pagePath', 'change', 'requester', 'details', 'status', 'page']


def form_definition(columns, labels, submit_label):
    rows = [{'Name': c, 'Type': 'text', 'Label': labels.get(c, c), 'Placeholder': '', 'Mandatory': '', 'Options': ''}
            for c in columns]
    rows.append({'Name': 'submit', 'Type': 'submit', 'Label': submit_label, 'Placeholder': '', 'Mandatory': '', 'Options': ''})
    return rows


def readme(lines):
    return [{'Setup (this tab is not published)': line} for line in lines]


FORM_README = [
    '1. Upload this file to the site folder in Google Drive, inside a folder named forms, and open it as a Google Sheet (File > Save as Google Sheets). Keep the file name.',
    '2. Share the sheet with forms@adobe.com as Editor (Adobe Forms Submission Service writes the rows).',
    '3. With Sidekick, Preview and then Publish this sheet (a supervisor/admin does this once).',
    '4. Rows are appended to the incoming tab. Do not rename incoming or change its header row.',
    '5. Only the shared-aem tab is public (as /forms/<name>.json). incoming and README are never served.',
]

SHEETS['forms/compliance-audit-log'] = {
    'shared-aem': form_definition(AUDIT_COLUMNS, {
        'timestamp': 'Timestamp', 'event': 'Event', 'advisor': 'Advisor', 'site': 'Site', 'pagePath': 'Page path',
        'changeSummary': 'Change summary', 'submittedBy': 'Submitted by', 'status': 'Status', 'reviewer': 'Reviewer',
        'decisionDate': 'Decision date', 'notes': 'Notes', 'reference': 'Reference', 'source': 'Source host'},
        'Log event'),
    'incoming': AUDIT_COLUMNS,
    'README': readme(FORM_README + [
        'Events written by the site: Submitted (advisor), Approved and Changes requested (supervisor console), Published (Sidekick publish).',
        'Treat this as an append-only log: protect the incoming tab (Data > Protect sheets and ranges) so only the owner can edit rows.',
    ]),
}

SHEETS['forms/figma-import-requests'] = {
    'shared-aem': form_definition(FIGMA_COLUMNS, {
        'submittedAt': 'Submitted', 'reference': 'Reference', 'figmaUrl': 'Figma file URL', 'siteName': 'Advisor or site name',
        'requester': 'Requested by', 'email': 'Contact email', 'deadline': 'Needed by', 'theme': 'Brand / theme',
        'pages': 'Pages needed', 'notes': 'Notes', 'requestType': 'Request type', 'status': 'Status', 'page': 'Sent from page'},
        'Send to MarTech Engineering'),
    'incoming': FIGMA_COLUMNS,
    'README': readme(FORM_README + [
        'MarTech Engineering: turn on Tools > Notification settings > "Any changes are made" to get an email for every new request.',
        'Update the status column as the request moves: New, Scoped, In build, In review, Done.',
    ]),
}

SHEETS['forms/layout-change-requests'] = {
    'shared-aem': form_definition(LAYOUT_COLUMNS, {
        'submittedAt': 'Submitted', 'reference': 'Reference', 'site': 'Site', 'pagePath': 'Page', 'change': 'Change type',
        'requester': 'Requested by', 'details': 'Details', 'status': 'Status', 'page': 'Sent from page'},
        'Send request'),
    'incoming': LAYOUT_COLUMNS,
    'README': readme(FORM_README),
}
