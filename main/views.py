from django.shortcuts import render, HttpResponseRedirect
import shutil
import os
from main import models, forms, art_res
from main.caption import generate_text, beam_search_predictions
from django.conf import settings
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, array_to_img, load_img
from googletrans import Translator
import googletrans

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate

from .forms import SignUpForm

code_to_lang = googletrans.LANGUAGES
lang_to_code = {}
genre = []
for key, val in code_to_lang.items():
    lang_to_code[val] = key
    genre.append([val, val])

global text
global username
global ans

# web: waitress-serve --port=$PORT ImageCaption.wsgi:application


def index(request):
    imgform = forms.ImageCaptionForm()
    context = {
        'imgform': imgform,
        'options': models.df_data
    }
    if request.method == 'POST':
        print("hello", request.POST)
        models.ImageCaption.objects.all().delete()
        try:
            shutil.rmtree("media/uploads/image/")
        except Exception as e:
            print(e)
        imgform = forms.ImageCaptionForm(request.POST, files=request.FILES)
        if imgform.is_valid():
            imgform = imgform.save()
            if str(models.ImageCaption.objects.all()[0].img) == "":
                url = "media/original/images.jpg"
            else:
                url = models.ImageCaption.objects.all()[0].img.url[1:]
            print(f"The selecterd image url is {url}")
            global text
            text = beam_search_predictions(url, 5)
            context = {
                'imgform': url,
                # 'text' : generate_text(url),
                'text': text,
                'res': True,
                'options': models.df_data,
                "genre": models.df_category
            }
    print("llll", context["options"])
    return render(request, "main/index.html", context)


def result(request):
    context = {}
    if request.method == 'POST':
        print("hello", request.POST)
        models.machine_translation.objects.all().delete()
        print(f"ac_format1")
        imgform = forms.machine_translation_form(
            request.POST, files=request.FILES)
        print(f"ac_format1", imgform.is_valid())
        if imgform.is_valid():
            print(f"ac_format1")
            imgform = imgform.save()
            print(f"ac_format1")
            url = models.machine_translation.objects.all()[0].format
            print(f"ac_format {url}")
            code = lang_to_code[url]
            print(code)
            translator = Translator()
            msg = translator.translate(text, dest=code).text
            print(msg)
            context = {
                "first_lang": "English",
                "second_lang": url.capitalize(),
                "Original": text,
                "Message": msg,
                "res": True,
                "genre": models.df_category
            }
    return render(request, "main/result2.html", context)


def find_article(request):
    article_form = forms.Article_finder_form(request.POST)
    print("jhj1")
    if article_form.is_valid():  # application label validation
        print("jhj1")
        student = article_form.save()
        print("jhj1")
    article_form = models.article_finder.objects.all()

    format = models.article_finder.objects.all().last().format
    print("ggggg", text, format)
    context = {
        'trans_form': article_form,
        "projects": settings.DATA["PROJECTS"]
    }
    print("sgsjshjs", context)
    # context["res"] = [["kjhgs", "kslkhks"], ["khgs", "kshks"],
    #                   ["kjhgs", "kskhks"], ["khgs", "ksh"]]
    context["res"] = art_res.req_res(text, format)
    print("hdhdhgd", context["res"])
    return render(request, 'main/result3.html', context)


def about_me(request):
    context = {}
    if request.method == 'POST':
        print("helloggg", request.POST)
    return render(request, 'main/about_me.html', context)


def technology(request):
    context = {
        "technology": settings.DATA["TECHNOLOGY"]
    }
    print(context)
    return render(request, 'main/technology.html', context)


def projects(request):
    context = {
        "projects": settings.DATA["PROJECTS"]
    }
    print(context)
    return render(request, 'main/projects.html', context)


class SignUpView(generic.CreateView):
    print("kskskkskkskskkskksk")
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "main/signup.html"


def signin(request):
    context = {}
    if request.method == 'POST':
        print("hello", request.POST)
        sigin_form = forms.Sign_in_form(
            request.POST)
        print(f"ac_format1", sigin_form.is_valid())
        if sigin_form.is_valid():
            sigin_form = sigin_form.save()
            print(f"ac_format1")
            url = models.signin_data.objects.all()
            print("dggdgdg", url)
    return render(request, "main/result2.html", context)


