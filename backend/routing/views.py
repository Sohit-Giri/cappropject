from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings as conf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import csv, json
import random
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

# UPDATED: Added UserOTP to this line
from .models import RouteLog, SavedRoute, UserPreference, UserOTP

from .serializers import (RouteRequestSerializer, RouteLogSerializer,
                           SavedRouteSerializer)
from .graph_manager import GraphManager
from .route_engine import RouteEngine

def _get_pref(user):
    pref, _ = UserPreference.objects.get_or_create(user=user)
    return pref


def _send_welcome(user):
    try:
        send_mail(
            subject='Welcome to RouteOptima! 🗺️',
            message=(
                f'''Hi {user.first_name or user.username},

Welcome to RouteOptima — Nepal's smart route optimizer!

You can now:
  • Find shortest paths across Kathmandu Valley + Nuwakot & Dhading
  • Search any place by name — tea shops, hospitals, schools
  • Compare two routes side by side
  • Save favourite routes and share them with friends

Open the app: https://your-app.vercel.app/dashboard/

— RouteOptima Team
  IIMS College · Group 36 · 2026'''
            ),
            from_email=conf.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email] if user.email else [],
            fail_silently=True,
        )
    except Exception:
        pass

def send_signup_email(email, otp):

    subject = "Verify your RouteOptima account"

    message = f"""
Hello,

Welcome to RouteOptima.

Your verification code is

{otp}

This OTP expires in 5 minutes.

If you did not request this, simply ignore this email.

RouteOptima
"""

    send_mail(
        subject,
        message,
        conf.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=True
    )

# ── Public pages ──────────────────────────────────────────────────────────────
def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'routing/landing.html')

# 1. REQUEST OTP VIEW
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            otp_record = UserOTP.generate_for_user(user)
            
            # Send Email containing the Code
            subject = "Your RouteOptima Password Reset OTP"
            message = f"Hello {user.first_name or user.username},\n\nYour OTP for resetting your password is: {otp_record.otp_code}\n\nThis code expires in 5 minutes."
            
            send_mail(subject, message, conf.DEFAULT_FROM_EMAIL or 'noreply@routeoptima.com', [user.email], fail_silently=False)
            
            # Store target email temporarily in session to identify user during verification step
            request.session['reset_email'] = email
            messages.success(request, 'A 6-digit OTP has been sent to your email address!')
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'No account found matching that email address.')
            
    return render(request, 'routing/forgot_password.html')


# 2. VERIFY OTP & RESEND VIEW
def verify_otp_view(request):
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Session expired. Please request a new OTP.')
        return redirect('forgot_password')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Handle Resend Request explicitly
        if action == 'resend':
            try:
                user = User.objects.get(email=email)
                otp_record = UserOTP.generate_for_user(user)
                subject = "Your RouteOptima Password Reset OTP"
                message = f"Your new RouteOptima OTP is: {otp_record.otp_code}"
# FIXED: Swapped out the hardcoded string for your system's global default settings configurations
                send_mail(
                    subject, 
                    message, 
                    getattr(conf, 'DEFAULT_FROM_EMAIL', 'RouteOptima <noreply@routeoptima.com>'), 
                    [email],
                    fail_silently=False
                )
                messages.success(request, 'A fresh OTP code has been dispatched!')
            except Exception:
                messages.error(request, 'Error sending new OTP. Try again.')
            return redirect('verify_otp')

        # Handle Standard Verification Check
        otp_input = request.POST.get('otp', '').strip()
        try:
            user = User.objects.get(email=email)
            otp_record = UserOTP.objects.filter(user=user, otp_code=otp_input).latest('created_at')
            
            if otp_record.is_valid():
                otp_record.is_verified = True
                otp_record.save()
                request.session['otp_verified'] = True
                messages.success(request, 'OTP verified successfully. Set your new password.')
                return redirect('reset_password')
            else:
                messages.error(request, 'This OTP has expired. Click resend below.')
        except UserOTP.DoesNotExist:
            messages.error(request, 'Invalid code. Check your mailbox and try again.')

    return render(request, 'routing/verify_otp.html', {'email': email})


