DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
UTC_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'


class ApiErrorCode:
    OK = 200
    FAILURE = 400


DRIVERS_NOTIFICATIONS = {
    # Enroll
    'APRD': (
        "Hey {driver_name} congrats! You’ve been approved for the '{campaign_name}' campaign! "
        "Please book a time ASAP to get your car wrapped."
    ),
    'REJ': (
        "Hey {driver_name} congrats! You’ve been approved for the '{campaign_name}' campaign! "
        "Please book a time ASAP to get your car wrapped."
    ),
    'REM': (
        "Hey {driver_name}, you have been removed from the '{campaign_name}' campaign. Please "
        "contact us through the FAQ section of the mobile app if you think this was an error."
    ),
    'UREM': (
        "Hey {driver_name}, you have been added back to the '{campaign_name}' campaign. Please "
        "contact us through the FAQ section of the mobile app if you think this was an error."
    ),

    # Wraps
    'WSCH': "Hey {driver_name}, your wrap appointment is booked for campaign '{campaign_name}'. "
            "Please arrive 5 minutes early to the wrap location so that we can get you in and out "
            "quickly. See you soon!",
    "WAPRD": "Hey {driver_name}, your wrap photos have been approved! Please wait for your first "
             "payment to be initiated.",
    "WREJ": "Hey {driver_name}, your wrap photos have been rejected. Please contact us if you "
            "think this was an error.",
    "EWAPRD": "Hey {driver_name}, your final wrap photos have been approved! Don't forget to "
              "submit photos of your car unwrapped too.",
    "EWREJ": "Hey {driver_name}, your final wrap photos have been rejected. Please contact us if "
             "you think this was an error.",
    "UWAPRD": "Hey {driver_name}, your unwrap photos have been approved! Please wait for your "
              "final payment to be initiated.",
    "UWREJ": "Hey {driver_name}, your unwrap photos have been rejected. Please contact us if you "
             "think this was an error.",
    # Payments
    "APAYD": "Hey {driver_name}, your first payment for the '{}' campaign is on its way to your "
             "bank account! We will send you a notification once you can push the 'start ride' "
             "button inside the app so that we can verify your hours and pay you for them.",
    "APAYF": "Hey {driver_name}, your first payment for the '{campaign_name}' campaign failed. "
             "Please check your bank account details or contact us to resolve this.",

    "FD": "Hey {driver_name}, great news! Your final payment is on its way to your bank "
          "account! We hope you enjoyed your wrap. Thanks for driving with us and we'll see you "
          "at the next campaign!",
    "FF": "Hey {driver_name}, your final payment for the '{campaign_name}' campaign failed. "
          "Please check your bank account details or contact us to resolve this.",
    "ADHOCD": "Hey {driver_name}, you've received an additional payment for the '{campaign_name}' "
              "campaign.",
    "ADHOCF": "Hey {driver_name}, your additional payment for the '{campaign_name}' campaign "
              "failed. Please check your bank account details or contact us to resolve this.",
    "FUWD": "Hey {driver_name}, your Unwrap Payment for '{campaign_name}' campaign is on its way to your bank account!",
    "FUWF": "Hey {driver_name}, your Unwrap Payment for '{campaign_name}' failed."
            "Please check your bank account details or contact us to resolve this.",
    # Campaigns
    "NEWCAMP": "Hey {driver_name}, exciting news! We have a campaign available in your area. "
               "Schedule your wrap appointment now to save your spot.",
    "WRAPAPPT": "Hey {driver_name}, quick reminder of your appointment with mobilads for your "
                "car. Please arrive 5 minutes early so we can get you in and out quickly. See "
                "you soon!",
    "OFFNOTI": "Hey {driver_name}, it's been more than 2 days since the last time you were "
               "online. Please 'start ride' again so we can verify your hours and pay you for "
               "them!",
    "2DAYS": "Hey {driver_name}, FYI your campaign is coming to an end soon! DO NOT REMOVE YOUR "
             "WRAP YET. We will follow up on the last day of the campaign with instructions to "
             "submit your final photos and receive final payment. Stay tuned!",
    "CAMPEND": "Hey {driver_name}, the '{campaign_name}' campaign has officially ended. Please "
               "submit your photos with the car wrap still on for verification in the app. Once "
               "approved, you will receive your final payment!",
    'MID_DAYS': (
        "Congrats {driver_name}!, you’re halfway done with the campaign and on your way to "
        "receiving your second payment. Keep up the great work and don't forget to hit that "
        "Start Ride button when you drive!"
    )
}

ADMINS_NOTIFICATIONS = {
    # Enroll
    "APLD": "{driver_name} has applied for the '{campaign_name}' campaign.",

    # Wraps
    "PWAPR": "{driver_name} has uploaded wrap photos for the '{campaign_name}' campaign. Waiting "
             "for your approval.",
    "PEWAPR": "{driver_name} has uploaded END wrap photos for the '{campaign_name}' campaign. "
              "Waiting for your approval.",
    "PUWAPR": "{driver_name} has uploaded UN wrap photos for the '{campaign_name}' campaign. "
              "Waiting for your approval.",

    # Payments
    "APAYF": "Advance payment for the driver '{driver_name}' has failed for the '{"
             "campaign_name}' campaign.",
    "APAYD": "Advance payment for the driver '{driver_name}' has been initiated for the '{"
             "campaign_name}' campaign..",
    "FD": "Final payment for the driver '{driver_name}' has been initiated for the '{"
          "campaign_name}' campaign.",
    "FF": "Final payment for the driver '{driver_name}' has failed for the '{campaign_name}' "
          "campaign.",
    "ADHOCD": "Adhoc payment for the driver '{driver_name}' has been initiated for the '{"
              "campaign_name}' campaign.",
    "ADHOCF": "Adhoc payment for the driver '{driver_name}' has failed for the '{campaign_name}' "
              "campaign.",
}

UPDATE_CAMPAIGN_FIELDS_STATUS = {
    'DFT': {
        'name', 'description', 'city', 'city_id', 'audience', 'description', 'start_date',
        'end_date', 'campaign_type', 'total_estimated', 'number_of_drivers', 'amount_per_car',
        'client_price', 'upfront_payment'
    },
    'ACT': {
        'name', 'description', 'audience', 'description', 'start_date', 'end_date',
        'campaign_type', 'total_estimated', 'number_of_drivers', 'amount_per_car', 'client_price',
        'upfront_payment'
    },
    'PUB': {
        'name', 'description', 'audience', 'end_date', 'campaign_type', 'total_estimated',
        'number_of_drivers', 'amount_per_car', 'client_price', 'upfront_payment'
    },
    'COM': {
        'audience', 'reports_generated'
    }
}
