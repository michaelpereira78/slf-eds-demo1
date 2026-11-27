"""Content for /michael-pereira/: an internal demo replica of a Sun Life advisor site
(layout modelled on https://advisor.sunlife.ca/ben.aldridge/), personalised for Michael Pereira.

Contact details are FICTIONAL placeholders (555 numbers, example.com email, example street).
Rendered by tools/michael-pereira/build.py into drafts/, Word documents and da.live HTML.
"""
BASE = '/michael-pereira'
NAME = 'Michael Pereira'
PHONE = '(519) 555-0100'
TEL = 'tel:5195550100'
EMAIL = 'michael.pereira@example.com'
ADDRESS = ['100 Example Street, Suite 200', 'Cambridge, ON N1R 0A0', 'Canada']
MAP_QUERY = 'Cambridge, Ontario'
BOOK = f'{BASE}/connect#lets-connect'


def p(*runs):
    return ('p', list(runs))


def a(text, href, kind='a'):
    return ('p', [(kind, text, href)])


def photo(name, alt):
    return ('photo', name, alt)


def block(name, rows):
    return ('block', name, rows)


def style(s):
    return ('block', 'Section Metadata', [[[('p', ['Style'])], [('p', [s])]]])


def meta(title, desc, **extra):
    m = {
        'Title': f'{title} | {NAME} | Sun Life advisor demo',
        'Description': desc,
        'Template': 'sunlife-advisor',
        'Nav': f'{BASE}/nav',
        'Footer': f'{BASE}/footer',
    }
    m.update(extra)
    return m


def banner(img, alt, heading, text, cta=None, href=f'{BASE}/connect'):
    """Home has a button; subpages (like the original) do not, which makes the banner shorter."""
    content = [('h1', heading), p(text)] + ([a(cta, href, 'b-a')] if cta else [])
    return [block('Advisor Banner', [[[photo(img, alt)], content]])]


def cta_box():
    return [block('CTA Box', [[[photo('mp-meeting', 'An advisor reviewing a plan with clients')],
                               [('h2', 'Have questions?'),
                                p('Here to help answer your questions, provide clarity about products and get you '
                                  'started on the road to achieving your goals.'),
                                a('Let\u2019s connect', f'{BASE}/connect')]]])]


def profile():
    return [block('Advisor Profile', [[
        [photo('mp-headshot-placeholder', f'Placeholder headshot for {NAME}')],
        [('h2', NAME),
         p('Job title: Financial Advisor, Sun Life'),
         p('Demo profile for internal use'),
         p('Languages spoken: English, Portuguese'),
         p('Area(s) served: Cambridge, Kitchener-Waterloo, Guelph and Waterloo Region'),
         a('Book an appointment', BOOK),
         ('ul', [[('a', 'Facebook', 'https://www.facebook.com/')],
                 [('a', 'Instagram', 'https://www.instagram.com/')],
                 [('a', 'LinkedIn', 'https://www.linkedin.com/')]])],
    ]])]


def office():
    return [('h2', 'Office information'),
            block('Office Map', [[
                [p(MAP_QUERY)],
                [('h3', 'Cambridge, Ontario'),
                 p(('b', 'Phone:')), p(('a', PHONE, TEL)),
                 p(('b', 'Email:')), p(('a', EMAIL, f'mailto:{EMAIL}')),
                 p(('b', 'Address:')),
                 p(('a', ', '.join(ADDRESS), 'https://www.google.com/maps/search/?api=1&query=Cambridge%2C+Ontario'))],
            ]])]


def lead_form():
    return [block('Lead Form', [[[('h2', 'Let\u2019s connect'),
                                  p('All fields below are required unless labeled optional.')]]])]


