from telegram import Update
from telegram.ext import ContextTypes, ChatMemberHandler
from config import CHANNEL_ID

async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.chat_member.new_chat_member.status == 'member':
        user_id = update.chat_member.new_chat_member.user.id
        chat_id = update.chat_member.chat.id

        # 发送欢迎消息
        message = await context.bot.send_message(
            chat_id=chat_id,
            text=f"欢迎新成员！请在60秒内关注频道 {CHANNEL_ID}，否则将被移出群组。"
        )

        # 设置定时器检查是否关注频道
        context.job_queue.run_once(
            kick_member_if_not_subscribed,
            60,  # 60秒后执行
            data={"chat_id": chat_id, "user_id": user_id, "message_id": message.message_id}
        )

async def kick_member_if_not_subscribed(context: ContextTypes.DEFAULT_TYPE) -> None:
    job_data = context.job.data
    chat_id = job_data["chat_id"]
    user_id = job_data["user_id"]
    message_id = job_data["message_id"]
    bot = context.bot

    try:
        # 检查用户是否关注了频道
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ['member', 'administrator', 'creator']:
            # 未关注，移出群组
            await bot.kick_chat_member(chat_id, user_id)
            await bot.send_message(chat_id=chat_id, text=f"用户 {user_id} 未关注频道，已被移出群组。")
        else:
            # 已关注，发送欢迎信息
            await bot.send_message(chat_id=chat_id, text=f"用户 {user_id} 已关注频道，欢迎加入！")
    except Exception as e:
        await bot.send_message(chat_id=chat_id, text=f"检查用户订阅状态时出错: {e}")

    # 删除欢迎消息
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

# ChatMemberHandler 实例
handle_new_member_handler = ChatMemberHandler(handle_new_member, ChatMemberHandler.CHAT_MEMBER)
