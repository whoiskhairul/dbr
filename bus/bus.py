from django.contrib import messages

from .models import Bus_info, From_to, Cord, Station#importing the model/database table 'bus_info' .



def bus_stoppage_list(): #to find stoppage list,this list will be placed on dropdown dataset in home page.
    querydict = Bus_info.objects.all() #getting all data from database from Bus_info table.
    arr, dict = set(), {} 
    for i in querydict: #i means bus_name for every index
        x = i.stoppage #initializing all stoppage list in x.
        x = x.split('\r\n') #actually every element in x contains '\r\n',so removing these by split() function
        arr.update(set(x)) #updating all elements in arr ,it is a set.
    arr = sorted(list(arr)) #sorting the list to present it alphabatically.
    #converting the list to a dictionary.
    for i in range(len(arr)):
        dict[i] = arr[i]
        
    return dict #passing to the view 'index'




#To show All bus name in a page,here id will be in href and bus_name will be the text.
def all_bus_list(): 
    context = {}
    q = Bus_info.objects.values('id','bus_name')
    q = q.order_by('bus_name')
    for i in q:
        context[i['id']] = i['bus_name']
    return context




def find_bus_list(request,source,destination): #to provide the bus list according to the query of user.
    context = {}
    querydict = Bus_info.objects.order_by('bus_name') #getting all data from 'bus_info' table ,it is sorted alphabatically by bus_name. 

    if source and destination: #if user provide both source and destination in the html from
        for i in querydict: #iterating every bus.
            list = i.stoppage.split('\r\n')
            s,d = False,False
            for stp in list:
                if stp == source:s=True
                if stp == destination:d=True
            if s==True and d==True:
                context[i.id] = i.bus_name

            # psuducode
            # if(source in i.stoppage and destination in i.stoppage): #if source and destination both found in ith bus
            #     context[i.id] = i.bus_name #input 'ith bus id' as key of context and 'ith bus name' as value .

 #if it gets any bus that satisfy the condition,then 'context{}' must have at least one value.
 #if context is empty,then we can tell that no bus can satisfy desired condition.
 #so,we can show a message to the user.
    if not context:
        messages.error(request, 'Opps Sorry!')
        messages.error(request, ' No Bus Found On This Route!')
    
    return context







def find_each_bus_info(id): #this function will show stoppage of every bus.
    context = {}
    querydict = Bus_info.objects.all() #getting all value from table.

    #we will pass the id of bus by url.
    #here we will match the id with each bus,if found,we will show all stoppage list.
    for i in querydict: #i means every bus_info.
        if id == i.id: #matching id from url with id of the bus.
            #if matched
            bus_name = i.bus_name #getting the name of the bus.
            stoppage_list_of_ith_bus = i.stoppage.split('\r\n')
            image = i

            input_in_from_to(stoppage_list_of_ith_bus)

            #getting the stoppage of the bus,converting it to a dictionary.
            for i in range(len(stoppage_list_of_ith_bus)):
                context[i] = stoppage_list_of_ith_bus[i]

    return context,bus_name,image #return stoppage list and bus name.







def input_in_from_to(stoppage_list_of_ith_bus):

    q = From_to.objects.all()
    test = []
    for i in q:
        x, y = i.From, i.To
        test.append(x+y)

    for j in range(len(stoppage_list_of_ith_bus)-1):
        start_location, end_location = stoppage_list_of_ith_bus[j], stoppage_list_of_ith_bus[j+1]
        if start_location + end_location not in test:
            From_to_instance = From_to.objects.create(From=start_location,To=end_location)
            Cord_instance = Cord.objects.create(From_to=From_to_instance,coordinates=None) #creating & pushing reversed coordinate to the following From_to object.








def cord_for_map(id):
    stoppage_list, arr = [], [] #initializing both as list
    stoppage_dict, _, _= find_each_bus_info(id) #calling the function to get the stoppage list as dictionary.
    
    #to convert dictionary into a list
    for key,value in stoppage_dict.items():
        stoppage_list.append(value)
    
    for i in range(len(stoppage_list)-1):
        query1 = stoppage_list[i]
        query2 = stoppage_list[i+1]

        from_to = From_to.objects.get(From=query1, To=query2)

        cord_of_2_location = Cord.objects.get(From_to = from_to.id)
        cord = cord_of_2_location.coordinates
        if cord is not None:
            cord = cord.split('\r\n')
        if cord is not None:
            for cord_per_line in cord:
                cord_per_line = cord_per_line.replace(',','').split()
                if cord_per_line[0].isalpha()==False:
                    cord_per_line[0], cord_per_line[1] = float(cord_per_line[1]), float(cord_per_line[0])
                arr.append(cord_per_line)
   
    return arr





def customized_map(source, destination, context):
    stoppage_list, arr = [], []
    id = list(context.keys())
    if id:
        id = id[0]
        stoppage_dict, _, _ = find_each_bus_info(id)
        for key,value in stoppage_dict.items():
            stoppage_list.append(value)
        s = stoppage_list.index(source)
        d = stoppage_list.index(destination)
        if d < s:
            s, d = d, s

        for i in range(s, d):
            query1 = stoppage_list[i]
            query2 = stoppage_list[i+1]
            from_to = From_to.objects.get(From=query1, To=query2)

            cord_of_2_location = Cord.objects.get(From_to = from_to.id)
            cord = cord_of_2_location.coordinates
            if cord is not None:
                cord = cord.split('\r\n')
            if cord is not None:
                for cord_per_line in cord:
                    cord_per_line = cord_per_line.replace(',','').split()
                    if cord_per_line[0].isalpha()==False:
                        cord_per_line[0], cord_per_line[1] = float(cord_per_line[1]), float(cord_per_line[0])
                    arr.append(cord_per_line)
        
    return arr
    
        



def reverse():
    querydict = From_to.objects.all()
    all_from_to_list = []
    for i in querydict:
        x, y = i.From, i.To
        all_from_to_list.append(x+y)

    for i in querydict:
        start_location, end_location = i.From, i.To
        start_location, end_location = end_location, start_location #swap for saving in database the reverse path.
        
        if start_location+end_location not in all_from_to_list:
            cord_object = Cord.objects.get(From_to_id = i.id) #cord_object is a object of Cord model,it will store the objects of specific id of From_to model.
            
            #as we will input data in model of the letest model in reverse order,so we need to convert the object into list,and with reverse function,we will reverse it,then make it string again, and push in the database.
            coordinate_list = cord_object.coordinates.split('\r\n') #spliting the coordinates as user input.
            coordinate_list.reverse() #reversing the list.
            coordinate_str = '\r\n'.join(coordinate_list) #converting to string again.
            From_to_instance = From_to.objects.create(From=start_location,To=end_location) #making new From_to objects by Start and end location
            Cord_instance = Cord.objects.create(From_to=From_to_instance,coordinates=coordinate_str) #creating & pushing reversed coordinate to the following From_to object.

        
def DataForStationModel():
    all_stoppage_dict = bus_stoppage_list()
    for key, value in all_stoppage_dict.items():
        if Station.objects.filter(single_station = value).exists():
            pass
        else:
            Station.objects.create(single_station=value)

    


if __name__ == "__main__":
    pass