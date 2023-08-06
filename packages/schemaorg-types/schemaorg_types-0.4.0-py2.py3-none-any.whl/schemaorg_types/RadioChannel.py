"""
A unique instance of a radio BroadcastService on a CableOrSatelliteService lineup.

https://schema.org/RadioChannel
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class RadioChannel(BaseModel):
    """A unique instance of a radio BroadcastService on a CableOrSatelliteService lineup.

    References:
        https://schema.org/RadioChannel
    Note:
        Model Depth 4
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
        broadcastChannelId: (Union[List[Union[str, Any]], str, Any]): The unique address by which the BroadcastService can be identified in a provider lineup. In US, this is typically a number.
        providesBroadcastService: (Optional[Union[List[Union[str, Any]], str, Any]]): The BroadcastService offered on this channel.
        genre: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Genre of the creative work, broadcast channel or group.
        broadcastServiceTier: (Union[List[Union[str, Any]], str, Any]): The type of service required to have access to the channel (e.g. Standard or Premium).
        inBroadcastLineup: (Optional[Union[List[Union[str, Any]], str, Any]]): The CableOrSatelliteService offering the channel.
        broadcastFrequency: (Union[List[Union[str, Any]], str, Any]): The frequency used for over-the-air broadcasts. Numeric values or simple ranges, e.g. 87-99. In addition a shortcut idiom is supported for frequences of AM and FM radio channels, e.g. "87 FM".

    """

    type_: str = Field(default="RadioChannel", alias="@type", const=True)
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
    broadcastChannelId: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The unique address by which the BroadcastService can be identified in a provider lineup."
        "In US, this is typically a number.",
    )
    providesBroadcastService: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The BroadcastService offered on this channel.",
    )
    genre: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="Genre of the creative work, broadcast channel or group.",
    )
    broadcastServiceTier: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The type of service required to have access to the channel (e.g. Standard or Premium).",
    )
    inBroadcastLineup: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The CableOrSatelliteService offering the channel.",
    )
    broadcastFrequency: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The frequency used for over-the-air broadcasts. Numeric values or simple ranges, e.g."
        "87-99. In addition a shortcut idiom is supported for frequences of AM and FM radio channels,"
        'e.g. "87 FM".',
    )
