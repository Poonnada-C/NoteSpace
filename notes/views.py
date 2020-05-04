
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Note, Image, Tag, Review
from django.template.loader import get_template
# Create your views here.
def _clear_str_space(input):  # Delete excess space
    return " ".join(input.split())

def home_page(request):   # <domain>/
    notes = Note.objects.order_by('-upload_time')  # Get notes from db and order them by upload time
    return render(request, 'home_page.html', {'notes': notes})  # Return home_page.html with notes

def upload_page(request):   # <domain>/upload/
    return render(request, 'upload_page.html')  # Return upload_page.html

def upload_api(request):   # <domain>/api/upload/
    img_filetype = ["img", "png", "jpg" ,"jpeg", "tiff", "gif", "bmp"]
    if not request.COOKIES.get('owner'):
        response = HttpResponseRedirect('/')
        response.set_cookie('owner', str(newnote.name))    # Set Owner Cookies to notename
        return response   # Return to homepage
    else:
        cookies = request.COOKIES.get('owner')
        response = HttpResponseRedirect('/')
        response.set_cookie('owner', str(cookies) + ',' + str(newnote.name))    # Set Owner Cookies 
    return response   # Return to homepage
    # Set Cookie

    if request.POST:
        newnote = Note()
        newnote.name  =  _clear_str_space(request.POST['name'])  # Delete excess space and set note name
        newnote.owner =  _clear_str_space(request.POST['guestname'])  # Delete excess space and set owner name
        newnote.desc  =  _clear_str_space(request.POST['desc'])  # Delete excess space and set description
        newnote.save()  # Save note to database

        i = 0
        
        for file in request.FILES.getlist('myfile'):
            if(len(file.name.split(".")) > 1 and
                    file.name.split(".")[-1].lower() in img_filetype):   # Check file type (image type)
                newimg = Image()
                newimg.image = file   # Set image to current file
                newimg.index = i   # Set image index
                newimg.note = newnote   # Set note to newnote
                newimg.save()   # Save image to database
                i += 1
        if(i==0): # All file is invalid
            newnote.delete()    # Delete note
            return HttpResponse("File Type Error")  # Return file type error
        return HttpResponseRedirect('/')   # Return to homepage
    return HttpResponseRedirect('/')   # Return to homepage

def detial(request, note_index):  # <domain>/<note_index>/
    _n = get_object_or_404(Note, pk=note_index)   # Get note from database (if not found return 404)
    _images = Image.objects.filter(note=_n)    # Get images of the note from database
    img_url = [i.image.url for i in _images]   # Get list of urls of those images
    return render(request, 'detail.html', {'images_url': img_url, 'note': _n})  # Return detail.html with image_urls and note

def test_cookie(request):   
    if not request.COOKIES.get('color'):
        response = HttpResponse("Cookie Set")
        response.set_cookie('color', 'blue')
        return response
    else:
        return HttpResponse("Your favorite color is {0}".format(request.COOKIES['color']))

def track_user(request):
    if not request.COOKIES.get('visits'):
        response = HttpResponse("This is your first visit to the site. "
                                "From now on I will track your vistis to this site.")
        response.set_cookie('visits', '1', 3600 * 24 * 365 * 2)
    else:
        visits = int(request.COOKIES.get('visits')) + 1
        response = HttpResponse("This is your {0} visit".format(visits))
        response.set_cookie('visits', str(visits),  3600 * 24 * 365 * 2)
    return response

def stop_tracking(request):
    if request.COOKIES.get('visits'):
       response = HttpResponse("Cookies Cleared")
       response.delete_cookie("visits")
    else:
        response = HttpResponse("We are not tracking you.")
    return response
def about(request):   # <domain>/about/
    return render(request, 'about.html')  # Return about_page.html

def help(request):   # <domain>/help/
    return render(request, 'help_main.html')  # Return help_main.html

def help_detail(request, help_topic):
    try:
        get_template("help/%s.html" % (help_topic))
        return render(request, "help/%s.html" % (help_topic)) 
    except:
        return HttpResponseNotFound("<h1>404 Page not found</h1>")

def search(request):   # <domain>/search?q=<query_word>/
    query_word = request.GET.get("q", '')  # Set query_word value from request parameter 'q'
    searched_notes = Note.objects.filter(
	Q(name__icontains=query_word) |   # Get notes from database, filter by using query with name or description or tag
        Q(desc__icontains=query_word) |
        Q(tags__title__icontains=query_word) 
        ) 
   
    return render(request, 'search_result.html',   # Return search_result.html with search_key and searched_noted
    {
        'search_key':query_word,
        'searched_notes':searched_notes })

def tag_query(request, tag_title):   # <domain>/tag/<tag_name>
    query_tag = get_object_or_404(Tag, title=tag_title)  # Get tag from database (if not found return 404)
    return render(request, 'tag_result.html', {'tag': query_tag})  # Return tag_result.html  

def add_comment_api(request):   # <domain>/api/addcomment/
    note_id = request.POST['note_id']   # Set note_id value
    _n = Note.objects.get(id=note_id)   # Save note_id to _n

    author = request.POST['author']   # Set author value from  POST method request parameter 'note_id'
    text = request.POST['text']   # Set text value from POST method request parameter 'text'
    score = float(request.POST['score']) if request.POST['score'] in ["1", "2", "3", "4", "5"] else 0   # Set score value (if score is number 0-5 else 0)



    review = Review()   # Create review
    review.note = _n   # Set note of review
    review.author = author   # Set author review
    review.text = text   # Set text review
    review.score = score   # Set score review

    review.save()   # Save review to database
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   # Return to current page 