# 3. SET NEW PASSWORD VIEW
def reset_password_view(request):
    email = request.session.get('reset_email')
    verified = request.session.get('otp_verified')
    
    if not email or not verified:
        messages.error(request, 'Unauthorized access attempt. Verify via OTP first.')
        return redirect('forgot_password')

    if request.method == 'POST':
        p1 = request.POST.get('password1', '')
        p2 = request.POST.get('password2', '')
        
        if p1 != p2:
            messages.error(request, 'Passwords do not match.')
        elif len(p1) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        else:
            user = User.objects.get(email=email)
            user.set_password(p1)
            user.save()
            
            # Clear reset session completely 
            request.session.flush()
            messages.success(request, 'Password changed successfully! Log in now. 🎉')
            return redirect('login')

    return render(request, 'routing/reset_password.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip() or request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Try to find if a user exists with this email address
        try:
            if '@' in identifier:
                user_obj = User.objects.get(email=identifier)
                # Swap the email string for their actual database username
                identifier = user_obj.username
        except User.DoesNotExist:
            # If email isn't found, keep going; authenticate() will catch the error safely below
            pass

        # Authenticate using the structural database username
        user = authenticate(request, username=identifier, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}! 👋')
            return redirect(request.GET.get('next', '/dashboard/'))
        
        messages.error(request, 'Invalid username or password.')
        
    return render(request, 'routing/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        u, e = request.POST.get('username','').strip(), request.POST.get('email','').strip()
        fn   = request.POST.get('first_name','').strip()
        p1, p2 = request.POST.get('password1',''), request.POST.get('password2','')
        if not u:
            messages.error(request, 'Username is required.')
        elif p1 != p2:
            messages.error(request, 'Passwords do not match.')
        elif len(p1) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif User.objects.filter(username=u).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=u, email=e, password=p1,
                                            first_name=fn)
            UserPreference.objects.create(user=user)
            login(request, user)
            _send_welcome(user)
            messages.success(request, f'Account created! Welcome, {fn or u}! 🎉')
            return redirect('dashboard')
    return render(request, 'routing/register.html')

@require_POST
def send_signup_otp(request):

    username = request.POST.get("username","").strip()

    email = request.POST.get("email","").strip().lower()

    if not username:

        return JsonResponse({
            "success":False,
            "message":"Username is required."
        })

    if not email:

        return JsonResponse({
            "success":False,
            "message":"Email is required."
        })

    if User.objects.filter(username=username).exists():

        return JsonResponse({
            "success":False,
            "message":"Username already exists."
        })

    if User.objects.filter(email=email).exists():

        return JsonResponse({
            "success":False,
            "message":"Email already registered."
        })

    otp_record = UserOTP.generate_signup(email)

    try:

        send_signup_email(
            email,
            otp_record.otp_code
        )

    except Exception as e:

        return JsonResponse({
            "success":False,
            "message":"Unable to send email."
        })

    request.session["signup_username"] = username

    request.session["signup_email"] = email

    return JsonResponse({

        "success":True,

        "message":"OTP sent successfully."

    })

@require_POST
def verify_signup_otp(request):

    email = request.session.get("signup_email")

    if not email:
        return JsonResponse({
            "success": False,
            "message": "Registration session expired."
        })

    otp = request.POST.get("otp", "").strip()

    if not otp:
        return JsonResponse({
            "success": False,
            "message": "Enter OTP."
        })

    try:

        otp_record = UserOTP.objects.filter(
            email=email,
            purpose="signup",
            otp_code=otp
        ).latest("created_at")

    except UserOTP.DoesNotExist:

        return JsonResponse({
            "success": False,
            "message": "Invalid OTP."
        })

    if not otp_record.is_valid():

        return JsonResponse({
            "success": False,
            "message": "OTP expired."
        })

    otp_record.is_verified = True
    otp_record.save()

    request.session["signup_verified"] = True

    return JsonResponse({

        "success": True,

        "message": "Email verified."

    })

@require_POST
def create_signup_account(request):

    if not request.session.get("signup_verified"):

        return JsonResponse({
            "success": False,
            "message": "Verify your email first."
        })

    username = request.session.get("signup_username")
    email = request.session.get("signup_email")

    first_name = request.POST.get(
        "first_name",
        ""
    ).strip()

    password1 = request.POST.get(
        "password1",
        ""
    )

    password2 = request.POST.get(
        "password2",
        ""
    )

    if first_name == "":
        return JsonResponse({
            "success": False,
            "message": "Enter your name."
        })

    if password1 != password2:
        return JsonResponse({
            "success": False,
            "message": "Passwords do not match."
        })

    if len(password1) < 6:
        return JsonResponse({
            "success": False,
            "message": "Password must be at least 6 characters."
        })

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "success": False,
            "message": "Username already exists."
        })

    if User.objects.filter(email=email).exists():
        return JsonResponse({
            "success": False,
            "message": "Email already exists."
        })

    user = User.objects.create_user(

        username=username,

        email=email,

        first_name=first_name,

        password=password1

    )

    UserPreference.objects.create(user=user)

    login(request, user)

    _send_welcome(user)

    UserOTP.objects.filter(
        email=email,
        purpose="signup"
    ).delete()

    request.session.pop("signup_username", None)
    request.session.pop("signup_email", None)
    request.session.pop("signup_verified", None)

    return JsonResponse({

        "success": True,

        "redirect": "/dashboard/"

    })
