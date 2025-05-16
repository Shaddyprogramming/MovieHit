from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.decorators import login_required
from MovieHit.management.movies import Movies
from MovieHit.management.banners import Banners
from MovieHit.management.comments import Comment
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseForbidden
import os

def serve_media(request, path):
    """
    Serve media files in production.
    """
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if not os.path.exists(media_path):
        raise Http404("Media file not found.")
    
    with open(media_path, 'rb') as media_file:
        response = HttpResponse(media_file.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(media_path)}"'
        return response

def index(request):
    query = request.GET.get('q', '')  # Fixed variable name from 'y' to 'query'
    
    # Check for order sensitive preference (from session, cookie or GET parameter)
    order_sensitive = False
    
    # Check in session if user is logged in
    if request.user.is_authenticated and 'orderSensitiveSearch' in request.session:
        order_sensitive = request.session.get('orderSensitiveSearch')
    # Check in cookies as fallback
    elif request.COOKIES.get('orderSensitiveSearch') == 'true':
        order_sensitive = True
    
    if query:
        # Use different filters based on the order sensitive preference
        if order_sensitive:
            movies_data = Movies.objects.filter(name__istartswith=query)
        else:
            movies_data = Movies.objects.filter(name__icontains=query)
    else:
        movies_data = Movies.objects.all()
        
    banners_data = Banners.objects.all()
    
    return render(request, 'index.html', {'banners': banners_data, 'movies': movies_data, 'query': query})

