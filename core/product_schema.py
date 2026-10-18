
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Product:
    product_id: str
    source: str
    name: str
    product_url: str

    category: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    image_urls: Optional[list[str]] = None
    features: Optional[list[str]] = None
    target_audience: Optional[str] = None

    affiliate_url: Optional[str] = None
    affiliate_eligible: bool = False
    image_rights_verified: bool = False
    availability_verified: bool = False

    research_score: Optional[float] = None
    research_notes: Optional[str] = None

    def to_dict(self):
        return asdict(self)
