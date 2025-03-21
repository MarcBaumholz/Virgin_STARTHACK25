from flask import Blueprint, render_template, jsonify, request

# Create blueprint
bp = Blueprint('main', __name__)

# Dummy data for testing
COMPANIES = [
    {'id': 1, 'name': 'Virgin Atlantic', 'logo_url': 'https://via.placeholder.com/150'},
    {'id': 2, 'name': 'Virgin Atlantic & Virgin Unite', 'logo_url': 'https://via.placeholder.com/150'},
    {'id': 3, 'name': 'Virgin Voyages', 'logo_url': 'https://via.placeholder.com/150'},
    {'id': 4, 'name': 'Virgin Media O2', 'logo_url': 'https://via.placeholder.com/150'},
    {'id': 5, 'name': 'Virgin Limited Edition (VLE) & Virgin Unite', 'logo_url': 'https://via.placeholder.com/150'},
    {'id': 6, 'name': 'Virgin Unite', 'logo_url': 'https://via.placeholder.com/150'},
    {'id': 7, 'name': 'Eve Branson Foundation', 'logo_url': 'https://via.placeholder.com/150'},
    {'id': 8, 'name': 'Unite BVI', 'logo_url': 'https://via.placeholder.com/150'},
]

INITIATIVES = [
    {
        'id': 1,
        'company_id': 1,
        'title': 'Youngest, Cleanest Fleet in the Sky',
        'description': 'Virgin Atlantic is working to accelerate the development of sustainable fuels. On November 28th, we made history with Flight100 becoming the first commercial airline to fly across the Atlantic on 100% SAF - marking a key milestone on the path to decarbonising aviation.',
        'challenge': 'The time for action against climate change is now. Virgin Atlantic are on a mission to achieve net-zero by 2050.',
        'category': 'Carbon Reduction',
        'goals': 'Achieve net-zero by 2050',
        'status': 'active',
        'current_progress': 75,
        'target_date': '2050-12-31',
        'metrics': [
            {'name': 'SAF Flights', 'value': 1, 'target': 100, 'unit': 'flights'},
            {'name': 'Carbon Reduction', 'value': 45, 'target': 100, 'unit': '%'}
        ],
        'call_to_action': 'Stay informed and sign up for updates on ways you can get involved in making a difference',
        'links': ['https://corporate.virginatlantic.com/gb/en/business-for-good/planet.html', 'https://corporate.virginatlantic.com/gb/en/business-for-good/planet/fuel/flight100.html', 'https://corporate.virginatlantic.com/gb/en/business-for-good/planet/fuel.html']
    },
    {
        'id': 2,
        'company_id': 2,
        'title': 'Protecting our Planet',
        'description': 'Virgin Atlantic, Virgin Unite, and Flight100 have joined forces with RMI to establish the Contrail Impact Task Force, aiming to address the environmental impact of aircraft contrails.',
        'challenge': 'Contrails, aircraft condensation trails, heighten the effect of global warming, which may account for more than half (57%) of the entire climate impact of aviation.',
        'category': 'Environmental Protection',
        'goals': 'Reduce contrail impact on global warming',
        'status': 'active',
        'current_progress': 60,
        'target_date': '2025-12-31',
        'metrics': [
            {'name': 'Contrail Reduction', 'value': 30, 'target': 57, 'unit': '%'}
        ],
        'call_to_action': 'Stay informed and donate to RMI',
        'links': ['https://corporate.virginatlantic.com/gb/en/business-for-good/planet/fleet.html', 'https://www.virgin.com/virgin-unite/latest/flight100-virgin-atlantic-and-rmi-test-new-ways-to-reduce-aviations-climate']
    },
    {
        'id': 3,
        'company_id': 3,
        'title': 'Epic Sea Change For All',
        'description': 'Virgin Voyages have teamed up with Virgin\'s Foundation, Virgin Unite, to support mangrove forest projects in the Caribbean. The aim is to accelerate nature-based solutions to climate change, and create a scalable model for other regions in the world.',
        'challenge': 'Wildlife havens, carbon stores, storm defences, ocean purifiers - mangrove swamps are one of the hardest-working habitats on Earth, but they\'re disappearing fast.',
        'category': 'Ocean Conservation',
        'goals': 'Protect and restore mangrove forests',
        'status': 'active',
        'current_progress': 65,
        'target_date': '2025-12-31',
        'metrics': [
            {'name': 'Mangrove Restoration', 'value': 650, 'target': 1000, 'unit': 'hectares'}
        ],
        'call_to_action': 'Get involved in a Beach Clean onboard or donate to Sea Change For All Fund',
        'links': ['https://www.virginvoyages.com/sustainability']
    },
    {
        'id': 4,
        'company_id': 4,
        'title': 'Better Connections Plan - O2 Recycle',
        'description': 'O2 Recycle is a service launched in October 2009, which allows anyone in the UK whether an O2 customer or not, to trade in their devices and gadgets responsibly, in return for cash. The vast majority of phones we receive will be reused, repaired or recycled for parts. Since launch, the scheme has paid out more than £320 million, and sustainably recycled 3.8 million devices – with zero going to landfill.',
        'challenge': 'Old IT equipment can lead to electronic waste, or e-waste, polluting the environment. Recycling old IT equipment plays a vital role in preventing this. Virgin Media O2 have a zero landfill policy and will be come a zero-waste business by the end of 2025, and are committed to achieving zero waste operations and products.',
        'category': 'Waste Management',
        'goals': 'Become a zero-waste business by 2025',
        'status': 'active',
        'current_progress': 80,
        'target_date': '2025-12-31',
        'metrics': [
            {'name': 'Devices Recycled', 'value': 3.8, 'target': 5, 'unit': 'million'},
            {'name': 'Landfill Waste', 'value': 0, 'target': 0, 'unit': '%'}
        ],
        'call_to_action': 'Sell your old device with O2 Recycle',
        'links': ['https://www.virgin.com/about-virgin/latest/virgin-media-o2-launches-better-connections-plan', 'https://www.o2recycle.co.uk/']
    },
    {
        'id': 5,
        'company_id': 4,
        'title': 'Better Connections Plan - Community Calling',
        'description': 'Community Calling is a pioneering initiative by Virgin Media O2 and environmental charity Hubbub to tackle digital exclusion. It has already rehomed more than 20,000 unused smartphones with people who need them across the country.',
        'challenge': 'The digital divide, or the split between those with and without reliable internet connectivity and related technologies, has profound implications on society. Lack of internet access affects the economy, social opportunities, and educational equity, and many other areas.',
        'category': 'Digital Inclusion',
        'goals': 'Bridge the digital divide',
        'status': 'active',
        'current_progress': 70,
        'target_date': '2024-12-31',
        'metrics': [
            {'name': 'Phones Donated', 'value': 20000, 'target': 30000, 'unit': 'devices'}
        ],
        'call_to_action': 'Donate devices via Community Calling',
        'links': ['https://www.virgin.com/about-virgin/latest/virgin-media-o2-launches-better-connections-plan', 'https://hubbub.org.uk/community-calling']
    },
    {
        'id': 6,
        'company_id': 4,
        'title': 'Better Connections Plan - Eco Rating',
        'description': 'Virgin Media O2 is one of 5 of Europe\'s leading mobile operators to have joined forces to update and launch a new pan-industry Eco Rating labelling scheme that will help consumers identify and compare the most sustainable mobile phones and encourage suppliers to reduce the environmental impact of their devices.',
        'challenge': 'Mobile phones can have a significant environmental impact in their production and disposal. The mass production of smartphones not only contributes to environmental pollution but also results in a substantial carbon footprint.',
        'category': 'Sustainable Products',
        'goals': 'Reduce environmental impact of devices',
        'status': 'active',
        'current_progress': 75,
        'target_date': '2025-12-31',
        'metrics': [
            {'name': 'Eco-Rated Phones', 'value': 75, 'target': 100, 'unit': '%'}
        ],
        'call_to_action': 'Use the Eco Rating Scheme',
        'links': ['https://news.virginmediao2.co.uk/archive/new-pan-industry-eco-rating-scheme-launched-for-mobile-phones/', 'https://www.o2.co.uk/inspiration/the-drop/eco-rating-for-mobile-phones']
    },
    {
        'id': 7,
        'company_id': 4,
        'title': 'Better Connections Plan - Like-New Phones',
        'description': 'Virgin Media O2 offer a range of like-new second hand smart phones and tablets to help reduce your carbon footprint.',
        'challenge': 'Mobile phones can have a significant environmental impact in their production and disposal. The mass production of smartphones not only contributes to environmental pollution but also results in a substantial carbon footprint.',
        'category': 'Circular Economy',
        'goals': 'Extend device lifecycle',
        'status': 'active',
        'current_progress': 60,
        'target_date': '2025-12-31',
        'metrics': [
            {'name': 'Refurbished Sales', 'value': 6000, 'target': 10000, 'unit': 'devices'}
        ],
        'call_to_action': 'Buy a like-new second hand smartphone or tablet',
        'links': ['https://www.o2.co.uk/shop/like-new']
    },
    {
        'id': 8,
        'company_id': 5,
        'title': 'Pride \'n Purpose',
        'description': 'Pride \'n Purpose is a non-for-profit organisation, committed to helping disadvantaged communities living adjacent to the Sabi Sand Reserve. The Pride \'n Purpose philosophy is that people are most effectively helped if they are empowered to help themselves, with this in mind the organisation\'s work focuses primarily on sustainable initiatives and it is estimated that Pride \'n Purpose benefits over 35,000 people across six communities.',
        'challenge': 'Many communities surrounding Ulusaba lack basic needs such as access to clean drinking water, basic healthcare, food, childcare, and job opportunities.',
        'category': 'Community Development',
        'goals': 'Empower local communities',
        'status': 'active',
        'current_progress': 85,
        'target_date': '2024-12-31',
        'metrics': [
            {'name': 'People Benefited', 'value': 35000, 'target': 40000, 'unit': 'people'}
        ],
        'call_to_action': 'Volunteer during your visit to Ulusaba, Pack for a Purpose: Donate clothing and household supplies, Make a donation',
        'links': ['https://www.virginlimitededition.com/ulusaba/the-reserve/our-commitment/', 'https://www.packforapurpose.org/destinations/africa/south-africa/ulusaba-private-game-reserve/']
    },
    {
        'id': 9,
        'company_id': 5,
        'title': 'Mahali Mzuri: Inua Jamii',
        'description': 'Inua Jamii is Mahali Mzuri\'s charitable arm, committed to working with and supporting the local Maasai communities in the Olare Motorogi Conservancy to improve their standards of living. The name "Inua Jamii" means "uplifting the local community" in Swahili. Our philosophy is that people are most effectively helped if they are empowered to help themselves. Our aim is to nurture communities that thrive through our involvement, simultaneously fostering self-reliance and establishing sustainable resources for generations to come.',
        'challenge': 'A key conservation goal around Mahali Mzuri is to aid conservation and preserve the under-threat route of the Great Wildebeest Migration. We also aim to support and enhance the standard of living in local communities.',
        'category': 'Community Development',
        'goals': 'Support local Maasai communities',
        'status': 'active',
        'current_progress': 75,
        'target_date': '2024-12-31',
        'metrics': [
            {'name': 'Communities Supported', 'value': 6, 'target': 8, 'unit': 'communities'}
        ],
        'call_to_action': 'Volunteer during your visit to Mahali Mzuri, Visit the community or the Maa Trust, Pack for a Purpose: Donate clothing and household supplies, Make a donation',
        'links': ['https://www.virginlimitededition.com/mahali-mzuri/the-camp/our-commitment/', 'https://www.virginlimitededition.com/media/dvvi4c4q/mahali-mzuri-inua-jamii-brochure-oct-24.pdf']
    },
    {
        'id': 10,
        'company_id': 6,
        'title': 'Planetary Guardians',
        'description': 'The new assessment of the Planetary Boundaries was so stark it compelled Virgin Unite to work with the Potsdam Institute to convene a group of leaders and activists to become "Planetary Guardians", with an aim to "elevate the science, catalyse systems change to safeguard the global commons, and spark a movement to tackle the biggest crisis we have ever faced."',
        'challenge': 'The planetary boundaries framework is a key framework for grasping and addressing our footprint on Earth and identifies nine critical systems needed to regulate the health of the entire planet. From climate change to freshwater use, biodiversity loss to chemical pollution and the release of novel entities, these boundaries define the "safe operating space" for humanity. Veer too far beyond these limits and you risk causing irreversible damage to the very ecosystems that sustain life. We currently face an onslaught of environmental and social dilemmas.',
        'category': 'Environmental Protection',
        'goals': 'Address planetary boundaries',
        'status': 'active',
        'current_progress': 55,
        'target_date': '2030-12-31',
        'metrics': [
            {'name': 'Boundaries Addressed', 'value': 5, 'target': 9, 'unit': 'systems'}
        ],
        'call_to_action': 'Watch the video to learn more about our nine planetary boundaries',
        'links': ['https://www.youtube.com/watch?v=d4fdF8rq5h8', 'https://www.virgin.com/branson-family/richard-branson-blog/how-the-planetary-guardians-can-help-secure-earths-future', 'https://unite.virgin.com/our-work/planetary-guardians/index.html?region=gb']
    },
    {
        'id': 11,
        'company_id': 6,
        'title': 'The Elders',
        'description': 'The Elders were incubated by Virgin Unite and launched by Nelson Mandela in 2007 to create an independent global leaders working together for peace, justice, human rights and a sustainable plane. Their work has been truly world changing. They have written an open letter to call on world leaders to address the world\'s existential threats more decisivesly.',
        'challenge': 'The world is rapidly changing, and is facing challenges in leadership, peace-building, inequality, exclusion and injustice.',
        'category': 'Global Leadership',
        'goals': 'Promote peace and justice',
        'status': 'active',
        'current_progress': 80,
        'target_date': '2030-12-31',
        'metrics': [
            {'name': 'Global Initiatives', 'value': 12, 'target': 15, 'unit': 'initiatives'}
        ],
        'call_to_action': 'Sign their open letter calling for long view leadership on existential threats',
        'links': ['https://theelders.org/news/elders-and-future-life-institute-release-open-letter-calling-long-view-leadership-existential', 'https://futureoflife.org/open-letter/long-view-leadership-on-existential-threats/']
    },
    {
        'id': 12,
        'company_id': 6,
        'title': 'Ocean Unite / ORRAA',
        'description': 'In October 2016, Ocean Unite / ORRAA in collaboration with the Marine Conservation Institute and Oceans 5, brought together 30 of the largest NGOs from around the world, stimulating joint efforts towards the goal of strongly protecting at least 30 of the Ocean by 2030. A current campaign is to secure the largest act of Ocean Protection in history by protecting Antarcticas waters.',
        'challenge': 'The dual crises of climate change and mass wildlife extinctions threaten to forever change our world. By 2050, over 570 low-lying coastal cities will face threats from sea level rise and an estimated 800 million people will be at risk to storm surge and flooding from extreme weather events. The currents that swirl around Antarctica transport essential nutrients to other ocean currents that feed the rest of the worlds ocean. This vitally important region is on the frontline of the climate crisis',
        'category': 'Ocean Conservation',
        'goals': 'Protect 30% of oceans by 2030',
        'status': 'active',
        'current_progress': 40,
        'target_date': '2030-12-31',
        'metrics': [
            {'name': 'Ocean Protected', 'value': 12, 'target': 30, 'unit': '%'}
        ],
        'call_to_action': 'Add your name to the petition urging leaders from CCAMLR member countries to act now to protect Antarctica\'s waters #CallOnCCAMLR',
        'links': ['https://only.one/act/antarctica', 'https://www.virgin.com/virgin-unite/latest/securing-the-largest-act-of-ocean-protection-in-history']
    },
    {
        'id': 13,
        'company_id': 6,
        'title': 'Community Mapathon: Humanitarian OpenStreetMap (HOT)',
        'description': 'The Humanitarian OpenStreetMap Team (HOT) is community mapping organisation supporting humanitarian responses to nearly 100 crises; many caused by the impacts of Climate Change. Funded by one of Virgin Unite\'s co-funded initiative\'s Audacious, HOT specialises in humanitarian action and community development through open mapping, mapping areas for one billion people vulnerable to disasters in 94 countries. This covers a range of things – from supporting disaster relief efforts, to helping to inform action to combat the effects of climate change.',
        'challenge': 'Every day, millions of people worldwide face life-threatening crises. Humanitarian aid is a vital lifeline that delivers a variety of essential services to those in need. But as global crises escalate, so does the need for support. We cannot ignore the rise in global humanitarian needs.',
        'category': 'Disaster Response',
        'goals': 'Support communities through mapping',
        'status': 'active',
        'current_progress': 65,
        'target_date': '2025-12-31',
        'metrics': [
            {'name': 'Areas Mapped', 'value': 65, 'target': 100, 'unit': '%'}
        ],
        'call_to_action': 'Spare some time to join the mappers and help with mapping',
        'links': ['https://www.virgin.com/virgin-unite/latest/join-humanitarian-openstreetmap-team-to-help-map-el-nino-2023', 'https://www.hotosm.org/updates/mapping-for-el-nino-2023-early-warning-and-anticipatory-action/']
    },
    {
        'id': 14,
        'company_id': 6,
        'title': 'Project CETI (Cetacean Translation Initiative)',
        'description': 'Project CETI is one of Virgin Unite\'s co-funded Audacious projects. It uses machine learning and robotics to translate sperm whale clicks in Dominica. By shedding light on the intricate and intelligent communication of whales, the project not only aims to accelerate conservation efforts, but has the potential to transform the way we understand our relationship with the natural world.',
        'challenge': 'Humanity is facing the collapse of entire ecosystems, and the biodiversity of our planet is being eroded at unprecedented rates. It is a pivotal time for us to reshape how we co-exist in and with nature. Whales play a significant role in our environments health and understanding of marine mammals. They also support growing economies relying on whale watching and spectator activities by bringing tourism capital.',
        'category': 'Wildlife Conservation',
        'goals': 'Translate sperm whale communication',
        'status': 'active',
        'current_progress': 45,
        'target_date': '2030-12-31',
        'metrics': [
            {'name': 'Recordings Analyzed', 'value': 45, 'target': 100, 'unit': '%'}
        ],
        'call_to_action': 'Become a whale interpreter or donate to support Project CETI',
        'links': ['https://www.projectceti.org/get-involved', 'https://www.audaciousproject.org/grantees/project-ceti']
    },
    {
        'id': 15,
        'company_id': 7,
        'title': 'Eve Branson Foundation',
        'description': 'The Eve Branson Foundation is a small non-profit based in Morocco. Their mission is to create opportunities for local people in the High Atlas Mountains which can make a meaningful difference to their families and community. They have developed initiatives in four key areas: artisanal training, environment, healthcare and education.',
        'challenge': 'The aim of the Eve Branson Foundation is to support local people and communities around the Atlas Mountains. On 8th September 2023, Morocco was hit hard by a strong earthquake measuring magnitude 6.8. Remote communities in the High Atlas Mountains were badly affected.',
        'category': 'Community Development',
        'goals': 'Support local communities',
        'status': 'active',
        'current_progress': 70,
        'target_date': '2025-12-31',
        'metrics': [
            {'name': 'Communities Supported', 'value': 7, 'target': 10, 'unit': 'communities'}
        ],
        'call_to_action': 'Donate, Visit, Pack for a Purpose, Buy EBF products through Virgin Red',
        'links': ['https://evebransonfoundation.org.uk/', 'https://evebransonfoundation.org.uk/pack-for-a-purpose/', 'https://www.virgin.com/virgin-red']
    },
    {
        'id': 16,
        'company_id': 8,
        'title': 'Unite BVI',
        'description': 'Since its launch, Unite BVI has brought together people, ideas and resources to help tackle community and environmental challenges. The Unite BVI team collaborate with communities and BVI change-makers to solve the most pressing issues faced by the BVI and its people. Working across a wide range of projects, Unite BVI advocate for the protection of the environment as well as enriching the community through supporting entrepreneurs, investing in education, and addressing public health and social welfare issues with sustainable solutions.',
        'challenge': 'The BVI faces a number of pressing issues including creating opportunities in the community, improving the quality of education, developing a vibrant entrepeneurial cultre and preservation of the nartual environment.',
        'category': 'Community Support',
        'goals': 'Create opportunities and protect environment',
        'status': 'active',
        'current_progress': 65,
        'target_date': '2025-12-31',
        'metrics': [
            {'name': 'Projects Completed', 'value': 13, 'target': 20, 'unit': 'projects'}
        ],
        'call_to_action': 'Join the community',
        'links': ['https://unitebvi.com/get-involved/index.html?region=gb']
    }
]  # Close the INITIATIVES list properly

