from rest_framework.decorators import parser_classes,renderer_classes, api_view,permission_classes
from todoApp.serializers import TasksDocSerializer,TodoGroupDocSerializer,UserRegisterDocSerializer,AssigneeMgmtSerializer, UserRegistrationSerializer,TodoGroupsSerializer,TasksSerializer,OverdueTasksSerializer,UpdateTaskStatusSerializer,AddCommentSerializer
from rest_framework.response import Response
import random
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator,EmptyPage
import datetime
from django.core.mail import send_mail, BadHeaderError  
from todoApp.models import User,TodoGroups,Tasks
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import JSONRenderer
from drf_yasg import openapi



def authenticate(email, password):
    try:
        # Get the corresponding user.
        user = User.objects.get(email=email)
        #  If password, matches just return the user. Otherwise, return None.
        if check_password(password, user.password):
            return user
        return None
    except User.DoesNotExist:
        # No user was found.
        return None


@renderer_classes([JSONRenderer])
@swagger_auto_schema(
    method='POST',
    operation_description='Register a new user with email verification.',
    responses={
        200: 'OK - Registered successfully. Please check your email and activate your account.',
        400: 'Bad Request - Validation errors in the input data.',
        500: 'Internal Server Error - Error while sending email.',
    },
    request_body=UserRegisterDocSerializer,
   
)
@api_view(['POST'])
def UserRegistration(request):
    if request.method=='POST':
        data=request.data
        serializer=UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            otp = random.randint(1000,9999)
            serializer.validated_data['otp']=otp
            serializer.validated_data['password']=make_password(data['password'])
            serializer.save()
            email=serializer.data['email']
            subject='OTP for password reset'
            message=f'Your OTP for password reset is {otp}.Do not share it with anyone.'
            from_email="sia2121181@sicsr.ac.in"
            recipient_list=[email]
            try:
                send_mail(subject,message,from_email,recipient_list,fail_silently=False)
            
            except BadHeaderError:
                return Response({'message':'Error.'})
                
            print(email)
            return Response({'message':'Registered Successfully!!! Please check your email and activate your account.'})
    return Response(serializer.errors)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'otp': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['email', 'otp'],
    ),
    responses={
        200: openapi.Response('Account verified and activated successfully. You can now proceed with login.'),
        400: openapi.Response('Invalid input. Please provide valid email and OTP.'),
    },
)
@api_view(['POST'])
def verifyOTP(request):
    if request.method=='POST':
        email=request.data.get('email')
        if email is None or email=="":
            return Response({'message':'please enter email address'})
        
        otp=request.data.get('otp')
        if otp is None or otp=="":
            return Response({'message':'Please enter otp'})
        
        user=User.objects.get(email=email)
        if user is not None:
            if user.otp==int(otp):
                user.is_verified=True
                print(user.is_verified)
                user.save()
                return Response({'message':'Account verified and activated successfully. You can now proceed with login.'})
            return Response({'message':'invalid otp'})
        return Response({'message':'Email does not exists'})


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
        },
        required=['email', 'password'],
    ),
    responses={
        200: 'Login successful. Returns access and refresh tokens.',
        400: 'Invalid input data. Returns error message.',
    },
)
@api_view(['POST'])
def login(request):
    if request.method=='POST':
        email=request.data.get('email')
        if email is None or email=="":
            return Response({'message':'please enter email address'})
        
        password=request.data.get('password')
        if password is None or password=="":
            return Response({'message':'Please enter a password'})
        
        user=authenticate(email=email,password=password)
        print(user)
        if user is None:
            return Response({'message':'Invalid credentials'})

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({'message': 'Login successful', 'access_token': access, 'refresh_token': str(refresh)})
    

@swagger_auto_schema(
    methods=['POST'],
    request_body=TodoGroupDocSerializer,
    responses={
        201: 'Todo Group created successfully. Returns data of the created group.',
        400: 'Invalid input data. Returns error message.',
    },
)
@swagger_auto_schema(
    methods=['GET'],
    responses={
        200: 'Returns a list of Todo Groups.',
    },
)
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def todoGroup(request):
    if request.method=='POST':
        data=request.data
        serializers=TodoGroupsSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response({'message':'Todo Group created successfully.','data':serializers.data})
        return Response({'message':serializers.errors})
    elif request.method=='GET':
        objs=TodoGroups.objects.all()
        serializer=TodoGroupsSerializer(objs,many=True)
        return Response(serializer.data)
    