NEWS = [
    ('mp-card-family', 'Illustration: You\u2019re building a family', None, [
        p('Being a young parent means juggling everything.'),
        p('You\u2019re:'),
        p('- Building a career'), p('- Raising kids'), p('- Trying to save something'), p('- Running on coffee & hope'),
        p('Young families who plan ahead don\u2019t just survive, they thrive.'),
        p('From protecting your income to planning for education, smart money moves now mean more freedom later. '
          'I\u2019m here to help.'),
        p('Let\u2019s talk about your family\u2019s future.'),
    ]),
    ('mp-card-wealth', 'Illustration: Your wealth tells a story', None, [
        p('Building wealth is an accomplishment. Deciding what comes next deserves just as much attention.'),
        p('Whether you\u2019re thinking about retirement, your family, charitable giving or the legacy you\u2019d like to '
          'leave behind, a well-rounded financial strategy can help you move forward with confidence.'),
        p('Let\u2019s connect to discuss your priorities.'),
    ]),
    ('mp-card-cii', 'Video: 6 ways to use your critical illness insurance payout',
     '6 ways to use your critical illness insurance payout', [
         p('A critical illness can affect more than your health. It can affect your income, your expenses and how '
           'much time you\u2019re able to take away from work.'),
         p('That\u2019s where critical illness insurance can help. The payout is yours to use based on what you need most.'),
         p('Why bundle critical illness insurance with life insurance?'),
         p('\u2022 Life insurance helps protect your loved ones when you\u2019re gone.'),
         p('\u2022 Critical illness insurance helps protect you and your loved ones while you\u2019re still here.'),
         p('Reach out if you\u2019d like to learn more.'),
         p('*Terms and conditions apply.'),
         a('Watch video', 'https://www.sunlife.ca/en/health/critical-illness-insurance/'),
     ]),
    ('mp-card-retirement', 'Illustration: Retirement is a journey', 'Retirement is a journey, not a date', [
        p('Retirement doesn\u2019t start on a single day. It\u2019s a series of choices about when to slow down, where '
          'your income will come from and how to keep your plan flexible.'),
        p('Let\u2019s map out the next 5, 10 and 20 years together.'),
    ]),
    ('mp-card-budget', 'Illustration: Small habits, big savings', 'Small habits, big savings', [
        p('A coffee a day, a forgotten subscription, an unused gym pass. Small amounts add up.'),
        p('A simple budget can free up money for your TFSA or RRSP without changing how you live.'),
    ]),
]


def news_rows(items):
    rows = []
    for img, alt, title, body in items:
        cell = ([('h3', title)] if title else []) + body
        rows.append([[photo(img, alt)], cell])
    return rows


PAGES = {}

PAGES['index'] = {
    'metadata': meta('Home', f'{NAME} is a Sun Life Financial Advisor in Cambridge, Ontario (internal demo replica).',
                     **{'Compliance Status': 'Pending review', 'Reviewer': 'R. Castillo, Compliance',
                        'Review Date': '2026-11-26', 'Compliance ID': 'CR-2026-0457'}),
    'sections': [
        banner('hero-mp-autumn-walk', 'A mother and daughter walking through an autumn forest',
               'Help maximize your savings',
               'RRSP + TFSA = A powerful combo to help lower your taxes and build tax-free growth.',
               cta='Let\u2019s connect'),
        profile(),
        [style('intro'),
         p('I help families and business owners in Cambridge and Waterloo Region turn big goals into simple, '
           'step-by-step plans. Before becoming an advisor, I spent years leading teams and solving problems, so I '
           'know how much clear advice and good follow-up matter.'),
         p('My approach is straightforward: listen first, explain every option in plain language and build a plan '
           'that brings your savings, investments and insurance together. I review it with you every year so it '
           'keeps up with your life.'),
         a('View more options', f'{BASE}/about')],
        [('h2', 'Let\u2019s work together!'),
         block('Media Text (video)', [[
             [photo('mp-video-intro', 'Video: Meet Michael Pereira')],
             [p('My mission is to help families make confident financial decisions by keeping things simple and easy '
                'to understand. When we work together, I want you to feel at ease about the future and clear on the '
                'next step.'),
              p('Let\u2019s work together to build your savings, protect your family and live a healthier life. I\u2019ll '
                'develop a holistic plan that provides a mix of income, savings and insurance protection options. '
                'Whether it\u2019s through life insurance, health insurance or an investment strategy, I\u2019ll help you '
                'build lifetime financial security.'),
              p('My office is in Cambridge, Ontario. I serve Cambridge, Kitchener-Waterloo, Guelph and the surrounding '
                'area. I offer both in-person and virtual appointments. ', ('b-a', 'Contact my office',
                                                                          f'{BASE}/connect'), ' to get started.')],
         ]])],
        [block('Media Text', [
            [[photo('mp-coffee', 'Two cups of coffee on a sunlit table')],
             [('h2', 'Products and services'),
              p('Browse through the product and services offerings below to learn more. Every financial and protection '
                'strategy is different. When we meet, we\u2019ll discuss what might be right for your unique situation. '
                'Reach out if you have any questions or are ready to get started.'),
              ('h3', 'Health insurance products'),
              p('Health insurance gives you financial coverage to help pay for health-care needs. This insurance goes '
                'above and beyond Canadian health-care coverage.'),
              ('h3', 'Life insurance products'),
              p('Life insurance allows you to protect the people you love by providing your beneficiaries a tax-free '
                'cash payment when you die.'),
              ('h3', 'Saving, budgeting and investing'),
              p('Reaching your financial goals starts with a budget and savings plan. Let\u2019s make your money go '
                'further.'),
              a('Learn more', f'{BASE}/products-services')]],
        ]),
         block('Media Text (right, video)', [[[photo('mp-video-products', 'Video: How a plan comes together')]]])],
        [style('header-link'), ('h2', 'Stay informed'), a('See more articles', f'{BASE}/stay-informed'),
         block('Info Cards (news)', news_rows(NEWS[:3]))],
        office(),
        lead_form(),
    ],
}