# Routes
@bp.route('/')
def dashboard():
    # Calculate statistics
    total_initiatives = len(INITIATIVES)
    active_initiatives = len([i for i in INITIATIVES if i['status'] == 'active'])
    categories = {}
    companies_initiatives = {}
    
    for initiative in INITIATIVES:
        # Count categories
        if initiative['category'] in categories:
            categories[initiative['category']] += 1
        else:
            categories[initiative['category']] = 1
            
        # Count initiatives by company
        company_id = initiative['company_id']
        if company_id in companies_initiatives:
            companies_initiatives[company_id] += 1
        else:
            companies_initiatives[company_id] = 1
    
    # Sort categories by count (descending)
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    
    # Get company names for each company ID
    company_stats = []
    for company_id, count in companies_initiatives.items():
        company_name = next((c['name'] for c in COMPANIES if c['id'] == company_id), "Unknown")
        company_stats.append({
            'name': company_name,
            'count': count
        })
    
    # Sort companies by count (descending)
    company_stats.sort(key=lambda x: x['count'], reverse=True)
    
    # Calculate average progress with proper rounding
    avg_progress = round(sum(i['current_progress'] for i in INITIATIVES) / total_initiatives, 1) if total_initiatives > 0 else 0
    
    # Get top initiatives by progress
    top_initiatives = sorted(INITIATIVES, key=lambda x: x['current_progress'], reverse=True)[:5]
    
    return render_template('dashboard.html', 
                          total_initiatives=total_initiatives,
                          active_initiatives=active_initiatives,
                          categories=sorted_categories,
                          company_stats=company_stats,
                          avg_progress=avg_progress,
                          top_initiatives=top_initiatives,
                          companies=COMPANIES)