@swagger_auto_schema(
    method='POST',
    request_body=TasksSerializer,
    responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)},
    operation_description='Create a new task.',
)
@swagger_auto_schema(
    method='GET',
    manual_parameters=[
        openapi.Parameter('page', in_=openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
    ],
    responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)},
    operation_description='Retrieve a paginated list of tasks.',
)
@api_view(['GET','POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def tasks(request):
    if request.method=='POST':
        data=request.data
        serializer=TasksSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Task created successfully','data':serializer.data})
        return Response({'message':serializer.errors})
    
    elif request.method=='GET':
        tasks=Tasks.objects.all()
        page=request.GET.get('page',1)
        page_size=2
        try:
            paginator=Paginator(tasks,page_size)
            serializer=TasksSerializer(paginator.page(page),many=True)
            return Response({'page_no':page,'data':serializer.data})
        
        except EmptyPage:
            return Response({'message':'No more tasks.'})
            
        
        
@swagger_auto_schema(
    methods=['GET'],
    responses={
        200: 'Returns a list of users.',
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    objs=User.objects.all()
    serializer=UserRegistrationSerializer(objs,many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    methods=['GET'],
    responses={
        200: 'Returns a list of overdue tasks.',
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overdue_tasks(request):
    tasks=Tasks.objects.filter(due_date__lte=datetime.datetime.now(),completion_status="Incomplete")
    serializer=OverdueTasksSerializer(tasks,many=True)
    return Response(serializer.data) 


@swagger_auto_schema(
    method='GET',
    manual_parameters=[
        openapi.Parameter('search', in_=openapi.IN_QUERY, description='Search term for task name', type=openapi.TYPE_STRING),
    ],
    responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)},
    operation_description='Search for tasks based on task name.',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_tasks(request):
    query=request.GET.get('search')
    if query=="":
        return Response({'message':'Please enter any task name to search.'})
    tasks=Tasks.objects.filter(title__contains=query)
    if tasks.exists():
        serializer=TasksSerializer(tasks,many=True)
        return Response(serializer.data)
    return Response({'message':'No tasks with that name exists.'})
    
@swagger_auto_schema(
    method='PUT',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Task id'),
            'completion_status': openapi.Schema(type=openapi.TYPE_STRING, description='Completion status'),
        },
        required=['id', 'completion_status'],
    ),
    responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)},
    operation_description='Update the completion status of a task.',
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_status(request):
    data=request.data
    try:
        tasks=Tasks.objects.get(id=data['id'])
    except tasks.DoesNotExist:
        return Response({'message': 'Task not found'})

    # update_data=({'completion_status':data['completion_status']})
    
    serializer = UpdateTaskStatusSerializer(instance=tasks, data={'completion_status': data['completion_status']}, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Task updated successfully'})
    return Response(serializer.errors)


@swagger_auto_schema(
    method='POST',
    request_body=AddCommentSerializer,
    responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)},
    operation_description='Add comments to a task.',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comments(request):
    data=request.data
    serializer=AddCommentSerializer(data=data)
    if serializer.is_valid():
        user=User.objects.get(id=data['user'])
        task=Tasks.objects.get(id=data['task'])
        assignee=task.assignee.filter(id=user.id).exists()
        created_by = task.created_by.id if task.created_by else None
        if assignee or user.id==created_by:
            serializer.save()
            return Response({'message':'Comments added successfully.','data':serializer.data})
        return Response({'message':'you are not allowed to comment'})
    return Response(serializer.errors)


@swagger_auto_schema(
    method='POST',
    request_body=AssigneeMgmtSerializer,
    responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)},
    operation_description='Assign a user to any task.',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assignee_mgmt(request):
    data=request.data
    serializer=AssigneeMgmtSerializer(data=data)
    
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        task_id = serializer.validated_data['task_id']
        user = User.objects.get(id=user_id)
        task = Tasks.objects.get(id=task_id)
        if request.user.id==task.created_by.id:
            task.assignee.add(user)
            task.save()
            return Response({'message':'Task assignee added successfully.','data':serializer.data})
        return Response({'message':'You are not allowed to modify assignees for this task.'})
    return Response(serializer.errors)



@swagger_auto_schema(
    method='POST',
    request_body=AssigneeMgmtSerializer,
    responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)},
    operation_description='Remove an assignee from a task.',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_assignee(request):
    data=request.data
    serializer=AssigneeMgmtSerializer(data=data)
    
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        task_id = serializer.validated_data['task_id']
        user = User.objects.get(id=user_id)
        task = Tasks.objects.get(id=task_id)
        if request.user.id==task.created_by.id:
            if user in task.assignee.all():
                task.assignee.remove(user)
                task.save()
                return Response({'message':'Task assignee removed successfully.','data':serializer.data})
            return Response({'message': 'User is not assigned to the task.'})
        return Response({'message':'You are not allowed to modify assignees for this task.'})
    return Response(serializer.errors)