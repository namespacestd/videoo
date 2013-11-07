from django.http import *
from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.forms import *
from ase1.models import *
from movie.views import get_review_approvals
from django.db.models import Q
from datetime import timedelta, date, datetime
import logging

logger = logging.getLogger('root.' + __name__)


#TODO: Be able to create, delete, and rename lists
def user_main(request, username):
    target_user = Profile.find(username)

    if not target_user:
        return HttpResponse(status=404)
    logger.info("Generating profile page for %s", target_user)

    class Stats: pass

    stats = Stats()
    stats.join_date = target_user.join_date
    all_reviews = Review.objects.filter(user=target_user)
    stats.num_reviewed = len(all_reviews)
    watched_list = UserList.objects.filter(user=target_user, list_name='Watched')
    watched = UserListItem.objects.filter(user_list=watched_list)
    stats.num_watched = len(watched)
    all_ratings = Rating.objects.filter(user=target_user)
    stats.num_rated = len(all_ratings)

    sorted_objs = sorted(list(all_reviews), key=lambda x: x.date_created)
    # Only reviews posted in the last month are displayed
    stats.recent_reviews = filter(lambda x: date.today() - x.date_created.date() < timedelta(30), sorted_objs)
    logger.info("Excluded %d reviews from profile page", len(sorted_objs) - len(stats.recent_reviews))

    return render(request, 'profile/main.html', {
        'current_user': target_user.user.username,
        'review_list': get_review_approvals(request, stats.recent_reviews),
        'display_title': True,  # To display titles of movie next to Review
        'user_stats': stats,
    })


def main(request):
    return render(request, 'profile/main.html', {
        'review_list': get_review_approvals(request, Review.objects.filter(user=Profile.get(request.user))),
        'display_title': True,  # To display titles of movie next to Review
    })


def login(request):
    if request.method == 'POST':  # If the form has been submitted...

        # Ensure that default super-user exists. This check is placed here because
        # it affects performance the least here, and it's the first time the superuser
        # credentials could matter.
        su = User.objects.filter(username='ase1')
        if not su:
            logger.info('Did not find superuser ase1...creating...')
            su = Profile.create_new_user('ase1', '', 'password123', date.today())
            su.user.is_superuser = True
            su.user.save()

        AuthenticationForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponse('Success')
            else:
                error_msg = 'Your account has been disabled.'
        else:
            error_msg = "Your username and password didn't match. Please try again."

        logger.info('Login failed. User: %s, Reason: %s', username, error_msg)
        return HttpResponse(error_msg)
    else:
        return HttpResponse('No login page. Must be posted to by login form.')


def logout(request):
    user = request.user
    auth.logout(request)
    logger.info('Logout. User: %s', user)
    return HttpResponseRedirect('/')


def signup(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = CreateAccountForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                user = auth.authenticate(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password2'])
                auth.login(request, user)

                new_profile = Profile.find(form.cleaned_data['username'])
                logger.info('User Create successful. User: %s', new_profile)
                UserList.create_default_lists(new_profile)

                return HttpResponse('Success')  # Redirects to user's profile page
            else:
                logger.error('User Create failed. Invalid form.')
                raise Exception(form.errors.as_ul())
        except Exception as ex:
            logger.error('User Create failed. Validation or Authentication failed.')
            return HttpResponse(ex.message)
    else:
        logger.error('User Create failed. Invalid form submission.')
        return HttpResponse('Account creation failed.')


def lists(request, username):
    target_user = Profile.find(username)

    if not target_user:
        return HttpResponse(status=404)

    logger.info('Generating lists for user %s', target_user)

    user_lists = UserList.objects.filter(user=target_user)
    for user_list in user_lists:
        user_list.list_items = UserListItem.objects.filter(user_list=user_list)
        logger.info('User list %s has %d elements', user_list, len(user_list.list_items))

    return render(request, 'profile/lists.html', {
        'lists': user_lists
    })


#TODO: Mutual Exclusion for 'Watched', 'Planning to Watch' lists
def lists_quick_add(request):
    if request.method == 'POST':
        logger.info("Quick add for user %s", request.user)
        current_user = Profile.get(request.user)
        if not current_user:
            return HttpResponse(status=404)

        list_name = request.POST['list_to_add']
        user_list = UserList.objects.filter(list_name=list_name, user=current_user)
        if not len(user_list):
            # happens if user deletes list in other tab and tries to add on current page
            return HttpResponse(status=404)
        else:
            user_list = user_list[0]

        movie = Movie.objects.filter(m_id=request.POST['movie_id'])[0]
        rating = Rating.objects.filter(user=current_user, movie=movie)
        if not len(rating):
            rating = Rating(movie=movie, user=current_user, rating=-1)
            rating.save()
        else:
            rating = rating[0]

        already_exists = UserListItem.objects.filter(user_list=user_list, movie=movie)
        if not len(already_exists):
            new_entry = UserListItem(user_list=user_list,
                                     movie=movie,
                                     rating=rating)
            new_entry.save()
            logger.info("Added %s to %s's %s list", movie, request.user.username, list_name)
        else:
            #TODO: Make sure to alert the user of attempted re-add
            logger.info("User %s's %s list already contains %s", request.user.username, list_name, movie)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def create_list(request):
    if request.method == 'POST':
        logger.info("Create list for user %s", request.user)
        current_user = Profile.get(request.user)
        if not current_user:
            return HttpResponse(status=404)

        list_name = request.POST['list_name']
        already_exists = UserList.objects.filter(list_name=list_name, user=current_user)
        if len(already_exists):
            #TODO: Alert user of existing list
            logger.info("User %s attempted to create another list with the name %s", current_user, list_name)
        else:
            logger.info("Creating list named %s", list_name)
            UserList(list_name=list_name, user=current_user).save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def friends_list(request, username):
    return HttpResponseRedirect(request.META['HTTP_REFERER']) 


def admin_page(request):
    if not request.user.is_superuser:
        logger.info('Unauthorized attempt to access admin page by user %s', request.user.username)
        return HttpResponseForbidden()
    return render(request, 'profile/admin_page.html', {
        'all_users': Profile.objects.all(),
        'unapproved_reviews': get_review_approvals(request, Review.objects.filter(Q(approved=None) | Q(approved=False)))
    })


def apply_admin_changes(request):
    if request.method == 'POST':
        for profile in Profile.objects.all():
            set_to_superuser = request.POST.__contains__(profile.user.username)
            ban_user = request.POST.__contains__('ban_'+profile.user.username)
            if set_to_superuser:
                profile.set_to_superuser(request.user)
            elif ban_user:
                profile.set_to_banned(request.user)
                print profile.user_banned
            elif not ban_user and profile.user_banned:
                profile.remove_ban(request.user)
                print profile.user_banned
                

    return HttpResponseRedirect(request.META['HTTP_REFERER']) 

