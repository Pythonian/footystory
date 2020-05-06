from django import template
from django.db.models import Count
import datetime
from django.utils.timezone import now as tz_now

register = template.Library()

from story.models import Story #Category, Tag, Comment
# from ..forms import SearchForm 


### FILTERS ###

# function relative_time(time_value) {
#     var values = time_value.split(" ");
#     time_value = values[1] + " " + values[2] + ", " + values[5] + " " + values[3];
#     var parsed_date = Date.parse(time_value);
#     var relative_to = (arguments.length > 1) ? arguments[1] : new Date();
#     var delta = parseInt((relative_to.getTime() - parsed_date) / 1000);
#     delta = delta + (relative_to.getTimezoneOffset() * 60);

#     if (delta < 60) {
#         return 'less than a minute ago';
#     } else if (delta < 120) {
#         return 'about a minute ago';
#     } else if (delta < (60 * 60)) {
#         return (parseInt(delta / 60)).toString() + ' minutes ago';
#     } else if (delta < (120 * 60)) {
#         return 'about an hour ago';
#     } else if (delta < (24 * 60 * 60)) {
#         return 'about ' + (parseInt(delta / 3600)).toString() + ' hours ago';
#     } else if (delta < (48 * 60 * 60)) {
#         return '1 day ago';
#     } else {
#         return (parseInt(delta / 86400)).toString() + ' days ago';
#     }
# }


@register.filter(expects_localtime=True)
def days_since(value):
    """ Returns number of days between today and value."""

    today = tz_now().date()
    if isinstance(value, datetime.datetime):
        value = value.date()
    diff = today - value
    if diff.days > 1 and diff.days <= 7:
        return "%s days ago" % diff.days
    elif diff.days == 1:
        return "Yesterday"
    elif diff.days == 0:
        return "Today"
    else:
        # Return formatted date.
        return value.strftime("%b %d, %Y")





@register.assignment_tag
def get_latest_stories():    
    return Story.objects.all()[:3]

@register.simple_tag
def get_total_published_stories(user=None):
    return Story.published.filter(author=user).count()

# @register.assignment_tag
# def get_popular_posts():
#     return Post.objects.order_by(
#         '-impressions')[:3]

# @register.assignment_tag
# def get_recent_comments():    
#     return Comment.objects.filter(
#         active=True, parent=None)[:3]

# @register.assignment_tag
# def get_most_commented_posts():
#     return Post.objects.annotate(
#         total_comments=Count('comments')).order_by(
#             '-total_comments')[:3]

# @register.assignment_tag
# def get_sidebar_categories():    
#     return Category.objects.all()

# @register.assignment_tag
# def get_sidebar_tags():    
#     return Tag.objects.all()

# @register.inclusion_tag("blog/_sidebar_search_box.html")
# def search_box(request):
#     form = SearchForm()
#     return {'form': form}


# @register.filter(name='addcss')
# def addcss(field, css):
# 	return field.as_widget(attrs={"class":css})