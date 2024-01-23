from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from reservations.models import Reservation
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                print('Username already exists')
                return redirect('login_register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('login_register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'User created successfully')
                    return redirect('home') #login
        else:
            print('Passwords do not match')
            return redirect('login_register')

    return render(request, 'login_register.html')

def login_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if user exists
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('home')

    return render(request, 'login_user.html')

@staticmethod
def logout_user(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login_user')
def make_reservation(request):
    if request.method == 'POST':
        user = request.user
        phone = request.POST['phone']
        table = request.POST['table']
        date = request.POST['date']
        time = request.POST['time']
        number_of_people = request.POST['number_of_people']
        message = request.POST['message']

        # Verificar se já existe uma reserva para a mesma mesa e horário
        existing_reservation = Reservation.objects.filter(date=date, time=time)

        if existing_reservation.exists():
            # Se já existe uma reserva, você pode lidar com isso de diferentes maneiras,
            # como exibindo uma mensagem de erro ou redirecionando o usuário.
            # Neste exemplo, estou redirecionando o usuário para uma página de erro.
            messages.error(request, 'There is already a reservation for this date and time')
            return redirect('make_reservation')

        # Criar a nova reserva
        reservation = Reservation(
            user=user,
            phone=phone,
            table=table,
            date=date,
            time=time,
            number_of_people=number_of_people,
            message=message
        )

        reservation.save()
        messages.success(request, 'Reservation created successfully')
        return redirect('make_reservation')

    return render(request, 'make_reservation.html')

@login_required(login_url='login_user')
def profile(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)
    context = {
        'reservations': reservations
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login_user')
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

    if request.method == 'POST':
        # Atualize os campos da reserva com os dados do formulário
        reservation.date = request.POST['date']
        reservation.time = request.POST['time']
        reservation.table = request.POST['table']
        reservation.number_of_people = request.POST['number_of_people']
        reservation.save()
        return redirect('profile')
    
    

    return render(request, 'edit_reservation.html', {'reservation': reservation})

def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    reservation.delete()
    return redirect('profile')