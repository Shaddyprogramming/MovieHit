from django.shortcuts import render, redirect, get_object_or_404 # Importing necessary functions from Django's shortcuts module
from django.contrib.auth import authenticate, login # Importing authentication and login functions from Django's authentication system
from django.contrib.auth.models import User # Importing User model from Django's authentication system
from django.contrib.auth.tokens import default_token_generator # Importing default token generator for password reset and email confirmation
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # Importing functions for encoding and decoding URLs
from django.utils.encoding import force_bytes, force_str # Importing functions for encoding and decoding strings
from django.core.mail import send_mail # Importing send_mail function for sending emails
from django.template.loader import render_to_string # Importing render_to_string for rendering templates to strings
from django.contrib.sites.shortcuts import get_current_site # Importing get_current_site to get the current site information
from django.conf import settings # Importing settings from Django's configuration module
from django.contrib.auth.decorators import login_required # Importing login_required decorator to restrict access to authenticated users
from MovieHit.management.movies import Movies # Importing Movies model from the movies module in management package
from MovieHit.management.banners import Banners # Importing Banners model from the banners module in management package
from MovieHit.management.comments import Comment #  Importing Comment model from the comments module in management package
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseForbidden # Importing necessary HTTP response classes from Django's http module
import os # Importing os module for file path operations

def serve_media(request, path): 
    """
    Serve media files in production.
    """
    media_path = os.path.join(settings.MEDIA_ROOT, path) # Construct the full path to the media file
    
    if not os.path.exists(media_path): # Check if the media file exists
        raise Http404("Media file not found.") # Raise 404 error if the file does not exist
    
    with open(media_path, 'rb') as media_file: # Open the media file in binary read mode
        response = HttpResponse(media_file.read(), content_type="application/octet-stream") # Create an HTTP response with the file content and set the content type to binary
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(media_path)}"' # Set the Content-Disposition header to inline, allowing the browser to display the file if possible
        return response # Return the HTTP response with the media file content

def index(request):
    """
    Main view for the index/main page.
    """
    query = request.GET.get('q', '') # Get the search query from GET parameters, default to empty string if not provided
    sort_by = request.GET.get('sort', 'year') # Get the sort parameter from GET parameters, default to 'year' if not provided

    order_sensitive = False # Default to case-insensitive search

    if request.user.is_authenticated and 'orderSensitiveSearch' in request.session:  # Check if the user is authenticated and has a session variable for order sensitive search
        order_sensitive = request.session.get('orderSensitiveSearch') # Get the order sensitive search preference from the session
    elif request.COOKIES.get('orderSensitiveSearch') == 'true': # Check if the cookie for order sensitive search is set to 'true'
        order_sensitive = True # Set order sensitive search to True if the cookie is present and set to 'true'
    
    if query: # If a search query is provided
        if order_sensitive: # If order sensitive search is enabled
            movies_data = Movies.objects.filter(name__istartswith=query) # Perform case-sensitive search using istartswith for order sensitive search
        else: 
            movies_data = Movies.objects.filter(name__icontains=query) # Perform case-insensitive search using icontains for order insensitive search
    else:
        movies_data = Movies.objects.all() # If no query is provided, get all movies
    
    if sort_by == 'rating': # If the sort parameter is 'rating'
        movies_data = movies_data.order_by('-rating') # Order movies by rating in descending order
    else:
        movies_data = movies_data.order_by('-year') # Default ordering by year in descending order
        
    banners_data = Banners.objects.all() # Get all banners from the Banners model
    
    return render(request, 'index.html', { # Render the index template with the following context
        'banners': banners_data,  # List of banners to be displayed on the index page
        'movies': movies_data,  # List of movies to be displayed on the index page
        'query': query, # The search query entered by the user
        'sort': sort_by # The sorting parameter used for ordering the movies
    })

