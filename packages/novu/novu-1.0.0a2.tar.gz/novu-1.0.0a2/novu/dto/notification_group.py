"""This module is used to gather all DTO definitions related to the Notification Group resource in Novu"""
import dataclasses
from typing import Optional

from novu.dto.base import CamelCaseDto, DtoIterableDescriptor


@dataclasses.dataclass
class NotificationGroupDto(CamelCaseDto["NotificationGroupDto"]):
    """Definition of a notification group"""

    name: str

    _id: Optional[str] = None
    """Notification Group ID in Novu internal storage system"""

    _environment_id: Optional[str] = None
    """Environment ID in Novu internal storage system"""

    _organization_id: Optional[str] = None
    """Organization ID in Novu internal storage system"""

    _parent_id: Optional[str] = None
    """Parent ID in Novu internal storage system"""

    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclasses.dataclass
class PaginatedNotificationGroupDto(CamelCaseDto["PaginatedNotificationGroupDto"]):
    """Definition of paginated notification groups"""

    page: int = 0
    total_count: int = 0
    page_size: int = 0
    data: DtoIterableDescriptor[NotificationGroupDto] = DtoIterableDescriptor[NotificationGroupDto](
        default_factory=list, item_cls=NotificationGroupDto
    )
