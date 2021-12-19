from typing import Dict
from rest_framework.serializers import Serializer

def get_serializer_by_action(action:str, serializers:Dict[str, type[Serializer]]):
    for current_action, serializer in serializers.items():
        if action == current_action:
            return serializer
