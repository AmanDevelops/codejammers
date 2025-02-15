from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render, get_object_or_404

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
    if request.user.is_authenticated:
        comps = competitions.objects.all()
        return render(request, "main/dashboard.html", {"comps": comps})
    else:
        return redirect("login")


def view(request):
    if request.GET.get("id") is not None:
        idg = request.GET["id"]
        subs = submissions.objects.filter(pgid=idg)
        comp = get_object_or_404(competitions, id=idg)

        submitted = submissions.objects.filter(
            submitted_by=request.user.username, pgid=idg
        ).exists()

        return render(
            request,
            "main/view.html",
            {"comps": comp, "id": idg, "sub": subs, "submitted": submitted, "pos": 0},
        )
    else:
        return redirect("/login")


def submit(request):
    pgidget = request.GET.get("id")
    if pgidget is not None:
        username = request.user.username
        subs2 = submissions.objects.filter(submitted_by=username, pgid=pgidget).exists()
        # print(subs2)
        # a = ""
        # for subal in subs2:
        #     a = subal.submitted_by

        if not subs2:
            if request.method == "POST":
                link = request.POST["code"]
                pgidget = request.GET.get("id")
                temp_link = link.lower()
                if temp_link.find("https://gist.github.com/") == -1:
                    messages.info(request, "Please Paste The Google Collab Link")
                    return redirect("/submit?id=" + pgidget)
                else:
                    username = request.user.username

                    ready = submissions(pgid=pgidget, submitted_by=username, code=link)
                    ready.save()
                    return redirect("/view?id=" + pgidget)
            else:
                pgidget1 = request.GET["id"]
                return render(
                    request,
                    "main/submit.html",
                    {
                        "idgt": pgidget1,
                    },
                )
        else:
            return redirect("/view?id=" + pgidget)
    else:
        return redirect("/dashboard")


def code(request):
    idd = request.GET["id"]
    data = submissions.objects.filter(id=idd)

    return render(request, "main/submissions.html", {"data": data})


def result(request):
    cid = request.GET.get("id")
    if cid is not None:
        res = resultmodel.objects.filter(comp_id=cid)
        subs = submissions.objects.filter(pgid=cid)

        return render(request, "main/result.html", {"resmod": res, "submod": subs})
    else:
        return redirect("/dashboard")


def contact(request):
    return render(request, "main/contact.html")


def coming_soon(request):
    return render(request, "main/coming-soon.html")
