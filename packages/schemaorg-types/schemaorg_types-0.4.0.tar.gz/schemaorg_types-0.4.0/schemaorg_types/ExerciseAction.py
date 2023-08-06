"""
The act of participating in exertive activity for the purposes of improving health and fitness.

https://schema.org/ExerciseAction
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class ExerciseAction(BaseModel):
    """The act of participating in exertive activity for the purposes of improving health and fitness.

    References:
        https://schema.org/ExerciseAction
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
        endTime: (Optional[Union[List[Union[datetime, str, Any]], datetime, str, Any]]): The endTime of something. For a reserved event or service (e.g. FoodEstablishmentReservation), the time that it is expected to end. For actions that span a period of time, when the action was performed. E.g. John wrote a book from January to *December*. For media, including audio and video, it's the time offset of the end of a clip within a larger file.Note that Event uses startDate/endDate instead of startTime/endTime, even when describing dates with times. This situation may be clarified in future revisions.
        provider: (Optional[Union[List[Union[str, Any]], str, Any]]): The service provider, service operator, or service performer; the goods producer. Another party (a seller) may offer those services or goods on behalf of the provider. A provider may also serve as the seller.
        startTime: (Optional[Union[List[Union[datetime, str, Any]], datetime, str, Any]]): The startTime of something. For a reserved event or service (e.g. FoodEstablishmentReservation), the time that it is expected to start. For actions that span a period of time, when the action was performed. E.g. John wrote a book from *January* to December. For media, including audio and video, it's the time offset of the start of a clip within a larger file.Note that Event uses startDate/endDate instead of startTime/endTime, even when describing dates with times. This situation may be clarified in future revisions.
        result: (Optional[Union[List[Union[str, Any]], str, Any]]): The result produced in the action. E.g. John wrote *a book*.
        actionStatus: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates the current disposition of the Action.
        agent: (Optional[Union[List[Union[str, Any]], str, Any]]): The direct performer or driver of the action (animate or inanimate). E.g. *John* wrote a book.
        instrument: (Optional[Union[List[Union[str, Any]], str, Any]]): The object that helped the agent perform the action. E.g. John wrote a book with *a pen*.
        object: (Optional[Union[List[Union[str, Any]], str, Any]]): The object upon which the action is carried out, whose state is kept intact or changed. Also known as the semantic roles patient, affected or undergoer (which change their state) or theme (which doesn't). E.g. John read *a book*.
        error: (Optional[Union[List[Union[str, Any]], str, Any]]): For failed actions, more information on the cause of the failure.
        target: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Indicates a target EntryPoint, or url, for an Action.
        location: (Union[List[Union[str, Any]], str, Any]): The location of, for example, where an event is happening, where an organization is located, or where an action takes place.
        participant: (Optional[Union[List[Union[str, Any]], str, Any]]): Other co-agents that participated in the action indirectly. E.g. John wrote a book with *Steve*.
        event: (Optional[Union[List[Union[str, Any]], str, Any]]): Upcoming or past event associated with this place, organization, or action.
        audience: (Optional[Union[List[Union[str, Any]], str, Any]]): An intended audience, i.e. a group for whom something was created.
        toLocation: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of location. The final location of the object or the agent after the action.
        course: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of location. The course where this action was taken.
        fromLocation: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of location. The original location of the object or the agent before the action.
        exerciseRelatedDiet: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of instrument. The diet used in this action.
        exerciseCourse: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of location. The course where this action was taken.
        opponent: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of participant. The opponent on this action.
        sportsTeam: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of participant. The sports team that participated on this action.
        sportsEvent: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of location. The sports event where this action occurred.
        diet: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of instrument. The diet used in this action.
        exercisePlan: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of instrument. The exercise plan used on this action.
        exerciseType: (Union[List[Union[str, Any]], str, Any]): Type(s) of exercise or activity, such as strength training, flexibility training, aerobics, cardiac rehabilitation, etc.
        distance: (Optional[Union[List[Union[str, Any]], str, Any]]): The distance travelled, e.g. exercising or travelling.
        sportsActivityLocation: (Optional[Union[List[Union[str, Any]], str, Any]]): A sub property of location. The sports activity location where this action occurred.

    """

    type_: str = Field(default="ExerciseAction", alias="@type", const=True)
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
    provider: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The service provider, service operator, or service performer; the goods producer."
        "Another party (a seller) may offer those services or goods on behalf of the provider."
        "A provider may also serve as the seller.",
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
    result: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The result produced in the action. E.g. John wrote *a book*.",
    )
    actionStatus: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates the current disposition of the Action.",
    )
    agent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The direct performer or driver of the action (animate or inanimate). E.g. *John* wrote"
        "a book.",
    )
    instrument: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The object that helped the agent perform the action. E.g. John wrote a book with *a pen*.",
    )
    object: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The object upon which the action is carried out, whose state is kept intact or changed."
        "Also known as the semantic roles patient, affected or undergoer (which change their"
        "state) or theme (which doesn't). E.g. John read *a book*.",
    )
    error: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="For failed actions, more information on the cause of the failure.",
    )
    target: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="Indicates a target EntryPoint, or url, for an Action.",
    )
    location: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The location of, for example, where an event is happening, where an organization is located,"
        "or where an action takes place.",
    )
    participant: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Other co-agents that participated in the action indirectly. E.g. John wrote a book with"
        "*Steve*.",
    )
    event: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Upcoming or past event associated with this place, organization, or action.",
    )
    audience: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An intended audience, i.e. a group for whom something was created.",
    )
    toLocation: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of location. The final location of the object or the agent after the action.",
    )
    course: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of location. The course where this action was taken.",
    )
    fromLocation: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of location. The original location of the object or the agent before the"
        "action.",
    )
    exerciseRelatedDiet: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of instrument. The diet used in this action.",
    )
    exerciseCourse: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of location. The course where this action was taken.",
    )
    opponent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of participant. The opponent on this action.",
    )
    sportsTeam: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of participant. The sports team that participated on this action.",
    )
    sportsEvent: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of location. The sports event where this action occurred.",
    )
    diet: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of instrument. The diet used in this action.",
    )
    exercisePlan: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of instrument. The exercise plan used on this action.",
    )
    exerciseType: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Type(s) of exercise or activity, such as strength training, flexibility training,"
        "aerobics, cardiac rehabilitation, etc.",
    )
    distance: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The distance travelled, e.g. exercising or travelling.",
    )
    sportsActivityLocation: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A sub property of location. The sports activity location where this action occurred.",
    )
