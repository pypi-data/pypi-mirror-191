import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib.sites.models import Site
from .utils import unique_slugify


class StateChoices(models.IntegerChoices):
    PUBLISHED = 0, _("Published")
    DRAFT = 1, _("Draft")
    ARCHIVED = 2, _("Archived")


class FlagIssueChoices(models.IntegerChoices):
    OFF_TOPIC = 0, _("Off Topic")
    SPAM = 10, _("Spam")
    INAPPROPRIATE = 20, _("Inappropriate")


class RatingChoices(models.IntegerChoices):
    ONE = 1, _("1")
    TWO = 2, _("2")
    THREE = 3, _("3")
    FOUR = 4, _("4")
    FIVE = 5, _("5")


class EncodingChoices(models.IntegerChoices):
    # PLAIN_TEXT = 0, _("Plain Text")
    MARKDOWN = 1, _("Markdown")


"""
Wrapped choice collection in a function so it can be set by the developer without triggering a new
migration generation, which can wreak havoc if there are updates and additions. Using the tuple as
an argument bakes the values into the migration.
"""


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Post(models.Model):
    """The original posted article"""

    sites = models.ManyToManyField(Site, help_text=_("Set which sites this post is available on"))
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Used in response tracking
    created = models.DateField(_("Created"), auto_now_add=True)
    updated = models.DateField(_("Updated"), auto_now=True)

    title = models.CharField(_("Title"), max_length=120, help_text=_("Headline for the post."))
    slug = models.SlugField(_("Slug"), blank=True)

    release_date = models.DateField(
        _("Updated"), auto_now_add=True
    )  # Defaults to the created date.  Can be set to a later date for future publication.

    banner_image = models.ImageField(  # Need to process and rename the file to make sure there are no clashes
        _("Banner"),
        upload_to="blog/post/",
        height_field=1200,
        width_field=1800,
        max_length=1800,
        blank=True,
        null=True,
    )
    banner_alt = models.CharField(_("Banner Alt Tag String"), max_length=125, blank=True, null=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, related_name="blog_posts"
    )
    language = models.CharField(_("Language Code"), max_length=7, choices=settings.LANGUAGES)
    content = models.TextField(_("Content"))
    encoding_format = models.IntegerField(
        _("Encoding Format"), default=EncodingChoices.MARKDOWN, choices=EncodingChoices.choices
    )
    state = models.IntegerField(
        _("State"),
        default=StateChoices.DRAFT,
        choices=StateChoices.choices,
        help_text="What state is the writing in?",
    )
    active = models.BooleanField(_("Active"), help_text="Auto managed field based on state criteria when saved.")
    rating = models.IntegerField(_("Rating"), default=0)  # Calcuate an average of all the Ratings
    rating_count = models.IntegerField(_("Rating Count"), default=0)  # "cache" total Ratings cast
    sticky = models.IntegerField(
        _("Sticky"),
        default=0,
        help_text=_(
            "Give the blog posts a sticky value to sort to the top of the list of posts.  Higher value becomes higher in the list."
        ),
    )
    locked = models.BooleanField(_("Locked"), help_text=_("Can not add Comments and Replies."))
    hide_responses = models.BooleanField(_("Hide Responses"), help_text=_("Hide responses in display."))
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Parent"),
        on_delete=models.CASCADE,
        related_name="responses",
        blank=True,
        null=True,
        help_text=_("For detailed responses for use in How-To support threads.  Not used in Blogs."),
    )

    # Custom Manager
    objects = ActiveManager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = (
            "sticky",
            "created",
        )

    def save(self, **kwargs):
        if self.state == 0:
            self.active = True
        else:
            self.active = False
        unique_slugify(self, self.title)  # Needs to be unique accross all sites
        super(Post, self).save(**kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogorama-post", kwargs={"slug": self.slug})

    # TODO: Autotag based on text in title & content if setting is enabled.  Tasks should be queued and backgrounded.


class Tag(models.Model):
    """Tags for the Blog Post"""

    name = models.CharField(_("Tag Name"), max_length=50)
    language = models.CharField(_("Language Code"), max_length=7, choices=settings.LANGUAGES)
    active = models.BooleanField(_("Active"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, related_name="blog_post_tags"
    )
    posts = models.ManyToManyField(Post, verbose_name=_("Posts"))
    approved = models.BooleanField(_("Approved"), help_text=_("Check if approved for use when approval is required."))
    related = models.ManyToManyField(
        "self",
        verbose_name=_("Related"),
        help_text="Used to connect tags that are the same but in different languages.",
    )

    objects = ActiveManager()

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


class TagSuggestion(models.Model):
    """
    Used for suggesting tags based on ones used
    """

    tag = models.ForeignKey(Tag, verbose_name=_("Tag"), on_delete=models.CASCADE, related_name="referrals")
    suggestion = models.ForeignKey(
        Tag, verbose_name=_("Suggested Tag"), on_delete=models.CASCADE, related_name="suggestions"
    )
    score = models.IntegerField(_("Score"), help_text=_("How relevent the suggested tag is to the connected tag"))


class Comment(models.Model):
    """User Response to the Article"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateField(_("Created"), auto_now_add=True)
    updated = models.DateField(_("Updated"), auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, related_name="blog_comments"
    )
    language = models.CharField(_("Language Code"), max_length=7, choices=settings.LANGUAGES)
    content = models.TextField(_("Content"))
    encoding = models.IntegerField(
        _("Encoding Format"), default=EncodingChoices.MARKDOWN, choices=EncodingChoices.choices
    )
    up_vote = models.IntegerField(_("Up Vote"), default=0, help_text=_("Calculated value of all Votes"))
    up_vote_count = models.IntegerField(
        _("Up Vote Count"), default=0, help_text=_("Calculated total of Votes cast")
    )  # "cache" total Votes cast
    state = models.IntegerField(
        _("State"), default=StateChoices.DRAFT, choices=StateChoices.choices
    )  # What state is the writing in?
    solution = models.BooleanField(
        _("Solution"), help_text=_("This will tag a comment as an accepted solution if used.")
    )
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Parent"),
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
        help_text=_("For threading comments, no parent is a top level comment"),
    )
    objects = ActiveManager()

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = (
            "up_vote",
            "created",
        )

    def __str__(self):
        return self.name

    def calculate_votes(self):
        total_positive = 1
        total_negative = 1
        self.up_vote = total_positive - total_negative
        self.up_vote_count = total_positive + total_negative


class Vote(models.Model):
    """Up or down vote for the comment"""

    updated = models.DateField(_("Updated"), auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, related_name="blog_comment_votes"
    )
    upvote = models.BooleanField(_("Up-Vote"), help_text=_("Checked it's an up-vote, unchecked it's a down-vote"))
    comments = models.ForeignKey(
        Comment, verbose_name=_("Comment"), on_delete=models.CASCADE, related_name="blog_comment_votes"
    )

    objects = ActiveManager()

    class Meta:
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")

    def __str__(self):
        return self.name


class Rating(models.Model):
    """On a scale of 1-5, how good is the blog?"""

    active = models.BooleanField(_("Active"))
    created = models.DateField(_("Created"), auto_now_add=True)
    updated = models.DateField(_("Updated"), auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, related_name="blog_post_ratings"
    )
    value = models.SmallIntegerField(_("Vote Value"), choices=RatingChoices.choices, default=RatingChoices.THREE)
    post = models.ForeignKey(Post, verbose_name=_("Blog Post"), on_delete=models.CASCADE, related_name="ratings")

    objects = ActiveManager()

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")

    def calculate_rating(self):
        total_ratings_cast = self.post.ratings.count()  # Get a count of all ratings cast
        ratings_sum = 300
        self.rating = ratings_sum / total_ratings_cast
        self.rating_count = total_ratings_cast

    def __str__(self):
        return self.name


class Save(models.Model):
    """Save a blog post to an archive for reading later"""

    created = models.DateField(_("Created"), auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, related_name="blog_saves"
    )
    blog = models.ForeignKey(Post, verbose_name=_("Blog Post"), on_delete=models.CASCADE, related_name="blog_saves")

    class Meta:
        verbose_name = _("Archive")
        verbose_name_plural = _("Archives")

    def __str__(self):
        return self.name


class Flag(models.Model):
    """For flaging moderator attention; issues from minor to serious"""

    created = models.DateField(_("Created"), auto_now_add=True)
    updated = models.DateField(_("Updated"), auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, related_name="blog_comment_flags"
    )
    description = models.TextField(_("Description"))  # Description of the issue
    issue = models.IntegerField(_("Issue"), default=FlagIssueChoices.OFF_TOPIC, choices=FlagIssueChoices.choices)
    comments = models.ForeignKey(
        Comment, verbose_name=_("Comment Flagged"), on_delete=models.CASCADE, related_name="comment_flags"
    )

    class Meta:
        verbose_name = _("Flag")
        verbose_name_plural = _("Flags")

    def __str__(self):
        return self.name


class PostFlag(models.Model):
    """For flaging moderator attention; issues from minor to serious"""

    created = models.DateField(_("Created"), auto_now_add=True)
    updated = models.DateField(_("Updated"), auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, related_name="blog_post_flags"
    )
    description = models.TextField(_("Description"))  # Description of the issue
    issue = models.IntegerField(_("Issue"), default=FlagIssueChoices.OFF_TOPIC, choices=FlagIssueChoices.choices)
    post = models.ForeignKey(Post, verbose_name=_("Post Flagged"), on_delete=models.CASCADE, related_name="post_flags")

    class Meta:
        verbose_name = _("Flag")
        verbose_name_plural = _("Flags")

    def __str__(self):
        return self.name


class Ban(models.Model):
    """
    This is to flag a user as being banned to post a comment for a given period of time or
    indefinately.  They will be able to still read the posts and comments even if banned,
    just not participate in commentary.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, related_name="blog_comment_bans"
    )
    description = models.TextField(_("Content"), help_text=_("Description of the ban."))
    created = models.DateField(_("Created"), auto_now_add=True)
    expiration = models.DateField(_("Expiration"), blank=True, null=True)
    indefinite = models.BooleanField(_("Indefinitely Banned"))

    class Meta:
        verbose_name = _("Ban")
        verbose_name_plural = _("Bans")

    def __str__(self):
        return self.name
