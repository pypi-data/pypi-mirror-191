"""
Event type: Literary event.

https://schema.org/LiteraryEvent
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class LiteraryEvent(BaseModel):
    """Event type: Literary event.

    References:
        https://schema.org/LiteraryEvent
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
        performer: (Optional[Union[List[Union[str, Any]], str, Any]]): A performer at the event&#x2014;for example, a presenter, musician, musical group or actor.
        eventAttendanceMode: (Optional[Union[List[Union[str, Any]], str, Any]]): The eventAttendanceMode of an event indicates whether it occurs online, offline, or a mix.
        workFeatured: (Optional[Union[List[Union[str, Any]], str, Any]]): A work featured in some event, e.g. exhibited in an ExhibitionEvent.       Specific subproperties are available for workPerformed (e.g. a play), or a workPresented (a Movie at a ScreeningEvent).
        remainingAttendeeCapacity: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): The number of attendee places for an event that remain unallocated.
        actor: (Optional[Union[List[Union[str, Any]], str, Any]]): An actor, e.g. in TV, radio, movie, video games etc., or in an event. Actors can be associated with individual items or with a series, episode, clip.
        doorTime: (Optional[Union[List[Union[datetime, str, Any]], datetime, str, Any]]): The time admission will commence.
        previousStartDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): Used in conjunction with eventStatus for rescheduled or cancelled events. This property contains the previously scheduled start date. For rescheduled events, the startDate property should be used for the newly scheduled start date. In the (rare) case of an event that has been postponed and rescheduled multiple times, this field may be repeated.
        recordedIn: (Optional[Union[List[Union[str, Any]], str, Any]]): The CreativeWork that captured all or part of this Event.
        keywords: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Keywords or tags used to describe some item. Multiple textual entries in a keywords list are typically delimited by commas, or by repeating the property.
        contributor: (Optional[Union[List[Union[str, Any]], str, Any]]): A secondary contributor to the CreativeWork or Event.
        superEvent: (Optional[Union[List[Union[str, Any]], str, Any]]): An event that this event is a part of. For example, a collection of individual music performances might each have a music festival as their superEvent.
        eventSchedule: (Optional[Union[List[Union[str, Any]], str, Any]]): Associates an [[Event]] with a [[Schedule]]. There are circumstances where it is preferable to share a schedule for a series of      repeating events rather than data on the individual events themselves. For example, a website or application might prefer to publish a schedule for a weekly      gym class rather than provide data on every event. A schedule could be processed by applications to add forthcoming events to a calendar. An [[Event]] that      is associated with a [[Schedule]] using this property should not have [[startDate]] or [[endDate]] properties. These are instead defined within the associated      [[Schedule]], this avoids any ambiguity for clients using the data. The property might have repeated values to specify different schedules, e.g. for different months      or seasons.
        maximumVirtualAttendeeCapacity: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): The maximum physical attendee capacity of an [[Event]] whose [[eventAttendanceMode]] is [[OnlineEventAttendanceMode]] (or the online aspects, in the case of a [[MixedEventAttendanceMode]]).
        attendees: (Optional[Union[List[Union[str, Any]], str, Any]]): A person attending the event.
        review: (Optional[Union[List[Union[str, Any]], str, Any]]): A review of the item.
        eventStatus: (Optional[Union[List[Union[str, Any]], str, Any]]): An eventStatus of an event represents its status; particularly useful when an event is cancelled or rescheduled.
        funding: (Optional[Union[List[Union[str, Any]], str, Any]]): A [[Grant]] that directly or indirectly provide funding or sponsorship for this item. See also [[ownershipFundingInfo]].
        workPerformed: (Optional[Union[List[Union[str, Any]], str, Any]]): A work performed in some event, for example a play performed in a TheaterEvent.
        duration: (Optional[Union[List[Union[str, Any]], str, Any]]): The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).
        about: (Optional[Union[List[Union[str, Any]], str, Any]]): The subject matter of the content.
        composer: (Optional[Union[List[Union[str, Any]], str, Any]]): The person or organization who wrote a composition, or who is the composer of a work performed at some event.
        funder: (Optional[Union[List[Union[str, Any]], str, Any]]): A person or organization that supports (sponsors) something through some kind of financial contribution.
        isAccessibleForFree: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): A flag to signal that the item, event, or place is accessible for free.
        subEvent: (Optional[Union[List[Union[str, Any]], str, Any]]): An Event that is part of this event. For example, a conference event includes many presentations, each of which is a subEvent of the conference.
        typicalAgeRange: (Union[List[Union[str, Any]], str, Any]): The typical expected age range, e.g. '7-9', '11-'.
        audience: (Optional[Union[List[Union[str, Any]], str, Any]]): An intended audience, i.e. a group for whom something was created.
        attendee: (Optional[Union[List[Union[str, Any]], str, Any]]): A person or organization attending the event.
        subEvents: (Optional[Union[List[Union[str, Any]], str, Any]]): Events that are a part of this event. For example, a conference event includes many presentations, each subEvents of the conference.
        performers: (Optional[Union[List[Union[str, Any]], str, Any]]): The main performer or performers of the event&#x2014;for example, a presenter, musician, or actor.
        maximumAttendeeCapacity: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): The total number of individuals that may attend an event or venue.
        translator: (Optional[Union[List[Union[str, Any]], str, Any]]): Organization or person who adapts a creative work to different languages, regional differences and technical requirements of a target market, or that translates during some event.
        aggregateRating: (Optional[Union[List[Union[str, Any]], str, Any]]): The overall rating, based on a collection of reviews or ratings, of the item.
        maximumPhysicalAttendeeCapacity: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): The maximum physical attendee capacity of an [[Event]] whose [[eventAttendanceMode]] is [[OfflineEventAttendanceMode]] (or the offline aspects, in the case of a [[MixedEventAttendanceMode]]).
        director: (Optional[Union[List[Union[str, Any]], str, Any]]): A director of e.g. TV, radio, movie, video gaming etc. content, or of an event. Directors can be associated with individual items or with a series, episode, clip.
        inLanguage: (Union[List[Union[str, Any]], str, Any]): The language of the content or performance or used in an action. Please use one of the language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also [[availableLanguage]].
        startDate: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The start date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).
        offers: (Optional[Union[List[Union[str, Any]], str, Any]]): An offer to provide this item&#x2014;for example, an offer to sell a product, rent the DVD of a movie, perform a service, or give away tickets to an event. Use [[businessFunction]] to indicate the kind of transaction offered, i.e. sell, lease, etc. This property can also be used to describe a [[Demand]]. While this property is listed as expected on a number of common types, it can be used in others. In that case, using a second type, such as Product or a subtype of Product, can clarify the nature of the offer.
        endDate: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The end date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).
        location: (Union[List[Union[str, Any]], str, Any]): The location of, for example, where an event is happening, where an organization is located, or where an action takes place.
        sponsor: (Optional[Union[List[Union[str, Any]], str, Any]]): A person or organization that supports a thing through a pledge, promise, or financial contribution. E.g. a sponsor of a Medical Study or a corporate sponsor of an event.
        organizer: (Optional[Union[List[Union[str, Any]], str, Any]]): An organizer of an Event.

    """

    type_: str = Field(default="LiteraryEvent", alias="@type", const=True)
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
    performer: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A performer at the event&#x2014;for example, a presenter, musician, musical group"
        "or actor.",
    )
    eventAttendanceMode: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The eventAttendanceMode of an event indicates whether it occurs online, offline, or"
        "a mix.",
    )
    workFeatured: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A work featured in some event, e.g. exhibited in an ExhibitionEvent. Specific subproperties"
        "are available for workPerformed (e.g. a play), or a workPresented (a Movie at a ScreeningEvent).",
    )
    remainingAttendeeCapacity: Optional[
        Union[List[Union[str, int, Any]], str, int, Any]
    ] = Field(
        default=None,
        description="The number of attendee places for an event that remain unallocated.",
    )
    actor: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An actor, e.g. in TV, radio, movie, video games etc., or in an event. Actors can be associated"
        "with individual items or with a series, episode, clip.",
    )
    doorTime: Optional[
        Union[List[Union[datetime, str, Any]], datetime, str, Any]
    ] = Field(
        default=None,
        description="The time admission will commence.",
    )
    previousStartDate: Optional[
        Union[List[Union[str, Any, date]], str, Any, date]
    ] = Field(
        default=None,
        description="Used in conjunction with eventStatus for rescheduled or cancelled events. This property"
        "contains the previously scheduled start date. For rescheduled events, the startDate"
        "property should be used for the newly scheduled start date. In the (rare) case of an event"
        "that has been postponed and rescheduled multiple times, this field may be repeated.",
    )
    recordedIn: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The CreativeWork that captured all or part of this Event.",
    )
    keywords: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="Keywords or tags used to describe some item. Multiple textual entries in a keywords list"
        "are typically delimited by commas, or by repeating the property.",
    )
    contributor: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A secondary contributor to the CreativeWork or Event.",
    )
    superEvent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An event that this event is a part of. For example, a collection of individual music performances"
        "might each have a music festival as their superEvent.",
    )
    eventSchedule: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Associates an [[Event]] with a [[Schedule]]. There are circumstances where it is preferable"
        "to share a schedule for a series of repeating events rather than data on the individual"
        "events themselves. For example, a website or application might prefer to publish a schedule"
        "for a weekly gym class rather than provide data on every event. A schedule could be processed"
        "by applications to add forthcoming events to a calendar. An [[Event]] that is associated"
        "with a [[Schedule]] using this property should not have [[startDate]] or [[endDate]]"
        "properties. These are instead defined within the associated [[Schedule]], this avoids"
        "any ambiguity for clients using the data. The property might have repeated values to"
        "specify different schedules, e.g. for different months or seasons.",
    )
    maximumVirtualAttendeeCapacity: Optional[
        Union[List[Union[str, int, Any]], str, int, Any]
    ] = Field(
        default=None,
        description="The maximum physical attendee capacity of an [[Event]] whose [[eventAttendanceMode]]"
        "is [[OnlineEventAttendanceMode]] (or the online aspects, in the case of a [[MixedEventAttendanceMode]]).",
    )
    attendees: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A person attending the event.",
    )
    review: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A review of the item.",
    )
    eventStatus: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An eventStatus of an event represents its status; particularly useful when an event"
        "is cancelled or rescheduled.",
    )
    funding: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A [[Grant]] that directly or indirectly provide funding or sponsorship for this item."
        "See also [[ownershipFundingInfo]].",
    )
    workPerformed: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A work performed in some event, for example a play performed in a TheaterEvent.",
    )
    duration: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    about: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The subject matter of the content.",
    )
    composer: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The person or organization who wrote a composition, or who is the composer of a work performed"
        "at some event.",
    )
    funder: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A person or organization that supports (sponsors) something through some kind of financial"
        "contribution.",
    )
    isAccessibleForFree: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="A flag to signal that the item, event, or place is accessible for free.",
    )
    subEvent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An Event that is part of this event. For example, a conference event includes many presentations,"
        "each of which is a subEvent of the conference.",
    )
    typicalAgeRange: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The typical expected age range, e.g. '7-9', '11-'.",
    )
    audience: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An intended audience, i.e. a group for whom something was created.",
    )
    attendee: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A person or organization attending the event.",
    )
    subEvents: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Events that are a part of this event. For example, a conference event includes many presentations,"
        "each subEvents of the conference.",
    )
    performers: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The main performer or performers of the event&#x2014;for example, a presenter, musician,"
        "or actor.",
    )
    maximumAttendeeCapacity: Optional[
        Union[List[Union[str, int, Any]], str, int, Any]
    ] = Field(
        default=None,
        description="The total number of individuals that may attend an event or venue.",
    )
    translator: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Organization or person who adapts a creative work to different languages, regional"
        "differences and technical requirements of a target market, or that translates during"
        "some event.",
    )
    aggregateRating: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
    )
    maximumPhysicalAttendeeCapacity: Optional[
        Union[List[Union[str, int, Any]], str, int, Any]
    ] = Field(
        default=None,
        description="The maximum physical attendee capacity of an [[Event]] whose [[eventAttendanceMode]]"
        "is [[OfflineEventAttendanceMode]] (or the offline aspects, in the case of a [[MixedEventAttendanceMode]]).",
    )
    director: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A director of e.g. TV, radio, movie, video gaming etc. content, or of an event. Directors"
        "can be associated with individual items or with a series, episode, clip.",
    )
    inLanguage: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The language of the content or performance or used in an action. Please use one of the language"
        "codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also"
        "[[availableLanguage]].",
    )
    startDate: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The start date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).",
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
    endDate: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The end date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).",
    )
    location: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The location of, for example, where an event is happening, where an organization is located,"
        "or where an action takes place.",
    )
    sponsor: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A person or organization that supports a thing through a pledge, promise, or financial"
        "contribution. E.g. a sponsor of a Medical Study or a corporate sponsor of an event.",
    )
    organizer: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An organizer of an Event.",
    )