def logout_view(request):
    logout(request)
    return redirect('landing')


def about_view(request):   return render(request, 'routing/about.html')
def docs_view(request):    return render(request, 'routing/docs.html')
def help_view(request):    return render(request, 'routing/help.html')
def team_view(request):    return render(request, 'routing/team.html')


def share_view(request, token):
    route = get_object_or_404(RouteLog, share_token=token)
    return render(request, 'routing/share.html', {'route': route})


# ── Protected pages ───────────────────────────────────────────────────────────
@login_required
def warmup_graph(request):

    gm = GraphManager.get_instance()

    if not gm.is_loaded():

        from django.conf import settings

        gm.load_districts(settings.GRAPH_DISTRICTS)

    return JsonResponse({
        "status":"loading"
    })

@login_required
def dashboard(request):
    qs       = RouteLog.objects.filter(user=request.user)
    total    = qs.count()
    total_km = round(sum(r.path_distance_km for r in qs), 2)
    avg_km   = round(total_km / total, 2) if total else 0
    saved    = SavedRoute.objects.filter(user=request.user).count()
    gm       = GraphManager.get_instance()
    return render(request, 'routing/dashboard.html', {
        'total_routes': total, 'total_km': total_km,
        'avg_km': avg_km, 'saved_count': saved,
        'recent_routes': qs[:6],
        'graph_info': gm.get_info(),
    })


@login_required
def map_view(request):
    pref = _get_pref(request.user)
    return render(request, 'routing/map.html', {'mode': pref.speed_mode})


@login_required
def history_view(request):
    routes = RouteLog.objects.filter(user=request.user)
    return render(request, 'routing/history.html', {'routes': routes})


@login_required
def analytics_view(request):
    return render(request, 'routing/analytics.html')


@login_required
def algorithm_view(request):
    return render(request, 'routing/algorithm.html')


@login_required
def graph_explorer(request):
    return render(request, 'routing/graph_explorer.html',
                  {'graph_info': GraphManager.get_instance().get_info()})


