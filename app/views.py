from django.shortcuts import render,redirect,HttpResponseRedirect,reverse
from .models import *
from random import randint

from .utils import *
import socket
socket.getaddrinfo('localhost',8080)

from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum

from django.views.decorators.csrf import csrf_exempt

# from django.contrib.auth import authenticate, login as auth_login
# from django.conf import settings
# from .models import Transaction
# from .paytm import generate_checksum, verify_checksum
# from gateway.Checksum import generate_checksum
# from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def IndexPage(request):
    allshow=BookTable.objects.all()
    return render(request,"app/index.html",{'show':allshow})

def Single(request):
    return redirect('allshow')


def ShopGridPage(request):
    return render(request,"app/shop-grid.html")

def CartPage(request):
    return render(request,"app/cart.html")

# def checkoutpage(request):
#     return render(request,"app/checkout.html")
def ContactPage(request):
    return render(request,"app/contact.html")


def RegisterPage(request):
    return render(request,"app/register.html")

def OTPPage(request):
    return render(request,"app/otpverify.html")

def BuyerOTPPage(request):
    return render(request,"app/BuyerOtpverify.html")

def loginPage(request):
    return render(request,"app/login.html")  

def TeamList(request):
    return render(request,"app/team.html")

def FAQ(request):
    return render(request,"app/faq.html")

def ERROR(request):
    return render(request,"app/error404.html")

def ABOUT(request):
    return render(request,"app/about.html")

def BLOGPAGE(request):
    return render(request,"app/blog.html")


def SellerIndex(request):
    if 'Email' in request.session and 'Password' in request.session:
        return render(request,"app/seller/index.html")
    else:
        return redirect('loginpage')


def Issue(request):
    if 'Email' in request.session and 'Password' in request.session:
        
        c_id=request.session['id']
        custid =User.objects.get(id=c_id)
        
        if request.method=="POST":
            fullname = request.POST['firstname']
            email = request.POST['email']
            mobile = request.POST['mobile']
            subject = request.POST['subject']
            message = request.POST['message']
            
            contact.objects.create(Customer_id=custid,FullName=fullname,Email=email,Mobile=mobile,Subject=subject,Message=message)
            message = "Issue Successfully Submited"
            return render(request,"app/contact.html",{'msg':message,})

        
    else:
        return redirect('loginpage')

########################## Seller  Registration start #########################
def RegisterUser(request):
    try:

        if request.method=="POST":
            print("----------1-----------")
            if request.POST['role']=="Seller":
                print("----------2-----------")
                role = request.POST['role']
                fname = request.POST['fname']
                lname = request.POST['lname']
                email = request.POST['email']
                password = request.POST['password']
                cpassword = request.POST['confirm_password']

                user = User.objects.filter(Email=email)
                
                if user:
                    print("----------3-----------")
                    message = "User Already Exist"
                    return render(request,"app/login.html",{'msg':message})
                    print("----------4-----------")
                else:
                    print("----------5-----------")
                    if password==cpassword:
                        print("----------6-----------")
                        otp = randint(10000,99999)
                        print("----------7-----------")
                        newuser = User.objects.create(Email=email,Password=password,OTP=otp,Role=role)
                        print("----------8-----------")
                        newseller= Seller.objects.create(user_id=newuser,Firstname=fname,Lastname=lname)
                        email_subject = "Doctor Finder : Account Vericication"
                        sendmail(email_subject,'mail_template',email,{'name':fname,'otp':otp,'link':'http://localhost:8000/otppage/'})
                        
                        return redirect('otppage')
                        print("----------9-----------")
                    else:
                        print("----------10-----------")
                        message = "Password And ConfirmPassword DoestNot Match"
                        return render(request,"app/register.html",{'msg':message})

            else:
                print("=============1===========")
                if request.method=="POST":
                    print("=============2===========")
                    if request.POST['role']=="Buyer":
                        print("=============3===========")
                        role = request.POST['role']
                        fname = request.POST['fname']
                        lname = request.POST['lname']
                        email = request.POST['email']
                        password = request.POST['password']
                        cpassword = request.POST['confirm_password']

                        user = User.objects.filter(Email=email)

                        if user:
                            print("=============4===========")
                            message = "Buyer Already Exist"
                            return render(request, "app/login.html",{'msg':message})
                        else:
                            print("=============5===========")
                            if password == cpassword:
                                print("=============6===========")
                                otp = randint(20000,88888)
                                newuser = User.objects.create(Email=email,Password=password,OTP=otp,Role=role)
                                newBuyer = Customer.objects.create(user_id=newuser,Firstname=fname,Lastname=lname)
                                email_subject = "Doctor Finder : Account Vericication"
                                sendmail(email_subject,'mail_template',email,{'name':fname,'otp':otp,'link':'http://localhost:8000/otppage/'})
                                print("=============7===========")
                                sendem=User.objects.all().filter(Email=email)
                                print(sendem)
                                return render(request,"app/BuyerOtpverify.html",{'em':sendem})
                                print("=============8===========")
                            else:
                                message = "Password And ConfirmPassword DoestNot Match"
                                return render(request,"app/register.html",{'msg':message})

                else:
                    print("Buyer not exist")
    except Exception as e:
        print("Register Exception------------->",e)
