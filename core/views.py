import json
import requests as http_requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Room, Participant
from .forms import CreateRoomForm, JoinRoomForm


# ── MAIN PAGES ──────────────────────────────────────────────────────────────

def home(request):
    total_rooms = Room.objects.filter(is_active=True).count()
    total_participants = Participant.objects.filter(is_active=True).count()
    recent_rooms = Room.objects.filter(is_active=True).order_by('-created_at')[:6]
    return render(request, 'home.html', {
        'total_rooms': total_rooms,
        'total_participants': total_participants,
        'recent_rooms': recent_rooms,
    })


def create_room(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            Participant.objects.create(room=room, name=room.host_name)
            messages.success(request, f'Room "{room.name}" created successfully!')
            return redirect('room_detail', code=room.code)
    else:
        form = CreateRoomForm()
    return render(request, 'create_room.html', {'form': form})


def join_room(request):
    form = JoinRoomForm()
    if request.method == 'POST':
        form = JoinRoomForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].upper()
            name = form.cleaned_data['name']
            password = form.cleaned_data.get('password', '')
            try:
                room = Room.objects.get(code=code, is_active=True)
                if room.has_password and room.password != password:
                    messages.error(request, 'Incorrect room password.')
                    return render(request, 'join_room.html', {'form': form})
                Participant.objects.create(room=room, name=name)
                messages.success(request, f'Joined "{room.name}" successfully!')
                return redirect('room_detail', code=room.code)
            except Room.DoesNotExist:
                messages.error(request, 'Room not found. Please check the code.')
    return render(request, 'join_room.html', {'form': form})


def room_detail(request, code):
    room = get_object_or_404(Room, code=code, is_active=True)
    participants = room.participants.filter(is_active=True).order_by('joined_at')
    return render(request, 'room_detail.html', {'room': room, 'participants': participants})


def end_room(request, code):
    room = get_object_or_404(Room, code=code)
    if request.method == 'POST':
        room.is_active = False
        room.save()
        room.participants.update(is_active=False)
        messages.success(request, f'Room "{room.name}" has been ended.')
        return redirect('home')
    return render(request, 'end_room_confirm.html', {'room': room})


def about(request):
    return render(request, 'about.html')


# ── AI CHAT ──────────────────────────────────────────────────────────────────

def chat_page(request):
    """Dedicated full-page chat view."""
    return render(request, 'chat.html')


@require_POST
def chat_api(request):
    """AJAX endpoint — receives conversation history, returns AI reply."""
    try:
        body = json.loads(request.body)
        history = body.get('messages', [])          # [{role, content}, ...]
        user_message = body.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'Empty message.'}, status=400)

        api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
        model = getattr(settings, 'OPENROUTER_MODEL', 'deepseek/deepseek-v4-0724')

        system_prompt = (
            "You are Zoom AI — a friendly, smart assistant built into the Zoom meeting platform. "
            "You help users create and manage meeting rooms, answer questions about video calls, "
            "troubleshoot issues, and have helpful conversations. "
            "You can also answer general questions, help brainstorm ideas, explain topics, write content, "
            "and assist with anything the user needs. "
            "Keep responses clear, concise, and friendly. Use markdown formatting when helpful. "
            "When relevant, remind users they can create or join a Zoom room at any time."
        )

        # Build message list for the API
        api_messages = [{"role": "system", "content": system_prompt}]
        # Include prior conversation history (last 20 turns to stay within limits)
        for msg in history[-20:]:
            if msg.get('role') in ('user', 'assistant') and msg.get('content'):
                api_messages.append({"role": msg['role'], "content": msg['content']})
        api_messages.append({"role": "user", "content": user_message})

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://zoom-platform.app",
            "X-Title": "Zoom Platform",
        }

        payload = {
            "model": model,
            "messages": api_messages,
            "max_tokens": 1024,
            "temperature": 0.7,
        }

        response = http_requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        reply = data['choices'][0]['message']['content']
        return JsonResponse({'reply': reply})

    except http_requests.exceptions.Timeout:
        return JsonResponse({'error': 'AI took too long to respond. Please try again.'}, status=504)
    except http_requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Could not reach AI service: {str(e)}'}, status=502)
    except (KeyError, IndexError) as e:
        return JsonResponse({'error': 'Unexpected response from AI.'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
