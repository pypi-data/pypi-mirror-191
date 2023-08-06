"""
A process of progressive physical care and rehabilitation aimed at improving a health condition.

https://schema.org/PhysicalTherapy
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class PhysicalTherapy(BaseModel):
    """A process of progressive physical care and rehabilitation aimed at improving a health condition.

    References:
        https://schema.org/PhysicalTherapy
    Note:
        Model Depth 6
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
        howPerformed: (Union[List[Union[str, Any]], str, Any]): How the procedure is performed.
        procedureType: (Optional[Union[List[Union[str, Any]], str, Any]]): The type of procedure, for example Surgical, Noninvasive, or Percutaneous.
        status: (Union[List[Union[str, Any]], str, Any]): The status of the study (enumerated).
        bodyLocation: (Union[List[Union[str, Any]], str, Any]): Location in the body of the anatomical structure.
        followup: (Union[List[Union[str, Any]], str, Any]): Typical or recommended followup care after the procedure is performed.
        preparation: (Union[List[Union[str, Any]], str, Any]): Typical preparation that a patient must undergo before having the procedure performed.
        doseSchedule: (Optional[Union[List[Union[str, Any]], str, Any]]): A dosing schedule for the drug for a given population, either observed, recommended, or maximum dose based on the type used.
        drug: (Optional[Union[List[Union[str, Any]], str, Any]]): Specifying a drug or medicine used in a medication procedure.
        adverseOutcome: (Optional[Union[List[Union[str, Any]], str, Any]]): A possible complication and/or side effect of this therapy. If it is known that an adverse outcome is serious (resulting in death, disability, or permanent damage; requiring hospitalization; or otherwise life-threatening or requiring immediate medical attention), tag it as a seriousAdverseOutcome instead.
        seriousAdverseOutcome: (Optional[Union[List[Union[str, Any]], str, Any]]): A possible serious complication and/or serious side effect of this therapy. Serious adverse outcomes include those that are life-threatening; result in death, disability, or permanent damage; require hospitalization or prolong existing hospitalization; cause congenital anomalies or birth defects; or jeopardize the patient and may require medical or surgical intervention to prevent one of the outcomes in this definition.
        duplicateTherapy: (Optional[Union[List[Union[str, Any]], str, Any]]): A therapy that duplicates or overlaps this one.
        contraindication: (Union[List[Union[str, Any]], str, Any]): A contraindication for this therapy.

    """

    type_: str = Field(default="PhysicalTherapy", alias="@type", const=True)
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
    howPerformed: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="How the procedure is performed.",
    )
    procedureType: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The type of procedure, for example Surgical, Noninvasive, or Percutaneous.",
    )
    status: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The status of the study (enumerated).",
    )
    bodyLocation: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Location in the body of the anatomical structure.",
    )
    followup: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Typical or recommended followup care after the procedure is performed.",
    )
    preparation: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Typical preparation that a patient must undergo before having the procedure performed.",
    )
    doseSchedule: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A dosing schedule for the drug for a given population, either observed, recommended,"
        "or maximum dose based on the type used.",
    )
    drug: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Specifying a drug or medicine used in a medication procedure.",
    )
    adverseOutcome: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A possible complication and/or side effect of this therapy. If it is known that an adverse"
        "outcome is serious (resulting in death, disability, or permanent damage; requiring"
        "hospitalization; or otherwise life-threatening or requiring immediate medical attention),"
        "tag it as a seriousAdverseOutcome instead.",
    )
    seriousAdverseOutcome: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A possible serious complication and/or serious side effect of this therapy. Serious"
        "adverse outcomes include those that are life-threatening; result in death, disability,"
        "or permanent damage; require hospitalization or prolong existing hospitalization;"
        "cause congenital anomalies or birth defects; or jeopardize the patient and may require"
        "medical or surgical intervention to prevent one of the outcomes in this definition.",
    )
    duplicateTherapy: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A therapy that duplicates or overlaps this one.",
    )
    contraindication: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A contraindication for this therapy.",
    )