########################## Buyer  Registration End  #########################


########################## Seller OTP Verify start  #########################

def OTPverify(request):
    print("OTP VERIFY METHOD CALLED ")
    try: 
            if request.method=="POST":
                email=request.POST['email']
                otp= int(request.POST['otp'])

                user = User.objects.get(Email=email)
                if user.OTP == otp and user.Role == "Seller":
                    message = "OTP verification successfully"
                    return render(request,"app/login.html",{'msg':message})
                else:
                    message = "OTP verify Unsuccessfully "
                    return render(request,"app/otpverify.html",{'msg':message})
    except Exception as e:
        print("OTP Exception------------------------------>",e)
########################## Seller OTP Verify End   #########################

########################## Buyer  OTP Verify start  #########################

def BuyerOTPverify(request):
    print("OTP VERIFY METHOD CALLED ")
    try: 
            if request.method=="POST":
                email=request.POST['email']
                otp= int(request.POST['otp'])
                print("_____________1__________________")

                user = User.objects.get(Email=email)
                print("_____________2________________")
                if user.OTP == otp and user.Role == "Buyer":
                    print("_____________3________________")
                    message = "OTP verification successfully"
                    print("_____________4________________")
                    return render(request,"app/login.html",{'msg':message})
                    print("_____________5________________")
                else:
                    print("_____________6________________")
                    message = "OTP verify Unsuccessfully "
                    return render(request,"app/BuyerOtpverify.html",{'msg':message})
            else:
                print("Method not call")
    except Exception as e:
        print("OTP Exception------------------------------>",e)
########################## Buyer  OTP Verify  End  #########################


########################## Seller Login  start  #########################
def loginUser(request):
    if request.method=="POST":
        if request.POST['role']=="Seller":
            email= request.POST['email']
            password= request.POST['password']



            user = User.objects.get(Email=email)

            if user:
                if user.Password==password and user.Role=="Seller":
                    sell = Seller.objects.get(user_id=user)


                    request.session['Firstname']=sell.Firstname
                    request.session['Lastname']=sell.Lastname
                    request.session['Email']=user.Email
                    request.session['Password']=user.Password
                    request.session['id']=user.id

                    return redirect('sellerindex')
                else:
                    message = "Password Does not match"
                    return render(request,"app/login.html",{'msg':message})
            else:
                message="User doesnot exist"
                return render(request,"app/register.html",{'msg':message})

########################## Seller Login  End  #########################



########################## Buyer  Login  start  #########################

        else:
            if request.method=="POST":
                if request.POST['role']=="Buyer":
                    email= request.POST['email']
                    password= request.POST['password']



                    user = User.objects.get(Email=email)

                    if user:
                        if user.Password==password and user.Role=="Buyer":
                            cust = Customer.objects.get(user_id=user)


                            request.session['Firstname']=cust.Firstname
                            request.session['Lastname']=cust.Lastname
                            request.session['Email']=user.Email
                            request.session['Password']=user.Password
                            request.session['id']=user.id

                            return redirect('index')
                        else:
                            message = "Password Does not match"
                            return render(request,"app/login.html",{'msg':message})
                    else:
                        message="User doesnot exist"
                        return render(request,"app/register.html",{'msg':message})
    ##########################  Buyer Login End  #########################

# def BuyerLoginAccount(request):
#     if request.method=="POST":
#         if request.POST['role']=="Buyer":
#             email= request.POST['email']
#             password= request.POST['password']