@login_required
def compare_view(request):
    return render(request, 'routing/compare.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        u = request.user
        u.email      = request.POST.get('email',      u.email)
        u.first_name = request.POST.get('first_name', u.first_name)
        u.last_name  = request.POST.get('last_name',  u.last_name)
        u.save()
        messages.success(request, 'Profile updated.')
    total = RouteLog.objects.filter(user=request.user).count()
    return render(request, 'routing/profile.html', {'total_routes': total})


@login_required
def settings_view(request):
    pref = _get_pref(request.user)
    if request.method == 'POST':
        pref.theme      = request.POST.get('theme', pref.theme)
        pref.speed_mode = request.POST.get('speed_mode', pref.speed_mode)
        pref.save()
        messages.success(request, 'Settings saved.')
    return render(request, 'routing/settings.html', {'pref': pref})


@login_required
def benchmark_view(request):
    return render(request, 'routing/benchmark.html')


@login_required
def nodes_view(request):
    return render(request, 'routing/nodes.html',
                  {'graph_info': GraphManager.get_instance().get_info()})


@login_required
def simulation_view(request):
    return render(request, 'routing/simulation.html')


@login_required
def report_view(request):
    qs       = RouteLog.objects.filter(user=request.user)
    total    = qs.count()
    total_km = round(sum(r.path_distance_km for r in qs), 2)
    avg_km   = round(total_km / total, 2) if total else 0
    max_r    = qs.order_by('-path_distance_km').first()
    return render(request, 'routing/report.html', {
        'total': total, 'total_km': total_km,
        'avg_km': avg_km, 'max_route': max_r,
        'routes': qs[:20],
    })


@login_required
def export_view(request):
    fmt    = request.GET.get('format', '')
    routes = RouteLog.objects.filter(user=request.user)
    if fmt == 'csv':
        resp = HttpResponse(content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename="routes.csv"'
        w2 = csv.writer(resp)
        w2.writerow(['ID','From','To','Distance (km)','Nodes','Date'])
        for r in routes:
            w2.writerow([r.id, r.src_name or f'{r.src_lat:.4f},{r.src_lon:.4f}',
                         r.dst_name or f'{r.dst_lat:.4f},{r.dst_lon:.4f}',
                         r.path_distance_km, r.node_count, r.computed_at])
        return resp
    if fmt == 'json':
        data = list(routes.values())
        resp = HttpResponse(json.dumps(data, default=str), content_type='application/json')
        resp['Content-Disposition'] = 'attachment; filename="routes.json"'
        return resp
    return render(request, 'routing/export.html', {'routes': routes})


# ── Surprise Feature Views ────────────────────────────────────────────────────
@login_required
def favorites_view(request):
    saved = SavedRoute.objects.filter(user=request.user).select_related('route_log')
    return render(request, 'routing/favorites.html', {'saved': saved})


@login_required
def eta_view(request):
    return render(request, 'routing/eta.html')


@login_required
def heatmap_view(request):
    return render(request, 'routing/heatmap.html')


@login_required
def leaderboard_view(request):
    return render(request, 'routing/leaderboard.html')


@login_required
def replay_view(request, pk):
    route = get_object_or_404(RouteLog, pk=pk, user=request.user)
    return render(request, 'routing/replay.html', {'route': route})


# ── REST API ──────────────────────────────────────────────────────────────────
class RouteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = RouteRequestSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'status': 'error', 'errors': ser.errors}, status=400)
            
        gm = GraphManager.get_instance()
        
        # Serverless Container Lazy Load Check
        if not gm.is_loaded():
            try:
                from django.conf import settings
                gm.load_districts(settings.GRAPH_DISTRICTS)
            except Exception as e:
                return Response({
                    'status': 'error', 
                    'message': f'Server failed to load maps from disk: {str(e)}'
                }, status=500)
                
        if not gm.is_loaded():
            return Response({
                'status': 'error',
                'message': 'Graph asset data could not be allocated in container memory.'
            }, status=503)
            
        d = ser.validated_data
        try:
            sn = gm.get_nearest_node(d['src_lat'], d['src_lon'])
            dn = gm.get_nearest_node(d['dst_lat'], d['dst_lon'])
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)
            
        if sn == dn:
            return Response({'status': 'error', 'message': 'Source and destination are too close.'}, status=400)
                             
        engine = RouteEngine()
        try:
            # 1. Generate multi-modal response payload
            all_modes_data = engine.compute_all_routes(sn, dn)
        except (ValueError, RuntimeError) as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)
            
        # Verify that at least one drivable path exists
        if all_modes_data['car'] is None and all_modes_data['walk'] is None:
            return Response({'status': 'error', 'message': 'No traversable path found.'}, status=404)
                             
        # 2. Persist a primary entry in database history records using Car stats as standard
        primary_mode = all_modes_data['car'] or all_modes_data['walk']
        path_json = json.dumps(primary_mode['path_coords'])
        
        log = RouteLog.objects.create(
            user=request.user,
            src_name=d.get('src_name',''), dst_name=d.get('dst_name',''),
            src_lat=d['src_lat'],  src_lon=d['src_lon'],
            dst_lat=d['dst_lat'],  dst_lon=d['dst_lon'],
            src_node=sn, dst_node=dn,
            path_distance_m=primary_mode['total_distance_meters'],
            path_distance_km=primary_mode['total_distance_km'],
            node_count=primary_mode['node_count'],
            path_coords=path_json
        )
        
        # 3. Append relational details and respond
        return Response({
            'status': 'success',
            'route_id': log.id,
            'share_token': str(log.share_token),
            'routes': all_modes_data  # Contains data for 'walk', 'bike', and 'car'
        })


