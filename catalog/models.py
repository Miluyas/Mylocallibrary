from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Genre(models.Model):
    """
    Model representing a book gener (e.g Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200,
                            help_text="Enter a book genre (e.g. Science Fiction, French Potry etc.)")

    def __str__(self):
        """
        String for representing the Model object(in Admin site etc.)
        """
        return self.name


from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    def display_genre(self):
        """
        创造一个string给Genre,在Admin中要用
        :return:
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """
        Return the url to access a particular book instance.
        :return:
        """
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object
        :return:
        """
        return self.title


# 标记一下，使用

import uuid
from datetime import date


# Required for unique book instance

class BookInstance(models.Model):
    """
    Model representing a specific copy of a book(i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    # in this class is many to the book class is one,but the bookinstance are mant .local  class is many ,out is one,so,foreign.外来户是少的，这么理解
    # SET_NULL与SET_NULL()，第一个为一个值，第二个内部有4个不同的值
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability')

    # 标记choice？单复数问题
    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        String for representing the Model object
        :return:
        """
        return '%s, %s' % (self.id, self.book.title)


class Author(models.Model):
    """
    Model representing ana anthor
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance
        :return:
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object
        :return:
        """
        return '%s %s' % (self.last_name, self.first_name)
