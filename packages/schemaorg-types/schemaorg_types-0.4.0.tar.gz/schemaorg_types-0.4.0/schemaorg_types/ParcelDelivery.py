"""
The delivery of a parcel either via the postal service or a commercial service.

https://schema.org/ParcelDelivery
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class ParcelDelivery(BaseModel):
    """The delivery of a parcel either via the postal service or a commercial service.

    References:
        https://schema.org/ParcelDelivery
    Note:
        Model Depth 3
    Attributes:
        potentialAction: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates a potential Action, which describes an idealized action in which this thing would play an 'object' role.
        mainEntityOfPage: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Indicates a page (or other CreativeWork) for which this thing is the main entity being described. See [background notes](/docs/datamodel.html#mainEntityBackground) for details.
        subjectOf: (Optional[Union[List[Union[str, Any]], str, Any]]): A CreativeWork or Event about this Thing.
        url: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): URL of the item.
        alternateName: (Union[List[Union[str, Any]], str, Any]): An alias for the item.
        sameAs: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): URL of a reference Web page that unambiguously indicates the item's identity. E.g. the URL of the item's Wikipedia page, Wikidata entry, or official website.
        description: (Union[List[Union[str, Any]], str, Any]): A description of the item.
        disambiguatingDescription: (Union[List[Union[str, Any]], str, Any]): A sub property of description. A short description of the item used to disambiguate from other, similar items. Information from other properties (in particular, name) may be necessary for the description to be useful for disambiguation.
        identifier: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): The identifier property represents any kind of identifier for any kind of [[Thing]], such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See [background notes](/docs/datamodel.html#identifierBg) for more details.
        image: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): An image of the item. This can be a [[URL]] or a fully described [[ImageObject]].
        name: (Union[List[Union[str, Any]], str, Any]): The name of the item.
        additionalType: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): An additional type for the item, typically used for adding more specific types from external vocabularies in microdata syntax. This is a relationship between something and a class that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the 'typeof' attribute - for multiple types. Schema.org tools may have only weaker understanding of extra types, in particular those defined externally.
        itemShipped: (Optional[Union[List[Union[str, Any]], str, Any]]): Item(s) being shipped.
        trackingNumber: (Union[List[Union[str, Any]], str, Any]): Shipper tracking number.
        expectedArrivalUntil: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The latest date the package may arrive.
        provider: (Optional[Union[List[Union[str, Any]], str, Any]]): The service provider, service operator, or service performer; the goods producer. Another party (a seller) may offer those services or goods on behalf of the provider. A provider may also serve as the seller.
        deliveryAddress: (Optional[Union[List[Union[str, Any]], str, Any]]): Destination address.
        expectedArrivalFrom: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The earliest date the package may arrive.
        carrier: (Optional[Union[List[Union[str, Any]], str, Any]]): 'carrier' is an out-dated term indicating the 'provider' for parcel delivery and flights.
        originAddress: (Optional[Union[List[Union[str, Any]], str, Any]]): Shipper's address.
        deliveryStatus: (Optional[Union[List[Union[str, Any]], str, Any]]): New entry added as the package passes through each leg of its journey (from shipment to final delivery).
        trackingUrl: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Tracking url for the parcel delivery.
        partOfOrder: (Optional[Union[List[Union[str, Any]], str, Any]]): The overall order the items in this delivery were included in.
        hasDeliveryMethod: (Optional[Union[List[Union[str, Any]], str, Any]]): Method used for delivery or shipping.

    """

    type_: str = Field(default="ParcelDelivery", alias="@type", const=True)
    potentialAction: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates a potential Action, which describes an idealized action in which this thing"
        "would play an 'object' role.",
    )
    mainEntityOfPage: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="Indicates a page (or other CreativeWork) for which this thing is the main entity being"
        "described. See [background notes](/docs/datamodel.html#mainEntityBackground)"
        "for details.",
    )
    subjectOf: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A CreativeWork or Event about this Thing.",
    )
    url: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="URL of the item.",
    )
    alternateName: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An alias for the item.",
    )
    sameAs: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="URL of a reference Web page that unambiguously indicates the item's identity. E.g. the"
        "URL of the item's Wikipedia page, Wikidata entry, or official website.",
    )
    description: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A description of the item.",
    )
    disambiguatingDescription: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A sub property of description. A short description of the item used to disambiguate from"
        "other, similar items. Information from other properties (in particular, name) may"
        "be necessary for the description to be useful for disambiguation.",
    )
    identifier: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="The identifier property represents any kind of identifier for any kind of [[Thing]],"
        "such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for"
        "representing many of these, either as textual strings or as URL (URI) links. See [background"
        "notes](/docs/datamodel.html#identifierBg) for more details.",
    )
    image: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="An image of the item. This can be a [[URL]] or a fully described [[ImageObject]].",
    )
    name: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The name of the item.",
    )
    additionalType: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="An additional type for the item, typically used for adding more specific types from external"
        "vocabularies in microdata syntax. This is a relationship between something and a class"
        "that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the 'typeof'"
        "attribute - for multiple types. Schema.org tools may have only weaker understanding"
        "of extra types, in particular those defined externally.",
    )
    itemShipped: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Item(s) being shipped.",
    )
    trackingNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Shipper tracking number.",
    )
    expectedArrivalUntil: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The latest date the package may arrive.",
    )
    provider: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The service provider, service operator, or service performer; the goods producer."
        "Another party (a seller) may offer those services or goods on behalf of the provider."
        "A provider may also serve as the seller.",
    )
    deliveryAddress: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Destination address.",
    )
    expectedArrivalFrom: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The earliest date the package may arrive.",
    )
    carrier: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="'carrier' is an out-dated term indicating the 'provider' for parcel delivery and flights.",
    )
    originAddress: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Shipper's address.",
    )
    deliveryStatus: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="New entry added as the package passes through each leg of its journey (from shipment to"
        "final delivery).",
    )
    trackingUrl: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="Tracking url for the parcel delivery.",
    )
    partOfOrder: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The overall order the items in this delivery were included in.",
    )
    hasDeliveryMethod: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Method used for delivery or shipping.",
    )