#             user = User.objects.get(Email=email)

#             if user:
#                 if user.Password==password and user.Role=="Buyer":
#                     cust = Customer.objects.get(user_id=user)


#                     request.session['Firstname']=cust.Firstname
#                     request.session['Lastname']=cust.Lastname
#                     request.session['Email']=user.Email
#                     request.session['Password']=user.Password
#                     request.session['id']=user.id

#                     return redirect('Customerindex')
#                 else:
#                     message = "Password Does not match"
#                     return render(request,"app/login.html",{'msg':message})
#             else:
#                 message="User doesnot exist"
#                 return render(request,"app/register.html",{'msg':message})
#         else:
#             print("Not print")

######## Seller Logout page start ##########
def Sellerlogout(request):
    del request.session['Email']
    del request.session['Password']
    return redirect('loginpage')

######## Seller Logout page End  ##########



def ProfilePage(request,pk):
    if 'Email' in  request.session and 'Password' in request.session:
        udata = User.objects.get(id=pk)
        if udata.Role=="Seller":
            seller = Seller.objects.get(user_id=udata)
            return render(request,"app/seller/profile.html",{'key1':seller})
    else:
        return redirect('loginpage')

def SellerUpdateProfile(request,pk):
    if request.method=="POST":
        if 'Email' in  request.session and 'Password' in request.session:
            udata = User.objects.get(id=pk)
            if udata.Role=="Seller":
                seller = Seller.objects.get(user_id=udata)
                seller.Firstname = request.POST['fname']
                seller.Lastname = request.POST['lname']
                seller.Contact = request.POST['contact']
                seller.Gender = request.POST['gender']
                seller.Shopname = request.POST['shopname']
                seller.Businesstype = request.POST['bustype']
                seller.City = request.POST['city']
                seller.State = request.POST['state']
                seller.Address = request.POST['address']
                seller.Profile_pic = request.FILES['img']
                seller.save()
                url = f"/profilepage/{pk}"
                return redirect(url)
    else:
        return redirect('loginpage')

#############################Admin Side####################################33

def AdminIndexPage(request):
    if 'username' in request.session and 'password' in request.session:
        return render(request,"app/Admin/index.html")
    else:
        return redirect('loginadmin')
def AdminLoginPage(request):
    return render(request,"app/Admin/login.html")


def AdminLogin(request):
    username = request.POST['username']
    password = request.POST['password']

    if username == "admin" and password == "admin":
        request.session['username'] = username
        request.session['password'] = password

        return redirect('adminindex')
    else:
         message = "Username and Password does not match"
         return render(request,"app/admin/login.html",{'msg':message})


def AdminLogout(request):
    del request.session['username']
    del request.session['password']
    return redirect('loginadmin')     

def InCat(request):
    if 'username' in request.session and 'password' in request.session:
        return render(request,"app/Admin/MainCat.html")
    else:
        return redirect('loginadmin')

def AddCategory(request):
    if 'username' in request.session and 'password' in request.session:
    
        if request.method=="POST":
            Cat_n = request.POST['Cat_n']
            Cat_d = request.POST['Cat_d']

            cat = Category.objects.filter(Cat_name=Cat_n)

            if cat:
                message="Category Already Exist , Please Fill Different Type Category"
                return render(request,"app/Admin/MainCat.html",{'msg':message})

            else:
                newadd = Category.objects.create(Cat_name=Cat_n,Cat_des=Cat_d)
                message="Category Added"
                return render(request,"app/Admin/index.html",{'masg':message})

        else:
            print("not ")
    else:
        return redirect('loginadmin')


def SubCategoryPage(request):
    if 'username' in request.session and 'password' in request.session:
        all_Cat = Category.objects.all()
        return render(request,"app/Admin/SubCat.html",{'cat':all_Cat})
    else:
        return redirect('loginadmin')



def AddSubCategory(request):
    if 'username' in request.session and 'password' in request.session:
        cid = request.POST['category']
        c_id = Category.objects.get(id=cid)
        scat = request.POST['sub_cat']
        scatname = Sub_Category.objects.filter(sub_cat_name=scat)
        if scatname:
            message="SubCategory Already Exist"
            return render(request,"app/Admin/SubCat.html",{'msg':message})
        else:
            newscat = Sub_Category.objects.create(cat_id=c_id,sub_cat_name=scat)
            message="Sub Category Added"
            return render(request,"app/Admin/index.html",{'msg':message})
    else:
        return redirect('loginadmin')

    