def save_preference(request):
    """
    Save user preferences like order sensitive search setting or auto playing trailers.
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest': # Check if the request is a POST request and an AJAX request
        try:
            preference_name = request.POST.get('preference_name') # Get the preference name from POST data
            preference_value = request.POST.get('preference_value') == 'true' # Convert the preference value to boolean
            
            if preference_name == 'orderSensitiveSearch': # Check if the preference is for order sensitive search
                request.session['orderSensitiveSearch'] = preference_value # Save the preference in the session
                
                response = JsonResponse({'success': True}) # Create a JSON response indicating success
                
                max_age = 365 * 24 * 60 * 60  # One year in seconds
                response.set_cookie( # Set a cookie for the preference
                    'orderSensitiveSearch',
                    str(preference_value).lower(),  # Convert boolean to string and lower case
                    max_age=max_age, # Set the cookie to expire in one year
                    secure=request.is_secure(), # Use secure cookie if the request is secure (HTTPS)
                    httponly=False # Allow JavaScript to access the cookie (not httponly for AJAX requests, but consider security implications
                )
                return response
            
            return JsonResponse({'success': False, 'error': 'Unknown preference'}) # If the preference name is not recognized, return an error
        except Exception as e: # Handle any exceptions that occur during the process
            return JsonResponse({'success': False, 'error': str(e)}) # Return a JSON response with the error message
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400) # Bad request if the method is not POST or not an AJAX request


def movie_detail(request, movie_id): 
    """
    View for displaying details of a specific movie.
    Uses the unique_id field from the Movies model.
    """
    movie = get_object_or_404(Movies, unique_id=movie_id) # Get the movie object by unique_id, or return 404 if not found
    
    comments = Comment.objects.filter(movie=movie) # Get all comments related to the movie
    
    return render(request, 'movie_detail.html', {'movie': movie, 'comments': comments}) # Render the movie detail template with the movie and comments context

@login_required # Decorator to ensure the user is authenticated before accessing this view
def add_comment(request, movie_id): 
    """
    View for adding a comment to a movie.
    """
    if request.method == 'POST': # Check if the request method is POST
        movie = get_object_or_404(Movies, unique_id=movie_id) # Get the movie object by unique_id, or return 404 if not found
        text = request.POST.get('comment_text', '').strip() # Get the comment text from POST data and strip leading/trailing whitespace
        rating = int(request.POST.get('rating', 0)) # Get the rating from POST data, default to 0 if not provided
        
        if text: # If the comment text is not empty
            Comment.objects.create( # Create a new Comment object
                movie=movie, # Associate the comment with the movie
                user=request.user, # Associate the comment with the current user
                text=text, # Set the comment text
                rating=rating # Set the rating for the comment
            )
    
    return redirect('movie_detail', movie_id=movie_id) # Redirect to the movie detail page after adding the comment

@login_required # Decorator to ensure the user is authenticated before accessing this view
def edit_comment(request, movie_id, comment_id):
    """
    View for editing a comment on a movie.
    """
    comment = get_object_or_404(Comment, id=comment_id) # Get the comment object by its ID, or return 404 if not found
    
    if request.user != comment.user: # Check if the current user is the owner of the comment
        return HttpResponseForbidden("You don't have permission to edit this comment.") # Return 403 Forbidden if the user is not the owner of the comment
    
    if request.method == 'POST': # Check if the request method is POST
        text = request.POST.get('edit_comment_text', '').strip() # Get the edited comment text from POST data and strip leading/trailing whitespace
        rating = int(request.POST.get('edit_rating', 0)) # Get the edited rating from POST data, default to 0 if not provided
        
        if text:
            comment.text = text # Update the comment text
            comment.rating = rating # Update the rating for the comment
            comment.save() # Save the changes to the comment object
    
    return redirect('movie_detail', movie_id=movie_id) # Redirect to the movie detail page after editing the comment

@login_required
def delete_comment(request, movie_id, comment_id):
    """
    View for deleting a comment on a movie.
    """
    comment = get_object_or_404(Comment, id=comment_id) # Get the comment object by its ID, or return 404 if not found
    
    if request.user != comment.user: # Check if the current user is the owner of the comment
        return HttpResponseForbidden("You don't have permission to delete this comment.")  # Return 403 Forbidden if the user is not the owner of the comment
    
    if request.method == 'POST': # Check if the request method is POST
        comment.delete() # Delete the comment object
    
    return redirect('movie_detail', movie_id=movie_id) # Redirect to the movie detail page after deleting the comment

def account(request):
    """
    View for displaying the user's account information.
    """
    if request.user.is_authenticated: # Check if the user is authenticated
        email_parts = request.user.email.split('@') if request.user.email else ['', ''] # Split the email into parts if it exists, otherwise set to empty strings
        return render(request, 'account.html', {'email_parts': email_parts}) # Render the account template with the email parts context
    else:
        return redirect('signin') # Redirect to the sign-in page if the user is not authenticated

def edit_profile(request):
    """
    View for editing the user's profile information.
    """
    if not request.user.is_authenticated: # Check if the user is authenticated
        return redirect('signin') # Redirect to the sign-in page if the user is not authenticated
        
    message = None # Initialize message to None
    error = False # Initialize error to False
    
    if request.method == 'POST': # Check if the request method is POST
        username = request.POST.get('username') # Get the username from POST data
        first_name = request.POST.get('first_name') # Get the first name from POST data
        last_name = request.POST.get('last_name') # Get the last name from POST data
        
        if User.objects.exclude(pk=request.user.pk).filter(username=username).exists(): # Check if the username already exists, excluding the current user
            message = "Username already exists" # Set message if username already exists
            error = True # Set error to True if there is an error
        else:
            user = request.user # Get the current user object\
            user.username = username # Update the username of the user
            user.first_name = first_name # Update the first name of the user
            user.last_name = last_name # Update the last name of the user
            user.save() # Save the changes to the user object
            message = "Profile updated successfully" # Set success message after updating the profile
            
    return render(request, 'edit_profile.html', {'message': message, 'error': error}) # Render the edit profile template with the message and error context

def update_email(request):
    """
    View for initiating the email update process.
    """
    if not request.user.is_authenticated: # Check if the user is authenticated
        return JsonResponse({'success': False, 'error': 'Authentication required'}) # Return JSON response with error if user is not authenticated
    
    if request.method != 'POST' or not request.headers.get('X-Requested-With') == 'XMLHttpRequest': # Check if the request method is POST and if it is an AJAX request
        return JsonResponse({'success': False, 'error': 'Invalid request'}) # Return JSON response with error if the request is not valid
    
    try:
        user = request.user # Get the current user object
        
        if not user.email:
            return JsonResponse({'success': False, 'error': 'You need to have an email set up first'}) # Return JSON response with error if the user does not have an email set up
            
        token = default_token_generator.make_token(user) # Generate a token for the user using the default token generator
        uid = urlsafe_base64_encode(force_bytes(user.pk)) # Encode the user ID to a URL-safe base64 string
        new_email_b64 = urlsafe_base64_encode(force_bytes('placeholder')) # Placeholder for the new email, encoded to a URL-safe base64 string
        
        current_site = get_current_site(request) # Get the current site information
        protocol = 'https' if request.is_secure() else 'http' # Determine the protocol (https or http) based on the request
        
        context = {
            'user': user, # Current user object
            'domain': current_site.domain, # Domain of the current site
            'uid': uid, # Encoded user ID
            'token': token, # Generated token for the user
            'new_email_b64': new_email_b64, # Placeholder for the new email, encoded to a URL-safe base64 string
            'protocol': protocol, # Protocol (https or http)
            'site_name': 'MovieHit' # Name of the site to be used in the email template
        }
        
        email_subject = 'Change Email Address for MovieHit' # Subject of the email for changing the email address
        email_body = render_to_string('email_update_email.html', context) # Render the email body using the context and the email template
        
        send_mail(
            email_subject, # Send the email with the subject
            email_body, # Send the email with the rendered body
            settings.DEFAULT_FROM_EMAIL, # Default email address from settings
            [user.email], # Send the email to the user's current email address
            fail_silently=False
        )
        
        return JsonResponse({'success': True, 'message': 'Email update link sent to your current email address'}) # Return JSON response indicating success and message
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}) # Return JSON response with error if any exception occurs


def email_update_confirm(request, uidb64, token, new_email_b64):
    """
    View for confirming the email update process.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) # Decode the user ID from the URL-safe base64 string
        user = User.objects.get(pk=uid) # Get the user object by the decoded user ID
        
        if default_token_generator.check_token(user, token): # Check if the token is valid for the user
            if request.method == 'POST': # Check if the request method is POST
                new_email = request.POST.get('new_email') # Get the new email from POST data
                
                if not new_email:
                    return render(request, 'email_update_confirm.html', {
                        'validlink': True, # Email update link is valid
                        'message': 'Email address is required.', # Set message if email address is not provided
                        'form_submitted': False
                    })
                
                if User.objects.exclude(pk=user.pk).filter(email=new_email).exists(): # Check if the new email already exists for another user, excluding the current user
                    return render(request, 'email_update_confirm.html', { 
                        'validlink': True, # Email update link is valid
                        'message': 'This email is already in use by another account.', # Set message if the new email is already in use
                        'form_submitted': False # Set form_submitted to False to show the form again
                    })
                
                had_previous_email = bool(user.email) # Check if the user had a previous email address
                old_email = user.email # Store the old email address before updating
                user.email = new_email # Update the user's email address to the new email
                user.save()
                
                if had_previous_email: # If the user had a previous email address, send a notification to the old email
                    notification_subject = 'Email Address Updated for MovieHit Account' # Subject of the notification email for email address update
                    notification_body = "Your email address for your MovieHit account has been updated. If you did not make this change, please secure your account immediately by resetting your password." # Body of the notification email
                    send_mail(
                        notification_subject, #Send the notification email with the subject
                        notification_body, # Send the notification email with the body
                        settings.DEFAULT_FROM_EMAIL, # Default email address from settings
                        [old_email], # Send the notification email to the old email address
                        fail_silently=True # Fail silently if the email sending fails, to avoid breaking the user experience
                    )
                
                return render(request, 'email_update_confirm.html', {
                    'validlink': True, # Email update link is valid
                    'message': 'Your email has been updated successfully.', # Set success message after updating the email
                    'form_submitted': True # Set form_submitted to True to indicate that the form has been submitted
                })
            
            return render(request, 'email_update_confirm.html', {
                'validlink': True, # Email update link is valid
                'form_submitted': False # Set form_submitted to False to show the form for email update
            })
        else:
            return render(request, 'email_update_confirm.html', {
                'validlink': False, # Email update link is invalid
                'message': 'The confirmation link is invalid or has expired.' # Set message if the confirmation link is invalid or expired
            })
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'email_update_confirm.html', {
            'validlink': False, # Email update link is invalid
            'message': 'The confirmation link is invalid.' # Set message if the confirmation link is invalid
        })