PAGES['about'] = {
    'metadata': meta('About', f'About {NAME}, Sun Life Financial Advisor in Cambridge, Ontario (internal demo).'),
    'sections': [
        banner('hero-mp-boardwalk', 'A family walking hand in hand on a boardwalk',
               'Helping you reach your health and wealth goals.',
               'Let\u2019s work together towards your financial goals while protecting what matters most to you.'),
        [style('intro'), ('h2', 'Sound financial advice to help build lasting security'),
         p('Take the first step toward financial peace. Whether you\u2019re planning for retirement, building wealth, or '
           'protecting your family\u2019s future, I combine in-depth knowledge with genuine care to help you protect '
           'what matters most. Get answers to your toughest financial questions and build a strategy that works for you.'),
         p('One conversation can reveal opportunities you didn\u2019t know were possible. Reach out and connect with me '
           'to build your financial roadmap together.')],
        [block('Media Text', [[[photo('mp-family', 'A family walking together on a boardwalk')]]])],
        [block('Media Text', [[[photo('mp-headshot-placeholder', 'Placeholder headshot for the advisor assistant')],
                               [('h2', 'Jamie Silva'),
                                p('As an Advisor Assistant, I\u2019m often your first hello. I coordinate meetings, '
                                  'paperwork and follow-ups so nothing falls through the cracks, and I make sure your '
                                  'information is always up to date.'),
                                p('Job title: Advisor Assistant, Sun Life (fictional demo profile)'),
                                p('Languages spoken: English'),
                                p(('b', 'Phone: '), ('a', '(519) 555-0101', 'tel:5195550101')),
                                p(('b', 'Email: '), ('a', 'jamie.silva@example.com', 'mailto:jamie.silva@example.com')),
                                a('Book an appointment', BOOK)]]])],
        [block('Media Text', [[[photo('mp-planning', 'A couple reviewing their plan')],
                               [('h2', 'Giving back'),
                                p('Outside the office, I volunteer with local youth sports and support community food '
                                  'drives in Cambridge. I enjoy speaking to community groups about budgeting, saving for '
                                  'a first home and planning for retirement.'),
                                p('When I\u2019m not working, you\u2019ll find me with my family, on a trail along the '
                                  'Grand River or cheering on the Toronto Maple Leafs.')]]])],
        cta_box(),
    ],
}