def ShowAllCat(request):
    return render(request,"app/Admin/Allcat.html")

def AllCategoryShow(request):
    all_data = Category.objects.all()
    return render(request,"app/Admin/Allcat.html",{'key1':all_data})

def EditPage(request,pk):
    edata = Category.objects.get(pk=pk)
    return render(request,"app/Admin/edit.html",{'key2':edata})

def UpdateData(request,pk):
    udata = Category.objects.get(pk=pk)
    udata.Cat_name = request.POST['Cat_n']
    udata.Cat_des = request.POST['Cat_d']
    udata.save()
    return HttpResponseRedirect(reverse('showall'))


def DeleteData(request,pk):
    ddata = Category.objects.get(pk=pk)
    ddata.delete()
    return HttpResponseRedirect(reverse('showall'))





############################Seller Side Category#######################################
def ShowCategoryPage(request):
    if 'Email' in  request.session and 'Password' in request.session:
        all_data = Category.objects.all()
        return render(request,"app/seller/ShowCategory.html",{'cat':all_data})

    else:
        return redirect('loginpage')

def SelectCat(request):
    if 'Email' in  request.session and 'Password' in request.session:
        cat = request.POST['category']
        cid = Category.objects.get(id=cat)
       

        sdata=Sub_Category.objects.all().filter(cat_id=cat)
        return render(request,"app/seller/showSubcategory.html",{'sub':sdata,'cat':cid})

    else:
        return redirect('loginpage')


def Select_SubCat(request):
    
    if 'Email' in  request.session and 'Password' in request.session:
        mcat=request.POST['cc_id']
        cid = Category.objects.get(id=mcat)
        scat=request.POST['ss_id']
        sid = Sub_Category.objects.get(id=scat)

        return render(request,"app/seller/AddPost.html",{'mcat':cid,'scat':sid})

    else:
        return redirect('loginpage')


def AddProduct(request,pk):
    if 'Email' in  request.session and 'Password' in request.session:
        user=User.objects.get(id=pk)
        sellerd=Seller.objects.get(user_id=user)

        c_id=int(request.POST['c_id'])
        cdata=Category.objects.get(id=c_id)

        s_id=int(request.POST['s_id'])
        sdata=Sub_Category.objects.get(id=s_id)

        bookname=request.POST['bookname']
        bookdescriptions=request.POST['bookdescriptions']
        bookprice=request.POST['bookprice']
        bookAn=request.POST['bookAn']
        authordescription=request.POST['authordescription']
        bookpages=request.POST['bookpages']
        booklanguage=request.POST['booklanguage']
        bookpublisher=request.POST['bookpublisher']
        bookdate=request.POST['bookdate']
        mainimage=request.FILES['mainimage']
        bookimg1=request.FILES['bookimg1']
        bookimg2=request.FILES['bookimg2']
        bookimg3=request.FILES['bookimg3']
        fil=BookTable.objects.filter(Book_name=bookname)
        if fil:
            message="Book Already Exist"
            return render(request,"app/seller/AddPost.html",{'msg':message})
        else:
            
            newbook=BookTable.objects.create(cat_id=cdata,sub_cat_id=sdata,seller_id=sellerd,Book_name=bookname,Book_Des=bookdescriptions,Book_price=bookprice,MainImage=mainimage)
            BookDetails.objects.create(book_t_id=newbook,Author_name=bookAn,Author_des=authordescription,Book_Pages=bookpages,Book_lang=booklanguage,Book_Publish=bookpublisher,Book_Pub_Date=bookdate)
            BookGellery.objects.create(book_t_id=newbook,book_img1=bookimg1,book_img2=bookimg2,book_img3=bookimg3)
            message="Product Upload SuccessFully"
            return render(request,"app/seller/index.html",{'msg':message})


    else:
        return redirect('loginpage')
# def success(request):
#     return render(request,"app/seller/success.html")
    

def ShowAllProduct(request):
    if 'Email' in  request.session and 'Password' in request.session:
        
        sellerid=request.session['id']
        sid = Seller.objects.get(id=sellerid)
        all_pro=BookTable.objects.all().filter(seller_id=sid)
        
        

        return render(request,"app/seller/AllProduct.html",{'key':all_pro})

    else:
        return redirect('loginpage')

