from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Bus_info, Station, Restaurant
from map import views
from .bus import bus_stoppage_list, find_bus_list, find_each_bus_info, reverse, cord_for_map, all_bus_list, customized_map, DataForStationModel


#@login_required
def index(request):
    DataForStationModel()
    
    stoppage_list = bus_stoppage_list()
    if request.method == 'POST':
        source = request.POST['source']
        destination = request.POST['destination']
        context = find_bus_list(request,source,destination)

        c = customized_map(source, destination, context)

        if destination:
            res = Station.objects.get(single_station=destination).id
            res = Restaurant.objects.filter(restaurant_location_id=res)

        return render(request,'bus/temp.html', {'bus_stoppage_list':stoppage_list, 'context':context, 'c':c , 'res':res, 'dest':destination})
    else:
        return render(request, 'bus/temp.html', {'bus_stoppage_list':stoppage_list})

#@login_required
def each_bus_info(request,id):
    context,bus_name, image = find_each_bus_info(id)
    
    x = cord_for_map(id) #This line is for passing the variable to load map with the route of the bus.
    return render(request, 'bus/each_bus_info.html', {'context':context, 'bus_name':bus_name, 'image':image, 'x':x } ) #
    

#@login_required
def bus_list(request):
    bus = all_bus_list()
    return render(request, 'bus/bus_list.html', { 'bus_list' : bus })


def confirm(request):
    reverse()
    return HttpResponse('Data enlisted.')


#@login_required
def restaurant(request,id):
    res = Restaurant.objects.get(id = id)
    embed = res.embed
    return render(request, 'bus/restaurant.html', {'res':res, 'embed':embed})



def login(request):
    return render(request, 'accounts/login.html')
