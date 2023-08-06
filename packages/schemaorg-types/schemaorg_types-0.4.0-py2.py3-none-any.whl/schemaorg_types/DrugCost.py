"""
The cost per unit of a medical drug. Note that this type is not meant to represent the price in an offer of a drug for sale; see the Offer type for that. This type will typically be used to tag wholesale or average retail cost of a drug, or maximum reimbursable cost. Costs of medical drugs vary widely depending on how and where they are paid for, so while this type captures some of the variables, costs should be used with caution by consumers of this schema's markup.

https://schema.org/DrugCost
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class DrugCost(BaseModel):
    """The cost per unit of a medical drug. Note that this type is not meant to represent the price in an offer of a drug for sale; see the Offer type for that. This type will typically be used to tag wholesale or average retail cost of a drug, or maximum reimbursable cost. Costs of medical drugs vary widely depending on how and where they are paid for, so while this type captures some of the variables, costs should be used with caution by consumers of this schema's markup.

    References:
        https://schema.org/DrugCost
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
        recognizingAuthority: (Optional[Union[List[Union[str, Any]], str, Any]]): If applicable, the organization that officially recognizes this entity as part of its endorsed system of medicine.
        relevantSpecialty: (Optional[Union[List[Union[str, Any]], str, Any]]): If applicable, a medical specialty in which this entity is relevant.
        medicineSystem: (Optional[Union[List[Union[str, Any]], str, Any]]): The system of medicine that includes this MedicalEntity, for example 'evidence-based', 'homeopathic', 'chiropractic', etc.
        funding: (Optional[Union[List[Union[str, Any]], str, Any]]): A [[Grant]] that directly or indirectly provide funding or sponsorship for this item. See also [[ownershipFundingInfo]].
        legalStatus: (Union[List[Union[str, Any]], str, Any]): The drug or supplement's legal status, including any controlled substance schedules that apply.
        study: (Optional[Union[List[Union[str, Any]], str, Any]]): A medical study or trial related to this entity.
        guideline: (Optional[Union[List[Union[str, Any]], str, Any]]): A medical guideline related to this entity.
        code: (Optional[Union[List[Union[str, Any]], str, Any]]): A medical code for the entity, taken from a controlled vocabulary or ontology such as ICD-9, DiseasesDB, MeSH, SNOMED-CT, RxNorm, etc.
        costPerUnit: (Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]): The cost per unit of the drug.
        applicableLocation: (Optional[Union[List[Union[str, Any]], str, Any]]): The location in which the status applies.
        drugUnit: (Union[List[Union[str, Any]], str, Any]): The unit in which the drug is measured, e.g. '5 mg tablet'.
        costOrigin: (Union[List[Union[str, Any]], str, Any]): Additional details to capture the origin of the cost data. For example, 'Medicare Part B'.
        costCategory: (Optional[Union[List[Union[str, Any]], str, Any]]): The category of cost, such as wholesale, retail, reimbursement cap, etc.
        costCurrency: (Union[List[Union[str, Any]], str, Any]): The currency (in 3-letter) of the drug cost. See: http://en.wikipedia.org/wiki/ISO_4217.

    """

    type_: str = Field(default="DrugCost", alias="@type", const=True)
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
    recognizingAuthority: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="If applicable, the organization that officially recognizes this entity as part of its"
        "endorsed system of medicine.",
    )
    relevantSpecialty: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="If applicable, a medical specialty in which this entity is relevant.",
    )
    medicineSystem: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The system of medicine that includes this MedicalEntity, for example 'evidence-based',"
        "'homeopathic', 'chiropractic', etc.",
    )
    funding: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A [[Grant]] that directly or indirectly provide funding or sponsorship for this item."
        "See also [[ownershipFundingInfo]].",
    )
    legalStatus: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The drug or supplement's legal status, including any controlled substance schedules"
        "that apply.",
    )
    study: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A medical study or trial related to this entity.",
    )
    guideline: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A medical guideline related to this entity.",
    )
    code: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A medical code for the entity, taken from a controlled vocabulary or ontology such as"
        "ICD-9, DiseasesDB, MeSH, SNOMED-CT, RxNorm, etc.",
    )
    costPerUnit: Union[
        List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat
    ] = Field(
        default=None,
        description="The cost per unit of the drug.",
    )
    applicableLocation: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The location in which the status applies.",
    )
    drugUnit: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The unit in which the drug is measured, e.g. '5 mg tablet'.",
    )
    costOrigin: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Additional details to capture the origin of the cost data. For example, 'Medicare Part"
        "B'.",
    )
    costCategory: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The category of cost, such as wholesale, retail, reimbursement cap, etc.",
    )
    costCurrency: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The currency (in 3-letter) of the drug cost. See: http://en.wikipedia.org/wiki/ISO_4217.",
    )
