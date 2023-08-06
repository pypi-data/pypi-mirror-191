"""
 A point value or interval for product characteristics and other purposes.

https://schema.org/QuantitativeValue
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class QuantitativeValue(BaseModel):
    """A point value or interval for product characteristics and other purposes.

    References:
        https://schema.org/QuantitativeValue
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
        value: (Union[List[Union[str, StrictBool, Any, StrictInt, StrictFloat]], str, StrictBool, Any, StrictInt, StrictFloat]): The value of the quantitative value or property value node.* For [[QuantitativeValue]] and [[MonetaryAmount]], the recommended type for values is 'Number'.* For [[PropertyValue]], it can be 'Text', 'Number', 'Boolean', or 'StructuredValue'.* Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similar Unicode symbols.* Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator.
        additionalProperty: (Optional[Union[List[Union[str, Any]], str, Any]]): A property-value pair representing an additional characteristic of the entity, e.g. a product feature or another characteristic for which there is no matching property in schema.org.Note: Publishers should be aware that applications designed to use specific schema.org properties (e.g. https://schema.org/width, https://schema.org/color, https://schema.org/gtin13, ...) will typically expect such data to be provided using those properties, rather than using the generic property/value mechanism.
        valueReference: (Union[List[Union[str, Any]], str, Any]): A secondary value that provides additional information on the original value, e.g. a reference temperature or a type of measurement.
        unitCode: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): The unit of measurement given using the UN/CEFACT Common Code (3 characters) or a URL. Other codes than the UN/CEFACT Common Code may be used with a prefix followed by a colon.
        maxValue: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The upper value of some characteristic or property.
        unitText: (Union[List[Union[str, Any]], str, Any]): A string or text indicating the unit of measurement. Useful if you cannot provide a standard unit code for<a href='unitCode'>unitCode</a>.
        minValue: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The lower value of some characteristic or property.

    """

    type_: str = Field(default="QuantitativeValue", alias="@type", const=True)
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
    value: Union[
        List[Union[str, StrictBool, Any, StrictInt, StrictFloat]],
        str,
        StrictBool,
        Any,
        StrictInt,
        StrictFloat,
    ] = Field(
        default=None,
        description="The value of the quantitative value or property value node.* For [[QuantitativeValue]]"
        "and [[MonetaryAmount]], the recommended type for values is 'Number'.* For [[PropertyValue]],"
        "it can be 'Text', 'Number', 'Boolean', or 'StructuredValue'.* Use values from 0123456789"
        "(Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially"
        "similar Unicode symbols.* Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to"
        "indicate a decimal point. Avoid using these symbols as a readability separator.",
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
    valueReference: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A secondary value that provides additional information on the original value, e.g."
        "a reference temperature or a type of measurement.",
    )
    unitCode: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="The unit of measurement given using the UN/CEFACT Common Code (3 characters) or a URL."
        "Other codes than the UN/CEFACT Common Code may be used with a prefix followed by a colon.",
    )
    maxValue: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The upper value of some characteristic or property.",
    )
    unitText: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A string or text indicating the unit of measurement. Useful if you cannot provide a standard"
        "unit code for<a href='unitCode'>unitCode</a>.",
    )
    minValue: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The lower value of some characteristic or property.",
    )
