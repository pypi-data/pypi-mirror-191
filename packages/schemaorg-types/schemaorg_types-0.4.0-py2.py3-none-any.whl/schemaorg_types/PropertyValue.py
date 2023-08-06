"""
A property-value pair, e.g. representing a feature of a product or place. Use the 'name' property for the name of the property. If there is an additional human-readable version of the value, put that into the 'description' property. Always use specific schema.org properties when a) they exist and b) you can populate them. Using PropertyValue as a substitute will typically not trigger the same effect as using the original, specific property.    

https://schema.org/PropertyValue
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class PropertyValue(BaseModel):
    """A property-value pair, e.g. representing a feature of a product or place. Use the 'name' property for the name of the property. If there is an additional human-readable version of the value, put that into the 'description' property. Always use specific schema.org properties when a) they exist and b) you can populate them. Using PropertyValue as a substitute will typically not trigger the same effect as using the original, specific property.

    References:
        https://schema.org/PropertyValue
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
        valueReference: (Union[List[Union[str, Any]], str, Any]): A secondary value that provides additional information on the original value, e.g. a reference temperature or a type of measurement.
        measurementTechnique: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A technique or technology used in a [[Dataset]] (or [[DataDownload]], [[DataCatalog]]),corresponding to the method used for measuring the corresponding variable(s) (described using [[variableMeasured]]). This is oriented towards scientific and scholarly dataset publication but may have broader applicability; it is not intended as a full representation of measurement, but rather as a high level summary for dataset discovery.For example, if [[variableMeasured]] is: molecule concentration, [[measurementTechnique]] could be: "mass spectrometry" or "nmr spectroscopy" or "colorimetry" or "immunofluorescence".If the [[variableMeasured]] is "depression rating", the [[measurementTechnique]] could be "Zung Scale" or "HAM-D" or "Beck Depression Inventory".If there are several [[variableMeasured]] properties recorded for some given data object, use a [[PropertyValue]] for each [[variableMeasured]] and attach the corresponding [[measurementTechnique]].
        unitCode: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): The unit of measurement given using the UN/CEFACT Common Code (3 characters) or a URL. Other codes than the UN/CEFACT Common Code may be used with a prefix followed by a colon.
        maxValue: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The upper value of some characteristic or property.
        unitText: (Union[List[Union[str, Any]], str, Any]): A string or text indicating the unit of measurement. Useful if you cannot provide a standard unit code for<a href='unitCode'>unitCode</a>.
        propertyID: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A commonly used identifier for the characteristic represented by the property, e.g. a manufacturer or a standard code for a property. propertyID can be(1) a prefixed string, mainly meant to be used with standards for product properties; (2) a site-specific, non-prefixed string (e.g. the primary key of the property or the vendor-specific ID of the property), or (3)a URL indicating the type of the property, either pointing to an external vocabulary, or a Web resource that describes the property (e.g. a glossary entry).Standards bodies should promote a standard prefix for the identifiers of properties from their standards.
        minValue: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The lower value of some characteristic or property.

    """

    type_: str = Field(default="PropertyValue", alias="@type", const=True)
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
    valueReference: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A secondary value that provides additional information on the original value, e.g."
        "a reference temperature or a type of measurement.",
    )
    measurementTechnique: Union[
        List[Union[str, AnyUrl, Any]], str, AnyUrl, Any
    ] = Field(
        default=None,
        description="A technique or technology used in a [[Dataset]] (or [[DataDownload]], [[DataCatalog]]),corresponding"
        "to the method used for measuring the corresponding variable(s) (described using [[variableMeasured]])."
        "This is oriented towards scientific and scholarly dataset publication but may have"
        "broader applicability; it is not intended as a full representation of measurement,"
        "but rather as a high level summary for dataset discovery.For example, if [[variableMeasured]]"
        'is: molecule concentration, [[measurementTechnique]] could be: "mass spectrometry"'
        'or "nmr spectroscopy" or "colorimetry" or "immunofluorescence".If the [[variableMeasured]]'
        'is "depression rating", the [[measurementTechnique]] could be "Zung Scale" or'
        '"HAM-D" or "Beck Depression Inventory".If there are several [[variableMeasured]]'
        "properties recorded for some given data object, use a [[PropertyValue]] for each [[variableMeasured]]"
        "and attach the corresponding [[measurementTechnique]].",
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
    propertyID: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="A commonly used identifier for the characteristic represented by the property, e.g."
        "a manufacturer or a standard code for a property. propertyID can be(1) a prefixed string,"
        "mainly meant to be used with standards for product properties; (2) a site-specific,"
        "non-prefixed string (e.g. the primary key of the property or the vendor-specific ID"
        "of the property), or (3)a URL indicating the type of the property, either pointing to"
        "an external vocabulary, or a Web resource that describes the property (e.g. a glossary"
        "entry).Standards bodies should promote a standard prefix for the identifiers of properties"
        "from their standards.",
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
