"""
A set of requirements that must be fulfilled in order to perform an Action.

https://schema.org/ActionAccessSpecification
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class ActionAccessSpecification(BaseModel):
    """A set of requirements that must be fulfilled in order to perform an Action.

    References:
        https://schema.org/ActionAccessSpecification
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
        availabilityEnds: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The end of the availability of the product or service included in the offer.
        expectsAcceptanceOf: (Optional[Union[List[Union[str, Any]], str, Any]]): An Offer which must be accepted before the user can perform the Action. For example, the user may need to buy a movie before being able to watch it.
        availabilityStarts: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The beginning of the availability of the product or service included in the offer.
        requiresSubscription: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Indicates if use of the media require a subscription  (either paid or free). Allowed values are ```true``` or ```false``` (note that an earlier version had 'yes', 'no').
        eligibleRegion: (Union[List[Union[str, Any]], str, Any]): The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for the geo-political region(s) for which the offer or delivery charge specification is valid.See also [[ineligibleRegion]].
        ineligibleRegion: (Union[List[Union[str, Any]], str, Any]): The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for the geo-political region(s) for which the offer or delivery charge specification is not valid, e.g. a region where the transaction is not allowed.See also [[eligibleRegion]].
        category: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A category for the item. Greater signs or slashes can be used to informally indicate a category hierarchy.

    """

    type_: str = Field(default="ActionAccessSpecification", alias="@type", const=True)
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
    availabilityEnds: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The end of the availability of the product or service included in the offer.",
    )
    expectsAcceptanceOf: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An Offer which must be accepted before the user can perform the Action. For example, the"
        "user may need to buy a movie before being able to watch it.",
    )
    availabilityStarts: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The beginning of the availability of the product or service included in the offer.",
    )
    requiresSubscription: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Indicates if use of the media require a subscription (either paid or free). Allowed values"
        "are ```true``` or ```false``` (note that an earlier version had 'yes', 'no').",
    )
    eligibleRegion: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for"
        "the geo-political region(s) for which the offer or delivery charge specification is"
        "valid.See also [[ineligibleRegion]].",
    )
    ineligibleRegion: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for"
        "the geo-political region(s) for which the offer or delivery charge specification is"
        "not valid, e.g. a region where the transaction is not allowed.See also [[eligibleRegion]].",
    )
    category: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="A category for the item. Greater signs or slashes can be used to informally indicate a"
        "category hierarchy.",
    )