def login(request):
    global username
    form = SignUpForm()
    context = {
        "form": form,
    }
    if request.method == 'POST':
        print("tata", request.POST)
        user_name = request.POST.get("username")
        password = request.POST.get("password1")
        print("dhhdjjdjjh", user_name, password)
        user = authenticate(username=user_name, password=password)
        if user is not None:
            print("jhjvjhvdjvjdbvjhbjvjvjvjjvj", user_name, password)
            username = user_name
            context["username"] = username
            art_res.create_asset_transportation_request(username)
        else:
            return render(request, "main/login.html", context)
        if username == "last":
            return HttpResponseRedirect('my_asset_transportation_requests')
        else:
            return HttpResponseRedirect('my_asset_transportation_requests')

    return render(request, "main/login.html", context)


# def sign_up(request):
#     context = {}
#     if request.method == 'POST':
#         print("tata", request.POST)
#         sigin_form = forms.Sign_in_form(
#             request.POST)
#         print(f"ac_format1", sigin_form.is_valid())
#         print(f"ac_format1", sigin_form)
#         if sigin_form.is_valid():
#             print(f"ac_format1")
#             sigin_form = sigin_form.save()
#             print(f"ac_format1")
#             url = models.signin_data.objects.all()
#             print("dggdgdg", url)
#     return render(request, "main/sign_up.html", context)

def sign_up(request):
    global username
    try:
        context = {
            "username": username
        }
    except:
        return HttpResponseRedirect('login')
    if request.method == 'POST':
        print("tata", request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("tata1")
            user.set_password(request.POST.get("password1"))
            print("tata2")
            user = form.save()
            print("tata3")
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()
            username = request.POST.get("username")
            art_res.create_asset_transportation_request(username)
            return HttpResponseRedirect('my_asset_transportation_requests')
            # raw_password = form.cleaned_data.get('password1')
            # print("shbjhsbjbjhb", raw_password)

            # login user after signing up
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)

            # redirect user to home page
            # return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'main/sign_up.html', {'form': form})


def asset_transportation_request(request):
    global username
    try:
        context = {
            "asset_type": ["LAPTOP", "TRAVEL_BAG", "PACKAGE"],
            "sensitivity": ["HIGHLY_SENSITIVE", "SENSITIVE", "NORMAL"],
            "username": username
        }
    except:
        return HttpResponseRedirect('login')
    print(context)
    if request.method == 'POST':
        print("asset_transportation_request", request.POST)
        asset_transportation_request_form = forms.asset_transport_req_form(
            request.POST)
        print("asset_transportation_request",
              asset_transportation_request_form.is_valid())
        if asset_transportation_request_form.is_valid():  # application label validation
            print("asset_transportation_request")
            student = asset_transportation_request_form.save()
            print("jjjj", student)
            art_res.append_asset_transportation_request(
                models.asset_transport_request_model.objects.last().__dict__)
        print("gagagga", request.POST)
        return HttpResponseRedirect('my_asset_transportation_requests')
    return render(request, 'main/asset_transportation_request.html', context)


def share_travel_info(request):
    global username
    try:
        context = {
            "medium": ["BUS", "CAR", "TRAIN"],
            "username": username
        }
    except:
        return HttpResponseRedirect('login')
    print(context)
    if request.method == 'POST':
        print("share_travel_info", request.POST)
        share_travel_information_form = forms.share_travel_information_form(
            request.POST)
        print("share_travel_info",
              share_travel_information_form.is_valid())
        if share_travel_information_form.is_valid():  # application label validation
            print("share_travel_info")
            student = share_travel_information_form.save()
            print("jjjj", student)
            art_res.append_share_travel_info(
                models.share_travel_information_model.objects.last().__dict__)
        print("gagagga", request.POST)
        return HttpResponseRedirect('my_travel_info')
    return render(request, 'main/share_travel_info.html', context)


def my_travel_info(request):
    global username
    try:
        context = {
            "medium": ["BUS", "CAR", "TRAIN"],
            "username": username,
            "res": art_res.share_travel_info_lst
        }
    except:
        return HttpResponseRedirect('login')
    if username != "last":
        context["flag"] = False
        return render(request, 'main/my_asset_transportation_request.html', context)
    else:
        context["flag"] = True
    print("\n\nshare_travel_info_lst\n\n", context)
    if request.method == 'POST':
        print("jhj1", request.POST)
        if request.POST.get("data") is not None:
            art_res.update_asset_transportation_request(
                request.POST.get("data"))
            context["res"] = art_res.asset_transportation_request_lst
        asset_transportation_request_form = forms.asset_transport_req_form(
            request.POST)
        print("jhj1", asset_transportation_request_form.is_valid())
        if asset_transportation_request_form.is_valid():  # application label validation
            print("jhj1")
            student = asset_transportation_request_form.save()
            print("jjjj", student)
            art_res.append_share_travel_info(
                models.asset_transport_request_model.objects.last().__dict__)
        print("gagagga", request.POST)
    return render(request, 'main/my_travel_info.html', context)