class GraphInfoAPIView(APIView):
    def get(self, request):
        return Response(GraphManager.get_instance().get_info())


class HealthAPIView(APIView):
    def get(self, request):
        gm = GraphManager.get_instance()
        if not gm.is_loaded():
            from django.conf import settings
            try:
                gm.load_districts(settings.GRAPH_DISTRICTS)
            except Exception:
                pass
        return Response({
            'status': 'ready' if gm.is_loaded() else 'loading',
            'graph':  gm.get_info(),
        })


class HistoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logs = RouteLog.objects.filter(user=request.user)[:20]
        return Response(RouteLogSerializer(logs, many=True).data)


class AnalyticsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.db.models import Avg, Count, Sum
        from datetime import date, timedelta
        routes = RouteLog.objects.filter(user=request.user)
        stats  = routes.aggregate(
            total=Count('id'), avg_dist=Avg('path_distance_km'),
            total_dist=Sum('path_distance_km'), avg_nodes=Avg('node_count'),
        )
        today = date.today()
        daily = []
        for i in range(13, -1, -1):
            dd  = today - timedelta(days=i)
            cnt = routes.filter(computed_at__date=dd).count()
            daily.append({'date': str(dd), 'count': cnt})
        return Response({'stats': stats, 'daily': daily})


class SaveRouteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        route_id = request.data.get('route_id')
        label    = request.data.get('label', 'My Route')
        try:
            log = RouteLog.objects.get(pk=route_id, user=request.user)
        except RouteLog.DoesNotExist:
            return Response({'status': 'error', 'message': 'Route not found'}, status=404)
        sr = SavedRoute.objects.create(user=request.user, route_log=log, label=label)
        return Response({'status': 'ok', 'saved_id': sr.id})


class SavedRoutesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        saved = SavedRoute.objects.filter(user=request.user).select_related('route_log')[:30]
        return Response(SavedRouteSerializer(saved, many=True).data)


class DeleteSavedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        SavedRoute.objects.filter(pk=pk, user=request.user).delete()
        return Response({'status': 'ok'})


class HeatmapDataAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.db.models import Count
        logs = RouteLog.objects.all()[:500]
        pts  = [[r.src_lat, r.src_lon, 0.5] for r in logs] +                [[r.dst_lat, r.dst_lon, 0.5] for r in logs]
        return Response({'points': pts})


class LeaderboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.db.models import Sum, Count
        users = (RouteLog.objects
                 .values('user__username')
                 .annotate(total_km=Sum('path_distance_km'), routes=Count('id'))
                 .order_by('-total_km')[:10])
        return Response({'leaderboard': list(users)})


class SetThemeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pref = _get_pref(request.user)
        pref.theme = request.data.get('theme', pref.theme)
        pref.save()
        return Response({'status': 'ok', 'theme': pref.theme})
