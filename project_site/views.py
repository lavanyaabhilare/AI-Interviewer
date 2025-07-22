from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Database_user
import time
import random
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fuzzywuzzy import fuzz
from email import encoders
import datetime

# all global variables here

host_email_id = "priyans.mehta2003@gmail.com"
host_email_password = "Priyansh@1712"
final_otp = ""
mylist=[]

User_Confidence_list= []
List_of_Accuracy_of_Answer= []
quotes_list=[
            "'We become what we think about' – Earl Nightingale",
            "'People who are crazy enough to think they can change the world, are the ones who do.'- Rob Siltanen",
            "' Optimism is the one quality more associated with success and happiness than any other.'- Brian Tracy",
            "'Happiness is not something readymade. It comes from your own actions.'- Dalai Lama",
            "'All our dreams can come true if we have the courage to pursue them.'- Walt Disney",
            "'Believe you can and you’re halfway there.'- Theodore Roosevelt",
            "'You are never too old to set another goal or to dream a new dream.'– C.S. Lewis",
            "'Everything you've ever wanted is on the other side of fear.' - George Addair",
            "'You get what you give.' – Jennifer Lopez",
            "'Your life only gets better when you get better.'- Brian Tracy",
            "'Happiness is not by chance, but by choice.' – Jim Rohn",
            "'Be the change that you wish to see in the world.' - Mahatma Ghandi",
            "'If I cannot do great things, I can do small things in a great way.' – Martin Luther King Jr.",
            "'We generate fears while we sit. We overcome them by action.' –  Dr. Henry Link",
            "'Today's accomplishments were yesterday's impossibilities'– Robert H. Schuller",
            "'Light tomorrow with today!' –  Elizabeth Barrett Browning",
            "'The only limit to our realization of tomorrow will be our doubts of today.' – Franklin D. Roosevelt",
            "'Keep your face always toward the sunshine, and shadows will fall behind you.' – Walt Whitma",
            "'The bad news is time flies. The good news is you're the pilot.' – Michael Altshuler",
            "'Let us make our future now, and let us make our dreams tomorrow's reality.' –  Malala Yousafzai",
            "'Don't Let Yesterday Take Up Too Much Of Today.' – Will Rogers",
            ]
Questions_list=["Define Function in C",#1
                "What is  the use  of printf()",#2
                "Types of Array in C ?",#3
                "Define keywords in C and give example ?",#4
                "In C which function is used to take input from console?",#5
                "Who Developed C Programming?",#6
                "What is the use of main function?",#7
                #"What are Data Types in C?",#8
                "Define Operator and State it's types?",#9
                "what is the use of default keyword?"]#10
# all support method starts from here




