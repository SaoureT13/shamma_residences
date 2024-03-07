from shamma_residences import settings
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)  # Sert a decoder/encoder du text
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .utils import keys
from twilio.rest import Client
import random
import string

from resi.models import CustomUser, Customer, Department, Room


def generate_random_code():
    characters = string.ascii_letters + string.digits
    # Générer un code aléatoire à 6 caractères
    code = "".join(random.choices(characters, k=6))
    return code


def index(request):
    context = {}
    # department_name = request.GET.get("department")
    # if department_name:
    #     department = Department.objects.get(name=department_name)
    #     return render(request, "resi/index.html", {"department": department})
    context["departments"] = Department.objects.all()
    rooms = Room.objects.all()
    context["rooms"] = render_to_string(
        "resi/residences.html", context={"rooms": rooms}
    )

    return render(request, "resi/index.html", {"context": context})
    # return render(request, "resi/authentification/signup.html")


code = generate_random_code()
print(code)


def sign_up(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        contact = request.POST.get("contact")

        if email != "":
            if CustomUser.objects.filter(email=email):
                return JsonResponse({"error": "This email has an account"})
            else:
                my_user = CustomUser.objects.create_user(email=email, password=password)

        if contact != "":
            if CustomUser.objects.filter(phone_number=contact):
                return JsonResponse({"error": "This number has an account"})
            else:
                my_user = CustomUser.objects.create_user(
                    phone_number=contact, password=password
                )

        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()

        my_customer = Customer.objects.create(
            user=my_user, first_name=firstname, last_name=lastname, phone_number=contact
        )
        my_customer.save()

        ##Pour la mise en production, envoyer le code par email  s'il a entrer une email ou par numero de telephone s'il a entrer un numero de telephone

        # Envoi de code de validation par email
        company_name = "SHAMMA Residences"
        confirmation_code = code

        email_subject = "Verification de compte"
        email_template = "resi/authentification/confirmation_sent.html"
        email_context = {
            "company_name": company_name,
            "confirmation_code": confirmation_code,
            "user_lastname": my_user.last_name,
            "user_email": my_user.email,
        }
        email_content = render_to_string(email_template, email_context)

        send_mail(
            email_subject,
            "",
            settings.EMAIL_HOST_USER,
            [my_user.email],
            html_message=email_content,
        )

        # Envoi de code de validation par message
        # client = Client(keys.account_sid, keys.auth_token)
        # message = client.messages.create(
        #     from_="+12698415390", body=f"{code}", to=f"+225{contact}"
        # )

        uid = urlsafe_base64_encode(force_bytes(my_user.pk))
        print(uid)
        return JsonResponse({"uid": uid})
    # return JsonResponse({"message": "Méthode non autorisée"}, status=405)
    return render(request, "resi/authentification/signup.html")


def confirm_account(request):
    if request.method == "POST":
        user_code = request.POST.get("code")
        uidb64 = request.POST.get("user_id")

        if user_code == code:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                my_user = CustomUser.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                my_user = None

            if my_user is not None:
                my_user.is_active = True
                my_user.save()
                login(request, my_user)
            return redirect("resi:home")
        else:
            messages.add_message(request, messages.ERROR, "The code did not match! ")
            return render(
                request,
                "resi/authentification/confirm.html",
                {"messages": messages.get_messages(request)},
            )

    return render(request, "resi/authentification/confirm.html")


def log_in(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        password = request.POST["password"]
        # user = authenticate(request, username=email, password=password)

        try:
            user = CustomUser.objects.get(pk=user_id)
            if user.check_password(password):
                login(request, user)
                return redirect("resi:home")
            else:
                messages.add_message(
                    request, messages.ERROR, "Password did not match! "
                )
                return render(
                    request,
                    "resi/authentification/login.html",
                    {"messages": messages.get_messages(request)},
                )
        except CustomUser.DoesNotExist:
            messages.add_message(request, messages.ERROR, "User not found! ")
            return render(
                request,
                "resi/authentification/login.html",
                {"messages": messages.get_messages(request)},
            )

    return render(request, "resi/authentification/login.html")


def verification_account(request):
    if request.method == "POST":
        input = request.POST["email_or_number"]

        if "@" in input:
            email = input
            user = CustomUser.objects.get(email=email)
            if user is not None:
                return render(
                    request, "resi/authentification/login.html", {"user_id": user.id}
                )
            else:
                messages.add_message(request, messages.ERROR, "This user not exist! ")
                return render(
                    request,
                    "resi/authentification/login.html",
                    {"messages": messages.get_messages(request)},
                )

        else:
            phone_number = input
            user = CustomUser.objects.get(phone_number=phone_number)

            if user is not None:
                return render(
                    request, "resi/authentification/login.html", {"user_id": user.id}
                )
            else:
                messages.add_message(request, messages.ERROR, "This user not exist! ")
                return render(
                    request,
                    "resi/authentification/login.html",
                    {"messages": messages.get_messages(request)},
                )

    return render(request, "resi/authentification/login.html")


def log_out(request):
    logout(request)
    messages.success(request, "logout successfully!")
    return redirect("resi:home")


def account_details(request):
    return render(request, "resi/customer/account.html")


def get_rooms(request, department_pk):

    # department = Department.objects.get(pk=department_pk)
    department = get_object_or_404(Department, pk=department_pk)
    rooms = department.rooms.all()
    return render(request, "resi/residences.html", {"rooms": rooms})
