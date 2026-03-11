from django.core.management.base import BaseCommand
from admin_panel.models import Blog, BlogImage
from django.utils.text import slugify
from datetime import datetime, timedelta
from django.core.files.base import ContentFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Add 6 sample blog posts with featured and content images'

    def handle(self, *args, **kwargs):
        # Clear existing blogs first (optional)
        self.stdout.write('Creating 6 new blog posts...')

        blogs_data = [
            {
                'title': 'Exploring the Backwaters of Kerala: A Serene Journey',
                'excerpt': 'Discover the tranquil beauty of Kerala\'s backwaters, where palm-fringed canals and traditional houseboats create an unforgettable experience.',
                'content': '''Kerala's backwaters are a network of interconnected canals, rivers, lakes, and inlets that stretch along the coast. This unique ecosystem is home to diverse wildlife and traditional villages.

{{image1-right}}

The best way to experience the backwaters is aboard a traditional houseboat, known locally as "kettuvallam". These floating homes offer all modern amenities while you drift through scenic waterways.

{{image2-left}}

Local cuisine is a highlight of any backwater journey. Fresh seafood, coconut-based curries, and traditional Kerala dishes are prepared right on your houseboat.

{{image3}}

The sunset views over the backwaters are simply breathtaking, painting the sky in shades of orange and pink as fishermen return with their daily catch.''',
                'author_name': 'Priya Menon',
                'author_summary': 'Travel writer and Kerala native with over 10 years of experience exploring South India\'s hidden gems.',
                'reading_time': 8,
                'hashtags': 'Kerala,Backwaters,Houseboat,SouthIndia,NatureTravel',
                'featured_image_url': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800',
                'content_images': [
                    'https://images.unsplash.com/photo-1593693397690-362cb9666fc2?w=600',
                    'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600',
                    'https://images.unsplash.com/photo-1588409002681-b3c6c4e6e4e7?w=800'
                ]
            },
            {
                'title': 'Rajasthan\'s Desert Safari: An Adventure Through Time',
                'excerpt': 'Experience the magic of Rajasthan\'s Thar Desert with camel safaris, royal forts, and vibrant cultural performances under starlit skies.',
                'content': '''The Thar Desert in Rajasthan offers one of India's most iconic travel experiences. Golden sand dunes stretch as far as the eye can see, creating a landscape that seems frozen in time.

{{image1-left}}

Camel safaris are the traditional way to explore the desert. These gentle giants have been the desert's primary mode of transport for centuries, and riding them offers a unique perspective of the landscape.

{{image2-right}}

The desert comes alive at night with cultural performances. Folk dancers, musicians, and fire performers showcase Rajasthan's rich heritage under a canopy of stars.

{{image3}}

Don't miss visiting the magnificent forts and palaces that dot the desert landscape. Jaisalmer Fort, known as the "Golden Fort," rises from the sand like a mirage.''',
                'author_name': 'Arjun Singh',
                'author_summary': 'Adventure travel specialist focusing on desert expeditions and cultural tourism across Rajasthan.',
                'reading_time': 10,
                'hashtags': 'Rajasthan,Desert,CamelSafari,Jaisalmer,Adventure',
                'featured_image_url': 'https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=800',
                'content_images': [
                    'https://images.unsplash.com/photo-1599661046289-e31897846e41?w=600',
                    'https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=600',
                    'https://images.unsplash.com/photo-1597074866923-dc0589150358?w=800'
                ]
            },
            {
                'title': 'Himalayan Trekking: Conquering the Roof of the World',
                'excerpt': 'Journey through pristine mountain trails, ancient monasteries, and breathtaking vistas in the majestic Himalayas.',
                'content': '''The Himalayas offer some of the world's most spectacular trekking routes. From beginner-friendly trails to challenging high-altitude expeditions, there's something for every adventurer.

{{image1-right}}

Popular treks like the Valley of Flowers and Roopkund Lake combine natural beauty with cultural experiences. You'll pass through remote villages where time seems to stand still.

{{image2-left}}

Acclimatization is crucial when trekking at high altitudes. Take your time, stay hydrated, and listen to your body. The journey is as important as the destination.

{{image3}}

The reward for your efforts? Panoramic views of snow-capped peaks, pristine alpine meadows, and the profound sense of accomplishment that comes with conquering the mountains.''',
                'author_name': 'Vikram Thapa',
                'author_summary': 'Professional mountain guide and trekking expert with 15 years of Himalayan expedition experience.',
                'reading_time': 12,
                'hashtags': 'Himalayas,Trekking,Mountains,Adventure,India',
                'featured_image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
                'content_images': [
                    'https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=600',
                    'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=600',
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'
                ]
            },
            {
                'title': 'Goa Beyond Beaches: Hidden Cultural Treasures',
                'excerpt': 'Discover Goa\'s rich Portuguese heritage, spice plantations, and vibrant local markets beyond its famous beaches.',
                'content': '''While Goa is famous for its beaches, the state's interior holds equally fascinating attractions. Portuguese colonial architecture, ancient temples, and lush spice plantations await exploration.

{{image1-left}}

Old Goa's churches and cathedrals are UNESCO World Heritage sites. The Basilica of Bom Jesus houses the remains of St. Francis Xavier and showcases stunning baroque architecture.

{{image2-right}}

Spice plantation tours offer insight into Goa's agricultural heritage. Walk through aromatic gardens of cardamom, pepper, and vanilla while learning about traditional farming methods.

{{image3}}

Local markets like Anjuna Flea Market and Mapusa Market burst with color and energy. Shop for handicrafts, textiles, and spices while experiencing authentic Goan culture.''',
                'author_name': 'Maria Fernandes',
                'author_summary': 'Cultural historian and Goa native passionate about preserving and sharing the state\'s rich heritage.',
                'reading_time': 7,
                'hashtags': 'Goa,Culture,Heritage,Portugal,India',
                'featured_image_url': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800',
                'content_images': [
                    'https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=600',
                    'https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=600',
                    'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800'
                ]
            },
            {
                'title': 'Northeast India: The Land of Seven Sisters',
                'excerpt': 'Explore India\'s most diverse region, where pristine landscapes, unique cultures, and warm hospitality create unforgettable memories.',
                'content': '''Northeast India comprises seven states, each with its own distinct culture, cuisine, and natural beauty. This region remains one of India's best-kept secrets.

{{image1-right}}

Meghalaya, the "abode of clouds," is home to living root bridges and some of the wettest places on Earth. These natural wonders are created by training tree roots over decades.

{{image2-left}}

The region's biodiversity is astounding. From one-horned rhinos in Assam's Kaziranga to red pandas in Sikkim, wildlife enthusiasts will find paradise here.

{{image3}}

Local festivals showcase the region's cultural richness. Hornbill Festival in Nagaland and Bihu in Assam offer glimpses into ancient traditions that continue to thrive.''',
                'author_name': 'Tenzin Dorji',
                'author_summary': 'Northeast India specialist and cultural ambassador promoting sustainable tourism in the region.',
                'reading_time': 9,
                'hashtags': 'Northeast,Meghalaya,Assam,Culture,Adventure',
                'featured_image_url': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800',
                'content_images': [
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600',
                    'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600',
                    'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800'
                ]
            },
            {
                'title': 'Varanasi: A Spiritual Journey Along the Ganges',
                'excerpt': 'Experience the spiritual heart of India in Varanasi, where ancient rituals, sacred ghats, and timeless traditions converge.',
                'content': '''Varanasi, one of the world's oldest continuously inhabited cities, offers a profound spiritual experience. The city's ghats along the Ganges River have witnessed centuries of devotion and ritual.

{{image1-left}}

The Ganga Aarti ceremony at Dashashwamedh Ghat is a mesmerizing spectacle. Priests perform synchronized rituals with fire, bells, and chants as the sun sets over the sacred river.

{{image2-right}}

Early morning boat rides on the Ganges offer a unique perspective of the city. Watch pilgrims perform their morning ablutions and witness the city slowly come to life.

{{image3}}

Beyond the ghats, explore narrow lanes filled with silk weavers, street food vendors, and ancient temples. Every corner of Varanasi tells a story spanning millennia.''',
                'author_name': 'Anand Sharma',
                'author_summary': 'Spiritual tourism guide and scholar of Indian philosophy with deep roots in Varanasi.',
                'reading_time': 8,
                'hashtags': 'Varanasi,Spiritual,Ganges,India,Culture',
                'featured_image_url': 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=800',
                'content_images': [
                    'https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=600',
                    'https://images.unsplash.com/photo-1548013146-72479768bada?w=600',
                    'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=800'
                ]
            }
        ]

        for idx, blog_data in enumerate(blogs_data, 1):
            try:
                # Create blog
                publish_date = datetime.now().date() - timedelta(days=30-idx*5)
                
                blog = Blog.objects.create(
                    title=blog_data['title'],
                    slug=slugify(blog_data['title']),
                    excerpt=blog_data['excerpt'],
                    content=blog_data['content'],
                    status='published',
                    author_name=blog_data['author_name'],
                    author_summary=blog_data['author_summary'],
                    reading_time=blog_data['reading_time'],
                    publish_date=publish_date,
                    hashtags=blog_data['hashtags'],
                    tags=blog_data['hashtags'],
                    featured_image_url=blog_data['featured_image_url']
                )

                # Download and add content images
                for img_idx, img_url in enumerate(blog_data['content_images']):
                    try:
                        response = requests.get(img_url, timeout=10)
                        if response.status_code == 200:
                            img_content = ContentFile(response.content)
                            blog_image = BlogImage.objects.create(
                                blog=blog,
                                order=img_idx
                            )
                            blog_image.image.save(f'blog_{blog.id}_content_{img_idx+1}.jpg', img_content, save=True)
                            self.stdout.write(f'  Added content image {img_idx+1}')
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'  Failed to download content image {img_idx+1}: {str(e)}'))

                self.stdout.write(self.style.SUCCESS(f'✓ Created blog: {blog.title}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to create blog {idx}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Successfully created 6 blog posts!'))
