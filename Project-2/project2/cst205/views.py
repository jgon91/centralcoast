from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
import base64
from PIL import Image
from PIL import ImageFilter
import json

# Create your views here.
def home(request):
    return render(request, 'home.html')

def uploadImagePage(request):
    return render(request, 'uploadImage.html')

def applyContour(request):
    
    result = {"Success": True}

    #Get image using PILLOW
    pic = Image.open("static/img/img.png")
    pic = pic.filter(ImageFilter.CONTOUR)
    pic.save("static/img/newImage.png")
    
    with open("static/img/newImage.png", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        result['image'] = str
    
    #pic.show()
    
    return HttpResponse(json.dumps(result),content_type='application/json')

def uploadImage(request):

    result = {"Success": True}
    
    #Get the image from front-end
    imageBase64 = request.POST["image"] 
    
    #Convert image base64 to image.png
    image = imageBase64.decode('base64')

    fh = open("static/img/img.png", "wb") 
    fh.write(image)
    fh.close()
    
    with open("static/img/img.png", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        result['image'] = str
    
    return HttpResponse(json.dumps(result),content_type='application/json')