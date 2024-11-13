import graphene
from graphene_django import DjangoObjectType
from django.db.models import QuerySet
import base64
from typing import Type, Optional, Any

class PageInfo(graphene.ObjectType):
    has_next_page = graphene.Boolean(required=True)
    has_previous_page = graphene.Boolean(required=True)
    start_cursor = graphene.String()
    end_cursor = graphene.String()

def create_connection(node_type: Type[DjangoObjectType]) -> Type[graphene.ObjectType]:
    """
    Creates a Connection type for any node type.
    """
    class Edge(graphene.ObjectType):
        cursor = graphene.String(required=True)
        node = graphene.Field(node_type, required=True)

    class Connection(graphene.ObjectType):
        page_info = graphene.Field(PageInfo, required=True)
        edges = graphene.List(Edge)
        total_count = graphene.Int()

    return Connection

def paginate_queryset(
    queryset: QuerySet,
    ordering_field: str = 'id',
    first: Optional[int] = None,
    after: Optional[str] = None,
    last: Optional[int] = None,
    before: Optional[str] = None
) -> dict:
    """
    Generic pagination function that works with any queryset.
    """
    # Ensure queryset is ordered
    queryset = queryset.order_by(ordering_field)
    
    # Get total count before slicing
    total_count = queryset.count()

    # Handle cursor-based pagination
    if after:
        cursor_value = from_base64(after)
        queryset = queryset.filter(**{f"{ordering_field}__gt": cursor_value})
    if before:
        cursor_value = from_base64(before)
        queryset = queryset.filter(**{f"{ordering_field}__lt": cursor_value})

    # Handle limits
    if first:
        queryset = queryset[:first]
    elif last:
        queryset = queryset[max(0, queryset.count() - last):]

    # Create edges
    edges = []
    for item in queryset:
        cursor = to_base64(getattr(item, ordering_field))
        edges.append({
            "cursor": cursor,
            "node": item
        })

    # Get start and end cursors
    start_cursor = edges[0]["cursor"] if edges else None
    end_cursor = edges[-1]["cursor"] if edges else None

    # Calculate has_next/has_previous
    has_next = has_previous = False
    
    if edges:
        has_next = queryset.model.objects.filter(
            **{f"{ordering_field}__gt": from_base64(end_cursor)}
        ).exists()
        has_previous = queryset.model.objects.filter(
            **{f"{ordering_field}__lt": from_base64(start_cursor)}
        ).exists()

    return {
        "edges": edges,
        "page_info": {
            "has_next_page": has_next,
            "has_previous_page": has_previous,
            "start_cursor": start_cursor,
            "end_cursor": end_cursor
        },
        "total_count": total_count
    }

def to_base64(value: Any) -> str:
    """Convert any value to base64 cursor."""
    return base64.b64encode(str(value).encode()).decode()

def from_base64(cursor: str) -> Any:
    """Convert base64 cursor back to original value."""
    return base64.b64decode(cursor.encode()).decode()