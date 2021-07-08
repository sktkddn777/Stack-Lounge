from django.shortcuts import render, HttpResponse

def get_stack_result(request):
    context = {'test_syntax': "This is a test"}
    return render(request, 'stackscraper/index.html', context)


    