"""
Any constitutionally or isotopically distinct atom, molecule, ion, ion pair, radical, radical ion, complex, conformer etc., identifiable as a separately distinguishable entity.

https://schema.org/MolecularEntity
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class MolecularEntity(BaseModel):
    """Any constitutionally or isotopically distinct atom, molecule, ion, ion pair, radical, radical ion, complex, conformer etc., identifiable as a separately distinguishable entity.

    References:
        https://schema.org/MolecularEntity
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
        hasBioChemEntityPart: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates a BioChemEntity that (in some sense) has this BioChemEntity as a part.
        isEncodedByBioChemEntity: (Optional[Union[List[Union[str, Any]], str, Any]]): Another BioChemEntity encoding by this one.
        taxonomicRange: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): The taxonomic grouping of the organism that expresses, encodes, or in some way related to the BioChemEntity.
        isLocatedInSubcellularLocation: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Subcellular location where this BioChemEntity is located; please use PropertyValue if you want to include any evidence.
        bioChemInteraction: (Optional[Union[List[Union[str, Any]], str, Any]]): A BioChemEntity that is known to interact with this item.
        funding: (Optional[Union[List[Union[str, Any]], str, Any]]): A [[Grant]] that directly or indirectly provide funding or sponsorship for this item. See also [[ownershipFundingInfo]].
        isPartOfBioChemEntity: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates a BioChemEntity that is (in some sense) a part of this BioChemEntity.
        bioChemSimilarity: (Optional[Union[List[Union[str, Any]], str, Any]]): A similar BioChemEntity, e.g., obtained by fingerprint similarity algorithms.
        hasRepresentation: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A common representation such as a protein sequence or chemical structure for this entity. For images use schema.org/image.
        biologicalRole: (Optional[Union[List[Union[str, Any]], str, Any]]): A role played by the BioChemEntity within a biological context.
        isInvolvedInBiologicalProcess: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Biological process this BioChemEntity is involved in; please use PropertyValue if you want to include any evidence.
        associatedDisease: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Disease associated to this BioChemEntity. Such disease can be a MedicalCondition or a URL. If you want to add an evidence supporting the association, please use PropertyValue.
        hasMolecularFunction: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Molecular function performed by this BioChemEntity; please use PropertyValue if you want to include any evidence.
        chemicalRole: (Optional[Union[List[Union[str, Any]], str, Any]]): A role played by the BioChemEntity within a chemical context.
        smiles: (Union[List[Union[str, Any]], str, Any]): A specification in form of a line notation for describing the structure of chemical species using short ASCII strings.  Double bond stereochemistry \ indicators may need to be escaped in the string in formats where the backslash is an escape character.
        potentialUse: (Optional[Union[List[Union[str, Any]], str, Any]]): Intended use of the BioChemEntity by humans.
        monoisotopicMolecularWeight: (Union[List[Union[str, Any]], str, Any]): The monoisotopic mass is the sum of the masses of the atoms in a molecule using the unbound, ground-state, rest mass of the principal (most abundant) isotope for each element instead of the isotopic average mass. Please include the units in the form '&lt;Number&gt; &lt;unit&gt;', for example '770.230488 g/mol' or as '&lt;QuantitativeValue&gt;.
        molecularWeight: (Union[List[Union[str, Any]], str, Any]): This is the molecular weight of the entity being described, not of the parent. Units should be included in the form '&lt;Number&gt; &lt;unit&gt;', for example '12 amu' or as '&lt;QuantitativeValue&gt;.
        inChIKey: (Union[List[Union[str, Any]], str, Any]): InChIKey is a hashed version of the full InChI (using the SHA-256 algorithm).
        iupacName: (Union[List[Union[str, Any]], str, Any]): Systematic method of naming chemical compounds as recommended by the International Union of Pure and Applied Chemistry (IUPAC).
        molecularFormula: (Union[List[Union[str, Any]], str, Any]): The empirical formula is the simplest whole number ratio of all the atoms in a molecule.
        inChI: (Union[List[Union[str, Any]], str, Any]): Non-proprietary identifier for molecular entity that can be used in printed and electronic data sources thus enabling easier linking of diverse data compilations.

    """

    type_: str = Field(default="MolecularEntity", alias="@type", const=True)
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
    hasBioChemEntityPart: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates a BioChemEntity that (in some sense) has this BioChemEntity as a part.",
    )
    isEncodedByBioChemEntity: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Another BioChemEntity encoding by this one.",
    )
    taxonomicRange: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="The taxonomic grouping of the organism that expresses, encodes, or in some way related"
        "to the BioChemEntity.",
    )
    isLocatedInSubcellularLocation: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="Subcellular location where this BioChemEntity is located; please use PropertyValue"
        "if you want to include any evidence.",
    )
    bioChemInteraction: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A BioChemEntity that is known to interact with this item.",
    )
    funding: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A [[Grant]] that directly or indirectly provide funding or sponsorship for this item."
        "See also [[ownershipFundingInfo]].",
    )
    isPartOfBioChemEntity: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates a BioChemEntity that is (in some sense) a part of this BioChemEntity.",
    )
    bioChemSimilarity: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A similar BioChemEntity, e.g., obtained by fingerprint similarity algorithms.",
    )
    hasRepresentation: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="A common representation such as a protein sequence or chemical structure for this entity."
        "For images use schema.org/image.",
    )
    biologicalRole: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A role played by the BioChemEntity within a biological context.",
    )
    isInvolvedInBiologicalProcess: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="Biological process this BioChemEntity is involved in; please use PropertyValue if"
        "you want to include any evidence.",
    )
    associatedDisease: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="Disease associated to this BioChemEntity. Such disease can be a MedicalCondition or"
        "a URL. If you want to add an evidence supporting the association, please use PropertyValue.",
    )
    hasMolecularFunction: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="Molecular function performed by this BioChemEntity; please use PropertyValue if you"
        "want to include any evidence.",
    )
    chemicalRole: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A role played by the BioChemEntity within a chemical context.",
    )
    smiles: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A specification in form of a line notation for describing the structure of chemical species"
        "using short ASCII strings. Double bond stereochemistry \ indicators may need to be escaped"
        "in the string in formats where the backslash is an escape character.",
    )
    potentialUse: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Intended use of the BioChemEntity by humans.",
    )
    monoisotopicMolecularWeight: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The monoisotopic mass is the sum of the masses of the atoms in a molecule using the unbound,"
        "ground-state, rest mass of the principal (most abundant) isotope for each element instead"
        "of the isotopic average mass. Please include the units in the form '&lt;Number&gt; &lt;unit&gt;',"
        "for example '770.230488 g/mol' or as '&lt;QuantitativeValue&gt;.",
    )
    molecularWeight: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="This is the molecular weight of the entity being described, not of the parent. Units should"
        "be included in the form '&lt;Number&gt; &lt;unit&gt;', for example '12 amu' or as '&lt;QuantitativeValue&gt;.",
    )
    inChIKey: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="InChIKey is a hashed version of the full InChI (using the SHA-256 algorithm).",
    )
    iupacName: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Systematic method of naming chemical compounds as recommended by the International"
        "Union of Pure and Applied Chemistry (IUPAC).",
    )
    molecularFormula: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The empirical formula is the simplest whole number ratio of all the atoms in a molecule.",
    )
    inChI: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Non-proprietary identifier for molecular entity that can be used in printed and electronic"
        "data sources thus enabling easier linking of diverse data compilations.",
    )
