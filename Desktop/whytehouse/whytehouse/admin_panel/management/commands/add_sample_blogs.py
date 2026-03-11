from django.core.management.base import BaseCommand
from admin_panel.models import Blog
from django.utils.text import slugify
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Add 6 sample blog posts with beautiful content'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to create blog posts...'))

        # Calculate publish dates (spread over last 30 days)
        today = datetime.now().date()
        
        # Blog 1: Kerala
        if not Blog.objects.filter(title="10 Hidden Gems in Kerala You Must Visit").exists():
            Blog.objects.create(
                title="10 Hidden Gems in Kerala You Must Visit",
                slug=slugify("10 Hidden Gems in Kerala You Must Visit"),
                author_name="Priya Sharma",
                author_summary="Travel blogger and Kerala native with 8 years of experience exploring hidden destinations across South India.",
                excerpt="Discover Kerala's best-kept secrets beyond the popular backwaters and beaches. From pristine waterfalls to serene hill stations, explore 10 hidden gems in God's Own Country.",
                content="""Kerala, often called 'God's Own Country', is renowned for its backwaters and beaches. But beyond the popular destinations lie hidden treasures waiting to be discovered.

**1. Athirappilly Waterfalls** - Often called the 'Niagara of India', this stunning waterfall is a sight to behold during monsoon season.

**2. Vagamon** - This hill station offers pristine meadows, pine forests, and tea gardens perfect for tranquility seekers.

**3. Bekal Fort** - A magnificent fort overlooking the Arabian Sea with breathtaking sunset views.

**4. Munroe Island** - Experience authentic village life on this cluster of eight islands.

**5. Gavi** - A biodiversity hotspot in the Periyar Tiger Reserve for wildlife enthusiasts.

**6. Poovar Island** - Where the river meets the sea, offering floating cottages.

**7. Thenmala** - India's first planned eco-tourism destination.

**8. Nelliampathy** - A serene hill station with orange groves and tea plantations.

**9. Perunthenaruvi Waterfall** - Perfect for a refreshing dip in natural pools.

**10. Marari Beach** - An unspoiled beach village with authentic Kerala coastal life.""",
                hashtags="#Kerala #HiddenGems #TravelIndia #Backwaters #HillStations",
                tags="#Kerala #HiddenGems #TravelIndia #Backwaters #HillStations",
                reading_time=8,
                publish_date=today,
                status='published',
            )
            self.stdout.write(self.style.SUCCESS('1. Created: Kerala Hidden Gems'))
        
        # Blog 2: Himachal
        if not Blog.objects.filter(title="Ultimate Guide to Backpacking Through Himachal Pradesh").exists():
            Blog.objects.create(
                title="Ultimate Guide to Backpacking Through Himachal Pradesh",
                slug=slugify("Ultimate Guide to Backpacking Through Himachal Pradesh"),
                author_name="Vikram Singh",
                author_summary="Adventure travel expert and mountain enthusiast who has trekked across the Himalayas for over a decade.",
                excerpt="Your complete guide to backpacking through Himachal Pradesh on a budget. Discover must-visit destinations, budget tips, and essential packing advice.",
                content="""Himachal Pradesh is a backpacker's paradise. Here's your complete guide to exploring this Himalayan wonderland on a budget.

**Must-Visit Destinations:**

**Manali** - Adventure hub with paragliding, ancient temples, and Old Manali cafes.

**Kasol** - Mini-Israel of India, perfect for budget travelers. Trek to Kheerganga for hot springs.

**Spiti Valley** - Cold desert offering monasteries and high-altitude villages.

**Dharamshala & McLeod Ganj** - Home to the Dalai Lama with Tibetan culture and Triund trek.

**Bir Billing** - World's second-best paragliding site.

**Budget Tips:**
- Stay in hostels (₹300-500/night)
- Eat at local dhabas
- Use HRTC buses
- Book activities directly
- Travel in groups

**Essential Packing:**
- Warm clothes
- Trekking shoes
- Sunscreen
- First aid kit
- Power bank""",
                hashtags="#HimachalPradesh #Backpacking #BudgetTravel #MountainLife #Trekking",
                tags="#HimachalPradesh #Backpacking #BudgetTravel #MountainLife #Trekking",
                reading_time=10,
                publish_date=today - timedelta(days=5),
                status='published',
            )
            self.stdout.write(self.style.SUCCESS('2. Created: Himachal Backpacking Guide'))
        
        # Blog 3: Goa
        if not Blog.objects.filter(title="Goa Beyond Beaches: Exploring the Cultural Side").exists():
            Blog.objects.create(
                title="Goa Beyond Beaches: Exploring the Cultural Side",
                slug=slugify("Goa Beyond Beaches: Exploring the Cultural Side"),
                author_name="Amit Patel",
                author_summary="Cultural heritage enthusiast and food blogger specializing in Goan history, architecture, and traditional cuisine.",
                excerpt="Discover Goa's rich Portuguese heritage, traditional cuisine, and hidden cultural treasures beyond the famous beaches and nightlife.",
                content="""While Goa is famous for beaches, there's rich cultural heritage waiting to be explored.

**Portuguese Heritage:**

**Old Goa Churches** - Visit Basilica of Bom Jesus, a UNESCO World Heritage Site.

**Fontainhas** - Wander through the Latin Quarter with colorful Portuguese houses.

**Ancestral Houses** - Visit Palacio do Deao and Menezes Braganza House.

**Local Experiences:**

**Spice Plantations** - Tour organic farms and enjoy traditional Goan lunch.

**Feni Distilleries** - Discover how Goa's famous feni is made.

**Local Markets** - Explore Mapusa Market and Anjuna Flea Market.

**Traditional Cuisine:**
- Fish Curry Rice
- Xacuti
- Bebinca (dessert)
- Sorpotel
- Sanna (rice cakes)

**Hidden Beaches:**
- Butterfly Beach
- Kakolem Beach
- Galgibaga Beach""",
                hashtags="#Goa #CulturalTravel #PortugueseHeritage #GoaBeyondBeaches #GoaFood",
                tags="#Goa #CulturalTravel #PortugueseHeritage #GoaBeyondBeaches #GoaFood",
                reading_time=9,
                publish_date=today - timedelta(days=10),
                status='published',
            )
            self.stdout.write(self.style.SUCCESS('3. Created: Goa Cultural Guide'))
        
        # Blog 4: Rajasthan
        if not Blog.objects.filter(title="Rajasthan Royal Heritage: A Journey Through Time").exists():
            Blog.objects.create(
                title="Rajasthan Royal Heritage: A Journey Through Time",
                slug=slugify("Rajasthan Royal Heritage: A Journey Through Time"),
                author_name="Sneha Reddy",
                author_summary="Heritage tourism specialist with expertise in Indian royal history. Has documented over 50 palaces across Rajasthan.",
                excerpt="Experience royal Rajasthan with magnificent forts, palace hotels, desert safaris, and vibrant culture. Your complete guide to India's most colorful state.",
                content="""Step into the land of maharajas and magnificent forts. Rajasthan offers a royal experience like no other.

**The Golden Triangle Plus:**

**Jaipur - The Pink City** - Amber Fort, City Palace, and Hawa Mahal.

**Udaipur - City of Lakes** - City Palace and Lake Pichola offer romantic settings.

**Jodhpur - The Blue City** - Mehrangarh Fort and blue-painted houses.

**Jaisalmer - The Golden City** - Thar Desert with camel safaris and living fort.

**Royal Experiences:**

**Heritage Hotels** - Stay in converted palaces and forts.

**Traditional Cuisine:**
- Dal Baati Churma
- Laal Maas
- Gatte ki Sabzi
- Ghevar (dessert)

**Shopping:**
- Bandhani textiles
- Silver jewelry
- Blue pottery
- Miniature paintings

**Best Time:** October to March

**Festivals:**
- Pushkar Camel Fair (November)
- Desert Festival (February)
- Diwali celebrations""",
                hashtags="#Rajasthan #RoyalIndia #HeritageTravel #Jaipur #Udaipur #DesertSafari",
                tags="#Rajasthan #RoyalIndia #HeritageTravel #Jaipur #Udaipur #DesertSafari",
                reading_time=11,
                publish_date=today - timedelta(days=15),
                status='published',
            )
            self.stdout.write(self.style.SUCCESS('4. Created: Rajasthan Royal Heritage'))
        
        # Blog 5: Northeast
        if not Blog.objects.filter(title="Northeast India: The Unexplored Paradise").exists():
            Blog.objects.create(
                title="Northeast India: The Unexplored Paradise",
                slug=slugify("Northeast India: The Unexplored Paradise"),
                author_name="Rajesh Kumar",
                author_summary="Wildlife photographer and Northeast India specialist. Has explored all seven sister states documenting tribal cultures.",
                excerpt="Discover Northeast India's pristine landscapes, unique tribal cultures, and unexplored destinations. From living root bridges to wildlife safaris.",
                content="""The Seven Sisters of Northeast India remain one of the country's best-kept secrets.

**Meghalaya - Abode of Clouds:**

**Cherrapunji** - Wettest place on Earth with waterfalls and living root bridges.

**Dawki** - Crystal-clear Umngot River where boats appear to float on air.

**Shillong** - The 'Scotland of the East' with pleasant weather.

**Assam - Land of Tea:**

**Kaziranga National Park** - Home to one-horned rhinoceros.

**Tea Gardens** - Tour estates and stay in heritage bungalows.

**Majuli Island** - World's largest river island.

**Arunachal Pradesh:**

**Tawang** - Stunning monastery surrounded by snow-capped mountains.

**Ziro Valley** - UNESCO Heritage Site with Apatani tribal culture.

**Nagaland:**

**Hornbill Festival** - Festival of Festivals in December.

**Sikkim:**

**Gangtok** - Monasteries and mountain views.

**Permits Required:**
- Inner Line Permit for Arunachal
- Protected Area Permit for Sikkim

**Best Time:** October to April""",
                hashtags="#NortheastIndia #Meghalaya #Assam #LivingRootBridges #UnexploredIndia",
                tags="#NortheastIndia #Meghalaya #Assam #LivingRootBridges #UnexploredIndia",
                reading_time=12,
                publish_date=today - timedelta(days=20),
                status='published',
            )
            self.stdout.write(self.style.SUCCESS('5. Created: Northeast Paradise'))
        
        # Blog 6: Temple Trail
        if not Blog.objects.filter(title="South India Temple Trail: Spiritual Journey").exists():
            Blog.objects.create(
                title="South India Temple Trail: Spiritual Journey",
                slug=slugify("South India Temple Trail: Spiritual Journey"),
                author_name="Priya Sharma",
                author_summary="Art historian and temple architecture expert specializing in Dravidian heritage. Has documented over 200 ancient temples.",
                excerpt="Explore South India's magnificent temple trail featuring ancient Dravidian architecture, spiritual experiences, and cultural heritage.",
                content="""Embark on a spiritual journey through South India's magnificent temples.

**Tamil Nadu - Temple Capital:**

**Madurai - Meenakshi Temple** - Towering gopurams with thousands of colorful sculptures.

**Thanjavur - Brihadeeswarar Temple** - UNESCO World Heritage Site showcasing Chola architecture.

**Rameswaram** - One of Char Dham pilgrimage sites.

**Kanchipuram** - City of Thousand Temples.

**Karnataka:**

**Hampi** - UNESCO World Heritage Site with Vijayanagara Empire ruins.

**Belur & Halebidu** - Hoysala temples with intricate carvings.

**Kerala:**

**Guruvayur Temple** - Important Krishna temple.

**Sabarimala** - Famous pilgrimage site in Western Ghats.

**Architecture Styles:**

**Dravidian Style** - Pyramid-shaped towers and pillared halls.

**Vesara Style** - Blend of North and South Indian styles.

**Kerala Style** - Sloping roofs and wooden architecture.

**Travel Tips:**
- Dress modestly
- Remove footwear
- Visit early morning or evening
- Respect temple customs

**Best Season:** October to March""",
                hashtags="#SouthIndia #TempleTrail #SpiritualIndia #DravidianArchitecture #Hampi",
                tags="#SouthIndia #TempleTrail #SpiritualIndia #DravidianArchitecture #Hampi",
                reading_time=13,
                publish_date=today - timedelta(days=25),
                status='published',
            )
            self.stdout.write(self.style.SUCCESS('6. Created: Temple Trail'))

        self.stdout.write(self.style.SUCCESS('\n✅ Successfully created all 6 blog posts!'))
        self.stdout.write(self.style.WARNING('\n⚠️  Featured images can be uploaded at: http://127.0.0.1:8000/admin-blog/blogs/'))
        self.stdout.write(self.style.SUCCESS('📝 View blogs at: http://127.0.0.1:8000/blog/'))