def signin(request):
    """
    View for handling user sign-in and registration.
    """
    error = None # Initialize error to None
    
    if request.method == 'POST': # Check if the request method is POST
        action = request.POST.get('action', '') # Get the action from POST data, default to empty string if not provided
        
        if action == 'register':
            username = request.POST.get('username') # Get the username from POST data
            password = request.POST.get('password') # Get the password from POST data
            confirm_password = request.POST.get('confirm_password') # Get the confirm password from POST data
            fullname = request.POST.get('fullname', '') # Get the full name from POST data, default to empty string if not provided
            
            if password != confirm_password:
                error = "Passwords do not match." # Set error if passwords do not match
            elif User.objects.filter(username=username).exists():
                error = "Username already exists." # Set error if the username already exists
            else:
                name_parts = fullname.split(' ', 1) # Split the full name into first and last name, allowing for a single space
                first_name = name_parts[0] # First part is the first name
                last_name = name_parts[1] if len(name_parts) > 1 else '' # Second part is the last name, if it exists, otherwise set to empty string
                
                user = User.objects.create_user(
                    username=username, # Create a new user with the provided username
                    password=password, # Set the password for the new user
                    first_name=first_name, # Set the first name for the new user
                    last_name=last_name # Set the last name for the new user (if provided, otherwise it will be empty
                )
                
                login(request, user) # Log in the user after successful registration
                return redirect('index') # Redirect to the index page after successful registration and login
        else:
            username = request.POST.get('username') # Get the username from POST data
            password = request.POST.get('password') # Get the password from POST data
            user = authenticate(request, username=username, password=password) # Authenticate the user with the provided username and password
            
            if user is not None:
                login(request, user)
                return redirect('index') # Redirect to the index page after successful login
            else:
                error = "Invalid credentials. Please try again."
    
    return render(request, 'signin.html', {'error': error}) # Render the sign-in template with the error context if any