@bp.route('/initiatives')
def initiatives():
    company_id = request.args.get('company_id', type=int)
    category = request.args.get('category')
    status = request.args.get('status')
    search = request.args.get('search', '').lower()

    filtered_initiatives = INITIATIVES.copy()

    if company_id:
        filtered_initiatives = [i for i in filtered_initiatives if i['company_id'] == company_id]
    if category:
        filtered_initiatives = [i for i in filtered_initiatives if i['category'].lower() == category.lower()]
    if status:
        filtered_initiatives = [i for i in filtered_initiatives if i['status'].lower() == status.lower()]
    if search:
        filtered_initiatives = [i for i in filtered_initiatives 
                              if search in i['title'].lower() or 
                              search in i['description'].lower()]

    # Get unique categories for filter dropdown
    categories = sorted(list(set(i['category'] for i in INITIATIVES)))
    
    return render_template('initiatives.html', 
                         initiatives=filtered_initiatives,
                         companies=COMPANIES,
                         categories=categories)

@bp.route('/initiatives/<int:initiative_id>')
def initiative_details(initiative_id):
    initiative = next((i for i in INITIATIVES if i['id'] == initiative_id), None)
    if initiative is None:
        return "Initiative not found", 404
    return render_template('initiative_details.html', initiative=initiative, companies=COMPANIES)

@bp.route('/api/initiatives')
def api_initiatives():
    return jsonify(INITIATIVES)

@bp.route('/api/initiatives/<int:initiative_id>/metrics')
def api_initiative_metrics(initiative_id):
    initiative = next((i for i in INITIATIVES if i['id'] == initiative_id), None)
    if initiative is None:
        return jsonify({'error': 'Initiative not found'}), 404
    return jsonify(initiative['metrics'])