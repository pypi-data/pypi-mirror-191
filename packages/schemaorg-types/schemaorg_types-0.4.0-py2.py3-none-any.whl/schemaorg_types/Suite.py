"""
A suite in a hotel or other public accommodation, denotes a class of luxury accommodations, the key feature of which is multiple rooms (source: Wikipedia, the free encyclopedia, see <a href="http://en.wikipedia.org/wiki/Suite_(hotel)">http://en.wikipedia.org/wiki/Suite_(hotel)</a>).<br /><br />See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.

https://schema.org/Suite
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class Suite(BaseModel):
    """A suite in a hotel or other public accommodation, denotes a class of luxury accommodations, the key feature of which is multiple rooms (source: Wikipedia, the free encyclopedia, see <a href="http://en.wikipedia.org/wiki/Suite_(hotel)">http://en.wikipedia.org/wiki/Suite_(hotel)</a>).<br /><br />See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.

    References:
        https://schema.org/Suite
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
        floorSize: (Optional[Union[List[Union[str, Any]], str, Any]]): The size of the accommodation, e.g. in square meter or squarefoot.Typical unit code(s): MTK for square meter, FTK for square foot, or YDK for square yard
        numberOfRooms: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The number of rooms (excluding bathrooms and closets) of the accommodation or lodging business.Typical unit code(s): ROM for room or C62 for no unit. The type of room can be put in the unitText property of the QuantitativeValue.
        floorLevel: (Union[List[Union[str, Any]], str, Any]): The floor level for an [[Accommodation]] in a multi-storey building. Since counting  systems [vary internationally](https://en.wikipedia.org/wiki/Storey#Consecutive_number_floor_designations), the local system should be used where possible.
        numberOfFullBathrooms: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): Number of full bathrooms - The total number of full and ¾ bathrooms in an [[Accommodation]]. This corresponds to the [BathroomsFull field in RESO](https://ddwiki.reso.org/display/DDW17/BathroomsFull+Field).
        amenityFeature: (Optional[Union[List[Union[str, Any]], str, Any]]): An amenity feature (e.g. a characteristic or service) of the Accommodation. This generic property does not make a statement about whether the feature is included in an offer for the main accommodation or available at extra costs.
        tourBookingPage: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): A page providing information on how to book a tour of some [[Place]], such as an [[Accommodation]] or [[ApartmentComplex]] in a real estate setting, as well as other kinds of tours as appropriate.
        numberOfBathroomsTotal: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): The total integer number of bathrooms in some [[Accommodation]], following real estate conventions as [documented in RESO](https://ddwiki.reso.org/display/DDW17/BathroomsTotalInteger+Field): "The simple sum of the number of bathrooms. For example for a property with two Full Bathrooms and one Half Bathroom, the Bathrooms Total Integer will be 3.". See also [[numberOfRooms]].
        numberOfBedrooms: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The total integer number of bedrooms in a some [[Accommodation]], [[ApartmentComplex]] or [[FloorPlan]].
        accommodationCategory: (Union[List[Union[str, Any]], str, Any]): Category of an [[Accommodation]], following real estate conventions, e.g. RESO (see [PropertySubType](https://ddwiki.reso.org/display/DDW17/PropertySubType+Field), and [PropertyType](https://ddwiki.reso.org/display/DDW17/PropertyType+Field) fields  for suggested values).
        leaseLength: (Optional[Union[List[Union[str, Any]], str, Any]]): Length of the lease for some [[Accommodation]], either particular to some [[Offer]] or in some cases intrinsic to the property.
        petsAllowed: (Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]): Indicates whether pets are allowed to enter the accommodation or lodging business. More detailed information can be put in a text value.
        permittedUsage: (Union[List[Union[str, Any]], str, Any]): Indications regarding the permitted usage of the accommodation.
        numberOfPartialBathrooms: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): Number of partial bathrooms - The total number of half and ¼ bathrooms in an [[Accommodation]]. This corresponds to the [BathroomsPartial field in RESO](https://ddwiki.reso.org/display/DDW17/BathroomsPartial+Field).
        accommodationFloorPlan: (Optional[Union[List[Union[str, Any]], str, Any]]): A floorplan of some [[Accommodation]].
        yearBuilt: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The year an [[Accommodation]] was constructed. This corresponds to the [YearBuilt field in RESO](https://ddwiki.reso.org/display/DDW17/YearBuilt+Field).
        numberOfRooms: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The number of rooms (excluding bathrooms and closets) of the accommodation or lodging business.Typical unit code(s): ROM for room or C62 for no unit. The type of room can be put in the unitText property of the QuantitativeValue.
        bed: (Union[List[Union[str, Any]], str, Any]): The type of bed or beds included in the accommodation. For the single case of just one bed of a certain type, you use bed directly with a text.      If you want to indicate the quantity of a certain kind of bed, use an instance of BedDetails. For more detailed information, use the amenityFeature property.
        occupancy: (Optional[Union[List[Union[str, Any]], str, Any]]): The allowed total occupancy for the accommodation in persons (including infants etc). For individual accommodations, this is not necessarily the legal maximum but defines the permitted usage as per the contractual agreement (e.g. a double room used by a single person).Typical unit code(s): C62 for person

    """

    type_: str = Field(default="Suite", alias="@type", const=True)
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
    floorSize: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The size of the accommodation, e.g. in square meter or squarefoot.Typical unit code(s):"
        "MTK for square meter, FTK for square foot, or YDK for square yard",
    )
    numberOfRooms: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The number of rooms (excluding bathrooms and closets) of the accommodation or lodging"
        "business.Typical unit code(s): ROM for room or C62 for no unit. The type of room can be"
        "put in the unitText property of the QuantitativeValue.",
    )
    floorLevel: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The floor level for an [[Accommodation]] in a multi-storey building. Since counting"
        "systems [vary internationally](https://en.wikipedia.org/wiki/Storey#Consecutive_number_floor_designations),"
        "the local system should be used where possible.",
    )
    numberOfFullBathrooms: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="Number of full bathrooms - The total number of full and ¾ bathrooms in an [[Accommodation]]."
        "This corresponds to the [BathroomsFull field in RESO](https://ddwiki.reso.org/display/DDW17/BathroomsFull+Field).",
    )
    amenityFeature: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An amenity feature (e.g. a characteristic or service) of the Accommodation. This generic"
        "property does not make a statement about whether the feature is included in an offer for"
        "the main accommodation or available at extra costs.",
    )
    tourBookingPage: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="A page providing information on how to book a tour of some [[Place]], such as an [[Accommodation]]"
        "or [[ApartmentComplex]] in a real estate setting, as well as other kinds of tours as appropriate.",
    )
    numberOfBathroomsTotal: Optional[
        Union[List[Union[str, int, Any]], str, int, Any]
    ] = Field(
        default=None,
        description="The total integer number of bathrooms in some [[Accommodation]], following real estate"
        "conventions as [documented in RESO](https://ddwiki.reso.org/display/DDW17/BathroomsTotalInteger+Field):"
        '"The simple sum of the number of bathrooms. For example for a property with two Full Bathrooms'
        'and one Half Bathroom, the Bathrooms Total Integer will be 3.". See also [[numberOfRooms]].',
    )
    numberOfBedrooms: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The total integer number of bedrooms in a some [[Accommodation]], [[ApartmentComplex]]"
        "or [[FloorPlan]].",
    )
    accommodationCategory: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Category of an [[Accommodation]], following real estate conventions, e.g. RESO (see"
        "[PropertySubType](https://ddwiki.reso.org/display/DDW17/PropertySubType+Field),"
        "and [PropertyType](https://ddwiki.reso.org/display/DDW17/PropertyType+Field)"
        "fields for suggested values).",
    )
    leaseLength: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Length of the lease for some [[Accommodation]], either particular to some [[Offer]]"
        "or in some cases intrinsic to the property.",
    )
    petsAllowed: Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any] = Field(
        default=None,
        description="Indicates whether pets are allowed to enter the accommodation or lodging business."
        "More detailed information can be put in a text value.",
    )
    permittedUsage: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Indications regarding the permitted usage of the accommodation.",
    )
    numberOfPartialBathrooms: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="Number of partial bathrooms - The total number of half and ¼ bathrooms in an [[Accommodation]]."
        "This corresponds to the [BathroomsPartial field in RESO](https://ddwiki.reso.org/display/DDW17/BathroomsPartial+Field).",
    )
    accommodationFloorPlan: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A floorplan of some [[Accommodation]].",
    )
    yearBuilt: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The year an [[Accommodation]] was constructed. This corresponds to the [YearBuilt"
        "field in RESO](https://ddwiki.reso.org/display/DDW17/YearBuilt+Field).",
    )
    numberOfRooms: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The number of rooms (excluding bathrooms and closets) of the accommodation or lodging"
        "business.Typical unit code(s): ROM for room or C62 for no unit. The type of room can be"
        "put in the unitText property of the QuantitativeValue.",
    )
    bed: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The type of bed or beds included in the accommodation. For the single case of just one bed"
        "of a certain type, you use bed directly with a text. If you want to indicate the quantity"
        "of a certain kind of bed, use an instance of BedDetails. For more detailed information,"
        "use the amenityFeature property.",
    )
    occupancy: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The allowed total occupancy for the accommodation in persons (including infants etc)."
        "For individual accommodations, this is not necessarily the legal maximum but defines"
        "the permitted usage as per the contractual agreement (e.g. a double room used by a single"
        "person).Typical unit code(s): C62 for person",
    )
