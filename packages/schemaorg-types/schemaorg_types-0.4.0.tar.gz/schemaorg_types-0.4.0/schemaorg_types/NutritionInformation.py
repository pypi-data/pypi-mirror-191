"""
Nutritional information about the recipe.

https://schema.org/NutritionInformation
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class NutritionInformation(BaseModel):
    """Nutritional information about the recipe.

    References:
        https://schema.org/NutritionInformation
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
        sodiumContent: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of milligrams of sodium.
        carbohydrateContent: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of grams of carbohydrates.
        fatContent: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of grams of fat.
        cholesterolContent: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of milligrams of cholesterol.
        calories: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of calories.
        unsaturatedFatContent: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of grams of unsaturated fat.
        sugarContent: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of grams of sugar.
        transFatContent: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of grams of trans fat.
        proteinContent: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of grams of protein.
        saturatedFatContent: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of grams of saturated fat.
        servingSize: (Union[List[Union[str, Any]], str, Any]): The serving size, in terms of the number of volume or mass.
        fiberContent: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of grams of fiber.

    """

    type_: str = Field(default="NutritionInformation", alias="@type", const=True)
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
    sodiumContent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of milligrams of sodium.",
    )
    carbohydrateContent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of grams of carbohydrates.",
    )
    fatContent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of grams of fat.",
    )
    cholesterolContent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of milligrams of cholesterol.",
    )
    calories: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of calories.",
    )
    unsaturatedFatContent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of grams of unsaturated fat.",
    )
    sugarContent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of grams of sugar.",
    )
    transFatContent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of grams of trans fat.",
    )
    proteinContent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of grams of protein.",
    )
    saturatedFatContent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of grams of saturated fat.",
    )
    servingSize: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The serving size, in terms of the number of volume or mass.",
    )
    fiberContent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of grams of fiber.",
    )
