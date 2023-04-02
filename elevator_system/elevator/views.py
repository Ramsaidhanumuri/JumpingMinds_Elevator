from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Elevator, Request
from .serializers import ElevatorSerializer, RequestSerializer

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    # To validate the floors
    def perform_create(self, serializer):
        current_floor = self.request.data['current_floor']
        top_target_floor = self.request.data['top_target_floor']
        ground_target_floor = self.request.data['ground_target_floor']
        
        if ground_target_floor <= current_floor <= top_target_floor:
            serializer.save()

        elif current_floor < ground_target_floor:
            raise serializers.ValidationError({'message': 'Current floor is less than ground floor'})
        
        else:
            raise serializers.ValidationError({'message': 'Current floor is greater than top floor'})

    # To move the elevator to up
    @action(detail=True, methods=['post'])
    def move_up(self, request, pk=None):
        elevator = self.get_object()

        if elevator.status == 'maintenance':
            return Response({'message': 'the elevator in maintenance'})

        if elevator.direction == 'down':
            return Response({'message': 'the elevator moves down'})
        
        if elevator.current_floor >= elevator.top_target_floor:
            elevator.status = 'idle'
            elevator.direction = 'None'
            elevator.save()

            return Response({'message': 'the elevator reached the top floor'})
        
        if elevator.status == 'idle' or elevator.direction == 'up':
            elevator.current_floor += 1
            elevator.direction = 'up'
            elevator.status = 'moving'
            elevator.save()

            return Response({'status': 'moved up'})
        
        return Response({'error': 'elevator not available'}, status=status.HTTP_400_BAD_REQUEST)

    # To move the elevator to down
    @action(detail=True, methods=['post'])
    def move_down(self, request, pk=None):
        elevator = self.get_object()

        if elevator.status == 'maintenance':
            return Response({'message': 'the elevator in maintenance'})
        
        if elevator.direction == 'up':
            return Response({'message': 'the elevator moves up'})
        
        if elevator.current_floor <= elevator.ground_target_floor:
            elevator.status = 'idle'
            elevator.direction = 'None'
            elevator.save()

            return Response({'message': 'the elevator reached the ground floor'})
        
        if elevator.status == 'idle' or elevator.direction == 'down':
            elevator.current_floor -= 1
            elevator.direction = 'down'
            elevator.status = 'moving'
            elevator.save()
            return Response({'status': 'moved down'})
        
        return Response({'error': 'elevator not available'}, status=status.HTTP_400_BAD_REQUEST)

    # To open the elevator door
    @action(detail=True, methods=['post'])
    def open_door(self, request, pk=None):
        elevator = self.get_object()

        if elevator.status == 'maintenance':
            return Response({'message': 'the elevator in maintenance'})
        
        if elevator.status != 'idle':
            return Response({'message': 'the elevator moving'})

        if elevator.status == 'idle':
            return Response({'status': 'door opened'})
        
        return Response({'error': 'elevator not available'}, status=status.HTTP_400_BAD_REQUEST)

    # To close the elevator door
    @action(detail=True, methods=['post'])
    def close_door(self, request, pk=None):
        elevator = self.get_object()

        if elevator.status == 'maintenance':
            return Response({'message': 'the elevator in maintenance'})
        
        if elevator.status != 'idle':
            return Response({'message': 'the elevator moving'})
        
        if elevator.status == 'idle':
            return Response({'status': 'door closed'})
        
        return Response({'error': 'elevator not available'}, status=status.HTTP_400_BAD_REQUEST)

    # To stop the elevator
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        elevator = self.get_object()

        if elevator.status == 'maintenance':
            return Response({'message': 'the elevator in maintenance'})

        if elevator.status == 'idle':
            return Response({'message': 'the elevator is idle'})
        
        if elevator.status == 'moving':
            elevator.status = 'idle'
            elevator.save()

            return Response({'status': 'stopped'})

        return Response({'error': 'elevator not moving'}, status=status.HTTP_400_BAD_REQUEST)
    
    # TO check the elevator next destination
    @action(detail=True, methods=['get'])
    def next_destination(self, request, pk=None):
        elevator = self.get_object()

        if elevator.status == 'maintenance':
            return Response({'message': 'the elevator in maintenance'})

        if elevator.direction == 'up' and elevator.current_floor < elevator.top_target_floor:
            next_floor = elevator.current_floor + 1

        elif elevator.current_floor == elevator.top_target_floor:
            next_floor = elevator.current_floor - 1

        if elevator.direction == 'down' and elevator.current_floor > elevator.ground_target_floor:
            next_floor = elevator.current_floor - 1

        elif elevator.current_floor == elevator.ground_target_floor:
            next_floor = elevator.current_floor + 1

        if next_floor is not None:
            return Response({'next_destination': next_floor})
        
        return Response({'error': 'No next destination'}, status=status.HTTP_400_BAD_REQUEST)
    
    # To mark the elevator as a maintenance
    @action(detail=True, methods=['post'])
    def make_maintenance(self, request, pk=None):
        elevator = self.get_object()
        if elevator.status == 'moving':
            return Response({'message': 'the elevator is currently moving, please stop and make it to maintenance.'})
        
        if elevator.status == 'idle':
            elevator.status = 'Maintenance'
            elevator.save()

            return Response({'status': 'Marked as Maintenance'})
        
        return Response({'error': 'elevator not available'}, status=status.HTTP_400_BAD_REQUEST)

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        floor = self.request.data['floor']
        elevator = self.assign_elevator(floor)
        if elevator:
            serializer.save(elevator=elevator)
        else:
            raise serializers.ValidationError("No available elevators")

    def assign_elevator(self, floor):
        idle_elevators = Elevator.objects.filter(status='idle')
        if idle_elevators:
            return idle_elevators.first()
        return None