from django.db import models

# Create your models here.
class User(models.Model):
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=50)
    Role = models.CharField(max_length=50)
    OTP = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_created = models.DateTimeField(auto_now_add=True)
    is_update = models.DateTimeField(auto_now_add=True)

class Seller(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Contact = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50)
    Businesstype = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Profile_pic = models.ImageField(upload_to="img/", default="abc.jpg")
    Shopname= models.CharField(max_length=50)

class Customer(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Contact = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Pincode = models.CharField(max_length=50)
    Profile_pic = models.ImageField(upload_to="img/", default="1.jpg")


class Category(models.Model):
    Cat_name = models.CharField(max_length=50)
    Cat_des = models.TextField()
    created_Date = models.DateTimeField(auto_now_add=True)
    update_Date = models.DateTimeField(auto_now_add=True)
    



class Sub_Category(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_cat_name = models.CharField(max_length=50)
    created_Date = models.DateTimeField(auto_now_add=True)
    update_Date = models.DateTimeField(auto_now_add=True)

class BookTable(models.Model):
    cat_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_cat_id = models.ForeignKey(Sub_Category,on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Seller,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    Book_name = models.CharField(max_length=50)
    Book_Des = models.CharField(max_length=50)
    Book_price = models.CharField(max_length=50)
    MainImage = models.ImageField(upload_to='img/')
    created_Date = models.DateTimeField(auto_now_add=True)
    update_Date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class BookDetails(models.Model):
    book_t_id  = models.ForeignKey(BookTable,on_delete=models.CASCADE)
    Author_name = models.CharField(max_length=50)
    Author_des = models.CharField(max_length=200)
    Book_Pages = models.IntegerField()
    Book_lang = models.CharField(max_length=50)
    Book_Publish = models.CharField(max_length=50)
    Book_Pub_Date = models.CharField(max_length=50)
    created_Date = models.DateTimeField(auto_now_add=True)
    update_Date = models.DateTimeField(auto_now_add=True)

class BookGellery(models.Model):
    book_t_id  = models.ForeignKey(BookTable,on_delete=models.CASCADE)
    book_img1 = models.ImageField(upload_to="img/")
    book_img2 = models.ImageField(upload_to="img/")
    book_img3 = models.ImageField(upload_to="img/")
    created_Date = models.DateTimeField(auto_now_add=True)
    update_Date = models.DateTimeField(auto_now_add=True)




class AddToCart(models.Model):
    Customer_id  = models.ForeignKey(Customer,on_delete=models.CASCADE)
    Product_id  = models.ForeignKey(BookTable,on_delete=models.CASCADE)
    Price = models.IntegerField()
    Quantity = models.IntegerField()
    Total = models.IntegerField()
    SubTotal = models.IntegerField()
    Book = models.CharField(max_length=50)
    
    created_Date = models.DateTimeField(auto_now_add=True)
    update_Date = models.DateTimeField(auto_now_add=True)

# class CheckOut(models.Model):


class contact(models.Model):
    Customer_id  = models.ForeignKey(User,on_delete=models.CASCADE)
    FullName = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)
    Mobile = models.CharField(max_length=50)
    Subject = models.CharField(max_length=50)
    Message = models.TextField()
    
    

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)






