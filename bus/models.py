from django.db import models

class Bus_info(models.Model):
    bus_name = models.CharField(max_length=100)
    stoppage = models.TextField(help_text='Dont forget to add coordinates.')
    bus_image = models.ImageField(default= 'default.jpg')

    def __str__(self):
        return self.bus_name


class From_to(models.Model):
    From = models.CharField(max_length=60)
    To = models.CharField(max_length=60)

    def __str__(self):
        return self.From+' to '+self.To

class Cord(models.Model):
    From_to = models.OneToOneField(From_to, primary_key=True, on_delete= models.CASCADE)
    coordinates = models.TextField(max_length=700, default=None, null=True)

    def __str__(self):
        return self.From_to.From+' to '+self.From_to.To

class Station(models.Model):
    single_station = models.CharField(max_length=100)
    def __str__(self):
        return self.single_station
    

class Restaurant(models.Model):
    restaurant_location = models.ForeignKey(Station, blank= True, null= True, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=200, null=True, default=None)
    restaurant_link = models.CharField(max_length=200, null=True, default=None)
    embed = models.TextField(null= True, default=None)

    def __str__(self):
        return self.restaurant_name
        