def SelEditPage(request,pk):
    edata = BookTable.objects.get(pk=pk)
    ddata = BookDetails.objects.get(pk=pk)
    return render(request,"app/Seller/Edit.html",{'key2':edata,'key3':ddata})

def SelUpdateData(request,pk):
    pdata = BookTable.objects.get(pk=pk)
    ddata = BookDetails.objects.get(pk=pk)
    


    pdata.Book_name = request.POST['bookname']
    pdata.Book_Des = request.POST['bookdescriptions']
    pdata.Book_price=request.POST['bookprice']
    pdata.MainImage=request.FILES['mainimage']

    ddata.Author_name = request.POST['bookAn']
    ddata.Author_des = request.POST['authordescription']
    ddata.Book_Pages = request.POST['bookpages']
    ddata.Book_lang = request.POST['booklanguage']
    ddata.Book_Publish = request.POST['bookpublisher']
    ddata.Book_Pub_Date = request.POST['bookdate']

   

    pdata.save()
    ddata.save()
    
    return HttpResponseRedirect(reverse('allproduct'))


def SelDeleteData(request,pk):
    pdata = BookTable.objects.get(pk=pk)
    ddata = BookDetails.objects.get(pk=pk)
    gdata = BookGellery.objects.get(pk=pk)
    pdata.delete()
    ddata.delete()
    gdata.delete()

    return HttpResponseRedirect(reverse('allproduct'))


def ImageShow(request,pk):
    p=BookTable.objects.get(id=pk)
    # bg=BookGellery.objects.get(book_t_id=p)
    bookd=BookGellery.objects.all().filter(book_t_id=p)
    return render(request,"app/Seller/Image.html",{'cat':bookd})

def EditImage(request,pk):
    g=BookGellery.objects.get(pk=pk)
    return render(request,"app/Seller/editimage.html",{'img':g})

def UpdateImage(request,pk):
    gdata = BookGellery.objects.get(pk=pk)

    gdata.book_img1=request.FILES['bookimg1']
    gdata.book_img2=request.FILES['bookimg2']
    gdata.book_img3=request.FILES['bookimg3']

    
    gdata.save()
    message="Image Update SuccessFully "
    return HttpResponseRedirect(reverse('allproduct'))
    #return render(request,"app/Seller/index.html",{'masg':message})

def AllPrShow(request):
    allshow=BookTable.objects.all()
    #alldetail = BookDetails.objects.all()
    # allgall = BookGellery.objects.all()
    # allmap = BookMapping.objects.all().filter(pid,bd,bg)
    return render(request,"app/shopList.html",{'show':allshow})

def ShowIndex(request):
    allshow=BookTable.objects.all()
    return render(request,"app/index.html",{'index':allshow})   

def SingleProduct(request,pk):
    if 'Email' in  request.session and 'Password' in request.session:
        allshow=BookTable.objects.get(id=pk)
        bg=BookGellery.objects.get(book_t_id=allshow)
        bd=BookDetails.objects.get(book_t_id=allshow)
        # abc=BookTable.objects.all()
        #alldetail=BookDetails.objects.all().filter(book_t_id=allshow)
        return render(request,"app/single-product.html",{'Product':allshow,'BookGallery':bg,'BookDetails':bd})
    else:
        return redirect('loginpage')

# def ShowSingle(request):
#     sellerid=request.session['id']
#     # bid = BookTable.objects.get(id=sellerid)
#     bd= BookGellery.objects.filter(book_t_id=sellerid)
#     return render(request,"app/single-product.html",{'ab':bd})


def AddtoCart(request,pk):
    buyer=int(request.session['id'])
    user=User.objects.get(id=buyer)
    buyerid = Customer.objects.get(user_id=user)
    proid=int(request.POST['id'])
    Productid=BookTable.objects.get(id=proid)
    book=request.POST['book']
    

    price=int(request.POST['price'])
    Quant=int(request.POST['qty'])
    
    total = Quant*price
    AddToCart.objects.create(Customer_id=buyerid,Product_id=Productid,Book=book,Price=price,Quantity=Quant,Total=total,SubTotal=total)
    
    return redirect('showallcart')

    
        # sellerid=request.session['id']
        # sid = Seller.objects.get(id=sellerid)
        # all_pro=BookTable.objects.all().filter(seller_id=sid)
