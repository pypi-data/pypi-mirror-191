"""
A MerchantReturnPolicy provides information about product return policies associated with an [[Organization]], [[Product]], or [[Offer]].

https://schema.org/MerchantReturnPolicy
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class MerchantReturnPolicy(BaseModel):
    """A MerchantReturnPolicy provides information about product return policies associated with an [[Organization]], [[Product]], or [[Offer]].

    References:
        https://schema.org/MerchantReturnPolicy
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
        refundType: (Optional[Union[List[Union[str, Any]], str, Any]]): A refund type, from an enumerated list.
        customerRemorseReturnFees: (Optional[Union[List[Union[str, Any]], str, Any]]): The type of return fees if the product is returned due to customer remorse.
        additionalProperty: (Optional[Union[List[Union[str, Any]], str, Any]]): A property-value pair representing an additional characteristic of the entity, e.g. a product feature or another characteristic for which there is no matching property in schema.org.Note: Publishers should be aware that applications designed to use specific schema.org properties (e.g. https://schema.org/width, https://schema.org/color, https://schema.org/gtin13, ...) will typically expect such data to be provided using those properties, rather than using the generic property/value mechanism.
        itemDefectReturnLabelSource: (Optional[Union[List[Union[str, Any]], str, Any]]): The method (from an enumeration) by which the customer obtains a return shipping label for a defect product.
        inStoreReturnsOffered: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Are in-store returns offered? (For more advanced return methods use the [[returnMethod]] property.)
        itemCondition: (Optional[Union[List[Union[str, Any]], str, Any]]): A predefined value from OfferItemCondition specifying the condition of the product or service, or the products or services included in the offer. Also used for product return policies to specify the condition of products accepted for returns.
        restockingFee: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): Use [[MonetaryAmount]] to specify a fixed restocking fee for product returns, or use [[Number]] to specify a percentage of the product price paid by the customer.
        returnPolicyCategory: (Optional[Union[List[Union[str, Any]], str, Any]]): Specifies an applicable return policy (from an enumeration).
        returnLabelSource: (Optional[Union[List[Union[str, Any]], str, Any]]): The method (from an enumeration) by which the customer obtains a return shipping label for a product returned for any reason.
        applicableCountry: (Union[List[Union[str, Any]], str, Any]): A country where a particular merchant return policy applies to, for example the two-letter ISO 3166-1 alpha-2 country code.
        returnMethod: (Optional[Union[List[Union[str, Any]], str, Any]]): The type of return method offered, specified from an enumeration.
        returnShippingFeesAmount: (Optional[Union[List[Union[str, Any]], str, Any]]): Amount of shipping costs for product returns (for any reason). Applicable when property [[returnFees]] equals [[ReturnShippingFees]].
        itemDefectReturnShippingFeesAmount: (Optional[Union[List[Union[str, Any]], str, Any]]): Amount of shipping costs for defect product returns. Applicable when property [[itemDefectReturnFees]] equals [[ReturnShippingFees]].
        returnPolicySeasonalOverride: (Optional[Union[List[Union[str, Any]], str, Any]]): Seasonal override of a return policy.
        customerRemorseReturnShippingFeesAmount: (Optional[Union[List[Union[str, Any]], str, Any]]): The amount of shipping costs if a product is returned due to customer remorse. Applicable when property [[customerRemorseReturnFees]] equals [[ReturnShippingFees]].
        returnFees: (Optional[Union[List[Union[str, Any]], str, Any]]): The type of return fees for purchased products (for any return reason).
        customerRemorseReturnLabelSource: (Optional[Union[List[Union[str, Any]], str, Any]]): The method (from an enumeration) by which the customer obtains a return shipping label for a product returned due to customer remorse.
        merchantReturnLink: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Specifies a Web page or service by URL, for product returns.
        itemDefectReturnFees: (Optional[Union[List[Union[str, Any]], str, Any]]): The type of return fees for returns of defect products.
        merchantReturnDays: (Optional[Union[List[Union[datetime, date, int, str, Any]], datetime, date, int, str, Any]]): Specifies either a fixed return date or the number of days (from the delivery date) that a product can be returned. Used when the [[returnPolicyCategory]] property is specified as [[MerchantReturnFiniteReturnWindow]].
        returnPolicyCountry: (Union[List[Union[str, Any]], str, Any]): The country where the product has to be sent to for returns, for example "Ireland" using the [[name]] property of [[Country]]. You can also provide the two-letter [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1). Note that this can be different from the country where the product was originally shipped from or sent to.

    """

    type_: str = Field(default="MerchantReturnPolicy", alias="@type", const=True)
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
    refundType: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A refund type, from an enumerated list.",
    )
    customerRemorseReturnFees: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The type of return fees if the product is returned due to customer remorse.",
    )
    additionalProperty: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A property-value pair representing an additional characteristic of the entity, e.g."
        "a product feature or another characteristic for which there is no matching property"
        "in schema.org.Note: Publishers should be aware that applications designed to use specific"
        "schema.org properties (e.g. https://schema.org/width, https://schema.org/color,"
        "https://schema.org/gtin13, ...) will typically expect such data to be provided using"
        "those properties, rather than using the generic property/value mechanism.",
    )
    itemDefectReturnLabelSource: Optional[
        Union[List[Union[str, Any]], str, Any]
    ] = Field(
        default=None,
        description="The method (from an enumeration) by which the customer obtains a return shipping label"
        "for a defect product.",
    )
    inStoreReturnsOffered: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Are in-store returns offered? (For more advanced return methods use the [[returnMethod]]"
        "property.)",
    )
    itemCondition: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A predefined value from OfferItemCondition specifying the condition of the product"
        "or service, or the products or services included in the offer. Also used for product return"
        "policies to specify the condition of products accepted for returns.",
    )
    restockingFee: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="Use [[MonetaryAmount]] to specify a fixed restocking fee for product returns, or use"
        "[[Number]] to specify a percentage of the product price paid by the customer.",
    )
    returnPolicyCategory: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Specifies an applicable return policy (from an enumeration).",
    )
    returnLabelSource: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The method (from an enumeration) by which the customer obtains a return shipping label"
        "for a product returned for any reason.",
    )
    applicableCountry: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A country where a particular merchant return policy applies to, for example the two-letter"
        "ISO 3166-1 alpha-2 country code.",
    )
    returnMethod: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The type of return method offered, specified from an enumeration.",
    )
    returnShippingFeesAmount: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Amount of shipping costs for product returns (for any reason). Applicable when property"
        "[[returnFees]] equals [[ReturnShippingFees]].",
    )
    itemDefectReturnShippingFeesAmount: Optional[
        Union[List[Union[str, Any]], str, Any]
    ] = Field(
        default=None,
        description="Amount of shipping costs for defect product returns. Applicable when property [[itemDefectReturnFees]]"
        "equals [[ReturnShippingFees]].",
    )
    returnPolicySeasonalOverride: Optional[
        Union[List[Union[str, Any]], str, Any]
    ] = Field(
        default=None,
        description="Seasonal override of a return policy.",
    )
    customerRemorseReturnShippingFeesAmount: Optional[
        Union[List[Union[str, Any]], str, Any]
    ] = Field(
        default=None,
        description="The amount of shipping costs if a product is returned due to customer remorse. Applicable"
        "when property [[customerRemorseReturnFees]] equals [[ReturnShippingFees]].",
    )
    returnFees: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The type of return fees for purchased products (for any return reason).",
    )
    customerRemorseReturnLabelSource: Optional[
        Union[List[Union[str, Any]], str, Any]
    ] = Field(
        default=None,
        description="The method (from an enumeration) by which the customer obtains a return shipping label"
        "for a product returned due to customer remorse.",
    )
    merchantReturnLink: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="Specifies a Web page or service by URL, for product returns.",
    )
    itemDefectReturnFees: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The type of return fees for returns of defect products.",
    )
    merchantReturnDays: Optional[
        Union[List[Union[datetime, date, int, str, Any]], datetime, date, int, str, Any]
    ] = Field(
        default=None,
        description="Specifies either a fixed return date or the number of days (from the delivery date) that"
        "a product can be returned. Used when the [[returnPolicyCategory]] property is specified"
        "as [[MerchantReturnFiniteReturnWindow]].",
    )
    returnPolicyCountry: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description='The country where the product has to be sent to for returns, for example "Ireland" using'
        "the [[name]] property of [[Country]]. You can also provide the two-letter [ISO 3166-1"
        "alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1). Note that this"
        "can be different from the country where the product was originally shipped from or sent"
        "to.",
    )
