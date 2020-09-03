from django.shortcuts import render

# Create your views here.
def map(request):
    x  =  [
            [90.414879, 23.818858],
            [90.404959, 23.816055],
            [90.403639, 23.810919],
            [90.398211, 23.778461],
            [90.389868, 23.775251],
		    [90.421271, 23.812926]

        ]
    return render(request,'map/map.html',{'x': x})