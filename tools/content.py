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
    ('1. Generate a new website', 'Fill in a short request form and pick a theme and template. The platform '
     'team turns it into a ready-to-edit folder of documents in minutes.', 'Open the site request form', '/new-site'),
    ('2. Make content changes', 'Advisors edit the Word or Google Doc and click Preview. After approval a supervisor '
     'publishes, and it is live worldwide in seconds.', 'Open the advisor workspace', '/advisor'),
    ('3. Make minor layout changes', 'Change a section style (Light, Dark, Centered, Sidebar) or a block '
     'variant by typing one word in the document.', 'See the layout gallery', '/layouts'),
    ('4. Use approved templates', 'Start every page from an approved template: Advisor team, Solo advisor '
     'or Campaign. Developers can add new ones without touching existing sites.', 'Browse approved templates', '/templates'),
    ('5. Apply a brand theme', 'Each site picks a theme with one metadata value. Same platform, different look.',
     'See Harbourview (Harbour theme)', '/harbourview/'),
    ('6. Reuse approved content', 'Product descriptions, calls to action and disclosures are written once by '
     'Compliance and reused everywhere.', 'Open the approved content library', '/approved-content'),
    ('7. Compliance review and approval', 'Advisors submit for review; supervisors approve or send back changes '
     'and publish. Every step is logged in an audit sheet.', 'Open the supervisor console', '/admin'),
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
        [
            ('h2', 'Two workspaces, two roles'),
            ('p', ['Advisors maintain their own sites; supervisors approve, publish and grow the platform.']),
            ('block', 'Cards (Actions)', action_rows([
                ('edit', 'Advisor workspace', 'Edit and preview your site, use approved content and templates, request layout '
                 'changes, submit for compliance review and track your submissions. Author role: no publishing.',
                 'Open the advisor workspace', '/advisor'),
                ('approve', 'Supervisor console', 'Approve submissions, publish, create new advisor sites from templates, make '
                 'advanced layout updates and import custom designs from Figma. Publish role.',
                 'Open the supervisor console', '/admin'),
            ])),
            section_style('Light'),
        ],
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
# WORKSPACES: advisor landing page and supervisor / admin console
# =====================================================================
DRIVE_AUDIT_LOG = 'https://drive.google.com/drive/search?q=compliance-audit-log'