def save_preference(request):
    """
    Save user preferences like order sensitive search setting
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            preference_name = request.POST.get('preference_name')
            preference_value = request.POST.get('preference_value') == 'true'
            
            if preference_name == 'orderSensitiveSearch':
                # Save to session
                request.session['orderSensitiveSearch'] = preference_value
                
                # Prepare response
                response = JsonResponse({'success': True})
                
                # Set cookie as fallback for non-authenticated users
                max_age = 365 * 24 * 60 * 60  # 1 year in seconds
                response.set_cookie(
                    'orderSensitiveSearch', 
                    str(preference_value).lower(), 
                    max_age=max_age,
                    secure=request.is_secure(),
                    httponly=False  # Allow JavaScript access
                )
                return response
            
            return JsonResponse({'success': False, 'error': 'Unknown preference'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def movie_detail(request, movie_id):
    """
    View for displaying details of a specific movie.
    Uses the unique_id field from the Movies model.
    """
    # Get the movie by its unique_id or return 404
    movie = get_object_or_404(Movies, unique_id=movie_id)
    
    # Get all comments for this movie
    comments = Comment.objects.filter(movie=movie)
    
    # Render the movie detail template
    return render(request, 'movie_detail.html', {'movie': movie, 'comments': comments})

@login_required
def add_comment(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movies, unique_id=movie_id)
        text = request.POST.get('comment_text', '').strip()
        rating = int(request.POST.get('rating', 0))  # Get the rating
        
        if text:
            Comment.objects.create(
                movie=movie,
                user=request.user,
                text=text,
                rating=rating  # Add the rating here
            )
    
    # Redirect back to movie detail page
    return redirect('movie_detail', movie_id=movie_id)

@login_required
def edit_comment(request, movie_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the owner of the comment
    if request.user != comment.user:
        return HttpResponseForbidden("You don't have permission to edit this comment.")
    
    if request.method == 'POST':
        text = request.POST.get('edit_comment_text', '').strip()
        rating = int(request.POST.get('edit_rating', 0))
        
        if text:
            comment.text = text
            comment.rating = rating
            comment.save()
    
    return redirect('movie_detail', movie_id=movie_id)

@login_required
def delete_comment(request, movie_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the owner of the comment
    if request.user != comment.user:
        return HttpResponseForbidden("You don't have permission to delete this comment.")
    
    if request.method == 'POST':
        comment.delete()
    
    return redirect('movie_detail', movie_id=movie_id)

def account(request):
    if request.user.is_authenticated:
        email_parts = request.user.email.split('@') if request.user.email else ['', '']
        return render(request, 'account.html', {'email_parts': email_parts})
    else:
        return redirect('signin')

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('signin')
        
    message = None
    error = False
    
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Check if username already exists for another user
        if User.objects.exclude(pk=request.user.pk).filter(username=username).exists():
            message = "Username already exists"
            error = True
        else:
            user = request.user
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            message = "Profile updated successfully"
            
    return render(request, 'edit_profile.html', {'message': message, 'error': error})

def update_email(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    if request.method != 'POST' or not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    
    try:
        user = request.user
        
        if not user.email:
            return JsonResponse({'success': False, 'error': 'You need to have an email set up first'})
            
        # Generate token for email confirmation
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # Using empty string for new_email_b64 as it's a placeholder
        new_email_b64 = urlsafe_base64_encode(force_bytes('placeholder'))
        
        current_site = get_current_site(request)
        protocol = 'https' if request.is_secure() else 'http'
        
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
            'new_email_b64': new_email_b64,
            'protocol': protocol,
            'site_name': 'MovieHit'
        }
        
        email_subject = 'Change Email Address for MovieHit'
        email_body = render_to_string('email_update_email.html', context)
        
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )
        
        return JsonResponse({'success': True, 'message': 'Email update link sent to your current email address'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def email_update_confirm(request, uidb64, token, new_email_b64):
    try:
        # Decode the user id
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        # Validate the token
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_email = request.POST.get('new_email')
                
                if not new_email:
                    return render(request, 'email_update_confirm.html', {
                        'validlink': True,
                        'message': 'Email address is required.',
                        'form_submitted': False
                    })
                
                # Check if email is already in use by another user
                if User.objects.exclude(pk=user.pk).filter(email=new_email).exists():
                    return render(request, 'email_update_confirm.html', {
                        'validlink': True,
                        'message': 'This email is already in use by another account.',
                        'form_submitted': False
                    })
                
                # Update the email
                had_previous_email = bool(user.email)
                old_email = user.email
                user.email = new_email
                user.save()
                
                # Send notification to old email if it exists
                if had_previous_email:
                    notification_subject = 'Email Address Updated for MovieHit Account'
                    notification_body = "Your email address for your MovieHit account has been updated. If you did not make this change, please secure your account immediately by resetting your password."
                    send_mail(
                        notification_subject,
                        notification_body,
                        settings.DEFAULT_FROM_EMAIL,
                        [old_email],
                        fail_silently=True
                    )
                
                return render(request, 'email_update_confirm.html', {
                    'validlink': True,
                    'message': 'Your email has been updated successfully.',
                    'form_submitted': True
                })
            
            # Show the form to enter new email
            return render(request, 'email_update_confirm.html', {
                'validlink': True,
                'form_submitted': False
            })
        else:
            # Invalid token
            return render(request, 'email_update_confirm.html', {
                'validlink': False,
                'message': 'The confirmation link is invalid or has expired.'
            })
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # Invalid user id or email
        return render(request, 'email_update_confirm.html', {
            'validlink': False,
            'message': 'The confirmation link is invalid.'
        })


def signin(request):
    error = None
    
    if request.method == 'POST':
        action = request.POST.get('action', '')
        
        if action == 'register':
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            fullname = request.POST.get('fullname', '')
            
            if password != confirm_password:
                error = "Passwords do not match."
            elif User.objects.filter(username=username).exists():
                error = "Username already exists."
            else:
                name_parts = fullname.split(' ', 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ''
                
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                login(request, user)
                return redirect('index')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error = "Invalid credentials. Please try again."
    
    return render(request, 'signin.html', {'error': error})

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        direct_reset = request.POST.get('direct_reset')
        
        # Check if the email exists in the user database
        users = User.objects.filter(email=email)
        
        # Handle AJAX request for direct reset
        if direct_reset and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if not email or not users.exists():
                return JsonResponse({'success': False, 'error': 'Email not found or not provided'})
                
            for user in users:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                current_site = get_current_site(request)
                protocol = 'https' if request.is_secure() else 'http'
                
                context = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                    'protocol': protocol,
                    'site_name': 'MovieHit'
                }
                
                email_subject = 'Password Reset Request for MovieHit'
                email_body = render_to_string('password_reset_email.html', context)
                
                send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False
                )
            
            return JsonResponse({'success': True})
            
        # Regular form submission for password reset
        if users.exists():
            for user in users:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                current_site = get_current_site(request)
                protocol = 'https' if request.is_secure() else 'http'
                
                context = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                    'protocol': protocol,
                    'site_name': 'MovieHit'
                }
                
                email_subject = 'Password Reset Request for MovieHit'
                email_body = render_to_string('password_reset_email.html', context)
                
                send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False
                )
            
            # Always show success message even if email doesn't exist for security reasons
            return render(request, 'password_reset.html', {'message': 'Password reset email has been sent if the email is registered. The email might be at spam.'})
        else:
            # For security reasons, don't disclose that the email doesn't exist
            return render(request, 'password_reset.html', {'message': 'Password reset email has been sent if the email is registered. The email might be at spam.'})
    
    return render(request, 'password_reset.html')

def password_reset_confirm(request, uidb64, token):
    try:
        # Decode the user id
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        # Validate the token
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                
                if new_password1 != new_password2:
                    return render(request, 'password_reset_confirm.html', {
                        'validlink': True,
                        'message': 'Passwords do not match.'
                    })
                
                # Set the new password
                user.set_password(new_password1)
                user.save()
                
                # Redirect to sign in page with success message
                return redirect('signin')
            
            return render(request, 'password_reset_confirm.html', {'validlink': True})
        else:
            # Invalid token
            return render(request, 'password_reset_confirm.html', {'validlink': False})
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # Invalid user id
        return render(request, 'password_reset_confirm.html', {'validlink': False})
