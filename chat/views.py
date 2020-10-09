from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from intra import settings
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import json
# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

class ChatterBotAppView(APIView):
    permission_classes = [AllowAny]

    def initial(self, request, *args, **kwargs):
      self.chatterbot = ChatBot(**settings.CHATTERBOT)
      talk = [
          'Bienvenido a Super Salud', 'Quisera consulta', '¿Que deseas saber?', 'Mi estado', 'Introduzca su RUT'
      ]
      trainer = ListTrainer(self.chatterbot)
      trainer.train(talk)
      return super().initial(request, *args, **kwargs)

    def post(self, request, format=None):
        data = request.data

        if 'text' not in data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(data)
        response_data = response.serialize()

        return Response({"results": response_data["text"]}, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        return JsonResponse({
            'name': self.chatterbot.name
        })