def ShowAllCart(request):
    if 'Email' in  request.session and 'Password' in request.session:
        buy=request.session['id']
        userid=User.objects.get(id=buy)
        SubTotal=0
        
        buyerid = Customer.objects.get(user_id=userid)
        all_pro=AddToCart.objects.all().filter(Customer_id=buyerid)
        for t in all_pro:
            SubTotal += t.Total
        print(SubTotal)
        return render(request,"app/cart.html",{'key':all_pro,'subtotal':SubTotal})
        
    else:
        return redirect('loginpage')

###################### Buyer side #################3333



def CustomerIndex(request):
    if 'Email' in request.session and 'Password' in request.session:
        return render(request,"app/Customer/index.html")
    else:
        return redirect('loginpage')

def Buyerlogout(request):
    del request.session['Email']
    del request.session['Password']
    return redirect('index')
   
def CustomerProfilePage(request,pk):
    if 'Email' in  request.session and 'Password' in request.session:
        udata = User.objects.get(id=pk)
        if udata.Role=="Buyer":
            seller = Customer.objects.get(user_id=udata)
            return render(request,"app/profile.html",{'key1':seller})
        else:
            print("Not work")
    else:
        return redirect('loginpage')

def CustomerUpdateProfile(request,pk):
    if request.method=="POST":
        if 'Email' in  request.session and 'Password' in request.session:
            udata = User.objects.get(id=pk)
            if udata.Role=="Buyer":
                cust = Customer.objects.get(user_id=udata)
                cust.Firstname = request.POST['fname']
                cust.Lastname = request.POST['lname']
                cust.Contact = request.POST['contact']
                cust.Gender = request.POST['gender']
                cust.Pincode = request.POST['pincode']
               
                cust.City = request.POST['city']
                cust.State = request.POST['state']
                cust.Address = request.POST['address']
                cust.Profile_pic = request.FILES['img']
                cust.save()
                url = f"/custprofilepage/{pk}"
                return redirect(url)
    else:
        return redirect('loginpage')

def CartEditPage(request,pk):
    edata = AddToCart.objects.get(id=pk)
    # allshow=BookTable.objects.get(id=pk)
    # bg=BookGellery.objects.get(book_t_id=allshow)
    # bd=BookDetails.objects.get(book_t_id=allshow)
    return render(request,"app/cartedit.html",{'data':edata})

def UpdateCart(request,pk):
    gdata = AddToCart.objects.get(pk=pk)

    gdata.Price=request.POST['price']
    gdata.Quantity=request.POST['qty']
    gdata.Book=request.POST['book']
    gdata.Total = int(request.POST['price'])*int(request.POST['qty'] )

    
    gdata.save()
    return redirect('showallcart')

def DeleteCart(request,pk):
    cartd=AddToCart.objects.get(pk=pk)
    cartd.delete()
    return redirect('showallcart')


def CheckOut(request):
    if 'Email' in  request.session and 'Password' in request.session:
        buy=request.session['id']
        userid=User.objects.get(id=buy)
        SubTotal=0
        shipping=60
        
        buyerid = Customer.objects.get(user_id=userid)
        all_pro=AddToCart.objects.all().filter(Customer_id=buyerid)
        for t in all_pro:
            SubTotal += t.Total
            GrandTotal = SubTotal+shipping
        print(SubTotal)
        return render(request,"app/checkout.html",{'key':all_pro,'subtotal':SubTotal , 'cust':buyerid,'shipping':shipping,'grand':GrandTotal})
        
    else:
        return redirect('loginpage')

def EmailC(request):
    return render( request,"app/Email.html")




############################################# Paytm Block #################################################

def initiate_payment(request):
    try:
        udata = User.objects.get(Email=request.session['Email'])
        amount = int(request.POST['sub_total'])
        #user = authenticate(request, username=username, password=password)
    except Exception as err:
        print(err)
        return render(request, 'app/checkout.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=udata, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.Email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'app/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'app/callback.html', context=received_data)
        return render(request, 'app/callback.html', context=received_data)



def order(request):
    if 'Email' in  request.session and 'Password' in request.session:
        
        sellerid=request.session['id']
        sid = User.objects.get(id=sellerid)
        all_pro=Transaction.objects.all().filter(made_by=sid)
        return render(request,"app/order.html",{'key':all_pro })
       
        
    else:
        return redirect('loginpage')




