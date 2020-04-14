from django.contrib import admin

# Register your models here.
#admin.ModelAdmin是一个写好的对象，你继承它，进行操作


from django.contrib import admin

from .models import Author, Genre, BookInstance, Book


# admin.site.register(Book)
# admin.site.register(Author)
# define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

admin.site.register(Genre)


# admin.site.register(BookInstance)
# @register 装饰器，与admin.site.register()语法作用一样
# Regiter the Admin classes for Book using the decorator
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status','borrower','due_back','id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields':('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields':('status', 'due_back','borrower')
        }),
    )




