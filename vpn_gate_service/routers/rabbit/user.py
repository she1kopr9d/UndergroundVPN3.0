import config
import database.io.base
import database.io.config
import database.io.finance_account
import database.io.referrals
import database.io.telegram_user
import database.models
import faststream.rabbit.fastapi
import logic.server_query
import logic.server_session
import schemas.config
import schemas.servers
import schemas.telegram

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


@router.subscriber("conf_command")
async def conf_command_handler(data: schemas.telegram.RefPage):
    configs, max_page = await database.io.config.get_configs_with_pagination(
        data
    )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "message_id": data.message_id,
            "configs": configs,
            "max_page": max_page,
            "now_page": data.page,
        },
        queue="conf_command_answer",
    )


@router.subscriber("conf_info_command")
async def conf_info_handler(
    data: schemas.config.ConfigGetInfo,
):
    config_obj: database.models.Config = (
        await database.io.base.get_object_by_id(
            id=data.config_id,
            object_class=database.models.Config,
        )
    )
    server_obj: database.models.Server = (
        await database.io.base.get_object_by_id(
            id=config_obj.server_id,
            object_class=database.models.Server,
        )
    )
    server_data: schemas.servers.ServerPublicInfo = (
        logic.server_session.get_active_server(server_obj.name)
    )
    conf_url = await logic.server_query.create_config_url(
        user_uuid=config_obj.uuid,
        user_email=logic.server_query.get_user_email(config_obj.name),
        server_data=server_data,
    )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "message_id": data.message_id,
            "config_id": data.config_id,
            "config_name": config_obj.name,
            "config_url": conf_url,
            "server_id": server_obj.id,
            "server_name": server_obj.name,
            "now_page": data.now_page,
        },
        queue="conf_info_command_answer",
    )


@router.subscriber("delete_config_command")
async def conf_delete_handler(
    data: schemas.config.ConfigGetInfo,
):
    config_obj: database.models.Config = (
        await database.io.base.get_object_by_id(
            id=data.config_id,
            object_class=database.models.Config,
        )
    )
    server_obj: database.models.Server = (
        await database.io.base.get_object_by_id(
            id=config_obj.server_id,
            object_class=database.models.Server,
        )
    )
    server_data: schemas.servers.ServerPublicInfo = (
        logic.server_session.get_active_server(server_obj.name)
    )
    await logic.server_query.delete_config(
        data,
        server_data,
        config_obj,
    )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "message_id": data.message_id,
        },
        queue="delete_config_command_answer",
    )


@router.subscriber("handle_add")
async def handle_add_handler(
    data: schemas.telegram.UserData,
):
    await database.io.telegram_user.set_handle(data)
    await router.broker.publish(
        {
            "user_id": data.user_id,
        },
        queue="handle_add_answer",
    )
