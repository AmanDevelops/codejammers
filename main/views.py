import re
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse


from .models import competitions, resultmodel, submissions


def home(request):
    return render(request, "main/index.html")


def register(request):
    """
    Handle user registration.

    This function handles user registration by checking if the user is authenticated,
    processing the form data, and performing necessary validations before creating a new user.

    Parameters:
        request (HttpRequest): The request object containing form data and metadata.

    Returns:
        HttpResponse: Redirects to the dashboard if the user is authenticated or
                      the form is successfully submitted. Renders the registration page with
                      an error message if there are validation errors.
    """

    if request.user.is_authenticated:
        return redirect(
            "dash"
        )  # Redirect to dashboard if user is already authenticated

    if request.method != "POST":
        return render(
            request,
            "main/register.html",
        )  # Render the registration form if the request method is not POST

    # Retrieve form data from the request
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    # Check if any of the form fields are None
    if None in [first_name, last_name, username, email, password1, password2]:
        messages.info(request, "Something is Missing")  # Display an error message
        return redirect("register")  # Redirect back to the registration page

    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        messages.info(request, "Username already exists")  # Display an error message
        return redirect("register")  # Redirect back to the registration page

    # Check if the passwords match
    if password1 != password2:
        messages.info(request, "Password not matching")  # Display an error message
        return redirect("register")  # Redirect back to the registration page

    # Check if the email already exists
    if User.objects.filter(email=email).exists():
        messages.info(request, "Email Already Exists")  # Display an error message
        return redirect("register")  # Redirect back to the registration page

    # Create a new user
    new_user = User.objects.create_user(
        username=username,
        password=password1,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    new_user.save()  # Save the user to the database

    # Authenticate and log in the user
    auth_user = auth.authenticate(username=username, password=password1)
    auth.login(request, auth_user)
    return redirect("dash")  # Redirect to the dashboard after successful registration


def login(request):
    """
    Handle user login functionality.

    This function processes the login request. If the user is already authenticated,
    they are redirected to the dashboard. If a POST request is received, it retrieves
    the username and password from the request and attempts to authenticate the user.
    If authentication is successful, the user is logged in and redirected to the dashboard.
    Otherwise, appropriate error messages are displayed and the user is redirected back
    to the login page.

    Args:
        request: The HTTP request object containing user login information.

    Returns:
        HttpResponse: A redirect to the dashboard if login is successful, or the login page with error messages if not.
    """

    # Check if user is already authenticated
    if request.user.is_authenticated:
        return redirect("dash")

    # Handle POST request for login
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if username or password is missing
        if None in [username, password]:
            messages.info(request, "Something is missing")
            return redirect("login")

        # Authenticate the user
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("dash")

        # Authentication failed
        messages.info(request, "Invalid Credentials")
        return redirect("login")

    # Render the login page for GET request
    return render(request, "main/login.html")


def logout(request):
    """
    Handle user logout functionality.

    This function logs out the currently authenticated user and redirects them to the index page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A redirect to the index page after logging out the user.
    """
    # Log out the user
    auth.logout(request)

    # Redirect to the index page
    return redirect("index-load")


def dashboard(request):
    """
    Handle the dashboard view for authenticated users.

    This function checks if the user is authenticated. If so, it retrieves all competition
    objects and renders the dashboard page with the list of competitions. If the user is
    not authenticated, they are redirected to the login page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A rendered dashboard page with a list of competitions for authenticated users,
                      or a redirect to the login page if the user is not authenticated.
    """
    # Check if user is authenticated
    if request.user.is_authenticated:
        # Retrieve all competition objects
        competitions_list = competitions.objects.all()

        # Render the dashboard page with the list of competitions
        return render(
            request, "main/dashboard.html", {"competitions_list": competitions_list}
        )

    # Redirect to the login page if user is not authenticated
    return redirect("login")


def view(request):
    """
    Handle the view functionality for competitions.

    This function retrieves the requested competition id from the query parameters. If the
    id is present, it filters submissions for the current user and the specified competition
    id, retrieves the competition object, and checks if the user has submitted anything for
    the competition. It then renders the view page with the competition and submission details.
    If the id is not present, the user is redirected to the dashboard.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A rendered view page with competition and submission details if the id is present,
                      or a redirect to the dashboard if the id is not present.

    Raises:
        Http404: If the competition with the specified id does not exist.
    """

    # Retrieve the requested competition id from query parameters
    requested_id = request.GET.get("id")
    if requested_id is not None:
        # Filter submissions for the current user and specified competition id
        submissions_list = submissions.objects.filter(
            pgid=requested_id, submitted_by=request.user.username
        )
        # Retrieve the competition object
        competitions_list = get_object_or_404(competitions, id=requested_id)

        # Check if the user has submitted anything for the competition
        isSubmitted = True if len(submissions_list) > 0 else False

        # Render the view page with competition and submission details
        return render(
            request,
            "main/view.html",
            {
                "competitions_list": competitions_list,
                "id": requested_id,
                "submissions_list": submissions_list,
                "isSubmitted": isSubmitted,
            },
        )
    # Redirect to the dashboard if the id is not present
    return redirect("dash")


def submit(request):
    """
    Handle the submission functionality for competitions.

    This function retrieves the requested competition id from the query parameters. If the id is present, it checks if
    the user has already submitted for the competition. If not, it handles the POST request to submit the GitHub Gists
    link. If the link is valid, the submission is saved. If the id is not present or the link is invalid, appropriate
    messages are displayed and the user is redirected.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A rendered submit page for submission id if the id is present and submission does not exist,
                      or a redirect to the appropriate page based on the request status and conditions.

    Raises:
        Http404: If the competition with the specified id does not exist.
    """

    # Retrieve the requested competition id from query parameters
    requested_id = request.GET.get("id")

    if requested_id is not None:
        username = (
            request.user.username
        )  # Check if submission already exists for the user and competition id

        submission_exists = submissions.objects.filter(
            submitted_by=username, pgid=requested_id
        ).exists()

        competition = get_object_or_404(competitions, id=requested_id)

        if not submission_exists:
            # Handle POST request for submission
            if request.method == "POST":
                gists_link = request.POST.get("gists-url")
                gists_link = gists_link.lower()
                gist_url_pattern = (
                    r"https://gist.github.com/[A-Za-z0-9]+/[A-Za-z0-9]+/[A-Za-z0-9]+"
                )

                # Check if the provided gists link is valid
                if not bool(re.match(gist_url_pattern, gists_link)):
                    messages.info(request, "Please provide a Github Gists commit link")
                    return redirect(f"{reverse("submit")}?id={requested_id}")

                # Save the submission
                ready = submissions(
                    pgid=requested_id, submitted_by=username, code=gists_link
                )
                ready.save()
                competition.submissions += 1
                competition.save()
                return redirect(f"{reverse("view")}?id={requested_id}")

            # Render the submit page with submission id
            return render(
                request,
                "main/submit.html",
                {"submission_id": requested_id, "competition": competition},
            )
        # Redirect to the view page if submission already exists
        return redirect(f"{reverse("view")}?id={requested_id}")
    # Redirect to the dashboard if id is not present
    return redirect("dash")


def code(request):
    """
    Handle the view functionality for a specific submission.

    This function retrieves the requested submission id from the query parameters. If the id is present,
    it checks if the submission exists and whether the current user is authorized to view it based on the
    submission ownership or competition result availability. If authorized, it renders the submission page.
    If the id is not present, the user is redirected to the dashboard.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A rendered submissions page with the submission details if the id is present and the user
                      is authorized, or a redirect to the appropriate page based on the request status and conditions.

    Raises:
        Http404: If the submission with the specified id does not exist.
    """
    # Retrieve the requested submission id from query parameters
    request_id = request.GET.get("id")
    if request_id is None:
        return redirect("dash")

    # Retrieve the submission object
    data = get_object_or_404(submissions, id=request_id)
    is_result_declared = get_object_or_404(competitions, id=data.pgid).result
    # Check if the user is authorized to view the submission
    if data.submitted_by == request.user.username or is_result_declared:
        # Render the submissions page with the submission details
        return render(request, "main/submissions.html", {"data": data})
    # Redirect to the index page if the user is not authorized
    return redirect("dash")


def result(request):
    """
    Handle the result view functionality for a specific competition.

    This function retrieves the requested competition id from the query parameters. If the id is present,
    it checks if the competition results are available. If not, it redirects the user to the competition
    view page. If results are available, it retrieves the result list and submission list for the competition
    and renders the result page. If the id is not present, the user is redirected to the dashboard.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A rendered result page with competition results and submission details if the id is present and
                      results are available, or a redirect to the appropriate page based on the request status and conditions.

    Raises:
        Http404: If the competition with the specified id does not exist.
    """

    # Retrieve the requested competition id from query parameters
    request_id = request.GET.get("id")
    if request_id is not None:
        # Retrieve the competition object
        competition_list = get_object_or_404(competitions, id=request_id)
        # Check if competition results are available
        if not competition_list.result:
            return redirect(f"{reverse('view')}?id={request_id}")
        # Retrieve the result list and submission list for the competition
        result_list = resultmodel.objects.filter(comp_id=request_id)
        submission_list = submissions.objects.filter(pgid=request_id)

        # Render the result page with competition results and submission details
        return render(
            request,
            "main/result.html",
            {
                "results_list": result_list,
                "submod": submission_list,
                "competition_info": competition_list,
            },
        )
    # Redirect to the dashboard if id is not present
    return redirect("dash")


def contact(request):
    return render(request, "main/contact.html")


def coming_soon(request):
    return render(request, "main/coming-soon.html")
