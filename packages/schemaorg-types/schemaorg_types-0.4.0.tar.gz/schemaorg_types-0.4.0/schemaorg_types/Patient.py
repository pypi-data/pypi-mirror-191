"""
A patient is any person recipient of health care services.

https://schema.org/Patient
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class Patient(BaseModel):
    """A patient is any person recipient of health care services.

    References:
        https://schema.org/Patient
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
        audienceType: (Union[List[Union[str, Any]], str, Any]): The target group associated with a given audience (e.g. veterans, car owners, musicians, etc.).
        geographicArea: (Optional[Union[List[Union[str, Any]], str, Any]]): The geographic area associated with the audience.
        healthCondition: (Optional[Union[List[Union[str, Any]], str, Any]]): Specifying the health condition(s) of a patient, medical study, or other target audience.
        requiredGender: (Union[List[Union[str, Any]], str, Any]): Audiences defined by a person's gender.
        suggestedMinAge: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): Minimum recommended age in years for the audience or user.
        requiredMinAge: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): Audiences defined by a person's minimum age.
        suggestedMeasurement: (Optional[Union[List[Union[str, Any]], str, Any]]): A suggested range of body measurements for the intended audience or person, for example inseam between 32 and 34 inches or height between 170 and 190 cm. Typically found on a size chart for wearable products.
        suggestedGender: (Union[List[Union[str, Any]], str, Any]): The suggested gender of the intended person or audience, for example "male", "female", or "unisex".
        requiredMaxAge: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): Audiences defined by a person's maximum age.
        suggestedAge: (Optional[Union[List[Union[str, Any]], str, Any]]): The age or age range for the intended audience or person, for example 3-12 months for infants, 1-5 years for toddlers.
        suggestedMaxAge: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): Maximum recommended age in years for the audience or user.
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
        audienceType: (Union[List[Union[str, Any]], str, Any]): The target group associated with a given audience (e.g. veterans, car owners, musicians, etc.).
        geographicArea: (Optional[Union[List[Union[str, Any]], str, Any]]): The geographic area associated with the audience.
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
        sibling: (Optional[Union[List[Union[str, Any]], str, Any]]): A sibling of the person.
        isicV4: (Union[List[Union[str, Any]], str, Any]): The International Standard of Industrial Classification of All Economic Activities (ISIC), Revision 4 code for a particular organization, business person, or place.
        hasPOS: (Optional[Union[List[Union[str, Any]], str, Any]]): Points-of-Sales operated by the organization or person.
        globalLocationNumber: (Union[List[Union[str, Any]], str, Any]): The [Global Location Number](http://www.gs1.org/gln) (GLN, sometimes also referred to as International Location Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit number used to identify parties and physical locations.
        spouse: (Optional[Union[List[Union[str, Any]], str, Any]]): The person's spouse.
        knowsAbout: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Of a [[Person]], and less typically of an [[Organization]], to indicate a topic that is known about - suggesting possible expertise but not implying it. We do not distinguish skill levels here, or relate this to educational content, events, objectives or [[JobPosting]] descriptions.
        makesOffer: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to products or services offered by the organization or person.
        colleague: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): A colleague of the person.
        honorificSuffix: (Union[List[Union[str, Any]], str, Any]): An honorific suffix following a Person's name such as M.D./PhD/MSCSW.
        nationality: (Optional[Union[List[Union[str, Any]], str, Any]]): Nationality of the person.
        affiliation: (Optional[Union[List[Union[str, Any]], str, Any]]): An organization that this person is affiliated with. For example, a school/university, a club, or a team.
        memberOf: (Optional[Union[List[Union[str, Any]], str, Any]]): An Organization (or ProgramMembership) to which this Person or Organization belongs.
        publishingPrinciples: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): The publishingPrinciples property indicates (typically via [[URL]]) a document describing the editorial principles of an [[Organization]] (or individual, e.g. a [[Person]] writing a blog) that relate to their activities as a publisher, e.g. ethics or diversity policies. When applied to a [[CreativeWork]] (e.g. [[NewsArticle]]) the principles are those of the party primarily responsible for the creation of the [[CreativeWork]].While such policies are most typically expressed in natural language, sometimes related information (e.g. indicating a [[funder]]) can be expressed using schema.org terminology.
        height: (Optional[Union[List[Union[str, Any]], str, Any]]): The height of the item.
        knows: (Optional[Union[List[Union[str, Any]], str, Any]]): The most generic bi-directional social/work relation.
        relatedTo: (Optional[Union[List[Union[str, Any]], str, Any]]): The most generic familial relation.
        worksFor: (Optional[Union[List[Union[str, Any]], str, Any]]): Organizations that the person works for.
        award: (Union[List[Union[str, Any]], str, Any]): An award won by or for this item.
        email: (Union[List[Union[str, Any]], str, Any]): Email address.
        givenName: (Union[List[Union[str, Any]], str, Any]): Given name. In the U.S., the first name of a Person.
        workLocation: (Optional[Union[List[Union[str, Any]], str, Any]]): A contact location for a person's place of work.
        contactPoints: (Optional[Union[List[Union[str, Any]], str, Any]]): A contact point for a person or organization.
        jobTitle: (Union[List[Union[str, Any]], str, Any]): The job title of the person (for example, Financial Manager).
        owns: (Optional[Union[List[Union[str, Any]], str, Any]]): Products owned by the organization or person.
        awards: (Union[List[Union[str, Any]], str, Any]): Awards won by or for this item.
        children: (Optional[Union[List[Union[str, Any]], str, Any]]): A child of the person.
        parent: (Optional[Union[List[Union[str, Any]], str, Any]]): A parent of this person.
        funding: (Optional[Union[List[Union[str, Any]], str, Any]]): A [[Grant]] that directly or indirectly provide funding or sponsorship for this item. See also [[ownershipFundingInfo]].
        interactionStatistic: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of interactions for the CreativeWork using the WebSite or SoftwareApplication. The most specific child type of InteractionCounter should be used.
        seeks: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to products or services sought by the organization or person (demand).
        weight: (Optional[Union[List[Union[str, Any]], str, Any]]): The weight of the product or person.
        funder: (Optional[Union[List[Union[str, Any]], str, Any]]): A person or organization that supports (sponsors) something through some kind of financial contribution.
        birthDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): Date of birth.
        deathDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): Date of death.
        additionalName: (Union[List[Union[str, Any]], str, Any]): An additional name for a Person, can be used for a middle name.
        duns: (Union[List[Union[str, Any]], str, Any]): The Dun & Bradstreet DUNS number for identifying an organization or business person.
        performerIn: (Optional[Union[List[Union[str, Any]], str, Any]]): Event that this person is a performer or participant in.
        vatID: (Union[List[Union[str, Any]], str, Any]): The Value-added Tax ID of the organization or person.
        knowsLanguage: (Union[List[Union[str, Any]], str, Any]): Of a [[Person]], and less typically of an [[Organization]], to indicate a known language. We do not distinguish skill levels or reading/writing/speaking/signing here. Use language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47).
        honorificPrefix: (Union[List[Union[str, Any]], str, Any]): An honorific prefix preceding a Person's name such as Dr/Mrs/Mr.
        parents: (Optional[Union[List[Union[str, Any]], str, Any]]): A parents of the person.
        familyName: (Union[List[Union[str, Any]], str, Any]): Family name. In the U.S., the last name of a Person.
        siblings: (Optional[Union[List[Union[str, Any]], str, Any]]): A sibling of the person.
        hasCredential: (Optional[Union[List[Union[str, Any]], str, Any]]): A credential awarded to the Person or Organization.
        address: (Union[List[Union[str, Any]], str, Any]): Physical address of the item.
        brand: (Optional[Union[List[Union[str, Any]], str, Any]]): The brand(s) associated with a product or service, or the brand(s) maintained by an organization or business person.
        hasOccupation: (Optional[Union[List[Union[str, Any]], str, Any]]): The Person's occupation. For past professions, use Role for expressing dates.
        netWorth: (Optional[Union[List[Union[str, Any]], str, Any]]): The total financial value of the person as calculated by subtracting assets from liabilities.
        contactPoint: (Optional[Union[List[Union[str, Any]], str, Any]]): A contact point for a person or organization.
        homeLocation: (Optional[Union[List[Union[str, Any]], str, Any]]): A contact location for a person's residence.
        gender: (Union[List[Union[str, Any]], str, Any]): Gender of something, typically a [[Person]], but possibly also fictional characters, animals, etc. While https://schema.org/Male and https://schema.org/Female may be used, text strings are also acceptable for people who do not identify as a binary gender. The [[gender]] property can also be used in an extended sense to cover e.g. the gender of sports teams. As with the gender of individuals, we do not try to enumerate all possibilities. A mixed-gender [[SportsTeam]] can be indicated with a text value of "Mixed".
        hasOfferCatalog: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates an OfferCatalog listing for this Organization, Person, or Service.
        follows: (Optional[Union[List[Union[str, Any]], str, Any]]): The most generic uni-directional social relation.
        birthPlace: (Optional[Union[List[Union[str, Any]], str, Any]]): The place where the person was born.
        faxNumber: (Union[List[Union[str, Any]], str, Any]): The fax number.
        telephone: (Union[List[Union[str, Any]], str, Any]): The telephone number.
        taxID: (Union[List[Union[str, Any]], str, Any]): The Tax / Fiscal ID of the organization or person, e.g. the TIN in the US or the CIF/NIF in Spain.
        callSign: (Union[List[Union[str, Any]], str, Any]): A [callsign](https://en.wikipedia.org/wiki/Call_sign), as used in broadcasting and radio communications to identify people, radio and TV stations, or vehicles.
        naics: (Union[List[Union[str, Any]], str, Any]): The North American Industry Classification System (NAICS) code for a particular organization or business person.
        deathPlace: (Optional[Union[List[Union[str, Any]], str, Any]]): The place where the person died.
        alumniOf: (Optional[Union[List[Union[str, Any]], str, Any]]): An organization that the person is an alumni of.
        colleagues: (Optional[Union[List[Union[str, Any]], str, Any]]): A colleague of the person.
        sponsor: (Optional[Union[List[Union[str, Any]], str, Any]]): A person or organization that supports a thing through a pledge, promise, or financial contribution. E.g. a sponsor of a Medical Study or a corporate sponsor of an event.
        healthCondition: (Optional[Union[List[Union[str, Any]], str, Any]]): Specifying the health condition(s) of a patient, medical study, or other target audience.
        diagnosis: (Optional[Union[List[Union[str, Any]], str, Any]]): One or more alternative conditions considered in the differential diagnosis process as output of a diagnosis process.
        drug: (Optional[Union[List[Union[str, Any]], str, Any]]): Specifying a drug or medicine used in a medication procedure.

    """

    type_: str = Field(default="Patient", alias="@type", const=True)
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
    audienceType: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The target group associated with a given audience (e.g. veterans, car owners, musicians,"
        "etc.).",
    )
    geographicArea: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The geographic area associated with the audience.",
    )
    healthCondition: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Specifying the health condition(s) of a patient, medical study, or other target audience.",
    )
    requiredGender: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Audiences defined by a person's gender.",
    )
    suggestedMinAge: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="Minimum recommended age in years for the audience or user.",
    )
    requiredMinAge: Optional[Union[List[Union[str, int, Any]], str, int, Any]] = Field(
        default=None,
        description="Audiences defined by a person's minimum age.",
    )
    suggestedMeasurement: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A suggested range of body measurements for the intended audience or person, for example"
        "inseam between 32 and 34 inches or height between 170 and 190 cm. Typically found on a size"
        "chart for wearable products.",
    )
    suggestedGender: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description='The suggested gender of the intended person or audience, for example "male", "female",'
        'or "unisex".',
    )
    requiredMaxAge: Optional[Union[List[Union[str, int, Any]], str, int, Any]] = Field(
        default=None,
        description="Audiences defined by a person's maximum age.",
    )
    suggestedAge: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The age or age range for the intended audience or person, for example 3-12 months for infants,"
        "1-5 years for toddlers.",
    )
    suggestedMaxAge: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="Maximum recommended age in years for the audience or user.",
    )
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
    audienceType: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The target group associated with a given audience (e.g. veterans, car owners, musicians,"
        "etc.).",
    )
    geographicArea: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The geographic area associated with the audience.",
    )
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
    sibling: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sibling of the person.",
    )
    isicV4: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The International Standard of Industrial Classification of All Economic Activities"
        "(ISIC), Revision 4 code for a particular organization, business person, or place.",
    )
    hasPOS: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Points-of-Sales operated by the organization or person.",
    )
    globalLocationNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The [Global Location Number](http://www.gs1.org/gln) (GLN, sometimes also referred"
        "to as International Location Number or ILN) of the respective organization, person,"
        "or place. The GLN is a 13-digit number used to identify parties and physical locations.",
    )
    spouse: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The person's spouse.",
    )
    knowsAbout: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="Of a [[Person]], and less typically of an [[Organization]], to indicate a topic that"
        "is known about - suggesting possible expertise but not implying it. We do not distinguish"
        "skill levels here, or relate this to educational content, events, objectives or [[JobPosting]]"
        "descriptions.",
    )
    makesOffer: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to products or services offered by the organization or person.",
    )
    colleague: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="A colleague of the person.",
    )
    honorificSuffix: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An honorific suffix following a Person's name such as M.D./PhD/MSCSW.",
    )
    nationality: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Nationality of the person.",
    )
    affiliation: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An organization that this person is affiliated with. For example, a school/university,"
        "a club, or a team.",
    )
    memberOf: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An Organization (or ProgramMembership) to which this Person or Organization belongs.",
    )
    publishingPrinciples: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="The publishingPrinciples property indicates (typically via [[URL]]) a document describing"
        "the editorial principles of an [[Organization]] (or individual, e.g. a [[Person]]"
        "writing a blog) that relate to their activities as a publisher, e.g. ethics or diversity"
        "policies. When applied to a [[CreativeWork]] (e.g. [[NewsArticle]]) the principles"
        "are those of the party primarily responsible for the creation of the [[CreativeWork]].While"
        "such policies are most typically expressed in natural language, sometimes related"
        "information (e.g. indicating a [[funder]]) can be expressed using schema.org terminology.",
    )
    height: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The height of the item.",
    )
    knows: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The most generic bi-directional social/work relation.",
    )
    relatedTo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The most generic familial relation.",
    )
    worksFor: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Organizations that the person works for.",
    )
    award: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An award won by or for this item.",
    )
    email: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Email address.",
    )
    givenName: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Given name. In the U.S., the first name of a Person.",
    )
    workLocation: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A contact location for a person's place of work.",
    )
    contactPoints: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A contact point for a person or organization.",
    )
    jobTitle: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The job title of the person (for example, Financial Manager).",
    )
    owns: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Products owned by the organization or person.",
    )
    awards: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Awards won by or for this item.",
    )
    children: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A child of the person.",
    )
    parent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A parent of this person.",
    )
    funding: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A [[Grant]] that directly or indirectly provide funding or sponsorship for this item."
        "See also [[ownershipFundingInfo]].",
    )
    interactionStatistic: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of interactions for the CreativeWork using the WebSite or SoftwareApplication."
        "The most specific child type of InteractionCounter should be used.",
    )
    seeks: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to products or services sought by the organization or person (demand).",
    )
    weight: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The weight of the product or person.",
    )
    funder: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A person or organization that supports (sponsors) something through some kind of financial"
        "contribution.",
    )
    birthDate: Optional[Union[List[Union[str, Any, date]], str, Any, date]] = Field(
        default=None,
        description="Date of birth.",
    )
    deathDate: Optional[Union[List[Union[str, Any, date]], str, Any, date]] = Field(
        default=None,
        description="Date of death.",
    )
    additionalName: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An additional name for a Person, can be used for a middle name.",
    )
    duns: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The Dun & Bradstreet DUNS number for identifying an organization or business person.",
    )
    performerIn: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Event that this person is a performer or participant in.",
    )
    vatID: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The Value-added Tax ID of the organization or person.",
    )
    knowsLanguage: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Of a [[Person]], and less typically of an [[Organization]], to indicate a known language."
        "We do not distinguish skill levels or reading/writing/speaking/signing here. Use"
        "language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47).",
    )
    honorificPrefix: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An honorific prefix preceding a Person's name such as Dr/Mrs/Mr.",
    )
    parents: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A parents of the person.",
    )
    familyName: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Family name. In the U.S., the last name of a Person.",
    )
    siblings: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sibling of the person.",
    )
    hasCredential: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A credential awarded to the Person or Organization.",
    )
    address: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Physical address of the item.",
    )
    brand: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The brand(s) associated with a product or service, or the brand(s) maintained by an organization"
        "or business person.",
    )
    hasOccupation: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The Person's occupation. For past professions, use Role for expressing dates.",
    )
    netWorth: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The total financial value of the person as calculated by subtracting assets from liabilities.",
    )
    contactPoint: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A contact point for a person or organization.",
    )
    homeLocation: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A contact location for a person's residence.",
    )
    gender: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Gender of something, typically a [[Person]], but possibly also fictional characters,"
        "animals, etc. While https://schema.org/Male and https://schema.org/Female may"
        "be used, text strings are also acceptable for people who do not identify as a binary gender."
        "The [[gender]] property can also be used in an extended sense to cover e.g. the gender"
        "of sports teams. As with the gender of individuals, we do not try to enumerate all possibilities."
        'A mixed-gender [[SportsTeam]] can be indicated with a text value of "Mixed".',
    )
    hasOfferCatalog: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates an OfferCatalog listing for this Organization, Person, or Service.",
    )
    follows: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The most generic uni-directional social relation.",
    )
    birthPlace: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The place where the person was born.",
    )
    faxNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The fax number.",
    )
    telephone: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The telephone number.",
    )
    taxID: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The Tax / Fiscal ID of the organization or person, e.g. the TIN in the US or the CIF/NIF in"
        "Spain.",
    )
    callSign: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A [callsign](https://en.wikipedia.org/wiki/Call_sign), as used in broadcasting"
        "and radio communications to identify people, radio and TV stations, or vehicles.",
    )
    naics: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The North American Industry Classification System (NAICS) code for a particular organization"
        "or business person.",
    )
    deathPlace: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The place where the person died.",
    )
    alumniOf: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An organization that the person is an alumni of.",
    )
    colleagues: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A colleague of the person.",
    )
    sponsor: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A person or organization that supports a thing through a pledge, promise, or financial"
        "contribution. E.g. a sponsor of a Medical Study or a corporate sponsor of an event.",
    )
    healthCondition: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Specifying the health condition(s) of a patient, medical study, or other target audience.",
    )
    diagnosis: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="One or more alternative conditions considered in the differential diagnosis process"
        "as output of a diagnosis process.",
    )
    drug: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Specifying a drug or medicine used in a medication procedure.",
    )
