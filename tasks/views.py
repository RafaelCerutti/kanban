from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Board, Status, Card
from .serializers import BoardSerializer, StatusSerializer, CardSerializer

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def create_board(request, board_name = None):
    if request.method == 'GET':
        if board_name:
            board = Board.objects.filter(owner=request.user, title__iexact=board_name).first()
            if not board:
                return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = BoardSerializer(board)
            return Response(serializer.data)
        boards =  Board.objects.filter(owner=request.user)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BoardSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(owner = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def board_detail(request, board_name):
    board = Board.objects.filter(title__iexact=board_name, owner=request.user).first()
    if not board:
        return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        statuses = Status.objects.filter(board=board)
        status_with_cards = []
        for status_item in statuses:
            cards = Card.objects.filter(status=status_item)
            card_serializer = CardSerializer(cards, many=True)
            status_with_cards.append({'status':StatusSerializer(status_item).data, 'cards':card_serializer.data})
        return Response({'Board':BoardSerializer(board).data,'Status': status_with_cards})
        
    elif request.method == 'PUT':
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        board.delete()
        return Response({'message':'Board deleted successfully'},status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def status_manager(request, board_name=None, status_name=None):
    try:
        board = Board.objects.get(title=board_name, owner=request.user)
    except Board.DoesNotExist:
        return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        statuses = Status.objects.filter(board=board)
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.validated_data['board']
            if board.owner != request.user:
                return Response({'error': 'Invalid board'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            statuses = Status.objects.get(board=board,title__iexact=status_name)
        except Status.DoesNotExist:
            return Response({'error':'Status not found'},status=status.HTTP_404_NOT_FOUND)
        statuses.delete()
        return Response({'message':'Status deleted successfully'},status=status.HTTP_204_NO_CONTENT)



    
@api_view(['GET','POST','PUT','PATCH','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def card_manager(request,board_name=None,card_name=None):
    try:
        board = Board.objects.get(title=board_name, owner=request.user)
    except Board.DoesNotExist:
        return Response({'error':'Board not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        if card_name:
            card = Card.objects.filter (board=board, title__iexact=card_name).first()
            if not card:
                return Response("card not found", status=status.HTTP_404_NOT_FOUND)
            serializer = CardSerializer(card)
            return Response(serializer.data)
        cards = Card.objects.filter(board=board)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        if card_name:
            data['title'] = card_name
        serializer = CardSerializer(data=data)
        if serializer.is_valid():
            status_title = serializer.validated_data['status'].title
            board_title = serializer.validated_data['board'].title
            if not Status.objects.filter(title=status_title, board__owner=request.user).exists():
                return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
            if not Board.objects.filter(title=board_title, owner=request.user).exists():
                return Response({'error': 'Invalid board'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        if card_name:
            card = Card.objects.filter(board__owner=request.user, title__iexact=card_name).first()
            if not card:
                return Response("card not found", status=status.HTTP_404_NOT_FOUND)
            serializer = CardSerializer(card, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            card = Card.objects.get(title__iexact=card_name, board__owner=request.user)
        except Card.DoesNotExist:
            return Response({'error': 'Card not found'},status=status.HTTP_404_NOT_FOUND) 
        serializer = CardSerializer(card,data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        card = Card.objects.filter (board__owner=request.user, title__iexact=card_name).first()
        card.delete()
        return Response({'message':'Card deleted successfully'},status=status.HTTP_204_NO_CONTENT)