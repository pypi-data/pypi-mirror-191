"""
A motorcycle or motorbike is a single-track, two-wheeled motor vehicle.

https://schema.org/Motorcycle
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class Motorcycle(BaseModel):
    """A motorcycle or motorbike is a single-track, two-wheeled motor vehicle.

    References:
        https://schema.org/Motorcycle
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
        hasMeasurement: (Optional[Union[List[Union[str, Any]], str, Any]]): A product measurement, for example the inseam of pants, the wheel size of a bicycle, or the gauge of a screw. Usually an exact measurement, but can also be a range of measurements for adjustable products, for example belts and ski bindings.
        countryOfAssembly: (Union[List[Union[str, Any]], str, Any]): The place where the product was assembled.
        width: (Optional[Union[List[Union[str, Any]], str, Any]]): The width of the item.
        isAccessoryOrSparePartFor: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to another product (or multiple products) for which this product is an accessory or spare part.
        isConsumableFor: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to another product (or multiple products) for which this product is a consumable.
        depth: (Optional[Union[List[Union[str, Any]], str, Any]]): The depth of the item.
        additionalProperty: (Optional[Union[List[Union[str, Any]], str, Any]]): A property-value pair representing an additional characteristic of the entity, e.g. a product feature or another characteristic for which there is no matching property in schema.org.Note: Publishers should be aware that applications designed to use specific schema.org properties (e.g. https://schema.org/width, https://schema.org/color, https://schema.org/gtin13, ...) will typically expect such data to be provided using those properties, rather than using the generic property/value mechanism.
        isVariantOf: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates the kind of product that this is a variant of. In the case of [[ProductModel]], this is a pointer (from a ProductModel) to a base product from which this product is a variant. It is safe to infer that the variant inherits all product features from the base model, unless defined locally. This is not transitive. In the case of a [[ProductGroup]], the group description also serves as a template, representing a set of Products that vary on explicitly defined, specific dimensions only (so it defines both a set of variants, as well as which values distinguish amongst those variants). When used with [[ProductGroup]], this property can apply to any [[Product]] included in the group.
        slogan: (Union[List[Union[str, Any]], str, Any]): A slogan or motto associated with the item.
        manufacturer: (Optional[Union[List[Union[str, Any]], str, Any]]): The manufacturer of the product.
        gtin14: (Union[List[Union[str, Any]], str, Any]): The GTIN-14 code of the product, or the product to which the offer refers. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) for more details.
        keywords: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Keywords or tags used to describe some item. Multiple textual entries in a keywords list are typically delimited by commas, or by repeating the property.
        positiveNotes: (Union[List[Union[str, Any]], str, Any]): Provides positive considerations regarding something, for example product highlights or (alongside [[negativeNotes]]) pro/con lists for reviews.In the case of a [[Review]], the property describes the [[itemReviewed]] from the perspective of the review; in the case of a [[Product]], the product itself is being described.The property values can be expressed either as unstructured text (repeated as necessary), or if ordered, as a list (in which case the most positive is at the beginning of the list).
        reviews: (Optional[Union[List[Union[str, Any]], str, Any]]): Review of the item.
        height: (Optional[Union[List[Union[str, Any]], str, Any]]): The height of the item.
        model: (Union[List[Union[str, Any]], str, Any]): The model of the product. Use with the URL of a ProductModel or a textual representation of the model identifier. The URL of the ProductModel can be from an external source. It is recommended to additionally provide strong product identifiers via the gtin8/gtin13/gtin14 and mpn properties.
        itemCondition: (Optional[Union[List[Union[str, Any]], str, Any]]): A predefined value from OfferItemCondition specifying the condition of the product or service, or the products or services included in the offer. Also used for product return policies to specify the condition of products accepted for returns.
        award: (Union[List[Union[str, Any]], str, Any]): An award won by or for this item.
        nsn: (Union[List[Union[str, Any]], str, Any]): Indicates the [NATO stock number](https://en.wikipedia.org/wiki/NATO_Stock_Number) (nsn) of a [[Product]].
        awards: (Union[List[Union[str, Any]], str, Any]): Awards won by or for this item.
        review: (Optional[Union[List[Union[str, Any]], str, Any]]): A review of the item.
        gtin: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A Global Trade Item Number ([GTIN](https://www.gs1.org/standards/id-keys/gtin)). GTINs identify trade items, including products and services, using numeric identification codes.The GS1 [digital link specifications](https://www.gs1.org/standards/Digital-Link/) express GTINs as URLs (URIs, IRIs, etc.). Details including regular expression examples can be found in, Section 6 of the GS1 URI Syntax specification; see also [schema.org tracking issue](https://github.com/schemaorg/schemaorg/issues/3156#issuecomment-1209522809) for schema.org-specific discussion. A correct [[gtin]] value should be a valid GTIN, which means that it should be an all-numeric string of either 8, 12, 13 or 14 digits, or a "GS1 Digital Link" URL based on such a string. The numeric component should also have a [valid GS1 check digit](https://www.gs1.org/services/check-digit-calculator) and meet the other rules for valid GTINs. See also [GS1's GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) and [Wikipedia](https://en.wikipedia.org/wiki/Global_Trade_Item_Number) for more details. Left-padding of the gtin values is not required or encouraged. The [[gtin]] property generalizes the earlier [[gtin8]], [[gtin12]], [[gtin13]], and [[gtin14]] properties.Note also that this is a definition for how to include GTINs in Schema.org data, and not a definition of GTINs in general - see the GS1 documentation for authoritative details.
        isRelatedTo: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to another, somehow related product (or multiple products).
        negativeNotes: (Union[List[Union[str, Any]], str, Any]): Provides negative considerations regarding something, most typically in pro/con lists for reviews (alongside [[positiveNotes]]). For symmetry In the case of a [[Review]], the property describes the [[itemReviewed]] from the perspective of the review; in the case of a [[Product]], the product itself is being described. Since product descriptions tend to emphasise positive claims, it may be relatively unusual to find [[negativeNotes]] used in this way. Nevertheless for the sake of symmetry, [[negativeNotes]] can be used on [[Product]].The property values can be expressed either as unstructured text (repeated as necessary), or if ordered, as a list (in which case the most negative is at the beginning of the list).
        funding: (Optional[Union[List[Union[str, Any]], str, Any]]): A [[Grant]] that directly or indirectly provide funding or sponsorship for this item. See also [[ownershipFundingInfo]].
        mobileUrl: (Union[List[Union[str, Any]], str, Any]): The [[mobileUrl]] property is provided for specific situations in which data consumers need to determine whether one of several provided URLs is a dedicated 'mobile site'.To discourage over-use, and reflecting intial usecases, the property is expected only on [[Product]] and [[Offer]], rather than [[Thing]]. The general trend in web technology is towards [responsive design](https://en.wikipedia.org/wiki/Responsive_web_design) in which content can be flexibly adapted to a wide range of browsing environments. Pages and sites referenced with the long-established [[url]] property should ideally also be usable on a wide variety of devices, including mobile phones. In most cases, it would be pointless and counter productive to attempt to update all [[url]] markup to use [[mobileUrl]] for more mobile-oriented pages. The property is intended for the case when items (primarily [[Product]] and [[Offer]]) have extra URLs hosted on an additional "mobile site" alongside the main one. It should not be taken as an endorsement of this publication style.
        hasEnergyConsumptionDetails: (Optional[Union[List[Union[str, Any]], str, Any]]): Defines the energy efficiency Category (also known as "class" or "rating") for a product according to an international energy efficiency standard.
        weight: (Optional[Union[List[Union[str, Any]], str, Any]]): The weight of the product or person.
        hasMerchantReturnPolicy: (Optional[Union[List[Union[str, Any]], str, Any]]): Specifies a MerchantReturnPolicy that may be applicable.
        pattern: (Union[List[Union[str, Any]], str, Any]): A pattern that something has, for example 'polka dot', 'striped', 'Canadian flag'. Values are typically expressed as text, although links to controlled value schemes are also supported.
        isFamilyFriendly: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Indicates whether this content is family friendly.
        gtin12: (Union[List[Union[str, Any]], str, Any]): The GTIN-12 code of the product, or the product to which the offer refers. The GTIN-12 is the 12-digit GS1 Identification Key composed of a U.P.C. Company Prefix, Item Reference, and Check Digit used to identify trade items. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) for more details.
        isSimilarTo: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to another, functionally similar product (or multiple products).
        productID: (Union[List[Union[str, Any]], str, Any]): The product identifier, such as ISBN. For example: ``` meta itemprop="productID" content="isbn:123-456-789" ```.
        countryOfOrigin: (Optional[Union[List[Union[str, Any]], str, Any]]): The country of origin of something, including products as well as creative  works such as movie and TV content.In the case of TV and movie, this would be the country of the principle offices of the production company or individual responsible for the movie. For other kinds of [[CreativeWork]] it is difficult to provide fully general guidance, and properties such as [[contentLocation]] and [[locationCreated]] may be more applicable.In the case of products, the country of origin of the product. The exact interpretation of this may vary by context and product type, and cannot be fully enumerated here.
        hasAdultConsideration: (Optional[Union[List[Union[str, Any]], str, Any]]): Used to tag an item to be intended or suitable for consumption or use by adults only.
        purchaseDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The date the item, e.g. vehicle, was purchased by the current owner.
        audience: (Optional[Union[List[Union[str, Any]], str, Any]]): An intended audience, i.e. a group for whom something was created.
        logo: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): An associated logo.
        countryOfLastProcessing: (Union[List[Union[str, Any]], str, Any]): The place where the item (typically [[Product]]) was last processed and tested before importation.
        asin: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): An Amazon Standard Identification Number (ASIN) is a 10-character alphanumeric unique identifier assigned by Amazon.com and its partners for product identification within the Amazon organization (summary from [Wikipedia](https://en.wikipedia.org/wiki/Amazon_Standard_Identification_Number)'s article).Note also that this is a definition for how to include ASINs in Schema.org data, and not a definition of ASINs in general - see documentation from Amazon for authoritative details.ASINs are most commonly encoded as text strings, but the [asin] property supports URL/URI as potential values too.
        gtin8: (Union[List[Union[str, Any]], str, Any]): The GTIN-8 code of the product, or the product to which the offer refers. This code is also known as EAN/UCC-8 or 8-digit EAN. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) for more details.
        releaseDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The release date of a product or product model. This can be used to distinguish the exact variant of a product.
        brand: (Optional[Union[List[Union[str, Any]], str, Any]]): The brand(s) associated with a product or service, or the brand(s) maintained by an organization or business person.
        productionDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The date of production of the item, e.g. vehicle.
        inProductGroupWithID: (Union[List[Union[str, Any]], str, Any]): Indicates the [[productGroupID]] for a [[ProductGroup]] that this product [[isVariantOf]].
        size: (Union[List[Union[str, Any]], str, Any]): A standardized size of a product or creative work, specified either through a simple textual string (for example 'XL', '32Wx34L'), a  QuantitativeValue with a unitCode, or a comprehensive and structured [[SizeSpecification]]; in other cases, the [[width]], [[height]], [[depth]] and [[weight]] properties may be more applicable.
        mpn: (Union[List[Union[str, Any]], str, Any]): The Manufacturer Part Number (MPN) of the product, or the product to which the offer refers.
        category: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A category for the item. Greater signs or slashes can be used to informally indicate a category hierarchy.
        aggregateRating: (Optional[Union[List[Union[str, Any]], str, Any]]): The overall rating, based on a collection of reviews or ratings, of the item.
        color: (Union[List[Union[str, Any]], str, Any]): The color of the product.
        material: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A material that something is made from, e.g. leather, wool, cotton, paper.
        offers: (Optional[Union[List[Union[str, Any]], str, Any]]): An offer to provide this item&#x2014;for example, an offer to sell a product, rent the DVD of a movie, perform a service, or give away tickets to an event. Use [[businessFunction]] to indicate the kind of transaction offered, i.e. sell, lease, etc. This property can also be used to describe a [[Demand]]. While this property is listed as expected on a number of common types, it can be used in others. In that case, using a second type, such as Product or a subtype of Product, can clarify the nature of the offer.
        gtin13: (Union[List[Union[str, Any]], str, Any]): The GTIN-13 code of the product, or the product to which the offer refers. This is equivalent to 13-digit ISBN codes and EAN UCC-13. Former 12-digit UPC codes can be converted into a GTIN-13 code by simply adding a preceding zero. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) for more details.
        sku: (Union[List[Union[str, Any]], str, Any]): The Stock Keeping Unit (SKU), i.e. a merchant-specific identifier for a product or service, or the product to which the offer refers.
        vehicleSpecialUsage: (Union[List[Union[str, Any]], str, Any]): Indicates whether the vehicle has been used for special purposes, like commercial rental, driving school, or as a taxi. The legislation in many countries requires this information to be revealed when offering a car for sale.
        trailerWeight: (Optional[Union[List[Union[str, Any]], str, Any]]): The permitted weight of a trailer attached to the vehicle.Typical unit code(s): KGM for kilogram, LBR for pound* Note 1: You can indicate additional information in the [[name]] of the [[QuantitativeValue]] node.* Note 2: You may also link to a [[QualitativeValue]] node that provides additional information using [[valueReference]].* Note 3: Note that you can use [[minValue]] and [[maxValue]] to indicate ranges.
        cargoVolume: (Optional[Union[List[Union[str, Any]], str, Any]]): The available volume for cargo or luggage. For automobiles, this is usually the trunk volume.Typical unit code(s): LTR for liters, FTQ for cubic foot/feetNote: You can use [[minValue]] and [[maxValue]] to indicate ranges.
        steeringPosition: (Optional[Union[List[Union[str, Any]], str, Any]]): The position of the steering wheel or similar device (mostly for cars).
        fuelConsumption: (Optional[Union[List[Union[str, Any]], str, Any]]): The amount of fuel consumed for traveling a particular distance or temporal duration with the given vehicle (e.g. liters per 100 km).* Note 1: There are unfortunately no standard unit codes for liters per 100 km.  Use [[unitText]] to indicate the unit of measurement, e.g. L/100 km.* Note 2: There are two ways of indicating the fuel consumption, [[fuelConsumption]] (e.g. 8 liters per 100 km) and [[fuelEfficiency]] (e.g. 30 miles per gallon). They are reciprocal.* Note 3: Often, the absolute value is useful only when related to driving speed ("at 80 km/h") or usage pattern ("city traffic"). You can use [[valueReference]] to link the value for the fuel consumption to another value.
        modelDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The release date of a vehicle model (often used to differentiate versions of the same make and model).
        vehicleTransmission: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): The type of component used for transmitting the power from a rotating power source to the wheels or other relevant component(s) ("gearbox" for cars).
        emissionsCO2: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The CO2 emissions in g/km. When used in combination with a QuantitativeValue, put "g/km" into the unitText property of that value, since there is no UN/CEFACT Common Code for "g/km".
        meetsEmissionStandard: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Indicates that the vehicle meets the respective emission standard.
        payload: (Optional[Union[List[Union[str, Any]], str, Any]]): The permitted weight of passengers and cargo, EXCLUDING the weight of the empty vehicle.Typical unit code(s): KGM for kilogram, LBR for pound* Note 1: Many databases specify the permitted TOTAL weight instead, which is the sum of [[weight]] and [[payload]]* Note 2: You can indicate additional information in the [[name]] of the [[QuantitativeValue]] node.* Note 3: You may also link to a [[QualitativeValue]] node that provides additional information using [[valueReference]].* Note 4: Note that you can use [[minValue]] and [[maxValue]] to indicate ranges.
        fuelCapacity: (Optional[Union[List[Union[str, Any]], str, Any]]): The capacity of the fuel tank or in the case of electric cars, the battery. If there are multiple components for storage, this should indicate the total of all storage of the same type.Typical unit code(s): LTR for liters, GLL of US gallons, GLI for UK / imperial gallons, AMH for ampere-hours (for electrical vehicles).
        wheelbase: (Optional[Union[List[Union[str, Any]], str, Any]]): The distance between the centers of the front and rear wheels.Typical unit code(s): CMT for centimeters, MTR for meters, INH for inches, FOT for foot/feet
        vehicleIdentificationNumber: (Union[List[Union[str, Any]], str, Any]): The Vehicle Identification Number (VIN) is a unique serial number used by the automotive industry to identify individual motor vehicles.
        vehicleInteriorType: (Union[List[Union[str, Any]], str, Any]): The type or material of the interior of the vehicle (e.g. synthetic fabric, leather, wood, etc.). While most interior types are characterized by the material used, an interior type can also be based on vehicle usage or target audience.
        vehicleEngine: (Optional[Union[List[Union[str, Any]], str, Any]]): Information about the engine or engines of the vehicle.
        numberOfDoors: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The number of doors.Typical unit code(s): C62
        vehicleInteriorColor: (Union[List[Union[str, Any]], str, Any]): The color or color combination of the interior of the vehicle.
        driveWheelConfiguration: (Union[List[Union[str, Any]], str, Any]): The drive wheel configuration, i.e. which roadwheels will receive torque from the vehicle's engine via the drivetrain.
        numberOfAxles: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The number of axles.Typical unit code(s): C62
        vehicleSeatingCapacity: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The number of passengers that can be seated in the vehicle, both in terms of the physical space available, and in terms of limitations set by law.Typical unit code(s): C62 for persons.
        numberOfPreviousOwners: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The number of owners of the vehicle, including the current one.Typical unit code(s): C62
        purchaseDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The date the item, e.g. vehicle, was purchased by the current owner.
        bodyType: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Indicates the design and body style of the vehicle (e.g. station wagon, hatchback, etc.).
        fuelType: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): The type of fuel suitable for the engine or engines of the vehicle. If the vehicle has only one engine, this property can be attached directly to the vehicle.
        speed: (Optional[Union[List[Union[str, Any]], str, Any]]): The speed range of the vehicle. If the vehicle is powered by an engine, the upper limit of the speed range (indicated by [[maxValue]]) should be the maximum speed achievable under regular conditions.Typical unit code(s): KMH for km/h, HM for mile per hour (0.447 04 m/s), KNT for knot*Note 1: Use [[minValue]] and [[maxValue]] to indicate the range. Typically, the minimal value is zero.* Note 2: There are many different ways of measuring the speed range. You can link to information about how the given value has been determined using the [[valueReference]] property.
        mileageFromOdometer: (Optional[Union[List[Union[str, Any]], str, Any]]): The total distance travelled by the particular vehicle since its initial production, as read from its odometer.Typical unit code(s): KMT for kilometers, SMI for statute miles
        productionDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The date of production of the item, e.g. vehicle.
        knownVehicleDamages: (Union[List[Union[str, Any]], str, Any]): A textual description of known damages, both repaired and unrepaired.
        dateVehicleFirstRegistered: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The date of the first registration of the vehicle with the respective public authorities.
        weightTotal: (Optional[Union[List[Union[str, Any]], str, Any]]): The permitted total weight of the loaded vehicle, including passengers and cargo and the weight of the empty vehicle.Typical unit code(s): KGM for kilogram, LBR for pound* Note 1: You can indicate additional information in the [[name]] of the [[QuantitativeValue]] node.* Note 2: You may also link to a [[QualitativeValue]] node that provides additional information using [[valueReference]].* Note 3: Note that you can use [[minValue]] and [[maxValue]] to indicate ranges.
        numberOfAirbags: (Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]): The number or type of airbags in the vehicle.
        fuelEfficiency: (Optional[Union[List[Union[str, Any]], str, Any]]): The distance traveled per unit of fuel used; most commonly miles per gallon (mpg) or kilometers per liter (km/L).* Note 1: There are unfortunately no standard unit codes for miles per gallon or kilometers per liter. Use [[unitText]] to indicate the unit of measurement, e.g. mpg or km/L.* Note 2: There are two ways of indicating the fuel consumption, [[fuelConsumption]] (e.g. 8 liters per 100 km) and [[fuelEfficiency]] (e.g. 30 miles per gallon). They are reciprocal.* Note 3: Often, the absolute value is useful only when related to driving speed ("at 80 km/h") or usage pattern ("city traffic"). You can use [[valueReference]] to link the value for the fuel economy to another value.
        vehicleModelDate: (Optional[Union[List[Union[str, Any, date]], str, Any, date]]): The release date of a vehicle model (often used to differentiate versions of the same make and model).
        numberOfForwardGears: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The total number of forward gears available for the transmission system of the vehicle.Typical unit code(s): C62
        callSign: (Union[List[Union[str, Any]], str, Any]): A [callsign](https://en.wikipedia.org/wiki/Call_sign), as used in broadcasting and radio communications to identify people, radio and TV stations, or vehicles.
        vehicleConfiguration: (Union[List[Union[str, Any]], str, Any]): A short text indicating the configuration of the vehicle, e.g. '5dr hatchback ST 2.5 MT 225 hp' or 'limited edition'.
        tongueWeight: (Optional[Union[List[Union[str, Any]], str, Any]]): The permitted vertical load (TWR) of a trailer attached to the vehicle. Also referred to as Tongue Load Rating (TLR) or Vertical Load Rating (VLR).Typical unit code(s): KGM for kilogram, LBR for pound* Note 1: You can indicate additional information in the [[name]] of the [[QuantitativeValue]] node.* Note 2: You may also link to a [[QualitativeValue]] node that provides additional information using [[valueReference]].* Note 3: Note that you can use [[minValue]] and [[maxValue]] to indicate ranges.
        accelerationTime: (Optional[Union[List[Union[str, Any]], str, Any]]): The time needed to accelerate the vehicle from a given start velocity to a given target velocity.Typical unit code(s): SEC for seconds* Note: There are unfortunately no standard unit codes for seconds/0..100 km/h or seconds/0..60 mph. Simply use "SEC" for seconds and indicate the velocities in the [[name]] of the [[QuantitativeValue]], or use [[valueReference]] with a [[QuantitativeValue]] of 0..60 mph or 0..100 km/h to specify the reference speeds.
        seatingCapacity: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The number of persons that can be seated (e.g. in a vehicle), both in terms of the physical space available, and in terms of limitations set by law.Typical unit code(s): C62 for persons

    """

    type_: str = Field(default="Motorcycle", alias="@type", const=True)
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
    hasMeasurement: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A product measurement, for example the inseam of pants, the wheel size of a bicycle, or"
        "the gauge of a screw. Usually an exact measurement, but can also be a range of measurements"
        "for adjustable products, for example belts and ski bindings.",
    )
    countryOfAssembly: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The place where the product was assembled.",
    )
    width: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The width of the item.",
    )
    isAccessoryOrSparePartFor: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to another product (or multiple products) for which this product is an accessory"
        "or spare part.",
    )
    isConsumableFor: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to another product (or multiple products) for which this product is a consumable.",
    )
    depth: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The depth of the item.",
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
    isVariantOf: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates the kind of product that this is a variant of. In the case of [[ProductModel]],"
        "this is a pointer (from a ProductModel) to a base product from which this product is a variant."
        "It is safe to infer that the variant inherits all product features from the base model,"
        "unless defined locally. This is not transitive. In the case of a [[ProductGroup]], the"
        "group description also serves as a template, representing a set of Products that vary"
        "on explicitly defined, specific dimensions only (so it defines both a set of variants,"
        "as well as which values distinguish amongst those variants). When used with [[ProductGroup]],"
        "this property can apply to any [[Product]] included in the group.",
    )
    slogan: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A slogan or motto associated with the item.",
    )
    manufacturer: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The manufacturer of the product.",
    )
    gtin14: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The GTIN-14 code of the product, or the product to which the offer refers. See [GS1 GTIN"
        "Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin) for more details.",
    )
    keywords: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="Keywords or tags used to describe some item. Multiple textual entries in a keywords list"
        "are typically delimited by commas, or by repeating the property.",
    )
    positiveNotes: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Provides positive considerations regarding something, for example product highlights"
        "or (alongside [[negativeNotes]]) pro/con lists for reviews.In the case of a [[Review]],"
        "the property describes the [[itemReviewed]] from the perspective of the review; in"
        "the case of a [[Product]], the product itself is being described.The property values"
        "can be expressed either as unstructured text (repeated as necessary), or if ordered,"
        "as a list (in which case the most positive is at the beginning of the list).",
    )
    reviews: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Review of the item.",
    )
    height: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The height of the item.",
    )
    model: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The model of the product. Use with the URL of a ProductModel or a textual representation"
        "of the model identifier. The URL of the ProductModel can be from an external source. It"
        "is recommended to additionally provide strong product identifiers via the gtin8/gtin13/gtin14"
        "and mpn properties.",
    )
    itemCondition: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A predefined value from OfferItemCondition specifying the condition of the product"
        "or service, or the products or services included in the offer. Also used for product return"
        "policies to specify the condition of products accepted for returns.",
    )
    award: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An award won by or for this item.",
    )
    nsn: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Indicates the [NATO stock number](https://en.wikipedia.org/wiki/NATO_Stock_Number)"
        "(nsn) of a [[Product]].",
    )
    awards: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Awards won by or for this item.",
    )
    review: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A review of the item.",
    )
    gtin: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="A Global Trade Item Number ([GTIN](https://www.gs1.org/standards/id-keys/gtin))."
        "GTINs identify trade items, including products and services, using numeric identification"
        "codes.The GS1 [digital link specifications](https://www.gs1.org/standards/Digital-Link/)"
        "express GTINs as URLs (URIs, IRIs, etc.). Details including regular expression examples"
        "can be found in, Section 6 of the GS1 URI Syntax specification; see also [schema.org tracking"
        "issue](https://github.com/schemaorg/schemaorg/issues/3156#issuecomment-1209522809)"
        "for schema.org-specific discussion. A correct [[gtin]] value should be a valid GTIN,"
        "which means that it should be an all-numeric string of either 8, 12, 13 or 14 digits, or"
        'a "GS1 Digital Link" URL based on such a string. The numeric component should also have'
        "a [valid GS1 check digit](https://www.gs1.org/services/check-digit-calculator)"
        "and meet the other rules for valid GTINs. See also [GS1's GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin)"
        "and [Wikipedia](https://en.wikipedia.org/wiki/Global_Trade_Item_Number) for"
        "more details. Left-padding of the gtin values is not required or encouraged. The [[gtin]]"
        "property generalizes the earlier [[gtin8]], [[gtin12]], [[gtin13]], and [[gtin14]]"
        "properties.Note also that this is a definition for how to include GTINs in Schema.org"
        "data, and not a definition of GTINs in general - see the GS1 documentation for authoritative"
        "details.",
    )
    isRelatedTo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to another, somehow related product (or multiple products).",
    )
    negativeNotes: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Provides negative considerations regarding something, most typically in pro/con"
        "lists for reviews (alongside [[positiveNotes]]). For symmetry In the case of a [[Review]],"
        "the property describes the [[itemReviewed]] from the perspective of the review; in"
        "the case of a [[Product]], the product itself is being described. Since product descriptions"
        "tend to emphasise positive claims, it may be relatively unusual to find [[negativeNotes]]"
        "used in this way. Nevertheless for the sake of symmetry, [[negativeNotes]] can be used"
        "on [[Product]].The property values can be expressed either as unstructured text (repeated"
        "as necessary), or if ordered, as a list (in which case the most negative is at the beginning"
        "of the list).",
    )
    funding: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A [[Grant]] that directly or indirectly provide funding or sponsorship for this item."
        "See also [[ownershipFundingInfo]].",
    )
    mobileUrl: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The [[mobileUrl]] property is provided for specific situations in which data consumers"
        "need to determine whether one of several provided URLs is a dedicated 'mobile site'.To"
        "discourage over-use, and reflecting intial usecases, the property is expected only"
        "on [[Product]] and [[Offer]], rather than [[Thing]]. The general trend in web technology"
        "is towards [responsive design](https://en.wikipedia.org/wiki/Responsive_web_design)"
        "in which content can be flexibly adapted to a wide range of browsing environments. Pages"
        "and sites referenced with the long-established [[url]] property should ideally also"
        "be usable on a wide variety of devices, including mobile phones. In most cases, it would"
        "be pointless and counter productive to attempt to update all [[url]] markup to use [[mobileUrl]]"
        "for more mobile-oriented pages. The property is intended for the case when items (primarily"
        '[[Product]] and [[Offer]]) have extra URLs hosted on an additional "mobile site"'
        "alongside the main one. It should not be taken as an endorsement of this publication style.",
    )
    hasEnergyConsumptionDetails: Optional[
        Union[List[Union[str, Any]], str, Any]
    ] = Field(
        default=None,
        description='Defines the energy efficiency Category (also known as "class" or "rating") for'
        "a product according to an international energy efficiency standard.",
    )
    weight: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The weight of the product or person.",
    )
    hasMerchantReturnPolicy: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Specifies a MerchantReturnPolicy that may be applicable.",
    )
    pattern: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A pattern that something has, for example 'polka dot', 'striped', 'Canadian flag'."
        "Values are typically expressed as text, although links to controlled value schemes"
        "are also supported.",
    )
    isFamilyFriendly: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Indicates whether this content is family friendly.",
    )
    gtin12: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The GTIN-12 code of the product, or the product to which the offer refers. The GTIN-12"
        "is the 12-digit GS1 Identification Key composed of a U.P.C. Company Prefix, Item Reference,"
        "and Check Digit used to identify trade items. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin)"
        "for more details.",
    )
    isSimilarTo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to another, functionally similar product (or multiple products).",
    )
    productID: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description='The product identifier, such as ISBN. For example: ``` meta itemprop="productID"'
        'content="isbn:123-456-789" ```.',
    )
    countryOfOrigin: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The country of origin of something, including products as well as creative works such"
        "as movie and TV content.In the case of TV and movie, this would be the country of the principle"
        "offices of the production company or individual responsible for the movie. For other"
        "kinds of [[CreativeWork]] it is difficult to provide fully general guidance, and properties"
        "such as [[contentLocation]] and [[locationCreated]] may be more applicable.In the"
        "case of products, the country of origin of the product. The exact interpretation of this"
        "may vary by context and product type, and cannot be fully enumerated here.",
    )
    hasAdultConsideration: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Used to tag an item to be intended or suitable for consumption or use by adults only.",
    )
    purchaseDate: Optional[Union[List[Union[str, Any, date]], str, Any, date]] = Field(
        default=None,
        description="The date the item, e.g. vehicle, was purchased by the current owner.",
    )
    audience: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An intended audience, i.e. a group for whom something was created.",
    )
    logo: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="An associated logo.",
    )
    countryOfLastProcessing: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The place where the item (typically [[Product]]) was last processed and tested before"
        "importation.",
    )
    asin: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="An Amazon Standard Identification Number (ASIN) is a 10-character alphanumeric unique"
        "identifier assigned by Amazon.com and its partners for product identification within"
        "the Amazon organization (summary from [Wikipedia](https://en.wikipedia.org/wiki/Amazon_Standard_Identification_Number)'s"
        "article).Note also that this is a definition for how to include ASINs in Schema.org data,"
        "and not a definition of ASINs in general - see documentation from Amazon for authoritative"
        "details.ASINs are most commonly encoded as text strings, but the [asin] property supports"
        "URL/URI as potential values too.",
    )
    gtin8: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The GTIN-8 code of the product, or the product to which the offer refers. This code is also"
        "known as EAN/UCC-8 or 8-digit EAN. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin)"
        "for more details.",
    )
    releaseDate: Optional[Union[List[Union[str, Any, date]], str, Any, date]] = Field(
        default=None,
        description="The release date of a product or product model. This can be used to distinguish the exact"
        "variant of a product.",
    )
    brand: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The brand(s) associated with a product or service, or the brand(s) maintained by an organization"
        "or business person.",
    )
    productionDate: Optional[
        Union[List[Union[str, Any, date]], str, Any, date]
    ] = Field(
        default=None,
        description="The date of production of the item, e.g. vehicle.",
    )
    inProductGroupWithID: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Indicates the [[productGroupID]] for a [[ProductGroup]] that this product [[isVariantOf]].",
    )
    size: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A standardized size of a product or creative work, specified either through a simple"
        "textual string (for example 'XL', '32Wx34L'), a QuantitativeValue with a unitCode,"
        "or a comprehensive and structured [[SizeSpecification]]; in other cases, the [[width]],"
        "[[height]], [[depth]] and [[weight]] properties may be more applicable.",
    )
    mpn: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The Manufacturer Part Number (MPN) of the product, or the product to which the offer refers.",
    )
    category: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="A category for the item. Greater signs or slashes can be used to informally indicate a"
        "category hierarchy.",
    )
    aggregateRating: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
    )
    color: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The color of the product.",
    )
    material: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="A material that something is made from, e.g. leather, wool, cotton, paper.",
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
    gtin13: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The GTIN-13 code of the product, or the product to which the offer refers. This is equivalent"
        "to 13-digit ISBN codes and EAN UCC-13. Former 12-digit UPC codes can be converted into"
        "a GTIN-13 code by simply adding a preceding zero. See [GS1 GTIN Summary](http://www.gs1.org/barcodes/technical/idkeys/gtin)"
        "for more details.",
    )
    sku: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The Stock Keeping Unit (SKU), i.e. a merchant-specific identifier for a product or service,"
        "or the product to which the offer refers.",
    )
    vehicleSpecialUsage: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Indicates whether the vehicle has been used for special purposes, like commercial rental,"
        "driving school, or as a taxi. The legislation in many countries requires this information"
        "to be revealed when offering a car for sale.",
    )
    trailerWeight: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The permitted weight of a trailer attached to the vehicle.Typical unit code(s): KGM"
        "for kilogram, LBR for pound* Note 1: You can indicate additional information in the [[name]]"
        "of the [[QuantitativeValue]] node.* Note 2: You may also link to a [[QualitativeValue]]"
        "node that provides additional information using [[valueReference]].* Note 3: Note"
        "that you can use [[minValue]] and [[maxValue]] to indicate ranges.",
    )
    cargoVolume: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The available volume for cargo or luggage. For automobiles, this is usually the trunk"
        "volume.Typical unit code(s): LTR for liters, FTQ for cubic foot/feetNote: You can use"
        "[[minValue]] and [[maxValue]] to indicate ranges.",
    )
    steeringPosition: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The position of the steering wheel or similar device (mostly for cars).",
    )
    fuelConsumption: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The amount of fuel consumed for traveling a particular distance or temporal duration"
        "with the given vehicle (e.g. liters per 100 km).* Note 1: There are unfortunately no standard"
        "unit codes for liters per 100 km. Use [[unitText]] to indicate the unit of measurement,"
        "e.g. L/100 km.* Note 2: There are two ways of indicating the fuel consumption, [[fuelConsumption]]"
        "(e.g. 8 liters per 100 km) and [[fuelEfficiency]] (e.g. 30 miles per gallon). They are"
        "reciprocal.* Note 3: Often, the absolute value is useful only when related to driving"
        'speed ("at 80 km/h") or usage pattern ("city traffic"). You can use [[valueReference]]'
        "to link the value for the fuel consumption to another value.",
    )
    modelDate: Optional[Union[List[Union[str, Any, date]], str, Any, date]] = Field(
        default=None,
        description="The release date of a vehicle model (often used to differentiate versions of the same"
        "make and model).",
    )
    vehicleTransmission: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="The type of component used for transmitting the power from a rotating power source to"
        'the wheels or other relevant component(s) ("gearbox" for cars).',
    )
    emissionsCO2: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description='The CO2 emissions in g/km. When used in combination with a QuantitativeValue, put "g/km"'
        "into the unitText property of that value, since there is no UN/CEFACT Common Code for"
        '"g/km".',
    )
    meetsEmissionStandard: Union[
        List[Union[str, AnyUrl, Any]], str, AnyUrl, Any
    ] = Field(
        default=None,
        description="Indicates that the vehicle meets the respective emission standard.",
    )
    payload: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The permitted weight of passengers and cargo, EXCLUDING the weight of the empty vehicle.Typical"
        "unit code(s): KGM for kilogram, LBR for pound* Note 1: Many databases specify the permitted"
        "TOTAL weight instead, which is the sum of [[weight]] and [[payload]]* Note 2: You can"
        "indicate additional information in the [[name]] of the [[QuantitativeValue]] node.*"
        "Note 3: You may also link to a [[QualitativeValue]] node that provides additional information"
        "using [[valueReference]].* Note 4: Note that you can use [[minValue]] and [[maxValue]]"
        "to indicate ranges.",
    )
    fuelCapacity: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The capacity of the fuel tank or in the case of electric cars, the battery. If there are"
        "multiple components for storage, this should indicate the total of all storage of the"
        "same type.Typical unit code(s): LTR for liters, GLL of US gallons, GLI for UK / imperial"
        "gallons, AMH for ampere-hours (for electrical vehicles).",
    )
    wheelbase: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The distance between the centers of the front and rear wheels.Typical unit code(s):"
        "CMT for centimeters, MTR for meters, INH for inches, FOT for foot/feet",
    )
    vehicleIdentificationNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The Vehicle Identification Number (VIN) is a unique serial number used by the automotive"
        "industry to identify individual motor vehicles.",
    )
    vehicleInteriorType: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The type or material of the interior of the vehicle (e.g. synthetic fabric, leather,"
        "wood, etc.). While most interior types are characterized by the material used, an interior"
        "type can also be based on vehicle usage or target audience.",
    )
    vehicleEngine: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Information about the engine or engines of the vehicle.",
    )
    numberOfDoors: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The number of doors.Typical unit code(s): C62",
    )
    vehicleInteriorColor: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The color or color combination of the interior of the vehicle.",
    )
    driveWheelConfiguration: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The drive wheel configuration, i.e. which roadwheels will receive torque from the vehicle's"
        "engine via the drivetrain.",
    )
    numberOfAxles: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The number of axles.Typical unit code(s): C62",
    )
    vehicleSeatingCapacity: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The number of passengers that can be seated in the vehicle, both in terms of the physical"
        "space available, and in terms of limitations set by law.Typical unit code(s): C62 for"
        "persons.",
    )
    numberOfPreviousOwners: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The number of owners of the vehicle, including the current one.Typical unit code(s):"
        "C62",
    )
    purchaseDate: Optional[Union[List[Union[str, Any, date]], str, Any, date]] = Field(
        default=None,
        description="The date the item, e.g. vehicle, was purchased by the current owner.",
    )
    bodyType: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="Indicates the design and body style of the vehicle (e.g. station wagon, hatchback, etc.).",
    )
    fuelType: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="The type of fuel suitable for the engine or engines of the vehicle. If the vehicle has only"
        "one engine, this property can be attached directly to the vehicle.",
    )
    speed: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The speed range of the vehicle. If the vehicle is powered by an engine, the upper limit"
        "of the speed range (indicated by [[maxValue]]) should be the maximum speed achievable"
        "under regular conditions.Typical unit code(s): KMH for km/h, HM for mile per hour (0.447"
        "04 m/s), KNT for knot*Note 1: Use [[minValue]] and [[maxValue]] to indicate the range."
        "Typically, the minimal value is zero.* Note 2: There are many different ways of measuring"
        "the speed range. You can link to information about how the given value has been determined"
        "using the [[valueReference]] property.",
    )
    mileageFromOdometer: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The total distance travelled by the particular vehicle since its initial production,"
        "as read from its odometer.Typical unit code(s): KMT for kilometers, SMI for statute"
        "miles",
    )
    productionDate: Optional[
        Union[List[Union[str, Any, date]], str, Any, date]
    ] = Field(
        default=None,
        description="The date of production of the item, e.g. vehicle.",
    )
    knownVehicleDamages: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A textual description of known damages, both repaired and unrepaired.",
    )
    dateVehicleFirstRegistered: Optional[
        Union[List[Union[str, Any, date]], str, Any, date]
    ] = Field(
        default=None,
        description="The date of the first registration of the vehicle with the respective public authorities.",
    )
    weightTotal: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The permitted total weight of the loaded vehicle, including passengers and cargo and"
        "the weight of the empty vehicle.Typical unit code(s): KGM for kilogram, LBR for pound*"
        "Note 1: You can indicate additional information in the [[name]] of the [[QuantitativeValue]]"
        "node.* Note 2: You may also link to a [[QualitativeValue]] node that provides additional"
        "information using [[valueReference]].* Note 3: Note that you can use [[minValue]]"
        "and [[maxValue]] to indicate ranges.",
    )
    numberOfAirbags: Union[
        List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat
    ] = Field(
        default=None,
        description="The number or type of airbags in the vehicle.",
    )
    fuelEfficiency: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The distance traveled per unit of fuel used; most commonly miles per gallon (mpg) or kilometers"
        "per liter (km/L).* Note 1: There are unfortunately no standard unit codes for miles per"
        "gallon or kilometers per liter. Use [[unitText]] to indicate the unit of measurement,"
        "e.g. mpg or km/L.* Note 2: There are two ways of indicating the fuel consumption, [[fuelConsumption]]"
        "(e.g. 8 liters per 100 km) and [[fuelEfficiency]] (e.g. 30 miles per gallon). They are"
        "reciprocal.* Note 3: Often, the absolute value is useful only when related to driving"
        'speed ("at 80 km/h") or usage pattern ("city traffic"). You can use [[valueReference]]'
        "to link the value for the fuel economy to another value.",
    )
    vehicleModelDate: Optional[
        Union[List[Union[str, Any, date]], str, Any, date]
    ] = Field(
        default=None,
        description="The release date of a vehicle model (often used to differentiate versions of the same"
        "make and model).",
    )
    numberOfForwardGears: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The total number of forward gears available for the transmission system of the vehicle.Typical"
        "unit code(s): C62",
    )
    callSign: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A [callsign](https://en.wikipedia.org/wiki/Call_sign), as used in broadcasting"
        "and radio communications to identify people, radio and TV stations, or vehicles.",
    )
    vehicleConfiguration: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A short text indicating the configuration of the vehicle, e.g. '5dr hatchback ST 2.5"
        "MT 225 hp' or 'limited edition'.",
    )
    tongueWeight: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The permitted vertical load (TWR) of a trailer attached to the vehicle. Also referred"
        "to as Tongue Load Rating (TLR) or Vertical Load Rating (VLR).Typical unit code(s): KGM"
        "for kilogram, LBR for pound* Note 1: You can indicate additional information in the [[name]]"
        "of the [[QuantitativeValue]] node.* Note 2: You may also link to a [[QualitativeValue]]"
        "node that provides additional information using [[valueReference]].* Note 3: Note"
        "that you can use [[minValue]] and [[maxValue]] to indicate ranges.",
    )
    accelerationTime: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The time needed to accelerate the vehicle from a given start velocity to a given target"
        "velocity.Typical unit code(s): SEC for seconds* Note: There are unfortunately no standard"
        'unit codes for seconds/0..100 km/h or seconds/0..60 mph. Simply use "SEC" for seconds'
        "and indicate the velocities in the [[name]] of the [[QuantitativeValue]], or use [[valueReference]]"
        "with a [[QuantitativeValue]] of 0..60 mph or 0..100 km/h to specify the reference speeds.",
    )
    seatingCapacity: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The number of persons that can be seated (e.g. in a vehicle), both in terms of the physical"
        "space available, and in terms of limitations set by law.Typical unit code(s): C62 for"
        "persons",
    )
