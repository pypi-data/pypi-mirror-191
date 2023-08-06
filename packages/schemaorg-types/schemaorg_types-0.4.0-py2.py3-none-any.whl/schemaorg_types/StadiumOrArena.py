"""
A stadium.

https://schema.org/StadiumOrArena
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class StadiumOrArena(BaseModel):
    """A stadium.

    References:
        https://schema.org/StadiumOrArena
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
        geoCovers: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a covering geometry to a covered geometry. "Every point of b is a point of (the interior or boundary of) a". As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        longitude: (Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]): The longitude of a location. For example ```-122.08585``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).
        smokingAllowed: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Indicates whether it is allowed to smoke in the place, e.g. in the restaurant, hotel or hotel room.
        isicV4: (Union[List[Union[str, Any]], str, Any]): The International Standard of Industrial Classification of All Economic Activities (ISIC), Revision 4 code for a particular organization, business person, or place.
        globalLocationNumber: (Union[List[Union[str, Any]], str, Any]): The [Global Location Number](http://www.gs1.org/gln) (GLN, sometimes also referred to as International Location Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit number used to identify parties and physical locations.
        amenityFeature: (Optional[Union[List[Union[str, Any]], str, Any]]): An amenity feature (e.g. a characteristic or service) of the Accommodation. This generic property does not make a statement about whether the feature is included in an offer for the main accommodation or available at extra costs.
        additionalProperty: (Optional[Union[List[Union[str, Any]], str, Any]]): A property-value pair representing an additional characteristic of the entity, e.g. a product feature or another characteristic for which there is no matching property in schema.org.Note: Publishers should be aware that applications designed to use specific schema.org properties (e.g. https://schema.org/width, https://schema.org/color, https://schema.org/gtin13, ...) will typically expect such data to be provided using those properties, rather than using the generic property/value mechanism.
        slogan: (Union[List[Union[str, Any]], str, Any]): A slogan or motto associated with the item.
        photos: (Optional[Union[List[Union[str, Any]], str, Any]]): Photographs of this place.
        keywords: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Keywords or tags used to describe some item. Multiple textual entries in a keywords list are typically delimited by commas, or by repeating the property.
        reviews: (Optional[Union[List[Union[str, Any]], str, Any]]): Review of the item.
        tourBookingPage: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): A page providing information on how to book a tour of some [[Place]], such as an [[Accommodation]] or [[ApartmentComplex]] in a real estate setting, as well as other kinds of tours as appropriate.
        geoWithin: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a geometry to one that contains it, i.e. it is inside (i.e. within) its interior. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        containsPlace: (Optional[Union[List[Union[str, Any]], str, Any]]): The basic containment relation between a place and another that it contains.
        review: (Optional[Union[List[Union[str, Any]], str, Any]]): A review of the item.
        hasMap: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): A URL to a map of the place.
        containedIn: (Optional[Union[List[Union[str, Any]], str, Any]]): The basic containment relation between a place and one that contains it.
        events: (Optional[Union[List[Union[str, Any]], str, Any]]): Upcoming or past events associated with this place or organization.
        geoOverlaps: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a geometry to another that geospatially overlaps it, i.e. they have some but not all points in common. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        geoEquals: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents spatial relations in which two geometries (or the places they represent) are topologically equal, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM). "Two geometries are topologically equal if their interiors intersect and no part of the interior or boundary of one geometry intersects the exterior of the other" (a symmetric relationship).
        maps: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): A URL to a map of the place.
        isAccessibleForFree: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): A flag to signal that the item, event, or place is accessible for free.
        event: (Optional[Union[List[Union[str, Any]], str, Any]]): Upcoming or past event associated with this place, organization, or action.
        photo: (Optional[Union[List[Union[str, Any]], str, Any]]): A photograph of this place.
        containedInPlace: (Optional[Union[List[Union[str, Any]], str, Any]]): The basic containment relation between a place and one that contains it.
        logo: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): An associated logo.
        geoCrosses: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a geometry to another that crosses it: "a crosses b: they have some but not all interior points in common, and the dimension of the intersection is less than that of at least one of them". As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        address: (Union[List[Union[str, Any]], str, Any]): Physical address of the item.
        geo: (Optional[Union[List[Union[str, Any]], str, Any]]): The geo coordinates of the place.
        openingHoursSpecification: (Optional[Union[List[Union[str, Any]], str, Any]]): The opening hours of a certain place.
        geoDisjoint: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents spatial relations in which two geometries (or the places they represent) are topologically disjoint: "they have no point in common. They form a set of disconnected geometries." (A symmetric relationship, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).)
        geoIntersects: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents spatial relations in which two geometries (or the places they represent) have at least one point in common. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        latitude: (Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]): The latitude of a location. For example ```37.42242``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).
        maximumAttendeeCapacity: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): The total number of individuals that may attend an event or venue.
        aggregateRating: (Optional[Union[List[Union[str, Any]], str, Any]]): The overall rating, based on a collection of reviews or ratings, of the item.
        map: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): A URL to a map of the place.
        branchCode: (Union[List[Union[str, Any]], str, Any]): A short textual code (also called "store code") that uniquely identifies a place of business. The code is typically assigned by the parentOrganization and used in structured URLs.For example, in the URL http://www.starbucks.co.uk/store-locator/etc/detail/3047 the code "3047" is a branchCode for a particular branch.
        faxNumber: (Union[List[Union[str, Any]], str, Any]): The fax number.
        publicAccess: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): A flag to signal that the [[Place]] is open to public visitors.  If this property is omitted there is no assumed default boolean value
        geoTouches: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents spatial relations in which two geometries (or the places they represent) touch: "they have at least one boundary point in common, but no interior points." (A symmetric relationship, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).)
        geoCoveredBy: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a geometry to another that covers it. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        telephone: (Union[List[Union[str, Any]], str, Any]): The telephone number.
        hasDriveThroughService: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Indicates whether some facility (e.g. [[FoodEstablishment]], [[CovidTestingFacility]]) offers a service that can be used by driving through in a car. In the case of [[CovidTestingFacility]] such facilities could potentially help with social distancing from other potentially-infected users.
        specialOpeningHoursSpecification: (Optional[Union[List[Union[str, Any]], str, Any]]): The special opening hours of a certain place.Use this to explicitly override general opening hours brought in scope by [[openingHoursSpecification]] or [[openingHours]].
        geoContains: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a containing geometry to a contained geometry. "a contains b iff no points of b lie in the exterior of a, and at least one point of the interior of b lies in the interior of a". As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        priceRange: (Union[List[Union[str, Any]], str, Any]): The price range of the business, for example ```$$$```.
        currenciesAccepted: (Union[List[Union[str, Any]], str, Any]): The currency accepted.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system) (LETS) and other currency types, e.g. "Ithaca HOUR".
        branchOf: (Optional[Union[List[Union[str, Any]], str, Any]]): The larger organization that this local business is a branch of, if any. Not to be confused with (anatomical) [[branch]].
        paymentAccepted: (Union[List[Union[str, Any]], str, Any]): Cash, Credit Card, Cryptocurrency, Local Exchange Tradings System, etc.
        openingHours: (Union[List[Union[str, Any]], str, Any]): The general opening hours for a business. Opening hours can be specified as a weekly time range, starting with days, then times per day. Multiple days can be listed with commas ',' separating each day. Day or time ranges are specified using a hyphen '-'.* Days are specified using the following two-letter combinations: ```Mo```, ```Tu```, ```We```, ```Th```, ```Fr```, ```Sa```, ```Su```.* Times are specified using 24:00 format. For example, 3pm is specified as ```15:00```, 10am as ```10:00```. * Here is an example: <code>&lt;time itemprop="openingHours" datetime=&quot;Tu,Th 16:00-20:00&quot;&gt;Tuesdays and Thursdays 4-8pm&lt;/time&gt;</code>.* If a business is open 7 days a week, then it can be specified as <code>&lt;time itemprop=&quot;openingHours&quot; datetime=&quot;Mo-Su&quot;&gt;Monday through Sunday, all day&lt;/time&gt;</code>.
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
        geoCovers: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a covering geometry to a covered geometry. "Every point of b is a point of (the interior or boundary of) a". As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        longitude: (Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]): The longitude of a location. For example ```-122.08585``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).
        smokingAllowed: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Indicates whether it is allowed to smoke in the place, e.g. in the restaurant, hotel or hotel room.
        isicV4: (Union[List[Union[str, Any]], str, Any]): The International Standard of Industrial Classification of All Economic Activities (ISIC), Revision 4 code for a particular organization, business person, or place.
        globalLocationNumber: (Union[List[Union[str, Any]], str, Any]): The [Global Location Number](http://www.gs1.org/gln) (GLN, sometimes also referred to as International Location Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit number used to identify parties and physical locations.
        amenityFeature: (Optional[Union[List[Union[str, Any]], str, Any]]): An amenity feature (e.g. a characteristic or service) of the Accommodation. This generic property does not make a statement about whether the feature is included in an offer for the main accommodation or available at extra costs.
        additionalProperty: (Optional[Union[List[Union[str, Any]], str, Any]]): A property-value pair representing an additional characteristic of the entity, e.g. a product feature or another characteristic for which there is no matching property in schema.org.Note: Publishers should be aware that applications designed to use specific schema.org properties (e.g. https://schema.org/width, https://schema.org/color, https://schema.org/gtin13, ...) will typically expect such data to be provided using those properties, rather than using the generic property/value mechanism.
        slogan: (Union[List[Union[str, Any]], str, Any]): A slogan or motto associated with the item.
        photos: (Optional[Union[List[Union[str, Any]], str, Any]]): Photographs of this place.
        keywords: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Keywords or tags used to describe some item. Multiple textual entries in a keywords list are typically delimited by commas, or by repeating the property.
        reviews: (Optional[Union[List[Union[str, Any]], str, Any]]): Review of the item.
        tourBookingPage: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): A page providing information on how to book a tour of some [[Place]], such as an [[Accommodation]] or [[ApartmentComplex]] in a real estate setting, as well as other kinds of tours as appropriate.
        geoWithin: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a geometry to one that contains it, i.e. it is inside (i.e. within) its interior. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        containsPlace: (Optional[Union[List[Union[str, Any]], str, Any]]): The basic containment relation between a place and another that it contains.
        review: (Optional[Union[List[Union[str, Any]], str, Any]]): A review of the item.
        hasMap: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): A URL to a map of the place.
        containedIn: (Optional[Union[List[Union[str, Any]], str, Any]]): The basic containment relation between a place and one that contains it.
        events: (Optional[Union[List[Union[str, Any]], str, Any]]): Upcoming or past events associated with this place or organization.
        geoOverlaps: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a geometry to another that geospatially overlaps it, i.e. they have some but not all points in common. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        geoEquals: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents spatial relations in which two geometries (or the places they represent) are topologically equal, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM). "Two geometries are topologically equal if their interiors intersect and no part of the interior or boundary of one geometry intersects the exterior of the other" (a symmetric relationship).
        maps: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): A URL to a map of the place.
        isAccessibleForFree: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): A flag to signal that the item, event, or place is accessible for free.
        event: (Optional[Union[List[Union[str, Any]], str, Any]]): Upcoming or past event associated with this place, organization, or action.
        photo: (Optional[Union[List[Union[str, Any]], str, Any]]): A photograph of this place.
        containedInPlace: (Optional[Union[List[Union[str, Any]], str, Any]]): The basic containment relation between a place and one that contains it.
        logo: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): An associated logo.
        geoCrosses: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a geometry to another that crosses it: "a crosses b: they have some but not all interior points in common, and the dimension of the intersection is less than that of at least one of them". As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        address: (Union[List[Union[str, Any]], str, Any]): Physical address of the item.
        geo: (Optional[Union[List[Union[str, Any]], str, Any]]): The geo coordinates of the place.
        openingHoursSpecification: (Optional[Union[List[Union[str, Any]], str, Any]]): The opening hours of a certain place.
        geoDisjoint: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents spatial relations in which two geometries (or the places they represent) are topologically disjoint: "they have no point in common. They form a set of disconnected geometries." (A symmetric relationship, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).)
        geoIntersects: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents spatial relations in which two geometries (or the places they represent) have at least one point in common. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        latitude: (Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]): The latitude of a location. For example ```37.42242``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).
        maximumAttendeeCapacity: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): The total number of individuals that may attend an event or venue.
        aggregateRating: (Optional[Union[List[Union[str, Any]], str, Any]]): The overall rating, based on a collection of reviews or ratings, of the item.
        map: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): A URL to a map of the place.
        branchCode: (Union[List[Union[str, Any]], str, Any]): A short textual code (also called "store code") that uniquely identifies a place of business. The code is typically assigned by the parentOrganization and used in structured URLs.For example, in the URL http://www.starbucks.co.uk/store-locator/etc/detail/3047 the code "3047" is a branchCode for a particular branch.
        faxNumber: (Union[List[Union[str, Any]], str, Any]): The fax number.
        publicAccess: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): A flag to signal that the [[Place]] is open to public visitors.  If this property is omitted there is no assumed default boolean value
        geoTouches: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents spatial relations in which two geometries (or the places they represent) touch: "they have at least one boundary point in common, but no interior points." (A symmetric relationship, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).)
        geoCoveredBy: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a geometry to another that covers it. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        telephone: (Union[List[Union[str, Any]], str, Any]): The telephone number.
        hasDriveThroughService: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Indicates whether some facility (e.g. [[FoodEstablishment]], [[CovidTestingFacility]]) offers a service that can be used by driving through in a car. In the case of [[CovidTestingFacility]] such facilities could potentially help with social distancing from other potentially-infected users.
        specialOpeningHoursSpecification: (Optional[Union[List[Union[str, Any]], str, Any]]): The special opening hours of a certain place.Use this to explicitly override general opening hours brought in scope by [[openingHoursSpecification]] or [[openingHours]].
        geoContains: (Optional[Union[List[Union[str, Any]], str, Any]]): Represents a relationship between two geometries (or the places they represent), relating a containing geometry to a contained geometry. "a contains b iff no points of b lie in the exterior of a, and at least one point of the interior of b lies in the interior of a". As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).
        openingHours: (Union[List[Union[str, Any]], str, Any]): The general opening hours for a business. Opening hours can be specified as a weekly time range, starting with days, then times per day. Multiple days can be listed with commas ',' separating each day. Day or time ranges are specified using a hyphen '-'.* Days are specified using the following two-letter combinations: ```Mo```, ```Tu```, ```We```, ```Th```, ```Fr```, ```Sa```, ```Su```.* Times are specified using 24:00 format. For example, 3pm is specified as ```15:00```, 10am as ```10:00```. * Here is an example: <code>&lt;time itemprop="openingHours" datetime=&quot;Tu,Th 16:00-20:00&quot;&gt;Tuesdays and Thursdays 4-8pm&lt;/time&gt;</code>.* If a business is open 7 days a week, then it can be specified as <code>&lt;time itemprop=&quot;openingHours&quot; datetime=&quot;Mo-Su&quot;&gt;Monday through Sunday, all day&lt;/time&gt;</code>.

    """

    type_: str = Field(default="StadiumOrArena", alias="@type", const=True)
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
    geoCovers: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        'a covering geometry to a covered geometry. "Every point of b is a point of (the interior'
        'or boundary of) a". As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).',
    )
    longitude: Union[
        List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat
    ] = Field(
        default=None,
        description="The longitude of a location. For example ```-122.08585``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).",
    )
    smokingAllowed: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Indicates whether it is allowed to smoke in the place, e.g. in the restaurant, hotel or"
        "hotel room.",
    )
    isicV4: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The International Standard of Industrial Classification of All Economic Activities"
        "(ISIC), Revision 4 code for a particular organization, business person, or place.",
    )
    globalLocationNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The [Global Location Number](http://www.gs1.org/gln) (GLN, sometimes also referred"
        "to as International Location Number or ILN) of the respective organization, person,"
        "or place. The GLN is a 13-digit number used to identify parties and physical locations.",
    )
    amenityFeature: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An amenity feature (e.g. a characteristic or service) of the Accommodation. This generic"
        "property does not make a statement about whether the feature is included in an offer for"
        "the main accommodation or available at extra costs.",
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
    slogan: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A slogan or motto associated with the item.",
    )
    photos: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Photographs of this place.",
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
    tourBookingPage: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="A page providing information on how to book a tour of some [[Place]], such as an [[Accommodation]]"
        "or [[ApartmentComplex]] in a real estate setting, as well as other kinds of tours as appropriate.",
    )
    geoWithin: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        "a geometry to one that contains it, i.e. it is inside (i.e. within) its interior. As defined"
        "in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).",
    )
    containsPlace: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The basic containment relation between a place and another that it contains.",
    )
    review: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A review of the item.",
    )
    hasMap: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="A URL to a map of the place.",
    )
    containedIn: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The basic containment relation between a place and one that contains it.",
    )
    events: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Upcoming or past events associated with this place or organization.",
    )
    geoOverlaps: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        "a geometry to another that geospatially overlaps it, i.e. they have some but not all points"
        "in common. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).",
    )
    geoEquals: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents spatial relations in which two geometries (or the places they represent)"
        "are topologically equal, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM)."
        '"Two geometries are topologically equal if their interiors intersect and no part of'
        'the interior or boundary of one geometry intersects the exterior of the other" (a symmetric'
        "relationship).",
    )
    maps: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="A URL to a map of the place.",
    )
    isAccessibleForFree: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="A flag to signal that the item, event, or place is accessible for free.",
    )
    event: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Upcoming or past event associated with this place, organization, or action.",
    )
    photo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A photograph of this place.",
    )
    containedInPlace: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The basic containment relation between a place and one that contains it.",
    )
    logo: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="An associated logo.",
    )
    geoCrosses: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        'a geometry to another that crosses it: "a crosses b: they have some but not all interior'
        "points in common, and the dimension of the intersection is less than that of at least one"
        'of them". As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).',
    )
    address: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Physical address of the item.",
    )
    geo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The geo coordinates of the place.",
    )
    openingHoursSpecification: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The opening hours of a certain place.",
    )
    geoDisjoint: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents spatial relations in which two geometries (or the places they represent)"
        'are topologically disjoint: "they have no point in common. They form a set of disconnected'
        'geometries." (A symmetric relationship, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).)',
    )
    geoIntersects: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents spatial relations in which two geometries (or the places they represent)"
        "have at least one point in common. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).",
    )
    latitude: Union[
        List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat
    ] = Field(
        default=None,
        description="The latitude of a location. For example ```37.42242``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).",
    )
    maximumAttendeeCapacity: Optional[
        Union[List[Union[str, int, Any]], str, int, Any]
    ] = Field(
        default=None,
        description="The total number of individuals that may attend an event or venue.",
    )
    aggregateRating: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
    )
    map: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="A URL to a map of the place.",
    )
    branchCode: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description='A short textual code (also called "store code") that uniquely identifies a place of'
        "business. The code is typically assigned by the parentOrganization and used in structured"
        "URLs.For example, in the URL http://www.starbucks.co.uk/store-locator/etc/detail/3047"
        'the code "3047" is a branchCode for a particular branch.',
    )
    faxNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The fax number.",
    )
    publicAccess: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="A flag to signal that the [[Place]] is open to public visitors. If this property is omitted"
        "there is no assumed default boolean value",
    )
    geoTouches: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents spatial relations in which two geometries (or the places they represent)"
        'touch: "they have at least one boundary point in common, but no interior points." (A'
        "symmetric relationship, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).)",
    )
    geoCoveredBy: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        "a geometry to another that covers it. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).",
    )
    telephone: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The telephone number.",
    )
    hasDriveThroughService: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Indicates whether some facility (e.g. [[FoodEstablishment]], [[CovidTestingFacility]])"
        "offers a service that can be used by driving through in a car. In the case of [[CovidTestingFacility]]"
        "such facilities could potentially help with social distancing from other potentially-infected"
        "users.",
    )
    specialOpeningHoursSpecification: Optional[
        Union[List[Union[str, Any]], str, Any]
    ] = Field(
        default=None,
        description="The special opening hours of a certain place.Use this to explicitly override general"
        "opening hours brought in scope by [[openingHoursSpecification]] or [[openingHours]].",
    )
    geoContains: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        'a containing geometry to a contained geometry. "a contains b iff no points of b lie in'
        'the exterior of a, and at least one point of the interior of b lies in the interior of a".'
        "As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).",
    )
    priceRange: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The price range of the business, for example ```$$$```.",
    )
    currenciesAccepted: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The currency accepted.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217),"
        'e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies)'
        'for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)'
        '(LETS) and other currency types, e.g. "Ithaca HOUR".',
    )
    branchOf: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The larger organization that this local business is a branch of, if any. Not to be confused"
        "with (anatomical) [[branch]].",
    )
    paymentAccepted: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Cash, Credit Card, Cryptocurrency, Local Exchange Tradings System, etc.",
    )
    openingHours: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The general opening hours for a business. Opening hours can be specified as a weekly time"
        "range, starting with days, then times per day. Multiple days can be listed with commas"
        "',' separating each day. Day or time ranges are specified using a hyphen '-'.* Days are"
        "specified using the following two-letter combinations: ```Mo```, ```Tu```, ```We```,"
        "```Th```, ```Fr```, ```Sa```, ```Su```.* Times are specified using 24:00 format."
        "For example, 3pm is specified as ```15:00```, 10am as ```10:00```. * Here is an example:"
        '<code>&lt;time itemprop="openingHours" datetime=&quot;Tu,Th 16:00-20:00&quot;&gt;Tuesdays'
        "and Thursdays 4-8pm&lt;/time&gt;</code>.* If a business is open 7 days a week, then"
        "it can be specified as <code>&lt;time itemprop=&quot;openingHours&quot; datetime=&quot;Mo-Su&quot;&gt;Monday"
        "through Sunday, all day&lt;/time&gt;</code>.",
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
    geoCovers: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        'a covering geometry to a covered geometry. "Every point of b is a point of (the interior'
        'or boundary of) a". As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).',
    )
    longitude: Union[
        List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat
    ] = Field(
        default=None,
        description="The longitude of a location. For example ```-122.08585``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).",
    )
    smokingAllowed: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Indicates whether it is allowed to smoke in the place, e.g. in the restaurant, hotel or"
        "hotel room.",
    )
    isicV4: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The International Standard of Industrial Classification of All Economic Activities"
        "(ISIC), Revision 4 code for a particular organization, business person, or place.",
    )
    globalLocationNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The [Global Location Number](http://www.gs1.org/gln) (GLN, sometimes also referred"
        "to as International Location Number or ILN) of the respective organization, person,"
        "or place. The GLN is a 13-digit number used to identify parties and physical locations.",
    )
    amenityFeature: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An amenity feature (e.g. a characteristic or service) of the Accommodation. This generic"
        "property does not make a statement about whether the feature is included in an offer for"
        "the main accommodation or available at extra costs.",
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
    slogan: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A slogan or motto associated with the item.",
    )
    photos: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Photographs of this place.",
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
    tourBookingPage: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="A page providing information on how to book a tour of some [[Place]], such as an [[Accommodation]]"
        "or [[ApartmentComplex]] in a real estate setting, as well as other kinds of tours as appropriate.",
    )
    geoWithin: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        "a geometry to one that contains it, i.e. it is inside (i.e. within) its interior. As defined"
        "in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).",
    )
    containsPlace: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The basic containment relation between a place and another that it contains.",
    )
    review: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A review of the item.",
    )
    hasMap: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="A URL to a map of the place.",
    )
    containedIn: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The basic containment relation between a place and one that contains it.",
    )
    events: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Upcoming or past events associated with this place or organization.",
    )
    geoOverlaps: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        "a geometry to another that geospatially overlaps it, i.e. they have some but not all points"
        "in common. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).",
    )
    geoEquals: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents spatial relations in which two geometries (or the places they represent)"
        "are topologically equal, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM)."
        '"Two geometries are topologically equal if their interiors intersect and no part of'
        'the interior or boundary of one geometry intersects the exterior of the other" (a symmetric'
        "relationship).",
    )
    maps: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="A URL to a map of the place.",
    )
    isAccessibleForFree: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="A flag to signal that the item, event, or place is accessible for free.",
    )
    event: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Upcoming or past event associated with this place, organization, or action.",
    )
    photo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A photograph of this place.",
    )
    containedInPlace: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The basic containment relation between a place and one that contains it.",
    )
    logo: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="An associated logo.",
    )
    geoCrosses: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        'a geometry to another that crosses it: "a crosses b: they have some but not all interior'
        "points in common, and the dimension of the intersection is less than that of at least one"
        'of them". As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).',
    )
    address: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Physical address of the item.",
    )
    geo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The geo coordinates of the place.",
    )
    openingHoursSpecification: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The opening hours of a certain place.",
    )
    geoDisjoint: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents spatial relations in which two geometries (or the places they represent)"
        'are topologically disjoint: "they have no point in common. They form a set of disconnected'
        'geometries." (A symmetric relationship, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).)',
    )
    geoIntersects: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents spatial relations in which two geometries (or the places they represent)"
        "have at least one point in common. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).",
    )
    latitude: Union[
        List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat
    ] = Field(
        default=None,
        description="The latitude of a location. For example ```37.42242``` ([WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System)).",
    )
    maximumAttendeeCapacity: Optional[
        Union[List[Union[str, int, Any]], str, int, Any]
    ] = Field(
        default=None,
        description="The total number of individuals that may attend an event or venue.",
    )
    aggregateRating: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
    )
    map: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="A URL to a map of the place.",
    )
    branchCode: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description='A short textual code (also called "store code") that uniquely identifies a place of'
        "business. The code is typically assigned by the parentOrganization and used in structured"
        "URLs.For example, in the URL http://www.starbucks.co.uk/store-locator/etc/detail/3047"
        'the code "3047" is a branchCode for a particular branch.',
    )
    faxNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The fax number.",
    )
    publicAccess: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="A flag to signal that the [[Place]] is open to public visitors. If this property is omitted"
        "there is no assumed default boolean value",
    )
    geoTouches: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents spatial relations in which two geometries (or the places they represent)"
        'touch: "they have at least one boundary point in common, but no interior points." (A'
        "symmetric relationship, as defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).)",
    )
    geoCoveredBy: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        "a geometry to another that covers it. As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).",
    )
    telephone: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The telephone number.",
    )
    hasDriveThroughService: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Indicates whether some facility (e.g. [[FoodEstablishment]], [[CovidTestingFacility]])"
        "offers a service that can be used by driving through in a car. In the case of [[CovidTestingFacility]]"
        "such facilities could potentially help with social distancing from other potentially-infected"
        "users.",
    )
    specialOpeningHoursSpecification: Optional[
        Union[List[Union[str, Any]], str, Any]
    ] = Field(
        default=None,
        description="The special opening hours of a certain place.Use this to explicitly override general"
        "opening hours brought in scope by [[openingHoursSpecification]] or [[openingHours]].",
    )
    geoContains: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Represents a relationship between two geometries (or the places they represent), relating"
        'a containing geometry to a contained geometry. "a contains b iff no points of b lie in'
        'the exterior of a, and at least one point of the interior of b lies in the interior of a".'
        "As defined in [DE-9IM](https://en.wikipedia.org/wiki/DE-9IM).",
    )
    openingHours: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The general opening hours for a business. Opening hours can be specified as a weekly time"
        "range, starting with days, then times per day. Multiple days can be listed with commas"
        "',' separating each day. Day or time ranges are specified using a hyphen '-'.* Days are"
        "specified using the following two-letter combinations: ```Mo```, ```Tu```, ```We```,"
        "```Th```, ```Fr```, ```Sa```, ```Su```.* Times are specified using 24:00 format."
        "For example, 3pm is specified as ```15:00```, 10am as ```10:00```. * Here is an example:"
        '<code>&lt;time itemprop="openingHours" datetime=&quot;Tu,Th 16:00-20:00&quot;&gt;Tuesdays'
        "and Thursdays 4-8pm&lt;/time&gt;</code>.* If a business is open 7 days a week, then"
        "it can be specified as <code>&lt;time itemprop=&quot;openingHours&quot; datetime=&quot;Mo-Su&quot;&gt;Monday"
        "through Sunday, all day&lt;/time&gt;</code>.",
    )