def password_reset(request):
    """
    View for handling password reset requests.
    """
    if request.method == 'POST': # Check if the request method is POST
        email = request.POST.get('email') # Get the email from POST data
        direct_reset = request.POST.get('direct_reset') # Check if the direct reset option is selected
        
        users = User.objects.filter(email=email) # Get all users with the provided email address
        
        if direct_reset and request.headers.get('X-Requested-With') == 'XMLHttpRequest': # Check if the direct reset option is selected and if the request is an AJAX request
            if not email or not users.exists(): # Check if the email is provided and if there are users with that email
                return JsonResponse({'success': False, 'error': 'Email not found or not provided'}) # Return JSON response with error if email is not found or not provided
                
            for user in users: # For each user with the provided email address
                token = default_token_generator.make_token(user) # Generate a token for the user using the default token generator
                uid = urlsafe_base64_encode(force_bytes(user.pk)) # Encode the user ID to a URL-safe base64 string
                
                current_site = get_current_site(request) # Get the current site information
                protocol = 'https' if request.is_secure() else 'http' # Determine the protocol (https or http) based on the request
                
                context = {
                    'user': user, # Current user object
                    'domain': current_site.domain, # Domain of the current site
                    'uid': uid, # Encoded user ID
                    'token': token, # Generated token for the user
                    'protocol': protocol, # Protocol (https or http)
                    'site_name': 'MovieHit' # Name of the site to be used in the email template
                }
                
                email_subject = 'Password Reset Request for MovieHit' # Subject of the password reset email
                email_body = render_to_string('password_reset_email.html', context) # Render the email body using the context and the email template
                
                send_mail(
                    email_subject, # Send the email with the subject
                    email_body, # Send the email with the rendered body
                    settings.DEFAULT_FROM_EMAIL, # Default email address from settings
                    [user.email], # Send the email to the user's email address
                    fail_silently=False # Fail silently if the email sending fails, to avoid breaking the user experience
                )
            
            return JsonResponse({'success': True}) # Return JSON response indicating success for direct reset
            
        if users.exists(): # If there are users with the provided email address
            for user in users: # For each user with the provided email address
                token = default_token_generator.make_token(user)  # Generate a token for the user using the default token generator
                uid = urlsafe_base64_encode(force_bytes(user.pk)) # Encode the user ID to a URL-safe base64 string
                
                current_site = get_current_site(request) # Get the current site information
                protocol = 'https' if request.is_secure() else 'http' # Determine the protocol (https or http) based on the request
                
                context = {
                    'user': user, # Current user object
                    'domain': current_site.domain,  # Domain of the current site
                    'uid': uid, # Encoded user ID
                    'token': token, # Generated token for the user
                    'protocol': protocol, # Protocol (https or http)
                    'site_name': 'MovieHit' # Name of the site to be used in the email template
                }
                
                email_subject = 'Password Reset Request for MovieHit' # Subject of the password reset email
                email_body = render_to_string('password_reset_email.html', context) # Render the email body using the context and the email template
                
                send_mail(
                    email_subject, # Send the email with the subject
                    email_body,     # Send the email with the rendered body
                    settings.DEFAULT_FROM_EMAIL, # Default email address from settings
                    [user.email], # Send the email to the user's email address
                    fail_silently=False # Fail silently if the email sending fails, to avoid breaking the user experience
                )
            
            return render(request, 'password_reset.html', {'message': 'Password reset email has been sent if the email is registered. The email might be at spam.'})
        else:
            return render(request, 'password_reset.html', {'message': 'Password reset email has been sent if the email is registered. The email might be at spam.'})
    
    return render(request, 'password_reset.html') # Render the password reset template for GET requests

