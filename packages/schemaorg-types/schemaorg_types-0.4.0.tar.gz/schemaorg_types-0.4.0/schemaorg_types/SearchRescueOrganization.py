"""
A Search and Rescue organization of some kind.

https://schema.org/SearchRescueOrganization
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class SearchRescueOrganization(BaseModel):
    """A Search and Rescue organization of some kind.

    References:
        https://schema.org/SearchRescueOrganization
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
        serviceArea: (Optional[Union[List[Union[str, Any]], str, Any]]): The geographic area where the service is provided.
        founder: (Optional[Union[List[Union[str, Any]], str, Any]]): A person who founded this organization.
        isicV4: (Union[List[Union[str, Any]], str, Any]): The International Standard of Industrial Classification of All Economic Activities (ISIC), Revision 4 code for a particular organization, business person, or place.
        hasPOS: (Optional[Union[List[Union[str, Any]], str, Any]]): Points-of-Sales operated by the organization or person.
        globalLocationNumber: (Union[List[Union[str, Any]], str, Any]): The [Global Location Number](http://www.gs1.org/gln) (GLN, sometimes also referred to as International Location Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit number used to identify parties and physical locations.
        member: (Optional[Union[List[Union[str, Any]], str, Any]]): A member of an Organization or a ProgramMembership. Organizations can be members of organizations; ProgramMembership is typically for individuals.
        knowsAbout: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Of a [[Person]], and less typically of an [[Organization]], to indicate a topic that is known about - suggesting possible expertise but not implying it. We do not distinguish skill levels here, or relate this to educational content, events, objectives or [[JobPosting]] descriptions.
        makesOffer: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to products or services offered by the organization or person.
        ownershipFundingInfo: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]), a description of organizational ownership structure; funding and grants. In a news/media setting, this is with particular reference to editorial independence.   Note that the [[funder]] is also available and can be used to make basic funder information machine-readable.
        founders: (Optional[Union[List[Union[str, Any]], str, Any]]): A person who founded this organization.
        legalName: (Union[List[Union[str, Any]], str, Any]): The official name of the organization, e.g. the registered company name.
        actionableFeedbackPolicy: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): For a [[NewsMediaOrganization]] or other news-related [[Organization]], a statement about public engagement activities (for news media, the newsroom’s), including involving the public - digitally or otherwise -- in coverage decisions, reporting and activities after publication.
        areaServed: (Union[List[Union[str, Any]], str, Any]): The geographic area where a service or offered item is provided.
        parentOrganization: (Optional[Union[List[Union[str, Any]], str, Any]]): The larger organization that this organization is a [[subOrganization]] of, if any.
        slogan: (Union[List[Union[str, Any]], str, Any]): A slogan or motto associated with the item.
        department: (Optional[Union[List[Union[str, Any]], str, Any]]): A relationship between an organization and a department of that organization, also described as an organization (allowing different urls, logos, opening hours). For example: a store with a pharmacy, or a bakery with a cafe.
        keywords: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Keywords or tags used to describe some item. Multiple textual entries in a keywords list are typically delimited by commas, or by repeating the property.
        reviews: (Optional[Union[List[Union[str, Any]], str, Any]]): Review of the item.
        memberOf: (Optional[Union[List[Union[str, Any]], str, Any]]): An Organization (or ProgramMembership) to which this Person or Organization belongs.
        publishingPrinciples: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): The publishingPrinciples property indicates (typically via [[URL]]) a document describing the editorial principles of an [[Organization]] (or individual, e.g. a [[Person]] writing a blog) that relate to their activities as a publisher, e.g. ethics or diversity policies. When applied to a [[CreativeWork]] (e.g. [[NewsArticle]]) the principles are those of the party primarily responsible for the creation of the [[CreativeWork]].While such policies are most typically expressed in natural language, sometimes related information (e.g. indicating a [[funder]]) can be expressed using schema.org terminology.
        employee: (Optional[Union[List[Union[str, Any]], str, Any]]): Someone working for this organization.
        award: (Union[List[Union[str, Any]], str, Any]): An award won by or for this item.
        email: (Union[List[Union[str, Any]], str, Any]): Email address.
        contactPoints: (Optional[Union[List[Union[str, Any]], str, Any]]): A contact point for a person or organization.
        diversityStaffingReport: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]), a report on staffing diversity issues. In a news context this might be for example ASNE or RTDNA (US) reports, or self-reported.
        foundingDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The date that this organization was founded.
        owns: (Optional[Union[List[Union[str, Any]], str, Any]]): Products owned by the organization or person.
        awards: (Union[List[Union[str, Any]], str, Any]): Awards won by or for this item.
        review: (Optional[Union[List[Union[str, Any]], str, Any]]): A review of the item.
        dissolutionDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The date that this organization was dissolved.
        funding: (Optional[Union[List[Union[str, Any]], str, Any]]): A [[Grant]] that directly or indirectly provide funding or sponsorship for this item. See also [[ownershipFundingInfo]].
        interactionStatistic: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of interactions for the CreativeWork using the WebSite or SoftwareApplication. The most specific child type of InteractionCounter should be used.
        events: (Optional[Union[List[Union[str, Any]], str, Any]]): Upcoming or past events associated with this place or organization.
        seeks: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to products or services sought by the organization or person (demand).
        employees: (Optional[Union[List[Union[str, Any]], str, Any]]): People working for this organization.
        unnamedSourcesPolicy: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): For an [[Organization]] (typically a [[NewsMediaOrganization]]), a statement about policy on use of unnamed sources and the decision process required.
        subOrganization: (Optional[Union[List[Union[str, Any]], str, Any]]): A relationship between two organizations where the first includes the second, e.g., as a subsidiary. See also: the more specific 'department' property.
        foundingLocation: (Optional[Union[List[Union[str, Any]], str, Any]]): The place where the Organization was founded.
        funder: (Optional[Union[List[Union[str, Any]], str, Any]]): A person or organization that supports (sponsors) something through some kind of financial contribution.
        iso6523Code: (Union[List[Union[str, Any]], str, Any]): An organization identifier as defined in ISO 6523(-1). Note that many existing organization identifiers such as [leiCode](https://schema.org/leiCode), [duns](https://schema.org/duns) and [vatID](https://schema.org/vatID) can be expressed as an ISO 6523 identifier by setting the ICD part of the ISO 6523 identifier accordingly.
        diversityPolicy: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Statement on diversity policy by an [[Organization]] e.g. a [[NewsMediaOrganization]]. For a [[NewsMediaOrganization]], a statement describing the newsroom’s diversity policy on both staffing and sources, typically providing staffing data.
        hasMerchantReturnPolicy: (Optional[Union[List[Union[str, Any]], str, Any]]): Specifies a MerchantReturnPolicy that may be applicable.
        event: (Optional[Union[List[Union[str, Any]], str, Any]]): Upcoming or past event associated with this place, organization, or action.
        duns: (Union[List[Union[str, Any]], str, Any]): The Dun & Bradstreet DUNS number for identifying an organization or business person.
        alumni: (Optional[Union[List[Union[str, Any]], str, Any]]): Alumni of an organization.
        ethicsPolicy: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Statement about ethics policy, e.g. of a [[NewsMediaOrganization]] regarding journalistic and publishing practices, or of a [[Restaurant]], a page describing food source policies. In the case of a [[NewsMediaOrganization]], an ethicsPolicy is typically a statement describing the personal, organizational, and corporate standards of behavior expected by the organization.
        leiCode: (Union[List[Union[str, Any]], str, Any]): An organization identifier that uniquely identifies a legal entity as defined in ISO 17442.
        vatID: (Union[List[Union[str, Any]], str, Any]): The Value-added Tax ID of the organization or person.
        knowsLanguage: (Union[List[Union[str, Any]], str, Any]): Of a [[Person]], and less typically of an [[Organization]], to indicate a known language. We do not distinguish skill levels or reading/writing/speaking/signing here. Use language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47).
        correctionsPolicy: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): For an [[Organization]] (e.g. [[NewsMediaOrganization]]), a statement describing (in news media, the newsroom’s) disclosure and correction policy for errors.
        logo: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): An associated logo.
        hasCredential: (Optional[Union[List[Union[str, Any]], str, Any]]): A credential awarded to the Person or Organization.
        address: (Union[List[Union[str, Any]], str, Any]): Physical address of the item.
        brand: (Optional[Union[List[Union[str, Any]], str, Any]]): The brand(s) associated with a product or service, or the brand(s) maintained by an organization or business person.
        nonprofitStatus: (Optional[Union[List[Union[str, Any]], str, Any]]): nonprofitStatus indicates the legal status of a non-profit organization in its primary place of business.
        contactPoint: (Optional[Union[List[Union[str, Any]], str, Any]]): A contact point for a person or organization.
        hasOfferCatalog: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates an OfferCatalog listing for this Organization, Person, or Service.
        members: (Optional[Union[List[Union[str, Any]], str, Any]]): A member of this organization.
        aggregateRating: (Optional[Union[List[Union[str, Any]], str, Any]]): The overall rating, based on a collection of reviews or ratings, of the item.
        faxNumber: (Union[List[Union[str, Any]], str, Any]): The fax number.
        telephone: (Union[List[Union[str, Any]], str, Any]): The telephone number.
        taxID: (Union[List[Union[str, Any]], str, Any]): The Tax / Fiscal ID of the organization or person, e.g. the TIN in the US or the CIF/NIF in Spain.
        naics: (Union[List[Union[str, Any]], str, Any]): The North American Industry Classification System (NAICS) code for a particular organization or business person.
        location: (Union[List[Union[str, Any]], str, Any]): The location of, for example, where an event is happening, where an organization is located, or where an action takes place.
        numberOfEmployees: (Optional[Union[List[Union[str, Any]], str, Any]]): The number of employees in an organization, e.g. business.
        sponsor: (Optional[Union[List[Union[str, Any]], str, Any]]): A person or organization that supports a thing through a pledge, promise, or financial contribution. E.g. a sponsor of a Medical Study or a corporate sponsor of an event.

    """

    type_: str = Field(default="SearchRescueOrganization", alias="@type", const=True)
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
    serviceArea: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The geographic area where the service is provided.",
    )
    founder: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A person who founded this organization.",
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
    member: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A member of an Organization or a ProgramMembership. Organizations can be members of"
        "organizations; ProgramMembership is typically for individuals.",
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
    ownershipFundingInfo: Union[
        List[Union[str, AnyUrl, Any]], str, AnyUrl, Any
    ] = Field(
        default=None,
        description="For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]),"
        "a description of organizational ownership structure; funding and grants. In a news/media"
        "setting, this is with particular reference to editorial independence. Note that the"
        "[[funder]] is also available and can be used to make basic funder information machine-readable.",
    )
    founders: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A person who founded this organization.",
    )
    legalName: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The official name of the organization, e.g. the registered company name.",
    )
    actionableFeedbackPolicy: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="For a [[NewsMediaOrganization]] or other news-related [[Organization]], a statement"
        "about public engagement activities (for news media, the newsroom’s), including involving"
        "the public - digitally or otherwise -- in coverage decisions, reporting and activities"
        "after publication.",
    )
    areaServed: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The geographic area where a service or offered item is provided.",
    )
    parentOrganization: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The larger organization that this organization is a [[subOrganization]] of, if any.",
    )
    slogan: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A slogan or motto associated with the item.",
    )
    department: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A relationship between an organization and a department of that organization, also"
        "described as an organization (allowing different urls, logos, opening hours). For"
        "example: a store with a pharmacy, or a bakery with a cafe.",
    )
    keywords: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="Keywords or tags used to describe some item. Multiple textual entries in a keywords list"
        "are typically delimited by commas, or by repeating the property.",
    )
    reviews: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Review of the item.",
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
    employee: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Someone working for this organization.",
    )
    award: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An award won by or for this item.",
    )
    email: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Email address.",
    )
    contactPoints: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A contact point for a person or organization.",
    )
    diversityStaffingReport: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="For an [[Organization]] (often but not necessarily a [[NewsMediaOrganization]]),"
        "a report on staffing diversity issues. In a news context this might be for example ASNE"
        "or RTDNA (US) reports, or self-reported.",
    )
    foundingDate: Optional[Union[List[Union[str, Any, date]], str, Any, date]] = Field(
        default=None,
        description="The date that this organization was founded.",
    )
    owns: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Products owned by the organization or person.",
    )
    awards: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Awards won by or for this item.",
    )
    review: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A review of the item.",
    )
    dissolutionDate: Optional[
        Union[List[Union[str, Any, date]], str, Any, date]
    ] = Field(
        default=None,
        description="The date that this organization was dissolved.",
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
    events: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Upcoming or past events associated with this place or organization.",
    )
    seeks: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to products or services sought by the organization or person (demand).",
    )
    employees: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="People working for this organization.",
    )
    unnamedSourcesPolicy: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="For an [[Organization]] (typically a [[NewsMediaOrganization]]), a statement about"
        "policy on use of unnamed sources and the decision process required.",
    )
    subOrganization: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A relationship between two organizations where the first includes the second, e.g.,"
        "as a subsidiary. See also: the more specific 'department' property.",
    )
    foundingLocation: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The place where the Organization was founded.",
    )
    funder: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A person or organization that supports (sponsors) something through some kind of financial"
        "contribution.",
    )
    iso6523Code: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An organization identifier as defined in ISO 6523(-1). Note that many existing organization"
        "identifiers such as [leiCode](https://schema.org/leiCode), [duns](https://schema.org/duns)"
        "and [vatID](https://schema.org/vatID) can be expressed as an ISO 6523 identifier"
        "by setting the ICD part of the ISO 6523 identifier accordingly.",
    )
    diversityPolicy: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="Statement on diversity policy by an [[Organization]] e.g. a [[NewsMediaOrganization]]."
        "For a [[NewsMediaOrganization]], a statement describing the newsroom’s diversity"
        "policy on both staffing and sources, typically providing staffing data.",
    )
    hasMerchantReturnPolicy: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Specifies a MerchantReturnPolicy that may be applicable.",
    )
    event: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Upcoming or past event associated with this place, organization, or action.",
    )
    duns: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The Dun & Bradstreet DUNS number for identifying an organization or business person.",
    )
    alumni: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Alumni of an organization.",
    )
    ethicsPolicy: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="Statement about ethics policy, e.g. of a [[NewsMediaOrganization]] regarding journalistic"
        "and publishing practices, or of a [[Restaurant]], a page describing food source policies."
        "In the case of a [[NewsMediaOrganization]], an ethicsPolicy is typically a statement"
        "describing the personal, organizational, and corporate standards of behavior expected"
        "by the organization.",
    )
    leiCode: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An organization identifier that uniquely identifies a legal entity as defined in ISO"
        "17442.",
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
    correctionsPolicy: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="For an [[Organization]] (e.g. [[NewsMediaOrganization]]), a statement describing"
        "(in news media, the newsroom’s) disclosure and correction policy for errors.",
    )
    logo: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="An associated logo.",
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
    nonprofitStatus: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="nonprofitStatus indicates the legal status of a non-profit organization in its primary"
        "place of business.",
    )
    contactPoint: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A contact point for a person or organization.",
    )
    hasOfferCatalog: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates an OfferCatalog listing for this Organization, Person, or Service.",
    )
    members: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A member of this organization.",
    )
    aggregateRating: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
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
    naics: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The North American Industry Classification System (NAICS) code for a particular organization"
        "or business person.",
    )
    location: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The location of, for example, where an event is happening, where an organization is located,"
        "or where an action takes place.",
    )
    numberOfEmployees: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The number of employees in an organization, e.g. business.",
    )
    sponsor: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A person or organization that supports a thing through a pledge, promise, or financial"
        "contribution. E.g. a sponsor of a Medical Study or a corporate sponsor of an event.",
    )