PAGES['products-services'] = {
    'metadata': meta('Products and services', 'Insurance, investment and planning products (internal demo).'),
    'sections': [
        banner('hero-mp-meeting', 'An advisor meeting with clients at home',
               'You don\u2019t need a stress ball \u2013 you need an advisor',
               'The right advice can help you feel more confident about your financial decisions. Get clarity. '
               'Partner right.'),
        [style('intro'), ('h2', 'Tools and calculators'),
         p(('b-a', 'Life insurance calculator',
            'https://www.sunlife.ca/en/tools-and-resources/tools-and-calculators/life-insurance-calculator/'),
           ' - In just 2 minutes, calculate how much life insurance you may need.'),
         p(('b-a', 'Retirement savings calculator',
            'https://www.sunlife.ca/en/tools-and-resources/tools-and-calculators/retirement-savings-calculator/'),
           ' - Find out how much you will need to save for retirement and if you\u2019re on track.'),
         p(('b-a', 'Budget calculator',
            'https://www.sunlife.ca/en/tools-and-resources/tools-and-calculators/budget-calculator/'),
           ' - Use this monthly budget calculator to help you manage your spending.')],
        [('h2', 'Services'),
         block('Info Cards (plain)', [
             [[('h3', 'Business protection & planning'),
               p('A business plan should adapt as your business moves through its stages. Let\u2019s protect your '
                 'hard work.'), a('Get started now', f'{BASE}/connect')]],
             [[('h3', 'Financial planning'),
               p('Let\u2019s create a plan that brings together investment planning, tax planning, risk management and '
                 'a retirement strategy.'), a('Get started now', f'{BASE}/connect')]],
             [[('h3', 'Life and health insurance'),
               p('Protect what matters most to you so you can feel prepared no matter what life throws your way.'),
               a('Get started now', f'{BASE}/connect')]],
         ])],
        [('h2', 'Health insurance products'),
         p('Health insurance gives you financial coverage to help pay for health-care needs. This insurance goes '
           'above and beyond Canadian health-care coverage.'),
         block('Info Cards', [
             [[photo('mp-family', 'A family outdoors')],
              [('h3', 'Personal and family health insurance'),
               p('Coverage to help pay for prescription drugs, dental care, vision care and more.'),
               a('Find out more', 'https://www.sunlife.ca/en/health/')]],
             [[photo('mp-meeting', 'An advisor meeting with clients')],
              [('h3', 'Disability insurance'),
               p('Helps protect you financially by replacing a portion of your income if you can\u2019t work because '
                 'of an illness or injury.'),
               a('Find out more', 'https://www.sunlife.ca/en/health/disability-insurance/')]],
             [[photo('mp-retirement', 'A couple walking on a beach')],
              [('h3', 'Critical illness insurance'),
               p('A lump-sum payment you can use as you choose if you\u2019re diagnosed with a covered illness.'),
               a('Find out more', 'https://www.sunlife.ca/en/health/critical-illness-insurance/')]],
         ])],
        [('h2', 'Life insurance products'),
         p('Life insurance allows you to protect the people you love by providing your beneficiaries a tax-free cash '
           'payment when you die.'),
         block('Info Cards', [
             [[photo('mp-planning', 'A couple signing documents')],
              [('h3', 'Term life insurance'),
               p('Affordable protection for a set period of time, such as while you pay off a mortgage or raise a '
                 'family.'), a('Find out more', 'https://www.sunlife.ca/en/insurance/life/term-life-insurance/')]],
             [[photo('mp-coffee', 'Two cups of coffee on a table')],
              [('h3', 'Permanent life insurance'),
               p('Lifelong coverage to protect your loved ones that never expires, no matter your age or health.'),
               a('Find out more', 'https://www.sunlife.ca/en/insurance/life/permanent-life-insurance/')]],
             [[photo('mp-family', 'A family outdoors')],
              [('h3', 'Participating life insurance'),
               p('Lifetime insurance, cash-value growth and the chance to earn dividends.'),
               a('Find out more',
                 'https://www.sunlife.ca/en/insurance/life/permanent-life-insurance/participating/')]],
         ])],
        cta_box(),
    ],
}

PAGES['stay-informed'] = {
    'metadata': meta('Stay informed', 'Articles and posts from Michael Pereira (internal demo).'),
    'sections': [
        banner('hero-mp-planning', 'A couple planning with their advisor', 'One plan for you',
               'Create holistic and personalized actionable steps to reach your goals.'),
        [style('intro'), ('h2', 'Stay informed'),
         p('Browse posts that might be helpful to you. Come back regularly, as this page is kept up to date with '
           'timely topics.')],
        [block('Info Cards (news)', news_rows(NEWS))],
        cta_box(),
    ],
}