PAGES['advisor'] = {
    'metadata': {
        'Title': 'Advisor workspace | Advisor Demo',
        'Description': 'Everything an advisor needs to keep their own website current: edit, preview, '
                       'approved content, layout requests and compliance review.',
        'Theme': 'Forest',
        'Robots': 'noindex',
    },
    'sections': [
        [('block', 'Hero (Light)', [[[
            ('p', ['Advisor workspace']),
            ('h1', 'Keep your website current, without a developer'),
            ('p', ['Edit your pages in Google Docs, preview them, reuse approved wording and send changes to '
                   'Compliance, all from here. You author and preview; your supervisor publishes once '
                   'Compliance approves.']),
            link_p('Submit a change for review', '/advisor#submit-for-compliance-review', 'b-a'),
            link_p('See my submissions', '/advisor#my-submissions', 'i-a'),
        ]]])],
        [
            ('h2', 'What do you want to do?'),
            ('block', 'Cards (Actions)', action_rows([
                ('edit', 'Edit a page', 'Open the page\u2019s Google Doc from your site folder in Drive, make the change, then click Preview in Sidekick.', 'How to edit', '/advisor#how-to-update-your-site'),
                ('add', 'Add a new page', 'Copy an approved template (Advisor team, Solo advisor or Campaign) into your folder and fill in the brackets.', 'Browse templates', '/templates'),
                ('library', 'Use approved content', 'Paste Compliance-approved product wording, calls to action and the disclosure. You cannot change the wording.', 'Open the library', '/approved-content'),
                ('preview', 'Preview your changes', 'Preview shows your edits on a private address in seconds. Nothing is public until your supervisor publishes.', 'Open my site preview', '/harbourview/'),
                ('layout', 'Change the layout', 'Switch a section style or block variant yourself, or ask your supervisor for anything bigger.', 'Request a layout change', '/advisor#request-a-layout-change'),
                ('review', 'Submit for compliance review', 'Send the page to Compliance with a short note. Every submission is recorded in the audit log.', 'Submit for review', '/advisor#submit-for-compliance-review'),
                ('status', 'Track my submissions', 'See what is with Compliance, what was approved, and what came back with notes.', 'My submissions', '/advisor#my-submissions'),
                ('help', 'Get help', 'Answers to common questions, and who to contact when you are stuck.', 'Help and FAQ', '/advisor#help-and-faq'),
            ])),
        ],
        [
            ('block', 'Columns', [[
                [('h3', 'You can'), ('ul', [
                    ['Edit your own pages in Google Docs or Word'],
                    ['Preview changes on your private preview address'],
                    ['Use approved content and approved templates'],
                    ['Change section styles and block variants'],
                    ['Submit pages for compliance review'],
                ])],
                [('h3', 'Your supervisor does'), ('ul', [
                    ['Approves your changes with Compliance'],
                    ['Publishes approved pages to your live site'],
                    ['Makes advanced layout, theme and template changes'],
                    ['Creates new advisor sites and Figma imports'],
                ])],
            ]]),
            ('p', [('i', 'Publish is greyed out for advisors in Sidekick. This is enforced by the platform\u2019s '
                         'role settings, not just hidden: an advisor account has the author role, which cannot publish.')]),
            section_style('Light'),
        ],
        [
            ('h2', 'Submit for compliance review'),
            ('p', ['Finished a change? Tell Compliance what changed. The page joins the review queue and the '
                   'submission is written to the compliance audit log (date, advisor, site, page, summary).']),
            ('block', 'Request Form', [[[('p', ['Form'])], [('p', ['compliance-review'])]]]),
            ('p', [('i', 'Tip: you can also click Request compliance review in Sidekick, or Request review in the '
                         'status bar at the bottom of any preview page.')]),
        ],
        [
            ('h2', 'My submissions'),
            ('p', ['Your pages in the review process. Changes requested? Edit the page, Preview, then submit again.']),
            ('block', 'Compliance Queue (Mine)', [[[('p', ['My submissions'])]]]),
            section_style('Light'),
        ],
        [
            ('h2', 'Request a layout change'),
            ('p', ['Need something you cannot do with a section style? Describe it here and your supervisor will '
                   'pick it up (or pass it to MarTech Engineering).']),
            ('block', 'Request Form', [[[('p', ['Form'])], [('p', ['layout-change'])]]]),
        ],
        [
            ('h2', 'How to update your site'),
            ('block', 'Cards (Steps)', [
                [[('h3', 'Open the doc'), ('p', ['In Google Drive, open your site folder and the page\u2019s document (index is your home page).'])]],
                [[('h3', 'Make the change'), ('p', ['Edit text, swap a photo, or paste approved content from Sidekick > Library.'])]],
                [[('h3', 'Preview'), ('p', ['Click Preview in Sidekick. Your private preview updates in about three seconds.'])]],
                [[('h3', 'Submit for review'), ('p', ['Click Request compliance review and say what changed.'])]],
                [[('h3', 'Supervisor publishes'), ('p', ['After approval your supervisor publishes, and the live site updates worldwide.'])]],
            ]),
            section_style('Dark'),
        ],
        [
            ('h2', 'Help and FAQ'),
            ('block', 'Accordion', [
                [[('p', ['Why can\u2019t I publish?'])],
                 [('p', ['Advisor accounts have the author role: edit and preview only. Publishing is reserved for '
                         'supervisors so that only Compliance-approved content reaches the live site.'])]],
                [[('p', ['How do I change my photo?'])],
                 [('p', ['In the Team Cards table, click the photo in the first column, replace it with your new '
                         'picture (Insert > Image), then Preview.'])]],
                [[('p', ['How do I add approved product wording?'])],
                 [('p', ['Sidekick > Library > Approved content > Copy link, then paste the link on its own line. '
                         'Or copy the link from the approved content page.']), link_p('Approved content library', '/approved-content')]],
                [[('p', ['My change is not showing on the preview'])],
                 [('p', ['Wait five seconds and click Preview again; Google Docs saves in the background. Still '
                         'stuck? Check you edited the document in your own site folder.'])]],
                [[('p', ['Who do I contact?'])],
                 [('p', ['Your supervisor for content and layout questions; MarTech Engineering '
                         '(martech-engineering@example.com) for anything technical.'])]],
            ]),
            section_style('Narrow'),
        ],
    ],
}