def password_reset_confirm(request, uidb64, token):
    """
    View for confirming the password reset process.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) # Decode the user ID from the URL-safe base64 string
        user = User.objects.get(pk=uid) # Get the user object by the decoded user ID
        
        if default_token_generator.check_token(user, token): # Check if the token is valid for the user
            if request.method == 'POST': # Check if the request method is POST
                new_password1 = request.POST.get('new_password1') # Get the new password from POST data
                new_password2 = request.POST.get('new_password2') # Get the confirm new password from POST data
                
                if new_password1 != new_password2: # Check if the new passwords match
                    return render(request, 'password_reset_confirm.html', {
                        'validlink': True,
                        'message': 'Passwords do not match.'
                    })
                
                user.set_password(new_password1) # Set the new password for the user
                user.save() # Save the changes to the user object
                
                return redirect('signin') # Redirect to the sign-in page after successful password reset
            
            return render(request, 'password_reset_confirm.html', {'validlink': True}) # Render the password reset confirm template for GET requests with valid link
        else:
            return render(request, 'password_reset_confirm.html', {'validlink': False}) # Render the password reset confirm template with invalid link if the token is not valid for the user
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'password_reset_confirm.html', {'validlink': False}) # Render the password reset confirm template with invalid link if there is an error decoding the user ID or if the user does not exist
