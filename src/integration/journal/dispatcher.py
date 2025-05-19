# система событийной подписки
from collections import defaultdict
from typing import Callable, Type, Dict, List, Any

class EventDispatcher:
    def __init__(self):
        self._subscribers: Dict[Type, List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event_type: Type, handler: Callable[[Any], None]):
        self._subscribers[event_type].append(handler)

    def dispatch(self, event: Any):
        for handler in self._subscribers[type(event)]:
            handler(event)
