"""
A schedule defines a repeating time period used to describe a regularly occurring [[Event]]. At a minimum a schedule will specify [[repeatFrequency]] which describes the interval between occurrences of the event. Additional information can be provided to specify the schedule more precisely.      This includes identifying the day(s) of the week or month when the recurring event will take place, in addition to its start and end time. Schedules may also      have start and end dates to indicate when they are active, e.g. to define a limited calendar of events.

https://schema.org/Schedule
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class Schedule(BaseModel):
    """A schedule defines a repeating time period used to describe a regularly occurring [[Event]]. At a minimum a schedule will specify [[repeatFrequency]] which describes the interval between occurrences of the event. Additional information can be provided to specify the schedule more precisely.      This includes identifying the day(s) of the week or month when the recurring event will take place, in addition to its start and end time. Schedules may also      have start and end dates to indicate when they are active, e.g. to define a limited calendar of events.

    References:
        https://schema.org/Schedule
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
        endTime: (Optional[Union[List[Union[datetime, str, Any]], datetime, str, Any]]): The endTime of something. For a reserved event or service (e.g. FoodEstablishmentReservation), the time that it is expected to end. For actions that span a period of time, when the action was performed. E.g. John wrote a book from January to *December*. For media, including audio and video, it's the time offset of the end of a clip within a larger file.Note that Event uses startDate/endDate instead of startTime/endTime, even when describing dates with times. This situation may be clarified in future revisions.
        startTime: (Optional[Union[List[Union[datetime, str, Any]], datetime, str, Any]]): The startTime of something. For a reserved event or service (e.g. FoodEstablishmentReservation), the time that it is expected to start. For actions that span a period of time, when the action was performed. E.g. John wrote a book from *January* to December. For media, including audio and video, it's the time offset of the start of a clip within a larger file.Note that Event uses startDate/endDate instead of startTime/endTime, even when describing dates with times. This situation may be clarified in future revisions.
        exceptDate: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): Defines a [[Date]] or [[DateTime]] during which a scheduled [[Event]] will not take place. The property allows exceptions to      a [[Schedule]] to be specified. If an exception is specified as a [[DateTime]] then only the event that would have started at that specific date and time      should be excluded from the schedule. If an exception is specified as a [[Date]] then any event that is scheduled for that 24 hour period should be      excluded from the schedule. This allows a whole day to be excluded from the schedule without having to itemise every scheduled event.
        repeatFrequency: (Union[List[Union[str, Any]], str, Any]): Defines the frequency at which [[Event]]s will occur according to a schedule [[Schedule]]. The intervals between      events should be defined as a [[Duration]] of time.
        scheduleTimezone: (Union[List[Union[str, Any]], str, Any]): Indicates the timezone for which the time(s) indicated in the [[Schedule]] are given. The value provided should be among those listed in the IANA Time Zone Database.
        byMonthWeek: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): Defines the week(s) of the month on which a recurring Event takes place. Specified as an Integer between 1-5. For clarity, byMonthWeek is best used in conjunction with byDay to indicate concepts like the first and third Mondays of a month.
        duration: (Optional[Union[List[Union[str, Any]], str, Any]]): The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).
        byDay: (Union[List[Union[str, Any]], str, Any]): Defines the day(s) of the week on which a recurring [[Event]] takes place. May be specified using either [[DayOfWeek]], or alternatively [[Text]] conforming to iCal's syntax for byDay recurrence rules.
        byMonthDay: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): Defines the day(s) of the month on which a recurring [[Event]] takes place. Specified as an [[Integer]] between 1-31.
        repeatCount: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): Defines the number of times a recurring [[Event]] will take place.
        byMonth: (Optional[Union[List[Union[str, int, Any]], str, int, Any]]): Defines the month(s) of the year on which a recurring [[Event]] takes place. Specified as an [[Integer]] between 1-12. January is 1.
        startDate: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The start date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).
        endDate: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The end date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).

    """

    type_: str = Field(default="Schedule", alias="@type", const=True)
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
    endTime: Optional[
        Union[List[Union[datetime, str, Any]], datetime, str, Any]
    ] = Field(
        default=None,
        description="The endTime of something. For a reserved event or service (e.g. FoodEstablishmentReservation),"
        "the time that it is expected to end. For actions that span a period of time, when the action"
        "was performed. E.g. John wrote a book from January to *December*. For media, including"
        "audio and video, it's the time offset of the end of a clip within a larger file.Note that"
        "Event uses startDate/endDate instead of startTime/endTime, even when describing"
        "dates with times. This situation may be clarified in future revisions.",
    )
    startTime: Optional[
        Union[List[Union[datetime, str, Any]], datetime, str, Any]
    ] = Field(
        default=None,
        description="The startTime of something. For a reserved event or service (e.g. FoodEstablishmentReservation),"
        "the time that it is expected to start. For actions that span a period of time, when the action"
        "was performed. E.g. John wrote a book from *January* to December. For media, including"
        "audio and video, it's the time offset of the start of a clip within a larger file.Note that"
        "Event uses startDate/endDate instead of startTime/endTime, even when describing"
        "dates with times. This situation may be clarified in future revisions.",
    )
    exceptDate: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="Defines a [[Date]] or [[DateTime]] during which a scheduled [[Event]] will not take"
        "place. The property allows exceptions to a [[Schedule]] to be specified. If an exception"
        "is specified as a [[DateTime]] then only the event that would have started at that specific"
        "date and time should be excluded from the schedule. If an exception is specified as a [[Date]]"
        "then any event that is scheduled for that 24 hour period should be excluded from the schedule."
        "This allows a whole day to be excluded from the schedule without having to itemise every"
        "scheduled event.",
    )
    repeatFrequency: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Defines the frequency at which [[Event]]s will occur according to a schedule [[Schedule]]."
        "The intervals between events should be defined as a [[Duration]] of time.",
    )
    scheduleTimezone: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Indicates the timezone for which the time(s) indicated in the [[Schedule]] are given."
        "The value provided should be among those listed in the IANA Time Zone Database.",
    )
    byMonthWeek: Optional[Union[List[Union[str, int, Any]], str, int, Any]] = Field(
        default=None,
        description="Defines the week(s) of the month on which a recurring Event takes place. Specified as"
        "an Integer between 1-5. For clarity, byMonthWeek is best used in conjunction with byDay"
        "to indicate concepts like the first and third Mondays of a month.",
    )
    duration: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    byDay: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Defines the day(s) of the week on which a recurring [[Event]] takes place. May be specified"
        "using either [[DayOfWeek]], or alternatively [[Text]] conforming to iCal's syntax"
        "for byDay recurrence rules.",
    )
    byMonthDay: Optional[Union[List[Union[str, int, Any]], str, int, Any]] = Field(
        default=None,
        description="Defines the day(s) of the month on which a recurring [[Event]] takes place. Specified"
        "as an [[Integer]] between 1-31.",
    )
    repeatCount: Optional[Union[List[Union[str, int, Any]], str, int, Any]] = Field(
        default=None,
        description="Defines the number of times a recurring [[Event]] will take place.",
    )
    byMonth: Optional[Union[List[Union[str, int, Any]], str, int, Any]] = Field(
        default=None,
        description="Defines the month(s) of the year on which a recurring [[Event]] takes place. Specified"
        "as an [[Integer]] between 1-12. January is 1.",
    )
    startDate: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The start date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).",
    )
    endDate: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The end date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).",
    )
