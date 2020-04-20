
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Note, Image, Tag, Review
from django.template.loader import get_template
# Create your views here.
def _clear_str_space(input):  #delete excess space
    return " ".join(input.split())

def home_page(request):   # <domain>/
    notes = Note.objects.order_by('-upload_time')  #get notes from db and order them by upload time
    return render(request,'home_page.html',{'notes':notes})  #return home_page.html with notes

def upload_page(request):   # <domain>/upload/
    return render(request,'upload_page.html')  #return upload_page.html

def upload_api(request):   # <domain>/api/upload/
    img_filetype = ["img", "png", "jpg" ,"jpeg", "tiff", "gif", "bmp"]
    if request.POST:
        newnote = Note()
        newnote.name  =  _clear_str_space(request.POST['name'])  #delete excess space and set note name
        newnote.owner =  _clear_str_space(request.POST['guestname'])  #delete excess space and set owner name
        newnote.desc  =  _clear_str_space(request.POST['desc'])  #delete excess space and set description
        newnote.save()  #save note to database

        i = 0
        
        for file in request.FILES.getlist('myfile'):
            if(len(file.name.split(".")) > 1 and
                    file.name.split(".")[-1].lower() in img_filetype):   #check file type (image type)
                newimg = Image()
                newimg.image = file   #set image to current file
                newimg.index = i   #set image index
                newimg.note = newnote   #set note to newnote
                newimg.save()   #save image to database
                i += 1
        if(i==0): #all file is invalid
            newnote.delete()    #delete note
            return HttpResponse("File Type Error")  #return file type error
        
        return HttpResponseRedirect('/')   #return to homepage
    return HttpResponseRedirect('/')   #return to homepage

def detial(request,note_index):  # <domain>/<note_index>/
    _n = get_object_or_404(Note, pk=note_index)   #get note from database (if not found return 404)
    _images = Image.objects.filter(note=_n)    #get images of the note from database
    img_url = [i.image.url for i in _images]   #get list of urls of those images
    return render(request,'detail.html',{'images_url':img_url,'note':_n})  #return detail.html with image_urls and notes

def about(request):   # <domain>/about/
    return render(request, 'about.html')  #return about_page.html

def help(request):   # <domain>/help/
    return render(request, 'help_main.html')  #return help_main.html

def help_detail(request, help_topic):
    try:
        get_template("help/%s.html"%(help_topic))
        return render(request, "help/%s.html"%(help_topic) ) 
    except:
        return HttpResponseNotFound("<h1>404 Page not found</h1>")

def search(request):   # <domain>/search?q=<query_word>/
    query_word = request.GET.get("q",'')  #set query_word value from request parameter 'q'
    searched_notes = Note.objects.filter(Q(name__icontains=query_word) |   #get notes from database ,filter by using query with name or description or tag
                                            Q(desc__icontains=query_word) |
                                            Q(tags__title__icontains=query_word) 
                                            ) 
   
    return render(request, 'search_result.html',   #return search_result.html with search_key and searched_noted
    {
        'search_key':query_word,
        'searched_notes':searched_notes })

def tag_query(request, tag_title):   # <domain>/tag/<tag_name>
    query_tag = get_object_or_404(Tag , title=tag_title)  # get tag from database (if not found return 404)
    return render(request, 'tag_result.html',{'tag':query_tag})  #return tag_result.html  

def add_comment_api(request):   # <domain>/api/addcomment/
    note_id = request.POST['note_id']   #set note_id value
    _n = Note.objects.get(id=note_id)   #save note_id to n

    author = request.POST['author']   # set author value from  POST method request parameter 'note_id'
    text = request.POST['text']   # set text value from POST method request parameter 'text'
    score = float(request.POST['score']) if request.POST['score'] in ["1","2","3","4","5"] else 0   #set score value (if score is number 0-5 else 0)



    review = Review()   #create review
    review.note = _n   #set note of review
    review.author = author   #set author review
    review.text = text   #set text review
    review.score = score   #set score review

    review.save()   #save review to database
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   #return to current page 