PAGES['admin'] = {
    'metadata': {
        'Title': 'Supervisor console | Advisor Demo',
        'Description': 'Approve advisor content, publish, create advisor websites from templates, make advanced '
                       'layout updates and request custom designs from Figma.',
        'Theme': 'Forest',
        'Robots': 'noindex',
    },
    'sections': [
        [('block', 'Hero (Light)', [[[
            ('p', ['Supervisor and admin console']),
            ('h1', 'Approve, publish and grow your advisor sites'),
            ('p', ['Review what advisors submitted, publish approved updates, launch new sites from approved '
                   'templates, and send custom designs to MarTech Engineering.']),
            link_p('Open the approval queue', '/admin#approval-queue', 'b-a'),
            link_p('Import a design from Figma', '/admin/figma-import', 'i-a'),
        ]]])],
        [
            ('h2', 'Console'),
            ('block', 'Cards (Actions)', action_rows([
                ('approve', 'Approve content', 'Approve or send back pages advisors submitted for compliance review.', 'Approval queue', '/admin#approval-queue'),
                ('publish', 'Publish approved updates', 'Publish approved pages to the live site. Only the publish role can do this.', 'How to publish', '/admin#publish-approved-updates'),
                ('template', 'Create a new advisor website', 'Pick a template and theme; the platform generates the starter site.', 'Pick a template', '/admin#create-a-new-advisor-website'),
                ('layout', 'Advanced layout updates', 'Themes, templates, navigation, footers and new blocks for any advisor site.', 'Layout tools', '/admin#advanced-layout-updates'),
                ('figma', 'Import a design from Figma', 'Send a Figma file to MarTech Engineering for an agentic Figma-to-EDS build.', 'Start a Figma import', '/admin/figma-import'),
                ('audit', 'Compliance audit log', 'Every submission, approval and publish, in a Google Sheet for audits.', 'View the audit log', '/admin#compliance-audit-log'),
            ])),
        ],
        [
            ('h2', 'Approval queue'),
            ('p', ['Pages advisors submitted for review. Approve or Request changes; each decision is added to the '
                   'compliance audit log.']),
            ('block', 'Compliance Queue', [[[('p', ['Review queue'])]]]),
            section_style('Light'),
        ],
        [
            ('h2', 'Publish approved updates'),
            ('ol', [
                ['Open the approved page\u2019s preview (Open preview in the queue).'],
                ['Click Publish in Sidekick. It is only enabled for the publish role; advisors see it greyed out.'],
                ['The live site updates worldwide in seconds, and the Published event is added to the audit log.'],
            ]),
            ('p', ['Publishing many pages at once (for example a new site launch): select the documents in Google '
                   'Drive and use Sidekick\u2019s bulk Publish.']),
            ('p', [('i', 'Enforced by the platform: the Admin API rejects a publish from any account without the '
                         'publish role, whether it comes from Sidekick, a script or a bookmark.')]),
            section_style('Narrow'),
        ],
        [
            ('h2', 'Create a new advisor website'),
            ('p', ['Pick an approved template. The request form opens with it selected; choose the theme and '
                   'the platform generates the site\u2019s starter documents.']),
            ('block', 'Cards (Templates)', [
                [[('h3', name), ('p', [desc]), link_p('See an example', ex), link_p('Use this template', f'/new-site?template={key}')]]
                for name, key, desc, ex, _start in TEMPLATES
            ]),
            section_style('Light'),
        ],
        [
            ('h2', 'Advanced layout updates'),
            ('p', ['Changes beyond an advisor\u2019s section styles. All are made in documents or metadata, '
                   'so they are previewed and approved like any other change.']),
            ('block', 'Cards (Services)', service_rows([
                ('layout', 'Switch theme or template', 'Change the Theme or Template value in a page\u2019s metadata, or for a whole site at once.'),
                ('template', 'Navigation and footer', 'Edit the site\u2019s nav and footer documents: menu items, contact details, links.'),
                ('add', 'Add blocks', 'Stats, testimonials, banners, service cards and steps from Sidekick > Library > Blocks.'),
                ('figma', 'New block or template', 'Need something new? MarTech Engineering adds it once for every site.'),
            ])),
            link_p('See every section style and block variant', '/layouts', 'i-a'),
            ('h3', 'Layout change requests from advisors'),
            ('block', 'Submissions', [[[('p', ['Form'])], [('p', ['layout-change'])]]]),
        ],
        [
            ('h2', 'Import a custom website design from Figma'),
            ('p', ['Have a custom design for an advisor or a campaign? Send the Figma file to MarTech Engineering. '
                   'Their agentic Figma-to-EDS process maps the design to approved blocks, builds anything new, '
                   'and hands it back for review.']),
            ('block', 'Cards (Steps)', [
                [[('h3', 'Send the Figma file'), ('p', ['Fill in the import form: file link, site, pages and deadline.'])]],
                [[('h3', 'Scope confirmed'), ('p', ['MarTech Engineering replies with scope and timeline, usually within two business days.'])]],
                [[('h3', 'Agentic build'), ('p', ['AI agents map the design to blocks and draft new code; developers review every change.'])]],
                [[('h3', 'Review and publish'), ('p', ['You review the preview, Compliance approves, then you publish.'])]],
            ]),
            link_p('Import a design from Figma', '/admin/figma-import', 'b-a'),
            section_style('Dark'),
        ],
        [
            ('h2', 'Compliance audit log'),
            ('p', ['Every compliance submission, approval, request for changes and publish is appended to the '
                   'compliance-audit-log Google Sheet in Drive (incoming tab): timestamp, event, advisor, site, '
                   'page, change summary, submitted by, status, reviewer and decision date.']),
            ('block', 'Submissions', [
                [[('p', ['Form'])], [('p', ['compliance-audit'])]],
                [[('p', ['Sheet'])], [('p', [('a', 'compliance-audit-log', DRIVE_AUDIT_LOG)])]],
            ]),
            section_style('Light'),
        ],
        [
            ('h2', 'Roles and permissions'),
            ('block', 'Cards (Services)', service_rows([
                ('users', 'Advisor: author role', 'Edit, preview, delete their drafts and request reviews. Cannot publish or change site configuration.'),
                ('approve', 'Supervisor: publish role', 'Everything an advisor can do, plus publish and unpublish, review snapshots and bulk publishing.'),
                ('lock', 'Platform admin: admin role', 'Site configuration, roles, new sites and integrations. MarTech Engineering and the platform owner.'),
            ])),
            ('p', [('i', 'Roles are set once in the site\u2019s access configuration (docs/access-admin.json in the '
                         'repository) and enforced by the platform for every request.')]),
        ],
    ],
}

