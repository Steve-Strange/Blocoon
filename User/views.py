from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpRequest
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from User.models import UserProfile
from User.forms import LoginForm, MyUserCreationForm
from Utils.find import find_all_graphs, find_all_tags, find_all_favor_courses
from Neo4j.graph import Graph

# Create your views here.

class main_page(View):

    def get(self, request: HttpRequest):
        return render(request, "User/main.html", )

    def post(self, request: HttpRequest):
        return render(request, "User/login.html", )
        # fm = LoginForm()
        # if "login" in request.POST:
        #     return render(request, "User/login.html", {'form':fm, 'pwd_err':""})
        # elif "register" in request.POST:
        #     return render(request, "User/register.html", {'form': fm, 'pwd_err': ""})


class Login(View):
    def get(self, request : HttpRequest):
        fm = LoginForm()
        return render(request, "User/login.html", {'form':fm, 'pwd_err':""})
    
    def post(self, request : HttpRequest):
        # username = request.POST.get('username')
        # pwd = request.POST.get('pwd')
        fm = LoginForm(request.POST)
        if not fm.is_valid():
            return render(request, "User/login.html", {'form':fm, 'pwd_err':""})
        else:
            username = fm.cleaned_data.get('username')
            pwd = fm.cleaned_data.get('password')
            user = authenticate(username = username, password = pwd)
            if user is None:
                return render(request, "User/login.html", {'form':fm, 'pwd_err':"密码错误"})
            else:
                login(request, user)
                path = request.GET.get('next') or '/home/'
                # TODO: 
                return redirect(path)
            
class Logout(View):
    def get(self, request:HttpRequest):
        logout(request)
        return redirect('/login/')
            

class Register(View):
    '''
    注册用。用auth自带的UserCreationForm表单实现.  
    UserCreationField有三个fields: username(of User model), password1, password2.
    '''
    default_graph_path = "static/graphs/initial_graph.json"

    def get(self, request:HttpRequest):
        form = MyUserCreationForm()
        return render(request, 'User/register.html', {'form':form})
    
    def post(self, request:HttpRequest):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)   # 创建新用户了.
            # TODO: 初始化第一张默认图!
            default_graph = Graph(user)
            try:
                default_graph.import_json(Register.default_graph_path)  # 保证默认图没错.
            except Exception as e:
                user.delete()
                raise e
            return redirect('/register/success/')
        else:
            return render(request, 'User/register.html', {'form':form})
        

class RegisterSuccess(View):
    '''
    登录成功显示的界面，只有跳转到登录界面的一个链接是有用的。
    如果可以的话，登录成功后应该弹出一个模态框，关闭模态框之后自动回到登录界面比较好.
    '''
    def get(self, request:HttpRequest):
        return render(request, 'User/register_success.html')

        
class Homepage:
    @login_required
    def homepage(request: HttpRequest):
        # 下面那个context只是临时的...后面根据homepage.html更改..
        '''
        homepage.html context: 
        user: instance of UserProfile, means current user.
        GraphTag_List: list of GraphRoot instances.  
        KnowTag_List:  list of KnowledgeBlock instances.
        CourseTag_List:list of Course instances.
        Graph_List: list of GraphRoot instances.
        '''
        thisuser = UserProfile.objects.get(id = request.user.id)
        if request.method == "POST":
            t = request.POST.get("submitType")
            if t == "modifyHeadProfile":
                #file = request.POST.get("pic")
                file = request.FILES.get("pic")
                filename = thisuser.username + "_profile.jpg"
                p = "%s/image/%s"%(settings.MEDIA_ROOT, filename)
                content = file.chunks()
                with open(p, 'wb') as f:
                    for i in content:
                        f.write(i)
                thisuser.profile_picture = 'image/%s'%(filename)
                thisuser.save()

            elif t == "deleteGraph":
                uid = request.POST.get('uid')
                graph = Graph(thisuser, uid)
                graph.deleteSelf()

            elif t == "addGraph":
                try:
                    file = request.FILES.get("graph")
                except:
                    file = None
                newgraph = Graph(thisuser)
                if file is not None:
                    tmp_filename = thisuser.username + "_graph.json"
                    p =  "static/graphs/%s"%(tmp_filename)
                    with open(p, 'wb') as f:
                        for i in file.chunks():
                            f.write(i)
                    newgraph.import_json(p, False)
                else:
                    name = request.POST.get('name')
                    intro = request.POST.get('introduction')
                    if name:
                        newgraph.create_empty_graph(name, intro)
                    

        tags = find_all_tags(thisuser)
        graphs = find_all_graphs(thisuser)
        favors = find_all_favor_courses(thisuser)
        ctx = {
            'user': thisuser,
            'GraphTag_List': tags['GraphTags'],
            'KnowTag_List': tags['KnowTags'],
            'CourseTag_List': tags['CourseTags'],
            'Graph_List': graphs,
            'FavorCourses_List': favors
        }
        return render(request, "User/homepage.html", ctx)