from django.core.management.base import BaseCommand
from admin_panel.models import Blog, BlogImage


class Command(BaseCommand):
    help = 'Check blog images for all blogs'

    def handle(self, *args, **kwargs):
        blogs = Blog.objects.all()
        
        if not blogs.exists():
            self.stdout.write(self.style.WARNING('No blogs found in database'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'\nFound {blogs.count()} blog(s):\n'))
        
        for blog in blogs:
            self.stdout.write(f'\n{"="*60}')
            self.stdout.write(f'Blog ID: {blog.id}')
            self.stdout.write(f'Title: {blog.title}')
            self.stdout.write(f'Slug: {blog.slug}')
            self.stdout.write(f'Status: {blog.status}')
            
            images = blog.content_images.all()
            self.stdout.write(f'\nContent Images: {images.count()}')
            
            if images.exists():
                for img in images:
                    self.stdout.write(f'  - Image {img.order + 1}: {img.image.url}')
                    self.stdout.write(f'    Tag: {{{{image{img.order + 1}}}}}')
            else:
                self.stdout.write(self.style.WARNING('  No content images found'))
            
            # Check if placeholders are in content
            if blog.content:
                self.stdout.write(f'\nContent length: {len(blog.content)} characters')
                for i in range(1, images.count() + 1):
                    placeholder = f'{{{{image{i}}}'
                    if placeholder in blog.content:
                        self.stdout.write(self.style.SUCCESS(f'  ✓ Found placeholder: {{{{image{i}}}}}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'  ✗ Missing placeholder: {{{{image{i}}}}}'))
        
        self.stdout.write(f'\n{"="*60}\n')