PAGES['resources'] = {
    'metadata': meta('Resources', 'Tools, calculators and partners (internal demo).'),
    'sections': [
        banner('hero-mp-retirement', 'A couple walking along a beach', 'Turning your retirement dreams into a reality.',
               'Helping you feel confident in your future because you deserve to retire the way you want to.'),
        [style('intro'), ('h2', 'Resources'),
         p('Looking for more information to help kickstart your financial journey? Find tools and calculators, '
           'informative pages and more.')],
        [('h2', 'Tools and calculators'),
         p('Make planning for your financial future and retirement easier with some of our tools and calculators.'),
         block('Info Cards', [
             [[photo('mp-retirement', 'A couple walking on a beach')],
              [('h3', 'Retirement savings calculator'),
               p('Calculate how well your retirement savings align with what you can expect to spend.'),
               a('Try now', 'https://www.sunlife.ca/en/tools-and-resources/tools-and-calculators/retirement-savings-calculator/')]],
             [[photo('mp-family', 'A family outdoors')],
              [('h3', 'Life insurance calculator'),
               p('Calculate how much life insurance you\u2019ll need to help your loved ones cover financial '
                 'responsibilities.'),
               a('Try now', 'https://www.sunlife.ca/en/tools-and-resources/tools-and-calculators/life-insurance-calculator/')]],
             [[photo('mp-coffee', 'Two cups of coffee on a table')],
              [('h3', 'Budget calculator'),
               p('Find out where your money is going with this easy-to-use household budget calculator.'),
               a('Try now', 'https://www.sunlife.ca/en/tools-and-resources/tools-and-calculators/budget-calculator/')]],
         ])],
        [('h2', 'Partners'),
         block('Info Cards', [
             [[photo('mp-headshot-placeholder', 'Placeholder headshot')],
              [('h3', 'Estate & Financial Planning Services'),
               p('Sun Life\u2019s estate and financial planning consultants work with me on complex cases: wills, '
                 'trusts, estate planning, business succession and tax. (Demo placeholder: real partner profiles '
                 'would go here.)'),
               a('Learn more', 'https://www.sunlife.ca/en/tools-and-resources/financial-planning-and-advice/')]],
         ])],
        cta_box(),
    ],
}

PAGES['connect'] = {
    'metadata': meta('Connect', f'Contact {NAME} (internal demo).'),
    'sections': [
        banner('hero-mp-autumn-walk', 'A mother and daughter walking through an autumn forest',
               'Grow your wealth while protecting what matters most.',
               'Let\u2019s assess your short and long-term goals and create a strategy that you can feel confident in.'),
        [style('intro'), ('h2', 'Let\u2019s connect'),
         p('Whether you\u2019re curious about a specific product, have questions about how we work together or are '
           'ready to get started on a plan, let\u2019s connect. Reach out by phone, email or the contact form.')],
        profile(),
        office(),
        lead_form(),
        cta_box(),
    ],
}

PAGES['nav'] = {
    'sections': [
        [a('Sunlife', f'{BASE}/')],
        [('ul', [[('a', 'Home', f'{BASE}/')], [('a', 'About', f'{BASE}/about')],
                 [('a', 'Products and services', f'{BASE}/products-services')],
                 [('a', 'Stay informed', f'{BASE}/stay-informed')], [('a', 'Resources', f'{BASE}/resources')],
                 [('a', 'Connect', f'{BASE}/connect')]])],
        [p(('a', 'my Sunlife (Client sign in)', 'https://www.sunnet.sunlife.com/signin/mysunlife/home.wca')),
         p(('a', 'Support', 'https://www.sunlife.ca/en/support/'))],
    ],
}

PAGES['footer'] = {
    'sections': [
        [('h2', 'Making life brighter'),
         p('Advisors and their corporations conduct insurance business through Sun Life Financial Distributors '
           '(Canada) Inc.'),
         p('Mutual fund business is done with your advisor through Sun Life Financial Investment Services (Canada) Inc.'),
         p('\u00a9 Sun Life Assurance Company of Canada. All rights reserved.')],
        [('ul', [[('a', 'Legal', 'https://www.sunlife.ca/slf/PSLF+Canada/Legal?vgnLocale=en_CA')],
                 [('a', 'Privacy', 'https://www.sunlife.ca/slf/PSLF+Canada/Privacy?vgnLocale=en_CA')],
                 [('a', 'Security', 'https://www.sunlife.ca/slf/PSLF+Canada/Security?vgnLocale=en_CA')],
                 [('a', 'Accessibility', 'https://www.sunlife.ca/ca/About+us/Accessibility+commitment?vgnLocale=en_CA')],
                 [('a', 'Complaint Handling Procedures', 'https://www.sunlife.ca/en/about-us/complaint-handling/')]])],
        [p('Internal demo replica built on AEM Edge Delivery Services. Not a live advisor site: contact details are '
           'placeholders. Photos: Pexels.')],
    ],
}