# method for generating otp
def generate_otp():
    global final_otp
    otp = ""
    for i in range(8):
        otp = str(otp + random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']))
        print("otp : ", otp)
    print("final otp is : ", otp)
    final_otp = otp
    print("otp generated successfully..! ", final_otp)
    return otp

# method for sending email of otp to users
def send_email(subject_msg, body_msg, receivers_email_id, is_otp):

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            if is_otp:
                # calling method for generating otp  
                otp = generate_otp()
                print(otp)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(host_email_id, host_email_password)

            

            subject = subject_msg
            if is_otp:
                body = f'\n' + body_msg + '\n\n' + otp
            else:
                body = f'\n' + body_msg + '\n'
            complete_mail = f'Subject: {subject}\n\n\n{body}'

            smtp.sendmail(host_email_id, receivers_email_id, complete_mail)
            print("E-mail sent successfully..!")

    except Exception as error:
        print("error was :: ", error)


# all support method ends here



# Create your views here.

def index(request):

    if request.user.is_authenticated:

        print("User :: ", request.user)
        print("User name :: ", request.user.first_name)
        print("Is user authenticated :: ", request.user.is_authenticated)

        #reset_list()
        return redirect('home')
        #return render(request, 'home.html')
    else:
        return render(request, 'index.html')


    #return render(request, 'index.html')


def home(request): 
    mylist.clear()
    User_Confidence_list.clear()
    List_of_Accuracy_of_Answer.clear()


    if request.user.is_authenticated:
        
        print("User :: ", request.user)
        print("User name :: ", request.user.first_name)
        print("Is user authenticated :: ", request.user.is_authenticated)
        print(request.user.id)

        user_data=Database_user.objects.get(user=request.user)
        
        # reset_list()
        print(user_data.bio)
        print("Gender:",user_data.gender)
            
       
        no_img=True
        if user_data.image_dp == "NULL":
            no_img=True
        else:
            no_img=False
        return render(request, 'home.html',{"user_data":user_data,"profile_img":no_img})
    else:
        return render(request, 'index.html')
    
    #return render(request, 'index.html')


def user_login(request):
    
    if request.method == 'POST':

        login_email = str(request.POST.get('login_email'))
        login_password = str(request.POST.get('login_password'))
        
        print(login_email, login_password)

        try:
            current_user = authenticate(request, username = login_email, password = login_password)
            print("user login verified !", current_user)
        except Exception as error:
            print("Error occured !", error)
            
            if User.objects.filter(username=login_email).exists():
                user_exists = True
            else:
                user_exists = False

            return JsonResponse({"status":False, "user_exists":user_exists})

        if current_user is not None:
            login(request, current_user)
            print("User login successful!")
            #messages.success(request, "User login successful!")
            return JsonResponse({"status":True, "message":"Login successful"})
        else:
            if User.objects.filter(username=login_email).exists():
                print("user exists but password is wrong !")
                user_exists = True
            else:
                print("user does not exists !")
                user_exists = False

            return JsonResponse({"status":False, "message":"Invalid creadintial", "user_exists":user_exists})
    
    else:
        return render(request, 'index.html')


def create_account(request):

    if request.method == 'POST':

        signup_user_name = str(request.POST.get('signup_user_name'))
        signup_email = str(request.POST.get('signup_email'))
        signup_password = str(request.POST.get('signup_password'))
        signup_confirm_password = str(request.POST.get('signup_confirm_password'))

        print(signup_user_name, signup_email, signup_password, signup_confirm_password)

        if not(User.objects.filter(username=signup_email).exists()):

            print("sending email for verificaion of user email")

            send_email("From Intelligent.AI :: Verifying your Email",
            "Here is the One Time Password for verifying your email. \nDon't share with anyone. \nIt is valid for next 5 minutes.",
            signup_email, True)

            print("sent successfully !")

            return JsonResponse({"status":True, "user_email":signup_email, 
            "next_action":"otp_verification", "error_message":""})

        else:

            print("This email already in use.!")
            return JsonResponse({"status":False, "user_email":signup_email,
            "next_action":"Stay on signup page", "error_message":"This email already in use.!"})

    else:
        return render(request, 'index.html')


def otp_verification(request):

    if request.method == 'POST':

        signup_otp = str(request.POST.get('signup_otp'))
        print(signup_otp)


        signup_user_name = str(request.POST.get('signup_user_name'))
        signup_email = str(request.POST.get('signup_email'))
        signup_password = str(request.POST.get('signup_password'))
        signup_confirm_password = str(request.POST.get('signup_confirm_password'))

        print(signup_user_name, signup_email, signup_password, signup_confirm_password)

        # new_user = User.objects.create_user(username=signup_email, password=signup_password, 
        #             email=signup_email, first_name=signup_user_name)
        # new_user.save();
        # print("New user created ! : Added to database")

        if signup_otp == final_otp:

            print("New user creating....!")
            new_user = User.objects.create_user(username=signup_email, password=signup_password, 
                    email=signup_email, first_name=signup_user_name)
            new_extended_user=Database_user(user=new_user,image_dp="NULL")
            new_extended_user.save()


            # new_extended_user=Database_user(contact="",bio="",highest_qualification="",gender="",profile_photo="")
            # new_extended_user.save()

            # new_user = User.objects.create_user(username=signup_email, password=signup_password, 
            #         email=signup_email, first_name=signup_user_name,last_name="Jaiswal",Highest_Qualification="B.Tech",Contact_No="948488383",Gender="Male")
            
            
            
            new_user.save()
            print("New user created ! : Added to database")
            
            user = User.objects.get(username=signup_email)
            if user is not None:

                login(request, user)
                print("User login successful !")

                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
        else:
            return JsonResponse({'status':False})
    else:
        return render(request, 'index.html')

def update_user_info(request):
    print("In Update_Info  FUnction")
    if request.method=="POST":  
        print("In Update_Info  FUnction")
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        contact=request.POST.get('contact')
        bio=request.POST.get('bio')
        highest_qualification=request.POST.get('highest_qualification')
        gender=str(request.POST.get('gender'))
        #image_url=request.POST.get('image')
        #remove_picture=request.POST.get('remove_picture')       
        # profile_photo=request.FILES.getlist('imageField')
        print(request.user.id)
        #print("Image=",image_url)
        #print("remove Pic:",remove_picture)        
        print(first_name,last_name,contact,bio,highest_qualification)

        # fs=FileSystemStorage()
        # file_name=fs.save("eoeo.jpg","eoeo.jpg")
        # img_url=fs.url(file_name)

        print("Updated is Started")
        User.objects.filter(id=request.user.id).update(first_name=first_name,last_name=last_name)

        


        Database_user.objects.filter(user=request.user).update(contact=contact,bio=bio,
                highest_qualification=highest_qualification,gender=gender)
        
        print("Updated.....")

        # if not image_url=="":
        #     Database_user.objects.filter(user=request.user).update(image_dp=image_url)
        #     print("Profile Pic Updated....")
        # if remove_picture=="true":
        #     Database_user.objects.filter(user=request.user).update(image_dp="NULL")
        #     print("remove Pic 2 in if:",remove_picture)        






        return JsonResponse({"status":True, "message":"Information Updated..."})

    return redirect("/")



def short_reviwes(request):

    if request.method == "POST":

        msg_sender_name = str(request.POST.get('msg_sender_name'))
        msg_sender_email = str(request.POST.get('msg_sender_email'))
        msg_sender_message = str(request.POST.get('msg_sender_message'))

        mail_body = f"User reviews Or Bugs report.! \nSender name :: {msg_sender_name} \nSender email :: {msg_sender_email} \n\nMessage :: \n{msg_sender_message}"
        
        send_email("Reviews Or Bugs !", mail_body, host_email_id, False)
        print("Mail sent successfully !")
        
        return JsonResponse({"status":"Sent successfully..!", "message":"Thanks for your reviews!"})

    else:
        return render(request, 'index.html')


def forgot_password(request):

    if request.method == "POST":
        request_for = str(request.POST.get('request_for'))
        print(request_for)

        # verify user
        if request_for == "verify user":
            forgot_password_email = str(request.POST.get('fp_email'))
            
            if User.objects.filter(username=forgot_password_email).exists():

                send_email("From Intelligent.AI :: Verifying your Email to change password",
                "Here is the One Time Password for verifying your email. \nDon't share with anyone. \nIt is valid for next 5 minutes. \nAfter verification you can change your password.",
                forgot_password_email, True)
                print("mail sent successfully.!")

                return JsonResponse({"status":True, "user_email":forgot_password_email, 
                "next_action":"otp_verification", "error_message":""})
            else:
                return JsonResponse({"status":False, "user_email":forgot_password_email, 
                "next_action":"get valid email", "error_message":"This user does not exists.!"})

        # verify otp
        elif request_for == "verify otp":
            forgot_password_email = str(request.POST.get('fp_email'))
            forgot_password_email_otp = str(request.POST.get('fp_email_otp'))

            if forgot_password_email_otp == final_otp:
                return JsonResponse({"status":True, "user_email":forgot_password_email, 
                "next_action":"reset password", "error_message":""})
            else:
                return JsonResponse({"status":False, "user_email":forgot_password_email, 
                "next_action":"get valid otp", "error_message":"Invalid OTP !"})

        # reset pas
        # sword
        elif request_for == "reset password":
            forgot_password_email = str(request.POST.get('fp_email'))
            forgot_password_new_password = str(request.POST.get('fp_new_password'))

            
            user = User.objects.get(username=forgot_password_email)
            print(user)
            #print(user.id)

            #Database_user.objects.filter(id=2).update(last_name="jjjj",bio="BE in IT",gender="M",contact="9999988888",Profile_Photo="static/images/pic01.jpg")
            
            user.set_password(forgot_password_new_password)
            user.save()
            print("password updated")
            #send_email("Password changed!", f"Hello {request.user.first_name} !\nYour password has been changed successfully!", forgot_password_email, False)
            print("mail sent successfully !")

            return JsonResponse({"status":True, "user_email":forgot_password_email, 
            "next_action":"Password changed successfully", "error_message":""})
            # return JsonResponse({"status":False, "user_email":forgot_password_email, 
            # "next_action":"get valid email", "error_message":"This user does not exists.!"})


    else:
        return render(request, 'index.html')


def user_logout(request):
    logout(request)
    print("User logged out successfully !")
    return redirect('/')


def start_interview(request):

    if request.user.is_authenticated:
        
        print("User :: ", request.user)
        print("User name :: ", request.user.first_name)
        print("Is user authenticated :: ", request.user.is_authenticated)

        return render(request, 'interview_page.html')
    else:
        return redirect("/")


# def final_report(request):

#     if request.method == "GET":
        
#         answers = str(request.GET.get('answers'))
#         print("Answers :: " + answers)

#         return JsonResponse({"status":"Successfully collected and stored users answers !"})

#     else:
#         return render(request, 'interview_page.html')



def SendReport(request):
    print("Sending.....")
    mail_content = '''Hello,
    This is a test mail.
    In this mail we are sending some attachments.
    The mail is sent using Python SMTP library.
    Thank You
    '''
    #The mail addresses and password
    receiver_address = request.user.email
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = host_email_id
    message['To'] = receiver_address
    message['Subject'] = "Thank you "+request.user.first_name+" for attempting Quiz on Intelligence.AI We have attached your Report"
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'ReportCardofInterview.pdf'
    attach_file = open(attach_file_name, 'rb') # Open the file as binary mode

    print("Report 50%")

    payload = MIMEBase('application',"pdf",Name=attach_file_name)
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(host_email_id, host_email_password) #login with mail_id and password
    text = message.as_string()
    session.sendmail(host_email_id, receiver_address, text)
    session.quit()
    print('Mail Sent')
    time.sleep(3)
    redirect('index.html')





def bi(request):
    quotes_list=[
            "'We become what we think about' – Earl Nightingale",
            "'People who are crazy enough to think they can change the world, are the ones who do.'- Rob Siltanen",
            "' Optimism is the one quality more associated with success and happiness than any other.'- Brian Tracy",
            "'Happiness is not something readymade. It comes from your own actions.'- Dalai Lama",
            "'All our dreams can come true if we have the courage to pursue them.'- Walt Disney",
            "'Believe you can and you’re halfway there.'- Theodore Roosevelt",
            "'You are never too old to set another goal or to dream a new dream.'– C.S. Lewis",
            "'Everything you've ever wanted is on the other side of fear.' - George Addair",
            "'You get what you give.' – Jennifer Lopez",
            "'Your life only gets better when you get better.'- Brian Tracy",
            "'Happiness is not by chance, but by choice.' – Jim Rohn",
            "'Be the change that you wish to see in the world.' - Mahatma Ghandi",
            "'If I cannot do great things, I can do small things in a great way.' – Martin Luther King Jr.",
            "'We generate fears while we sit. We overcome them by action.' –  Dr. Henry Link",
            "'Today's accomplishments were yesterday's impossibilities'– Robert H. Schuller",
            "'Light tomorrow with today!' –  Elizabeth Barrett Browning",
            "'The only limit to our realization of tomorrow will be our doubts of today.' – Franklin D. Roosevelt",
            "'Keep your face always toward the sunshine, and shadows will fall behind you.' – Walt Whitma",
            "'The bad news is time flies. The good news is you're the pilot.' – Michael Altshuler",
            "'Let us make our future now, and let us make our dreams tomorrow's reality.' –  Malala Yousafzai",
            "'Don't Let Yesterday Take Up Too Much Of Today.” – Will Rogers'",
            ]
    random_quote=random.choice(quotes_list)
    user_data=Database_user.objects.get(user=request.user)        
    print("Gender:",user_data.gender)
    
    
    no_img=True
    if user_data.image_dp == "NULL":
        no_img=True
    else:
        no_img=False
    s=[1,2,3]
    return render(request, 'report_template.html',{"user_data":user_data,"profile_img":no_img,"count":List_of_Accuracy_of_Answer,"quote":random_quote})

   
def f1(request):
    if request.user.is_authenticated:
        
        print("User :: ", request.user)
        print("User name :: ", request.user.first_name)
        print("Is user authenticated :: ", request.user.is_authenticated)
        print(request.user.id)

        # user_data=Database_user.objects.get(user=request.user)
        
        # # print(user_data.bio)
        # print("Gender:",user_data.gender)
        
        # print("Image DP",user_data.image_dp)
        # no_img=True
        # if user_data.image_dp == "NULL":
        #     no_img=True
        # else:
        #     no_img=False
    
        # params={
        #     'today':datetime.date.today(),
        #     'user_data':user_data

        # }   
        # file_name,status=save_pdf(params);
        random_quote=random.choice(quotes_list)
        user_data=Database_user.objects.get(user=request.user)        
        print("Gender:",user_data.gender)
        
       
        no_img=True
        if user_data.image_dp == "NULL":
            no_img=True
        else:
            no_img=False
        #return render(request, 'report_template.html',{"user_data":user_data,"profile_img":no_img,"count":List_of_Accuracy_of_Answer,"quote":random_quote})
        

        return render(request, 'report_template.html',{"user_data":user_data,"profile_img":no_img})
    else:
        return render(request, 'index.html')
    
def ex(request):
    mylist.clear()
    User_Confidence_list.clear()
    List_of_Accuracy_of_Answer.clear()
    print("In EX Function")
    if request.user.is_authenticated:
        random_quote=random.choice(quotes_list)
        print("User :: ", request.user)
        print("User name :: ", request.user.first_name)
        print("Is user authenticated :: ", request.user.is_authenticated)
        print(request.user.id)

        user_data=Database_user.objects.get(user=request.user)
        
        # print(user_data.bio)
        print("Gender:",user_data.gender)
        
        
        no_img=True
        if user_data.image_dp == "NULL":
            no_img=True
        else:
            no_img=False
    

    Accuracy_of_answer=[]
    if request.method=="POST":
        global User_Answer
        
        Correct_Answer_list=[
            "A function is a group of statements that together perform a task. Every C program has at least one function, which is main(), and all the most trivial programs can define additional functions. You can divide up your code into separate functions. How you divide up your code among different functions is up to you, but logically the division is such that each function performs a specific task. A function declaration tells the compiler about a function's name, return type, and parameters. A function definition provides the actual body of the function.The C standard library provides numerous built-in functions that your program can call. For example, strcat() to concatenate two strings, memcpy() to copy one memory location to another location, and many more functions.",
            "printf() and scanf() functions are inbuilt library functions in C which are available in C library by default. These functions are declared and related macros are defined in “stdio.h” which is a header file. We have to include “stdio.h” file to make use of this printf() and scanf() library functions. C users these functions to write and read from I/O devices respectively.    printf() and scanf() functions are inbuilt library functions in C which are available in C library by default. These functions are declared and related macros are defined in “stdio.h” which is a header file. We have to include “stdio.h” file to make use of this printf() and scanf() library functions. C users these functions to write and read from I/O devices respectively.",
            "In c programming language, arrays are classified into two types. They are as follows...    Single Dimensional Array / One Dimensional Array Multi Dimensional Array Single Dimensional Array In c programming language, single dimensional arrays are used to store list of values of same datatype. In other words, single dimensional arrays are used to store a row of values. In single dimensional array, data is stored in linear form. Single dimensional arrays are also called as one-dimensional arrays, Linear Arrays or simply 1-D Arrays.",
            "Keywords are predefined, reserved words in C language and each of which is associated with specific features. These words help us to use the functionality of C language. They have special meaning to the compilers.A keyword is a reserved word. You cannot use it as a variable name, constant name, etc. There are only 32 reserved words (keywords) in the C language.auto	break	case	char	const	continue	default	do double 	else 	enum 	extern	float	for	goto	if int 	long	register	return	short	signed	sizeof	static struct	switch	typedef	union	unsigned	void	volatile	while",                             "Each variable in C has an associated data type. Each data type requires different amounts of memory and has some specific operations which can be performed over it. Let us briefly describe them one by one:    char: The most basic data type in C. It stores a single character and requires a single byte of memory in almost all compilers.int: As the name suggests, an int variable is used to store an integer.float: It is used to store decimal numbers (numbers with floating point value) with single precision.double: It is used to store decimal numbers (numbers with floating point value) with double precision. Different data types also have different ranges upto which they can store numbers. These ranges may vary from compiler to compiler. Below is list of ranges along with the memory requirement and format specifiers on 32 bit gcc compiler."
            "scanf() function is used to read input from the console or standard input of the application in C and C++ programming language. scanf() function can read different data types and assign the data into different variable types.",
            "C is Developed  by Dennis Ritchie",
            "main() function is the entry point of any C program. It is the point at which execution of program is started. When a C program is executed, the execution control goes directly to the main() function. Every C program have a main() function.    An operating system always calls the main() function when a programmers or users execute their programming code.It is responsible for starting and ends of the program. It is a universally accepted keyword in programming language and cannot change its meaning and name.    A main() function is a user-defined function in C that means we can pass parameters to the main() function according to the requirement of a program.    A main() function is used to invoke the programming code at the run time, not at the compile time of a program. A main() function is followed by opening and o parenthesis brackets.", 
            "An operator is a symbol that tells the compiler to perform specific mathematical or logical functions. C language is rich in built-in operators and provides the following types of operators −    Arithmetic Operators Relational Operators  Logical Operators  Bitwise Operators Assignment Operators Misc Operators",
            "default in C is used in a switch statement to indicate the control path when no other case is selected. Hence that is why it is used, i.e. to indicate which location in the code gets control “by default”. Default is also used in C++ in switch statements and also for class member functions specifiers for compiler generated functions (and constructors) but since we’re taking about C I won’t go into why you’d need them in C++."]

        
        
        User_Answer=str(request.POST.get('Answer'))
        User_Confidence=str(request.POST.get('Confidence'))
        Confidence_list=User_Confidence.split(',')
        print('Final_Confidence_list In Python',Confidence_list)

        User_Answer_list=User_Answer.split("NextAnswer")
        count=0
        print(User_Answer)
        print("User")
        print("Before Confidence...",Confidence_list)
        while '' in Confidence_list: Confidence_list.remove('')
        print("After Confidence...",Confidence_list)
        for i in User_Answer_list:
            print("{}User Answer {}".format(count,i))
            count+=1

        print("Length of User_Answer_List",len(User_Answer_list))
        #try:    
        for j in range(len(User_Answer_list)):
            Accuracy=fuzz.ratio(Correct_Answer_list[j],User_Answer_list[j])
            Accuracy_of_answer.append(Accuracy)#e=[13,5,6,6,4]
        print("Pankaj List",Accuracy_of_answer)
        List_of_Accuracy_of_Answer.extend(Accuracy_of_answer)#[1,[13,5,6,6,4]]
        print("Siddhirakj ",len(List_of_Accuracy_of_Answer))
        print("Siddhirakj ",List_of_Accuracy_of_Answer)
        User_Confidence_list.extend(Confidence_list)
        

        print(List_of_Accuracy_of_Answer)
        print(Confidence_list)
        print("User COnide list",User_Confidence_list)

        


    
    return JsonResponse({"status":True,'message':"Success"})
    
    #return render(request,"template_report.html",context)
    #return render(request,'report_template.html')

    # return redirect("/ex2")

def ex2(request):

    percentage=sum(List_of_Accuracy_of_Answer)/len(List_of_Accuracy_of_Answer)
    if percentage>75:
        grade="Excellent"
    elif percentage>60:
        grade="Very Good"
    elif percentage>50:
        grade="Good"
    elif percentage>40:
        grade="Need Improvement"
    else:
        grade="Poor"


    curr_time=datetime.datetime.now()
    
    datetime_object = datetime.datetime.strptime(str(curr_time.month), "%m")
    
    today=str(curr_time.day)+" "+str(datetime_object.strftime("%B"))+" "+str(curr_time.year)+"."

    random_quote=random.choice(quotes_list)
    print("IN EX2 Function")
    user_data=Database_user.objects.get(user=request.user)

    length_of_attempt = len(List_of_Accuracy_of_Answer)

    final_Questions_list = Questions_list[:length_of_attempt]
    final_User_Confidence_list=[]
    for j in User_Confidence_list:
        a=float(j)
        s=a*100
        s=int(s)
        final_User_Confidence_list.append(s)
    print("Old User Confidence",User_Confidence_list)
    final_User_Confidence_list = final_User_Confidence_list[:length_of_attempt]
    

        
    mylist = zip(final_Questions_list,list(range(1,length_of_attempt+1)),final_User_Confidence_list,List_of_Accuracy_of_Answer)    
    # print(user_data.bio)
    
    no_img=True
    if user_data.image_dp == "NULL":
        no_img=True
    else:
        no_img=False
    print("Main Line oF Software",final_Questions_list,list(range(1,length_of_attempt+1)),final_User_Confidence_list,List_of_Accuracy_of_Answer)
    
    print("Answer Accuracy",List_of_Accuracy_of_Answer)
    
    print("Length",length_of_attempt)
    print("Sr.no",list(range(1,length_of_attempt+1)))

    print("Question Final",final_Questions_list)

    print("Confidence Final",final_User_Confidence_list)
    return render(request,"template_report.html",{"user_data":user_data,"profile_img":no_img,"mylist":mylist,"quote":random_quote,"today":today,"grade":grade})
    #return render(request,"template_report.html")

def save_image(request):
    if request.method=="POST":
        image=request.POST.get("image")
        remove_picture=request.POST.get("image_change")
        print("IMG",image)
        print("remove_picture",remove_picture)
        Database_user.objects.filter(user=request.user).update(image_dp=image)
        print("Profile Pic Updated....")
        
        if remove_picture=="true":
            
            Database_user.objects.filter(user=request.user).update(image_dp="NULL")
            print("remove Pic 2 in if:",remove_picture)        

        return JsonResponse({"status":True,"message":"ImageSaved"})

    return HttpResponse("<h1>Error</h1>")

def tc(request):
    return render(request,"terms_and_condition.html")

def pp(request):
    return render(request,"privacy_policy.html")
def next_q(request):
    if request.method=="POST":
        status=False
        msg="Not Skipping answer.."
        neg_sent=["Lets move to the question","I don't known answer",'Sorry but I dont known',
        "I can't answer","I really don't known","please move to the next question",'next question'
        "I didn't heard about it","Can you please ask next question",'Sorry but I dont known about it'
        "I am not aware of it"]
        for i in neg_sent:
            print("Neg Answer",str(request.POST.get("Ans")))
            Accuracy=fuzz.ratio(i,str(request.POST.get("Ans")))
            print("Accuracy of  Neg Answer ",i,Accuracy)
            if Accuracy>60:
                status=True
                msg="skipping answer...."
    
                break
        return JsonResponse({"status":status,"message":msg})
    return HttpResponse('404 Not Found')