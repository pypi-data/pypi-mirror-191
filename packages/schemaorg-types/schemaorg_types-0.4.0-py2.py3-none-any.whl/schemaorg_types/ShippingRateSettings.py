"""
A ShippingRateSettings represents re-usable pieces of shipping information. It is designed for publication on an URL that may be referenced via the [[shippingSettingsLink]] property of an [[OfferShippingDetails]]. Several occurrences can be published, distinguished and matched (i.e. identified/referenced) by their different values for [[shippingLabel]].

https://schema.org/ShippingRateSettings
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class ShippingRateSettings(BaseModel):
    """A ShippingRateSettings represents re-usable pieces of shipping information. It is designed for publication on an URL that may be referenced via the [[shippingSettingsLink]] property of an [[OfferShippingDetails]]. Several occurrences can be published, distinguished and matched (i.e. identified/referenced) by their different values for [[shippingLabel]].

    References:
        https://schema.org/ShippingRateSettings
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
        shippingDestination: (Optional[Union[List[Union[str, Any]], str, Any]]): indicates (possibly multiple) shipping destinations. These can be defined in several ways, e.g. postalCode ranges.
        shippingLabel: (Union[List[Union[str, Any]], str, Any]): Label to match an [[OfferShippingDetails]] with a [[ShippingRateSettings]] (within the context of a [[shippingSettingsLink]] cross-reference).
        doesNotShip: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Indicates when shipping to a particular [[shippingDestination]] is not available.
        freeShippingThreshold: (Optional[Union[List[Union[str, Any]], str, Any]]): A monetary value above (or at) which the shipping rate becomes free. Intended to be used via an [[OfferShippingDetails]] with [[shippingSettingsLink]] matching this [[ShippingRateSettings]].
        shippingRate: (Optional[Union[List[Union[str, Any]], str, Any]]): The shipping rate is the cost of shipping to the specified destination. Typically, the maxValue and currency values (of the [[MonetaryAmount]]) are most appropriate.
        isUnlabelledFallback: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): This can be marked 'true' to indicate that some published [[DeliveryTimeSettings]] or [[ShippingRateSettings]] are intended to apply to all [[OfferShippingDetails]] published by the same merchant, when referenced by a [[shippingSettingsLink]] in those settings. It is not meaningful to use a 'true' value for this property alongside a transitTimeLabel (for [[DeliveryTimeSettings]]) or shippingLabel (for [[ShippingRateSettings]]), since this property is for use with unlabelled settings.

    """

    type_: str = Field(default="ShippingRateSettings", alias="@type", const=True)
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
    shippingDestination: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="indicates (possibly multiple) shipping destinations. These can be defined in several"
        "ways, e.g. postalCode ranges.",
    )
    shippingLabel: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Label to match an [[OfferShippingDetails]] with a [[ShippingRateSettings]] (within"
        "the context of a [[shippingSettingsLink]] cross-reference).",
    )
    doesNotShip: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Indicates when shipping to a particular [[shippingDestination]] is not available.",
    )
    freeShippingThreshold: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A monetary value above (or at) which the shipping rate becomes free. Intended to be used"
        "via an [[OfferShippingDetails]] with [[shippingSettingsLink]] matching this [[ShippingRateSettings]].",
    )
    shippingRate: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The shipping rate is the cost of shipping to the specified destination. Typically, the"
        "maxValue and currency values (of the [[MonetaryAmount]]) are most appropriate.",
    )
    isUnlabelledFallback: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="This can be marked 'true' to indicate that some published [[DeliveryTimeSettings]]"
        "or [[ShippingRateSettings]] are intended to apply to all [[OfferShippingDetails]]"
        "published by the same merchant, when referenced by a [[shippingSettingsLink]] in those"
        "settings. It is not meaningful to use a 'true' value for this property alongside a transitTimeLabel"
        "(for [[DeliveryTimeSettings]]) or shippingLabel (for [[ShippingRateSettings]]),"
        "since this property is for use with unlabelled settings.",
    )
