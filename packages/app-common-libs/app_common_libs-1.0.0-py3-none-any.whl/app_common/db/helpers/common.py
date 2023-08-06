import json
from datetime import datetime

from app_common.constants import DATE_FORMAT, DATETIME_FORMAT
from app_common.db.common import DriverStatus, seconds_to_hm
from app_common.db.models import (
    CampaignActivityModel, CampaignDriverModel, CampaignModel, CampaignTransitionStatus,
    DriverUserModel
)
from app_common.logger import Logger

UNWRAP_SCHEDULED = CampaignTransitionStatus.UNWRAP_SCHEDULED
WRAP_SCHEDULES = CampaignTransitionStatus.WRAP_SCHEDULED
WRAP_SCHEDULE_CSV_HEADER = [
    'Campaign name',
    'Brand',
    'Campaign city',
    'Driver name',
    'Driver Email',
    'Driver Phone no',
    'Car Maker',
    'Car Model',
    'Car Type',
    'Car Color',
    'Car Year',
    'Car Registration No',
    'Time Driven',
    'Wrap/Unwrap booked on',
    'Wrap/Unwrap type',
    'Wrap/Unwrap date',
    'Wrap/Unwrap slot',
    'Wrap/Unwrap location'
]
DRIVER_DETAILS_CSV_HEADER = [
    'Driver Name',
    'Driver Email',
    'Driver Phone no',
    'Driver added on',
    'Driver City',
    'Driver Score',
    'Car Maker',
    'Car Model',
    'Car Type',
    'Car Color',
    'Car Year',
    'Car Registration No',
]

logger = Logger.create_logger(__name__)


def get_file_key(query_type, campaign_id, today_date):
    if campaign_id:
        return f'brands/campaigns/{campaign_id}/{query_type.lower()}/{today_date}.csv'
    else:
        return f'brands/campaigns/{query_type.lower()}/{today_date}.csv'


def create_wrap_schedule_data(campaign_id):
    if not campaign_id:
        raise Exception('Campaign id is required to generate CSV report')
    wrap_schedule_info = [WRAP_SCHEDULE_CSV_HEADER]
    campaign = CampaignModel.get(campaign_id)

    campaign_name = campaign.name
    campaign_city = campaign.city
    campaign_brand = campaign.brand.name

    appointments_activity = CampaignActivityModel.filter(
        CampaignActivityModel.campaign_id == campaign_id,
        CampaignActivityModel.status.in_((
            WRAP_SCHEDULES, UNWRAP_SCHEDULED
        ))
    ).order_by(CampaignActivityModel.id.desc())

    latest_appointments = set()
    processed_users = []
    for appointment in appointments_activity:
        user_id = appointment.user_id
        campaign_driver = CampaignDriverModel.get_filter(
            CampaignDriverModel.campaign_id == campaign_id,
            CampaignDriverModel.user_id == user_id
        )
        if user_id not in latest_appointments:
            latest_appointments.add(user_id)
            user = appointment.user
            processed_users.append(user.id)
            first_name = user.first_name
            last_name = user.last_name

            row = [
                campaign_name,
                campaign_brand,
                campaign_city,
                f'{first_name} {last_name}',
                user.email,
                user.phone,
                *get_car_details(user.car),
                campaign_driver and seconds_to_hm(campaign_driver.total_time_driven) or '',
                appointment.created_at and datetime.strptime(
                    appointment.created_at, DATETIME_FORMAT
                ).strftime(DATE_FORMAT),
                appointment.status == WRAP_SCHEDULES and 'Wrap' or 'UnWrap',
                appointment.meta_data.get('appointment_date'),
                appointment.meta_data.get('appointment_time'),
                appointment.meta_data.get('location_address'),
            ]
            print(row)
            wrap_schedule_info.append(row)
    # Get all campaign driver apart from the drivers who's appointment is scheduled
    campaign_drivers = CampaignDriverModel.filter(
        CampaignDriverModel.campaign_id == campaign_id,
        CampaignDriverModel.active_status == DriverStatus.ACTIVE,
        CampaignDriverModel.user_id.notin_(processed_users)
    )
    for campaign_driver in campaign_drivers:
        user = campaign_driver.user
        first_name = user.first_name
        last_name = user.last_name
        row = [
            campaign_name,
            campaign_brand,
            campaign_city,
            f'{first_name} {last_name}',
            user.email,
            user.phone,
            *get_car_details(user.car),
            seconds_to_hm(campaign_driver.total_time_driven),
            '', '', '', '', '',
        ]
        print(row)
        wrap_schedule_info.append(row)
    return wrap_schedule_info


def create_drivers_details_data(campaign_id=None):
    drivers_details_data = [DRIVER_DETAILS_CSV_HEADER]
    if campaign_id:
        logger.info('Campaign specific driver list will be available soon')
        raise Exception('Campaign specific driver list will be available soon')
    driver_list = DriverUserModel.query().with_entities(
        DriverUserModel.first_name, DriverUserModel.last_name, DriverUserModel.email, DriverUserModel.phone,
        DriverUserModel.created_at, DriverUserModel.city, DriverUserModel.score, DriverUserModel.car
    ).all()

    if not driver_list:
        raise Exception('No Driver list available')

    for driver in driver_list:
        row = [
            f'{driver.first_name} {driver.last_name}',
            driver.email,
            driver.phone,
            driver.created_at and datetime.strptime(
                driver.created_at, DATETIME_FORMAT
            ).strftime(DATE_FORMAT),
            driver.city,
            driver.score,
            *get_car_details(driver.car),
        ]
        print(row)
        drivers_details_data.append(row)
    return drivers_details_data


def get_car_details(car):
    if car:
        return (
            car.get('carBrand'),
            car.get('carModel'),
            car.get('carType'),
            car.get('carColor'),
            car.get('carYear'),
            car.get('licensePlate')
        )
    return [''] * 6


def format_car_details(car_details):
    """
    Function returns flat car details for the json object
    """
    if isinstance(car_details, str):
        car_details = json.loads(car_details)
    if isinstance(car_details, dict):
        details = [f"{key.capitalize()}:- {value}" for key, value in car_details.items()]
        return ',\n'.join(details)
    return car_details
