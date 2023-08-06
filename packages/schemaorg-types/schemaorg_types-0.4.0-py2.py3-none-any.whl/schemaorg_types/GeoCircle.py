"""
A GeoCircle is a GeoShape representing a circular geographic area. As it is a GeoShape          it provides the simple textual property 'circle', but also allows the combination of postalCode alongside geoRadius.          The center of the circle can be indicated via the 'geoMidpoint' property, or more approximately using 'address', 'postalCode'.       

https://schema.org/GeoCircle
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class GeoCircle(BaseModel):
    """A GeoCircle is a GeoShape representing a circular geographic area. As it is a GeoShape          it provides the simple textual property 'circle', but also allows the combination of postalCode alongside geoRadius.          The center of the circle can be indicated via the 'geoMidpoint' property, or more approximately using 'address', 'postalCode'.

    References:
        https://schema.org/GeoCircle
    Note:
        Model Depth 5
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
        polygon: (Union[List[Union[str, Any]], str, Any]): A polygon is the area enclosed by a point-to-point path for which the starting and ending points are the same. A polygon is expressed as a series of four or more space delimited points where the first and final points are identical.
        circle: (Union[List[Union[str, Any]], str, Any]): A circle is the circular region of a specified radius centered at a specified latitude and longitude. A circle is expressed as a pair followed by a radius in meters.
        elevation: (Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]): The elevation of a location ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)). Values may be of the form 'NUMBER UNIT\_OF\_MEASUREMENT' (e.g., '1,000 m', '3,200 ft') while numbers alone should be assumed to be a value in meters.
        addressCountry: (Union[List[Union[str, Any]], str, Any]): The country. For example, USA. You can also provide the two-letter [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1).
        postalCode: (Union[List[Union[str, Any]], str, Any]): The postal code. For example, 94043.
        address: (Union[List[Union[str, Any]], str, Any]): Physical address of the item.
        line: (Union[List[Union[str, Any]], str, Any]): A line is a point-to-point path consisting of two or more points. A line is expressed as a series of two or more point objects separated by space.
        box: (Union[List[Union[str, Any]], str, Any]): A box is the area enclosed by the rectangle formed by two points. The first point is the lower corner, the second point is the upper corner. A box is expressed as two points separated by a space character.
        geoMidpoint: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates the GeoCoordinates at the centre of a GeoShape, e.g. GeoCircle.
        geoRadius: (Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]): Indicates the approximate radius of a GeoCircle (metres unless indicated otherwise via Distance notation).

    """

    type_: str = Field(default="GeoCircle", alias="@type", const=True)
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
    polygon: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A polygon is the area enclosed by a point-to-point path for which the starting and ending"
        "points are the same. A polygon is expressed as a series of four or more space delimited"
        "points where the first and final points are identical.",
    )
    circle: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A circle is the circular region of a specified radius centered at a specified latitude"
        "and longitude. A circle is expressed as a pair followed by a radius in meters.",
    )
    elevation: Union[
        List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat
    ] = Field(
        default=None,
        description="The elevation of a location ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System))."
        "Values may be of the form 'NUMBER UNIT\_OF\_MEASUREMENT' (e.g., '1,000 m', '3,200 ft')"
        "while numbers alone should be assumed to be a value in meters.",
    )
    addressCountry: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The country. For example, USA. You can also provide the two-letter [ISO 3166-1 alpha-2"
        "country code](http://en.wikipedia.org/wiki/ISO_3166-1).",
    )
    postalCode: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The postal code. For example, 94043.",
    )
    address: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Physical address of the item.",
    )
    line: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A line is a point-to-point path consisting of two or more points. A line is expressed as"
        "a series of two or more point objects separated by space.",
    )
    box: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A box is the area enclosed by the rectangle formed by two points. The first point is the"
        "lower corner, the second point is the upper corner. A box is expressed as two points separated"
        "by a space character.",
    )
    geoMidpoint: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates the GeoCoordinates at the centre of a GeoShape, e.g. GeoCircle.",
    )
    geoRadius: Union[
        List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat
    ] = Field(
        default=None,
        description="Indicates the approximate radius of a GeoCircle (metres unless indicated otherwise"
        "via Distance notation).",
    )
