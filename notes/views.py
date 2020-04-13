
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Note, Image, Tag, Review
from django.template.loader import get_template
# Create your views here.
def ClearStrSpace(input):  #delete excess space
    return " ".join(input.split())

def home_page(request):
    notes = Note.objects.order_by('-upload_time')  #get notes from db and order them by upload time
    return render(request,'home_page.html',{'notes':notes})  #return from home_page.html with notes
def upload_page(request):
    return render(request,'upload_page.html')  #return from upload_page.html
def upload_api(request):
    filetype_list = ["img", "png", "jpg" ,"jpeg", "tiff", "gif", "bmp"]
    if request.POST:
        newnote = Note()
        newnote.name  =  ClearStrSpace(request.POST['name'])  #delete excess space and set note name
        newnote.owner =  ClearStrSpace(request.POST['guestname'])  #delete excess space and set owner name
        newnote.desc  =  ClearStrSpace(request.POST['desc'])  #delete excess space and set description
        newnote.save()  #save note to database

        i = 0
        
        for file in request.FILES.getlist('myfile'):
            if(len(file.name.split(".")) > 1 and
                    file.name.split(".")[-1].lower() in filetype_list):    #check file type (image type)
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

def detial(request,note_index):
    n = get_object_or_404(Note, pk=note_index)
    images = Image.objects.filter(note=n)
    img_url = [i.image.url for i in images]
    return render(request,'detail.html',{'images_url':img_url,'note':n})  #return from detail.html with image_urls and notes

def about(request):
    return render(request, 'about.html')  #return from about_page.html

def help(request):
    return render(request, 'help_main.html')  #return from help_main.html

def help_detail(request, help_topic):
    try:
        get_template("help/%s.html"%(help_topic))
        return render(request, "help/%s.html"%(help_topic) ) 
    except:
        return HttpResponseNotFound("<h1>404 Page not found</h1>")

def search(request):
    query_word = request.GET.get("q",'')
    searched_notes = Note.objects.filter(Q(name__icontains=query_word) | 
                                            Q(desc__icontains=query_word) |
                                            Q(tags__title__icontains=query_word) 
                                            ) 
   
    return render(request, 'search_result.html', 
    {
        'search_key':query_word,
        'searched_notes':searched_notes })

def tagQuery(request, tag_title):
    query_tag = get_object_or_404(Tag , title=tag_title)
    return render(request, 'tag_result.html',{'tag':query_tag})

def addcomment_api(request):
    note_id = request.POST['note_id']
    n = Note.objects.get(id=note_id)

    author = request.POST['author']
    text = request.POST['text']
    score = float(request.POST['score']) if request.POST['score'] in ["1","2","3","4","5"] else 0

    review = Review()
    review.note = n
    review.author = author
    review.text = text
    review.score = score

    review.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
