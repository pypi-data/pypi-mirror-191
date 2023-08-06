"""
Information about the engine of the vehicle. A vehicle can have multiple engines represented by multiple engine specification entities.

https://schema.org/EngineSpecification
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class EngineSpecification(BaseModel):
    """Information about the engine of the vehicle. A vehicle can have multiple engines represented by multiple engine specification entities.

    References:
        https://schema.org/EngineSpecification
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
        enginePower: (Optional[Union[List[Union[str, Any]], str, Any]]): The power of the vehicle's engine.    Typical unit code(s): KWT for kilowatt, BHP for brake horsepower, N12 for metric horsepower (PS, with 1 PS = 735,49875 W)* Note 1: There are many different ways of measuring an engine's power. For an overview, see  [http://en.wikipedia.org/wiki/Horsepower#Engine\_power\_test\_codes](http://en.wikipedia.org/wiki/Horsepower#Engine_power_test_codes).* Note 2: You can link to information about how the given value has been determined using the [[valueReference]] property.* Note 3: You can use [[minValue]] and [[maxValue]] to indicate ranges.
        torque: (Optional[Union[List[Union[str, Any]], str, Any]]): The torque (turning force) of the vehicle's engine.Typical unit code(s): NU for newton metre (N m), F17 for pound-force per foot, or F48 for pound-force per inch* Note 1: You can link to information about how the given value has been determined (e.g. reference RPM) using the [[valueReference]] property.* Note 2: You can use [[minValue]] and [[maxValue]] to indicate ranges.
        engineType: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): The type of engine or engines powering the vehicle.
        fuelType: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): The type of fuel suitable for the engine or engines of the vehicle. If the vehicle has only one engine, this property can be attached directly to the vehicle.
        engineDisplacement: (Optional[Union[List[Union[str, Any]], str, Any]]): The volume swept by all of the pistons inside the cylinders of an internal combustion engine in a single movement. Typical unit code(s): CMQ for cubic centimeter, LTR for liters, INQ for cubic inches* Note 1: You can link to information about how the given value has been determined using the [[valueReference]] property.* Note 2: You can use [[minValue]] and [[maxValue]] to indicate ranges.

    """

    type_: str = Field(default="EngineSpecification", alias="@type", const=True)
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
    enginePower: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The power of the vehicle's engine. Typical unit code(s): KWT for kilowatt, BHP for brake"
        "horsepower, N12 for metric horsepower (PS, with 1 PS = 735,49875 W)* Note 1: There are"
        "many different ways of measuring an engine's power. For an overview, see [http://en.wikipedia.org/wiki/Horsepower#Engine\_power\_test\_codes](http://en.wikipedia.org/wiki/Horsepower#Engine_power_test_codes).*"
        "Note 2: You can link to information about how the given value has been determined using"
        "the [[valueReference]] property.* Note 3: You can use [[minValue]] and [[maxValue]]"
        "to indicate ranges.",
    )
    torque: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The torque (turning force) of the vehicle's engine.Typical unit code(s): NU for newton"
        "metre (N m), F17 for pound-force per foot, or F48 for pound-force per inch* Note 1: You"
        "can link to information about how the given value has been determined (e.g. reference"
        "RPM) using the [[valueReference]] property.* Note 2: You can use [[minValue]] and [[maxValue]]"
        "to indicate ranges.",
    )
    engineType: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="The type of engine or engines powering the vehicle.",
    )
    fuelType: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="The type of fuel suitable for the engine or engines of the vehicle. If the vehicle has only"
        "one engine, this property can be attached directly to the vehicle.",
    )
    engineDisplacement: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The volume swept by all of the pistons inside the cylinders of an internal combustion"
        "engine in a single movement. Typical unit code(s): CMQ for cubic centimeter, LTR for"
        "liters, INQ for cubic inches* Note 1: You can link to information about how the given value"
        "has been determined using the [[valueReference]] property.* Note 2: You can use [[minValue]]"
        "and [[maxValue]] to indicate ranges.",
    )
