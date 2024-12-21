from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# debug使用的dummy code

def calculate():
    x= 1 
    y = 2
    return x

def say_hello(request):
    # return HttpResponse('hello world')
    
    x = calculate() # breakpoint. 如果x=1，step over看到y；如果calculate(), step into进入calculate()
    y = 2  
    return render(request, 'hello.html', {'name': 'haoming'})
    # The render() function looks for the hello.html file in your templates directory.
    # It injects the context dictionary ({'name': 'haoming'}) into the template, making the name variable available in the template.