PAGES['admin/figma-import'] = {
    'metadata': {
        'Title': 'Import a design from Figma | Supervisor console',
        'Description': 'Request a custom advisor website design build from a Figma file. Sent to MarTech Engineering.',
        'Theme': 'Forest',
        'Robots': 'noindex',
    },
    'sections': [
        [('block', 'Hero (Light)', [[[
            ('p', ['Supervisor console \u00b7 MarTech Engineering intake']),
            ('h1', 'Import a custom website design from Figma'),
            ('p', ['Tell MarTech Engineering what to build. They run their agentic Figma-to-EDS process, '
                   'reuse approved blocks wherever possible, and send you a preview to review.']),
            link_p('Back to the console', '/admin', 'i-a'),
        ]]])],
        [
            ('block', 'Request Form', [
                [[('p', ['Form'])], [('p', ['figma-import'])]],
            ]),
        ],
        [
            ('h2', 'What happens next'),
            ('block', 'Cards (Steps)', [
                [[('h3', 'Intake'), ('p', ['Your request lands in the MarTech Engineering intake sheet with a reference number.'])]],
                [[('h3', 'Scope and timeline'), ('p', ['The team checks the Figma file and replies by email with scope and a date.'])]],
                [[('h3', 'Agentic build'), ('p', ['Agents map frames to blocks and themes and draft any new code. A developer reviews every change.'])]],
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
