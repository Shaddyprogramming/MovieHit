from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from MovieHit.management.movies import Movies
from django.http import HttpResponse, Http404, JsonResponse
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
    query = request.GET.get('q', '')

    if query:
        movies_data = Movies.objects.filter(name__icontains=query)
    else:
        movies_data = Movies.objects.all()

    return render(request, 'index.html', {'movies': movies_data, 'query': query})

def account(request):
    if request.user.is_authenticated:
        return render(request, 'account.html')
    else:
        return redirect('signin')


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
