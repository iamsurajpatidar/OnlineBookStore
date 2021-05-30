from django.urls import path, include
from . import views

urlpatterns = [
    path("",views.IndexPage,name="index"),
    path("shop-grid",views.ShopGridPage,name="shop-grid"),
    path("sing/",views.Single,name="sing"),
    path("cart/",views.CartPage,name="cart"),
    
    path("registerpage/",views.RegisterPage,name="registerpage"),
    path("loginpage/",views.loginPage,name="loginpage"),
    path("register/",views.RegisterUser,name="register"),
    path("otppage/",views.OTPPage,name="otppage"),
    path("buyerotppage/",views.BuyerOTPPage,name="buyerotppage"),
    path("otpverify/",views.OTPverify,name="otpverify"),
    path("buyerotpverify/",views.BuyerOTPverify,name="buyerotpverify"),
    



    path("contactpage/",views.ContactPage,name="contactpage"),
    path("teamlist/",views.TeamList,name="teamlist"),
    path("faql/",views.FAQ,name="faql"),
    path("error/",views.ERROR,name="error"),
    path("about/",views.ABOUT,name="about"),
    path("blogpage/",views.BLOGPAGE,name="blogpage"),
    path("issusub/",views.Issue,name="issusub"),
    











    ##################################### SELLER URLS ##############################
    path("sellerindex/",views.SellerIndex,name="sellerindex"),
    path("loginUser/",views.loginUser,name="login"),
    path("profilepage/<int:pk>",views.ProfilePage,name="profilepage"),
    path("sellerlogout/",views.Sellerlogout,name="slogout"),
    path("sellerupdate/<int:pk>",views.SellerUpdateProfile,name="sellerupdate"),
    

    ####################Admin URLs######################3
    path("adminloginpage/",views.AdminLoginPage,name="loginadmin"),
    path("adminlogin/",views.AdminLogin,name="adminlogin"),
    path("adminindex/",views.AdminIndexPage,name="adminindex"),
    path("adminlogout/",views.AdminLogout,name="adminlogout"),

    ##################Category####################

    path("Catindex/",views.InCat,name="Catindex"),
    path("addcategory/",views.AddCategory,name="addcategory"),
    
    path("addsubcategory/",views.AddSubCategory,name="addsubcategory"),
    path("allcat/",views.ShowAllCat,name="allcat"),
    path("showall/",views.AllCategoryShow,name="showall"),
    path("editpage/<int:pk>",views.EditPage,name="editpage"),
    path("update/<int:pk>",views.UpdateData,name="update"),
    path("delete/<int:pk>",views.DeleteData,name="delete"),


    path("SubCategory/",views.SubCategoryPage,name="SubCategory"),
    path("addsubcat/",views.AddSubCategory,name="addsubcat"),


    #############################Seller Add Post###########################333333
    
    path("shocategory/",views.ShowCategoryPage,name="shocategory"),
    path("sel_cat/",views.SelectCat,name="sel_cat"),
    path("sel_subcat/",views.Select_SubCat,name="sel_subcat"),
    path("addproduct/<int:pk>",views.AddProduct,name="addproduct"),
    #path("Succ/",views.success,name="Succ"),
#########################Seller show#####################33333333333
    path("allproduct/",views.ShowAllProduct,name="allproduct"),
    path("seleditpage/<int:pk>",views.SelEditPage,name="seleditpage"),
    path("selupdate/<int:pk>",views.SelUpdateData,name="selupdate"),
    path("seldelete/<int:pk>",views.SelDeleteData,name="seldelete"),


    path("image/<int:pk>",views.ImageShow,name="image"),
    path("editimage/<int:pk>",views.EditImage,name="editimage"),
    path("updateimage/<int:pk>",views.UpdateImage,name="updateimage"),
    path("allshow/",views.AllPrShow,name="allshow"),
    path("showindx/",views.ShowIndex,name="showindx"),
    path("singles/<int:pk>",views.SingleProduct,name="singles"),
    path("addtocart/<int:pk>",views.AddtoCart,name="addtocart"),
    path("showallcart/",views.ShowAllCart,name="showallcart"),
    # path("Showsingles/",views.ShowSingle,name="Showsingles"),



    ################# Customer Account#########3333333
    # path("Account/",views.MyAccountPage,name="Account"),
    path("BuyerLogout/",views.Buyerlogout,name="BuyerLogout"),
    path("Customerindex/",views.CustomerIndex,name="Customerindex"),
    path("custprofilepage/<int:pk>",views.CustomerProfilePage,name="custprofilepage"),
    path("customerupdate/<int:pk>",views.CustomerUpdateProfile,name="customerupdate"),
    path("EditCartpa/<int:pk>",views.CartEditPage,name="EditCartpa"),
    path("deletecart/<int:pk>",views.DeleteCart,name="deletecart"),
    path("updatecart/<int:pk>",views.UpdateCart,name="updatecart"),


    ####################Checkpout################333
    path("checkout/",views.CheckOut,name="checkout"),
    path("emailcehck/",views.EmailC,name="emailcehck"),


    path('pay/',views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),



    path('orders/',views.order,name="orders"),
    
]
