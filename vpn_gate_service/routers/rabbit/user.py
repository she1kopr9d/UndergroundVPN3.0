import faststream.rabbit.fastapi

import schemas.telegram
import database.io.telegram_user
import database.io.finance_account
import database.io.referrals
import database.models
import config


router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.subscriber("start_command")
async def handle_start(data: schemas.telegram.StartData):
    print("Start command")
    status = ""
    referrer: None | schemas.telegram.UserAllData = None
    if await database.io.telegram_user.telegram_user_exist(data):
        status = "user already exists"
    else:
        if data.referrer_user_id is not None:
            referrer = await database.io.telegram_user.get_telegram_user_data(
                data.referrer_user_id,
            )
            user = await database.io.telegram_user.create_telegram_user(
                data,
                referrer.id,
            )
            await database.io.finance_account.create_finance_account(user.id)
            await router.broker.publish(
                {
                    "referrer_user_id": referrer.user_id,
                    "referral_username": data.username,
                },
                queue="new_referral",
            )
        else:
            user = await database.io.telegram_user.create_telegram_user(data)
            await database.io.finance_account.create_finance_account(user.id)
        status = "registered"

    await router.broker.publish(
        {
            "user_id": data.user_id,
            "status": status,
            "is_referral": referrer is not None,
            "referrer_username": (referrer.username if referrer else None),
        },
        queue="start_command_answer",
    )


@router.subscriber("profile_command")
async def profile_command_hadler(
    data: schemas.telegram.ProfileData,
):
    user_data: schemas.telegram.UserAllData = (
        await database.io.telegram_user.get_telegram_user_data(
            user_id=data.user_id,
        )
    )
    finance_account: database.models.FinanceAccount = (
        await database.io.finance_account.get_finance_account(
            user_id=user_data.id,
        )
    )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "username": data.username,
            "referral_percentege": finance_account.referral_percent,
            "balance": finance_account.balance,
        },
        queue="profile_command_answer",
    )


@router.subscriber("ref_command")
async def ref_command_handler(data: schemas.telegram.RefPage):
    referrals, max_page = (
        await database.io.referrals.get_referrals_with_pagination(data)
    )
    referral_percentage = (
        await database.io.finance_account.get_referral_percentage(data.user_id)
    )
    referrer_username = await database.io.telegram_user.get_referrer_username(
        data.user_id
    )

    await router.broker.publish(
        {
            "user_id": data.user_id,
            "referrals": referrals if len(referrals) > 0 else None,
            "referral_percentage": referral_percentage,
            "referrer_username": referrer_username,
            "max_page": max_page,
            "now_page": data.page,
            "message_id": data.message_id,
        },
        queue="ref_command_answer",
    )