def my_asset_transportation_requests(request):
    global username
    try:
        context = {
            "asset_type": ["LAPTOP", "TRAVEL_BAG", "PACKAGE"],
            "sensitivity": ["HIGHLY_SENSITIVE", "SENSITIVE", "NORMAL"],
            "username": username,
            "res": art_res.asset_transportation_request_lst
        }
    except:
        return HttpResponseRedirect('login')
    if username != "last":
        context["flag"] = False
        return render(request, 'main/my_asset_transportation_request.html', context)
    else:
        context["flag"] = True
    print("\n\n\n\n\n\n\n\nhh", context)
    if request.method == 'POST':
        print("jhj1", request.POST)
        if request.POST.get("data") is not None:
            art_res.update_asset_transportation_request(
                request.POST.get("data"))
            context["res"] = art_res.asset_transportation_request_lst
        asset_transportation_request_form = forms.asset_transport_req_form(
            request.POST)
        print("jhj1", asset_transportation_request_form.is_valid())
        if asset_transportation_request_form.is_valid():  # application label validation
            print("jhj1")
            student = asset_transportation_request_form.save()
            print("jjjj", student)
            art_res.append_asset_transportation_request(
                models.asset_transport_request_model.objects.last().__dict__)
        print("gagagga", request.POST)
    return render(request, 'main/my_asset_transportation_request.html', context)


def matched_asset_transportation_requests(request):
    global username, ans
    try:
        context = {
            "asset_type": ["LAPTOP", "TRAVEL_BAG", "PACKAGE"],
            "sensitivity": ["HIGHLY_SENSITIVE", "SENSITIVE", "NORMAL"],
            "username": username
        }
    except:
        return HttpResponseRedirect('login')
    print(context)
    if request.method == 'POST':
        print("\n\nmatched_asset_transportation_requests", request.POST)
        ans = art_res.matched_asset_transportation_request(
            request.POST)
        return HttpResponseRedirect('selected_asset_transportation_requests')

        # data = []
        # all_data = models.asset_transport_request_model.objects.all()
        # for ele in all_data:
        #     data.append(ele.__dict__)
        # print("matched_asset_transportation_requests", data)

        # asset_transportation_request_form = forms.asset_transport_req_form(
        #     request.POST)
        # print("asset_transportation_request",
        #       asset_transportation_request_form.is_valid())
        # if asset_transportation_request_form.is_valid():  # application label validation
        #     print("asset_transportation_request")
        #     student = asset_transportation_request_form.save()
        #     print("jjjj", student)
        #     art_res.append_asset_transportation_request(
        #         models.asset_transport_request_model.objects.last().__dict__)
        # print("gagagga", request.POST)
        # return HttpResponseRedirect('my_asset_transportation_requests')
    return render(request, 'main/matched_asset_transportation_requests.html', context)


def selected_asset_transportation_requests(request):
    global username, ans
    try:
        context = {
            "asset_type": ["LAPTOP", "TRAVEL_BAG", "PACKAGE"],
            "sensitivity": ["HIGHLY_SENSITIVE", "SENSITIVE", "NORMAL"],
            "username": username,
            "res": ans
        }
    except:
        return HttpResponseRedirect('login')
    print("selected_asset_transportation_requests", context)
    if context["res"] == "no record":
        context["nodisplay"] = False
    else:
        context["nodisplay"] = True
    if request.method == 'POST':
        print("\n\nmatched_asset_transportation_requests", request.POST)
        context["res"] = art_res.matched_asset_transportation_request(
            request.POST)

        # data = []
        # all_data = models.asset_transport_request_model.objects.all()
        # for ele in all_data:
        #     data.append(ele.__dict__)
        # print("matched_asset_transportation_requests", data)

        # asset_transportation_request_form = forms.asset_transport_req_form(
        #     request.POST)
        # print("asset_transportation_request",
        #       asset_transportation_request_form.is_valid())
        # if asset_transportation_request_form.is_valid():  # application label validation
        #     print("asset_transportation_request")
        #     student = asset_transportation_request_form.save()
        #     print("jjjj", student)
        #     art_res.append_asset_transportation_request(
        #         models.asset_transport_request_model.objects.last().__dict__)
        # print("gagagga", request.POST)
        # return HttpResponseRedirect('my_asset_transportation_requests')
    return render(request, 'main/selected_asset_transportation_requests.html', context)
