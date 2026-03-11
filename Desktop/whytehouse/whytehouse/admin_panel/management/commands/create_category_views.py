# This file documents the changes needed for dynamic blog categories

# 1. Add to admin_panel/urls.py:
# path('blogs/category/', category_list, name='category_list'),
# path('blogs/category/add/', add_category, name='add_category'),
# path('blogs/category/edit/<int:pk>/', edit_category, name='edit_category'),
# path('blogs/category/delete/<int:pk>/', delete_category, name='delete_category'),

# 2. Views are already added to admin_panel/views.py

# 3. Templates need to be created in templates/admin/blog/category/

# 4. Update blog forms to use BlogCategory.objects.all() for dropdown

# 5. Update user_panel/views.py blog_list to use BlogCategory.objects.filter(is_active=True)
