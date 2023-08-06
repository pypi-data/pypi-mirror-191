"""
An [[OfferForPurchase]] in Schema.org represents an [[Offer]] to sell something, i.e. an [[Offer]] whose  [[businessFunction]] is [sell](http://purl.org/goodrelations/v1#Sell.). See [Good Relations](https://en.wikipedia.org/wiki/GoodRelations) for  background on the underlying concepts.  

https://schema.org/OfferForPurchase
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class OfferForPurchase(BaseModel):
    """An [[OfferForPurchase]] in Schema.org represents an [[Offer]] to sell something, i.e. an [[Offer]] whose  [[businessFunction]] is [sell](http://purl.org/goodrelations/v1#Sell.). See [Good Relations](https://en.wikipedia.org/wiki/GoodRelations) for  background on the underlying concepts.

    References:
        https://schema.org/OfferForPurchase
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
        hasMeasurement: (Optional[Union[List[Union[str, Any]], str, Any]]): A product measurement, for example the inseam of pants, the wheel size of a bicycle, or the gauge of a screw. Usually an exact measurement, but can also be a range of measurements for adjustable products, for example belts and ski bindings.
        eligibleQuantity: (Optional[Union[List[Union[str, Any]], str, Any]]): The interval and unit of measurement of ordering quantities for which the offer or price specification is valid. This allows e.g. specifying that a certain freight charge is valid only for a certain quantity.
        deliveryLeadTime: (Optional[Union[List[Union[str, Any]], str, Any]]): The typical delay between the receipt of the order and the goods either leaving the warehouse or being prepared for pickup, in case the delivery method is on site pickup.
        availabilityEnds: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The end of the availability of the product or service included in the offer.
        seller: (Optional[Union[List[Union[str, Any]], str, Any]]): An entity which offers (sells / leases / lends / loans) the services / goods.  A seller may also be a provider.
        availabilityStarts: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The beginning of the availability of the product or service included in the offer.
        areaServed: (Union[List[Union[str, Any]], str, Any]): The geographic area where a service or offered item is provided.
        advanceBookingRequirement: (Optional[Union[List[Union[str, Any]], str, Any]]): The amount of time that is required between accepting the offer and the actual usage of the resource or service.
        priceValidUntil: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The date after which the price is no longer available.
        gtin14: (Union[List[Union[str, Any]], str, Any]): The GTIN-14 code of the product, or the product to which the offer refers. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) for more details.
        reviews: (Optional[Union[List[Union[str, Any]], str, Any]]): Review of the item.
        warranty: (Optional[Union[List[Union[str, Any]], str, Any]]): The warranty promise(s) included in the offer.
        inventoryLevel: (Optional[Union[List[Union[str, Any]], str, Any]]): The current approximate inventory level for the item or items.
        eligibleDuration: (Optional[Union[List[Union[str, Any]], str, Any]]): The duration for which the given offer is valid.
        availability: (Optional[Union[List[Union[str, Any]], str, Any]]): The availability of this item&#x2014;for example In stock, Out of stock, Pre-order, etc.
        itemCondition: (Optional[Union[List[Union[str, Any]], str, Any]]): A predefined value from OfferItemCondition specifying the condition of the product or service, or the products or services included in the offer. Also used for product return policies to specify the condition of products accepted for returns.
        checkoutPageURLTemplate: (Union[List[Union[str, Any]], str, Any]): A URL template (RFC 6570) for a checkout page for an offer. This approach allows merchants to specify a URL for online checkout of the offered product, by interpolating parameters such as the logged in user ID, product ID, quantity, discount code etc. Parameter naming and standardization are not specified here.
        price: (Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]): The offer price of a product, or of a price component when attached to PriceSpecification and its subtypes.Usage guidelines:* Use the [[priceCurrency]] property (with standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system) (LETS) and other currency types, e.g. "Ithaca HOUR") instead of including [ambiguous symbols](http://en.wikipedia.org/wiki/Dollar_sign#Currencies_that_use_the_dollar_or_peso_sign) such as '$' in the value.* Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator.* Note that both [RDFa](http://www.w3.org/TR/xhtml-rdfa-primer/#using-the-content-attribute) and Microdata syntax allow the use of a "content=" attribute for publishing simple machine-readable values alongside more human-friendly formatting.* Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similar Unicode symbols.
        review: (Optional[Union[List[Union[str, Any]], str, Any]]): A review of the item.
        gtin: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A Global Trade Item Number ([GTIN](https://www.gs1.org/standards/id-keys/gtin)). GTINs identify trade items, including products and services, using numeric identification codes.The GS1 [digital link specifications](https://www.gs1.org/standards/Digital-Link/) express GTINs as URLs (URIs, IRIs, etc.). Details including regular expression examples can be found in, Section 6 of the GS1 URI Syntax specification; see also [schema.org tracking issue](https://github.com/schemaorg/schemaorg/issues/3156#issuecomment-1209522809) for schema.org-specific discussion. A correct [[gtin]] value should be a valid GTIN, which means that it should be an all-numeric string of either 8, 12, 13 or 14 digits, or a "GS1 Digital Link" URL based on such a string. The numeric component should also have a [valid GS1 check digit](https://www.gs1.org/services/check-digit-calculator) and meet the other rules for valid GTINs. See also [GS1's GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) and [Wikipedia](https://en.wikipedia.org/wiki/Global_Trade_Item_Number) for more details. Left-padding of the gtin values is not required or encouraged. The [[gtin]] property generalizes the earlier [[gtin8]], [[gtin12]], [[gtin13]], and [[gtin14]] properties.Note also that this is a definition for how to include GTINs in Schema.org data, and not a definition of GTINs in general - see the GS1 documentation for authoritative details.
        itemOffered: (Optional[Union[List[Union[str, Any]], str, Any]]): An item being offered (or demanded). The transactional nature of the offer or demand is documented using [[businessFunction]], e.g. sell, lease etc. While several common expected types are listed explicitly in this definition, others can be used. Using a second type, such as Product or a subtype of Product, can clarify the nature of the offer.
        mobileUrl: (Union[List[Union[str, Any]], str, Any]): The [[mobileUrl]] property is provided for specific situations in which data consumers need to determine whether one of several provided URLs is a dedicated 'mobile site'.To discourage over-use, and reflecting intial usecases, the property is expected only on [[Product]] and [[Offer]], rather than [[Thing]]. The general trend in web technology is towards [responsive design](https://en.wikipedia.org/wiki/Responsive_web_design) in which content can be flexibly adapted to a wide range of browsing environments. Pages and sites referenced with the long-established [[url]] property should ideally also be usable on a wide variety of devices, including mobile phones. In most cases, it would be pointless and counter productive to attempt to update all [[url]] markup to use [[mobileUrl]] for more mobile-oriented pages. The property is intended for the case when items (primarily [[Product]] and [[Offer]]) have extra URLs hosted on an additional "mobile site" alongside the main one. It should not be taken as an endorsement of this publication style.
        shippingDetails: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates information about the shipping policies and options associated with an [[Offer]].
        hasMerchantReturnPolicy: (Optional[Union[List[Union[str, Any]], str, Any]]): Specifies a MerchantReturnPolicy that may be applicable.
        businessFunction: (Optional[Union[List[Union[str, Any]], str, Any]]): The business function (e.g. sell, lease, repair, dispose) of the offer or component of a bundle (TypeAndQuantityNode). The default is http://purl.org/goodrelations/v1#Sell.
        isFamilyFriendly: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Indicates whether this content is family friendly.
        leaseLength: (Optional[Union[List[Union[str, Any]], str, Any]]): Length of the lease for some [[Accommodation]], either particular to some [[Offer]] or in some cases intrinsic to the property.
        gtin12: (Union[List[Union[str, Any]], str, Any]): The GTIN-12 code of the product, or the product to which the offer refers. The GTIN-12 is the 12-digit GS1 Identification Key composed of a U.P.C. Company Prefix, Item Reference, and Check Digit used to identify trade items. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) for more details.
        validThrough: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The date after when the item is not valid. For example the end of an offer, salary period, or a period of opening hours.
        hasAdultConsideration: (Optional[Union[List[Union[str, Any]], str, Any]]): Used to tag an item to be intended or suitable for consumption or use by adults only.
        includesObject: (Optional[Union[List[Union[str, Any]], str, Any]]): This links to a node or nodes indicating the exact quantity of the products included in  an [[Offer]] or [[ProductCollection]].
        eligibleRegion: (Union[List[Union[str, Any]], str, Any]): The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for the geo-political region(s) for which the offer or delivery charge specification is valid.See also [[ineligibleRegion]].
        asin: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): An Amazon Standard Identification Number (ASIN) is a 10-character alphanumeric unique identifier assigned by Amazon.com and its partners for product identification within the Amazon organization (summary from [Wikipedia](https://en.wikipedia.org/wiki/Amazon_Standard_Identification_Number)'s article).Note also that this is a definition for how to include ASINs in Schema.org data, and not a definition of ASINs in general - see documentation from Amazon for authoritative details.ASINs are most commonly encoded as text strings, but the [asin] property supports URL/URI as potential values too.
        gtin8: (Union[List[Union[str, Any]], str, Any]): The GTIN-8 code of the product, or the product to which the offer refers. This code is also known as EAN/UCC-8 or 8-digit EAN. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) for more details.
        ineligibleRegion: (Union[List[Union[str, Any]], str, Any]): The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for the geo-political region(s) for which the offer or delivery charge specification is not valid, e.g. a region where the transaction is not allowed.See also [[eligibleRegion]].
        priceSpecification: (Optional[Union[List[Union[str, Any]], str, Any]]): One or more detailed price specifications, indicating the unit price and delivery or payment charges.
        validFrom: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The date when the item becomes valid.
        eligibleTransactionVolume: (Optional[Union[List[Union[str, Any]], str, Any]]): The transaction volume, in a monetary unit, for which the offer or price specification is valid, e.g. for indicating a minimal purchasing volume, to express free shipping above a certain order volume, or to limit the acceptance of credit cards to purchases to a certain minimal amount.
        mpn: (Union[List[Union[str, Any]], str, Any]): The Manufacturer Part Number (MPN) of the product, or the product to which the offer refers.
        category: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A category for the item. Greater signs or slashes can be used to informally indicate a category hierarchy.
        aggregateRating: (Optional[Union[List[Union[str, Any]], str, Any]]): The overall rating, based on a collection of reviews or ratings, of the item.
        offeredBy: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to the organization or person making the offer.
        addOn: (Optional[Union[List[Union[str, Any]], str, Any]]): An additional offer that can only be obtained in combination with the first base offer (e.g. supplements and extensions that are available for a surcharge).
        availableAtOrFrom: (Optional[Union[List[Union[str, Any]], str, Any]]): The place(s) from which the offer can be obtained (e.g. store locations).
        priceCurrency: (Union[List[Union[str, Any]], str, Any]): The currency of the price, or a price component when attached to [[PriceSpecification]] and its subtypes.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system) (LETS) and other currency types, e.g. "Ithaca HOUR".
        eligibleCustomerType: (Optional[Union[List[Union[str, Any]], str, Any]]): The type(s) of customers for which the given offer is valid.
        gtin13: (Union[List[Union[str, Any]], str, Any]): The GTIN-13 code of the product, or the product to which the offer refers. This is equivalent to 13-digit ISBN codes and EAN UCC-13. Former 12-digit UPC codes can be converted into a GTIN-13 code by simply adding a preceding zero. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) for more details.
        serialNumber: (Union[List[Union[str, Any]], str, Any]): The serial number or any alphanumeric identifier of a particular product. When attached to an offer, it is a shortcut for the serial number of the product included in the offer.
        sku: (Union[List[Union[str, Any]], str, Any]): The Stock Keeping Unit (SKU), i.e. a merchant-specific identifier for a product or service, or the product to which the offer refers.
        acceptedPaymentMethod: (Optional[Union[List[Union[str, Any]], str, Any]]): The payment method(s) accepted by seller for this offer.
        availableDeliveryMethod: (Optional[Union[List[Union[str, Any]], str, Any]]): The delivery method(s) available for this offer.

    """

    type_: str = Field(default="OfferForPurchase", alias="@type", const=True)
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
    hasMeasurement: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A product measurement, for example the inseam of pants, the wheel size of a bicycle, or"
        "the gauge of a screw. Usually an exact measurement, but can also be a range of measurements"
        "for adjustable products, for example belts and ski bindings.",
    )
    eligibleQuantity: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The interval and unit of measurement of ordering quantities for which the offer or price"
        "specification is valid. This allows e.g. specifying that a certain freight charge is"
        "valid only for a certain quantity.",
    )
    deliveryLeadTime: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The typical delay between the receipt of the order and the goods either leaving the warehouse"
        "or being prepared for pickup, in case the delivery method is on site pickup.",
    )
    availabilityEnds: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The end of the availability of the product or service included in the offer.",
    )
    seller: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An entity which offers (sells / leases / lends / loans) the services / goods. A seller may"
        "also be a provider.",
    )
    availabilityStarts: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The beginning of the availability of the product or service included in the offer.",
    )
    areaServed: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The geographic area where a service or offered item is provided.",
    )
    advanceBookingRequirement: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The amount of time that is required between accepting the offer and the actual usage of"
        "the resource or service.",
    )
    priceValidUntil: Optional[
        Union[List[Union[str, Any, date]], str, Any, date]
    ] = Field(
        default=None,
        description="The date after which the price is no longer available.",
    )
    gtin14: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The GTIN-14 code of the product, or the product to which the offer refers. See [GS1 GTIN"
        "Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) for more details.",
    )
    reviews: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Review of the item.",
    )
    warranty: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The warranty promise(s) included in the offer.",
    )
    inventoryLevel: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The current approximate inventory level for the item or items.",
    )
    eligibleDuration: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The duration for which the given offer is valid.",
    )
    availability: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The availability of this item&#x2014;for example In stock, Out of stock, Pre-order,"
        "etc.",
    )
    itemCondition: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A predefined value from OfferItemCondition specifying the condition of the product"
        "or service, or the products or services included in the offer. Also used for product return"
        "policies to specify the condition of products accepted for returns.",
    )
    checkoutPageURLTemplate: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A URL template (RFC 6570) for a checkout page for an offer. This approach allows merchants"
        "to specify a URL for online checkout of the offered product, by interpolating parameters"
        "such as the logged in user ID, product ID, quantity, discount code etc. Parameter naming"
        "and standardization are not specified here.",
    )
    price: Union[
        List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat
    ] = Field(
        default=None,
        description="The offer price of a product, or of a price component when attached to PriceSpecification"
        "and its subtypes.Usage guidelines:* Use the [[priceCurrency]] property (with standard"
        "formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217),"
        'e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies)'
        'for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)'
        '(LETS) and other currency types, e.g. "Ithaca HOUR") instead of including [ambiguous'
        "symbols](http://en.wikipedia.org/wiki/Dollar_sign#Currencies_that_use_the_dollar_or_peso_sign)"
        "such as '$' in the value.* Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate"
        "a decimal point. Avoid using these symbols as a readability separator.* Note that both"
        "[RDFa](http://www.w3.org/TR/xhtml-rdfa-primer/#using-the-content-attribute)"
        'and Microdata syntax allow the use of a "content=" attribute for publishing simple'
        "machine-readable values alongside more human-friendly formatting.* Use values from"
        "0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially"
        "similar Unicode symbols.",
    )
    review: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A review of the item.",
    )
    gtin: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="A Global Trade Item Number ([GTIN](https://www.gs1.org/standards/id-keys/gtin))."
        "GTINs identify trade items, including products and services, using numeric identification"
        "codes.The GS1 [digital link specifications](https://www.gs1.org/standards/Digital-Link/)"
        "express GTINs as URLs (URIs, IRIs, etc.). Details including regular expression examples"
        "can be found in, Section 6 of the GS1 URI Syntax specification; see also [schema.org tracking"
        "issue](https://github.com/schemaorg/schemaorg/issues/3156#issuecomment-1209522809)"
        "for schema.org-specific discussion. A correct [[gtin]] value should be a valid GTIN,"
        "which means that it should be an all-numeric string of either 8, 12, 13 or 14 digits, or"
        'a "GS1 Digital Link" URL based on such a string. The numeric component should also have'
        "a [valid GS1 check digit](https://www.gs1.org/services/check-digit-calculator)"
        "and meet the other rules for valid GTINs. See also [GS1's GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin)"
        "and [Wikipedia](https://en.wikipedia.org/wiki/Global_Trade_Item_Number) for"
        "more details. Left-padding of the gtin values is not required or encouraged. The [[gtin]]"
        "property generalizes the earlier [[gtin8]], [[gtin12]], [[gtin13]], and [[gtin14]]"
        "properties.Note also that this is a definition for how to include GTINs in Schema.org"
        "data, and not a definition of GTINs in general - see the GS1 documentation for authoritative"
        "details.",
    )
    itemOffered: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An item being offered (or demanded). The transactional nature of the offer or demand"
        "is documented using [[businessFunction]], e.g. sell, lease etc. While several common"
        "expected types are listed explicitly in this definition, others can be used. Using a"
        "second type, such as Product or a subtype of Product, can clarify the nature of the offer.",
    )
    mobileUrl: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The [[mobileUrl]] property is provided for specific situations in which data consumers"
        "need to determine whether one of several provided URLs is a dedicated 'mobile site'.To"
        "discourage over-use, and reflecting intial usecases, the property is expected only"
        "on [[Product]] and [[Offer]], rather than [[Thing]]. The general trend in web technology"
        "is towards [responsive design](https://en.wikipedia.org/wiki/Responsive_web_design)"
        "in which content can be flexibly adapted to a wide range of browsing environments. Pages"
        "and sites referenced with the long-established [[url]] property should ideally also"
        "be usable on a wide variety of devices, including mobile phones. In most cases, it would"
        "be pointless and counter productive to attempt to update all [[url]] markup to use [[mobileUrl]]"
        "for more mobile-oriented pages. The property is intended for the case when items (primarily"
        '[[Product]] and [[Offer]]) have extra URLs hosted on an additional "mobile site"'
        "alongside the main one. It should not be taken as an endorsement of this publication style.",
    )
    shippingDetails: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates information about the shipping policies and options associated with an [[Offer]].",
    )
    hasMerchantReturnPolicy: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Specifies a MerchantReturnPolicy that may be applicable.",
    )
    businessFunction: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The business function (e.g. sell, lease, repair, dispose) of the offer or component"
        "of a bundle (TypeAndQuantityNode). The default is http://purl.org/goodrelations/v1#Sell.",
    )
    isFamilyFriendly: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Indicates whether this content is family friendly.",
    )
    leaseLength: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Length of the lease for some [[Accommodation]], either particular to some [[Offer]]"
        "or in some cases intrinsic to the property.",
    )
    gtin12: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The GTIN-12 code of the product, or the product to which the offer refers. The GTIN-12"
        "is the 12-digit GS1 Identification Key composed of a U.P.C. Company Prefix, Item Reference,"
        "and Check Digit used to identify trade items. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin)"
        "for more details.",
    )
    validThrough: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The date after when the item is not valid. For example the end of an offer, salary period,"
        "or a period of opening hours.",
    )
    hasAdultConsideration: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Used to tag an item to be intended or suitable for consumption or use by adults only.",
    )
    includesObject: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="This links to a node or nodes indicating the exact quantity of the products included in"
        "an [[Offer]] or [[ProductCollection]].",
    )
    eligibleRegion: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for"
        "the geo-political region(s) for which the offer or delivery charge specification is"
        "valid.See also [[ineligibleRegion]].",
    )
    asin: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="An Amazon Standard Identification Number (ASIN) is a 10-character alphanumeric unique"
        "identifier assigned by Amazon.com and its partners for product identification within"
        "the Amazon organization (summary from [Wikipedia](https://en.wikipedia.org/wiki/Amazon_Standard_Identification_Number)'s"
        "article).Note also that this is a definition for how to include ASINs in Schema.org data,"
        "and not a definition of ASINs in general - see documentation from Amazon for authoritative"
        "details.ASINs are most commonly encoded as text strings, but the [asin] property supports"
        "URL/URI as potential values too.",
    )
    gtin8: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The GTIN-8 code of the product, or the product to which the offer refers. This code is also"
        "known as EAN/UCC-8 or 8-digit EAN. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin)"
        "for more details.",
    )
    ineligibleRegion: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for"
        "the geo-political region(s) for which the offer or delivery charge specification is"
        "not valid, e.g. a region where the transaction is not allowed.See also [[eligibleRegion]].",
    )
    priceSpecification: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="One or more detailed price specifications, indicating the unit price and delivery or"
        "payment charges.",
    )
    validFrom: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The date when the item becomes valid.",
    )
    eligibleTransactionVolume: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The transaction volume, in a monetary unit, for which the offer or price specification"
        "is valid, e.g. for indicating a minimal purchasing volume, to express free shipping"
        "above a certain order volume, or to limit the acceptance of credit cards to purchases"
        "to a certain minimal amount.",
    )
    mpn: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The Manufacturer Part Number (MPN) of the product, or the product to which the offer refers.",
    )
    category: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="A category for the item. Greater signs or slashes can be used to informally indicate a"
        "category hierarchy.",
    )
    aggregateRating: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
    )
    offeredBy: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to the organization or person making the offer.",
    )
    addOn: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An additional offer that can only be obtained in combination with the first base offer"
        "(e.g. supplements and extensions that are available for a surcharge).",
    )
    availableAtOrFrom: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The place(s) from which the offer can be obtained (e.g. store locations).",
    )
    priceCurrency: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The currency of the price, or a price component when attached to [[PriceSpecification]]"
        "and its subtypes.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217),"
        'e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies)'
        'for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)'
        '(LETS) and other currency types, e.g. "Ithaca HOUR".',
    )
    eligibleCustomerType: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The type(s) of customers for which the given offer is valid.",
    )
    gtin13: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The GTIN-13 code of the product, or the product to which the offer refers. This is equivalent"
        "to 13-digit ISBN codes and EAN UCC-13. Former 12-digit UPC codes can be converted into"
        "a GTIN-13 code by simply adding a preceding zero. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin)"
        "for more details.",
    )
    serialNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The serial number or any alphanumeric identifier of a particular product. When attached"
        "to an offer, it is a shortcut for the serial number of the product included in the offer.",
    )
    sku: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The Stock Keeping Unit (SKU), i.e. a merchant-specific identifier for a product or service,"
        "or the product to which the offer refers.",
    )
    acceptedPaymentMethod: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The payment method(s) accepted by seller for this offer.",
    )
    availableDeliveryMethod: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The delivery method(s) available for this offer.",
    )
