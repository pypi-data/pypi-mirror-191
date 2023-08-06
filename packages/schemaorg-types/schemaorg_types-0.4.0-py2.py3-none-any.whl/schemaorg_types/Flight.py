"""
An airline flight.

https://schema.org/Flight
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class Flight(BaseModel):
    """An airline flight.

    References:
        https://schema.org/Flight
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
        departureTime: (Optional[Union[List[Union[datetime, str, Any]], datetime, str, Any]]): The expected departure time.
        itinerary: (Optional[Union[List[Union[str, Any]], str, Any]]): Destination(s) ( [[Place]] ) that make up a trip. For a trip where destination order is important use [[ItemList]] to specify that order (see examples).
        provider: (Optional[Union[List[Union[str, Any]], str, Any]]): The service provider, service operator, or service performer; the goods producer. Another party (a seller) may offer those services or goods on behalf of the provider. A provider may also serve as the seller.
        partOfTrip: (Optional[Union[List[Union[str, Any]], str, Any]]): Identifies that this [[Trip]] is a subTrip of another Trip.  For example Day 1, Day 2, etc. of a multi-day trip.
        arrivalTime: (Optional[Union[List[Union[datetime, str, Any]], datetime, str, Any]]): The expected arrival time.
        subTrip: (Optional[Union[List[Union[str, Any]], str, Any]]): Identifies a [[Trip]] that is a subTrip of this Trip.  For example Day 1, Day 2, etc. of a multi-day trip.
        offers: (Optional[Union[List[Union[str, Any]], str, Any]]): An offer to provide this item&#x2014;for example, an offer to sell a product, rent the DVD of a movie, perform a service, or give away tickets to an event. Use [[businessFunction]] to indicate the kind of transaction offered, i.e. sell, lease, etc. This property can also be used to describe a [[Demand]]. While this property is listed as expected on a number of common types, it can be used in others. In that case, using a second type, such as Product or a subtype of Product, can clarify the nature of the offer.
        seller: (Optional[Union[List[Union[str, Any]], str, Any]]): An entity which offers (sells / leases / lends / loans) the services / goods.  A seller may also be a provider.
        boardingPolicy: (Optional[Union[List[Union[str, Any]], str, Any]]): The type of boarding policy used by the airline (e.g. zone-based or group-based).
        webCheckinTime: (Optional[Union[List[Union[datetime, str, Any]], datetime, str, Any]]): The time when a passenger can check into the flight online.
        arrivalAirport: (Optional[Union[List[Union[str, Any]], str, Any]]): The airport where the flight terminates.
        estimatedFlightDuration: (Union[List[Union[str, Any]], str, Any]): The estimated time the flight will take.
        carrier: (Optional[Union[List[Union[str, Any]], str, Any]]): 'carrier' is an out-dated term indicating the 'provider' for parcel delivery and flights.
        departureAirport: (Optional[Union[List[Union[str, Any]], str, Any]]): The airport where the flight originates.
        mealService: (Union[List[Union[str, Any]], str, Any]): Description of the meals that will be provided or available for purchase.
        flightDistance: (Union[List[Union[str, Any]], str, Any]): The distance of the flight.
        departureGate: (Union[List[Union[str, Any]], str, Any]): Identifier of the flight's departure gate.
        departureTerminal: (Union[List[Union[str, Any]], str, Any]): Identifier of the flight's departure terminal.
        arrivalTerminal: (Union[List[Union[str, Any]], str, Any]): Identifier of the flight's arrival terminal.
        flightNumber: (Union[List[Union[str, Any]], str, Any]): The unique identifier for a flight including the airline IATA code. For example, if describing United flight 110, where the IATA code for United is 'UA', the flightNumber is 'UA110'.
        arrivalGate: (Union[List[Union[str, Any]], str, Any]): Identifier of the flight's arrival gate.
        aircraft: (Union[List[Union[str, Any]], str, Any]): The kind of aircraft (e.g., "Boeing 747").

    """

    type_: str = Field(default="Flight", alias="@type", const=True)
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
    departureTime: Optional[
        Union[List[Union[datetime, str, Any]], datetime, str, Any]
    ] = Field(
        default=None,
        description="The expected departure time.",
    )
    itinerary: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Destination(s) ( [[Place]] ) that make up a trip. For a trip where destination order is"
        "important use [[ItemList]] to specify that order (see examples).",
    )
    provider: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The service provider, service operator, or service performer; the goods producer."
        "Another party (a seller) may offer those services or goods on behalf of the provider."
        "A provider may also serve as the seller.",
    )
    partOfTrip: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Identifies that this [[Trip]] is a subTrip of another Trip. For example Day 1, Day 2, etc."
        "of a multi-day trip.",
    )
    arrivalTime: Optional[
        Union[List[Union[datetime, str, Any]], datetime, str, Any]
    ] = Field(
        default=None,
        description="The expected arrival time.",
    )
    subTrip: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Identifies a [[Trip]] that is a subTrip of this Trip. For example Day 1, Day 2, etc. of a"
        "multi-day trip.",
    )
    offers: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An offer to provide this item&#x2014;for example, an offer to sell a product, rent the"
        "DVD of a movie, perform a service, or give away tickets to an event. Use [[businessFunction]]"
        "to indicate the kind of transaction offered, i.e. sell, lease, etc. This property can"
        "also be used to describe a [[Demand]]. While this property is listed as expected on a number"
        "of common types, it can be used in others. In that case, using a second type, such as Product"
        "or a subtype of Product, can clarify the nature of the offer.",
    )
    seller: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An entity which offers (sells / leases / lends / loans) the services / goods. A seller may"
        "also be a provider.",
    )
    boardingPolicy: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The type of boarding policy used by the airline (e.g. zone-based or group-based).",
    )
    webCheckinTime: Optional[
        Union[List[Union[datetime, str, Any]], datetime, str, Any]
    ] = Field(
        default=None,
        description="The time when a passenger can check into the flight online.",
    )
    arrivalAirport: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The airport where the flight terminates.",
    )
    estimatedFlightDuration: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The estimated time the flight will take.",
    )
    carrier: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="'carrier' is an out-dated term indicating the 'provider' for parcel delivery and flights.",
    )
    departureAirport: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The airport where the flight originates.",
    )
    mealService: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Description of the meals that will be provided or available for purchase.",
    )
    flightDistance: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The distance of the flight.",
    )
    departureGate: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Identifier of the flight's departure gate.",
    )
    departureTerminal: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Identifier of the flight's departure terminal.",
    )
    arrivalTerminal: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Identifier of the flight's arrival terminal.",
    )
    flightNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The unique identifier for a flight including the airline IATA code. For example, if describing"
        "United flight 110, where the IATA code for United is 'UA', the flightNumber is 'UA110'.",
    )
    arrivalGate: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Identifier of the flight's arrival gate.",
    )
    aircraft: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description='The kind of aircraft (e.g., "Boeing 747").',
    )
