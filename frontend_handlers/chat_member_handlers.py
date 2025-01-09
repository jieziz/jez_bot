from telegram import Update
from telegram.ext import ContextTypes, ChatMemberHandler
from config import CHANNEL_ID, CHANNEL_LINK  # 确保 CHANNEL_LINK 是频道的链接

async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.chat_member.new_chat_member.status == 'member':
        user = update.chat_member.new_chat_member.user
        username = f"@{user.username}" if user.username else user.first_name
        chat_id = update.chat_member.chat.id

        # 发送欢迎消息，包含频道的链接
        message = await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"✨ 欢迎 {username} 加入我们的群组！\n\n"
                f"为确保你不错过精彩内容，请在 **60秒内** 订阅我们的频道 [ClawCloud]({CHANNEL_LINK})。\n"
                f"订阅完成后，你就可以畅聊无阻啦！🚀\n\n"
                f"⏳ 还在等什么？快行动吧！"
            ),
            parse_mode='Markdown'
        )

        # 设置定时器检查是否关注频道
        context.job_queue.run_once(
            kick_member_if_not_subscribed,
            60,  # 60秒后执行
            data={"chat_id": chat_id, "user_id": user.id, "message_id": message.message_id, "username": username}
        )

async def kick_member_if_not_subscribed(context: ContextTypes.DEFAULT_TYPE) -> None:
    job_data = context.job.data
    chat_id = job_data["chat_id"]
    user_id = job_data["user_id"]
    username = job_data["username"]
    message_id = job_data["message_id"]
    bot = context.bot

    try:
        # 检查用户是否关注了频道
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ['member', 'administrator', 'creator']:
            # 未关注，移出群组
            await bot.kick_chat_member(chat_id, user_id)
            warning_message = await bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🚨 很抱歉 {username}，你没有完成频道订阅。\n\n"
                    f"为了维护群组的秩序，我们不得不暂时移除你。\n"
                    f"📢 下次记得订阅频道 [ClawCloud]({CHANNEL_LINK}) 后再加入哦！\n\n"
                    f"期待未来再次见到你！🌟"
                ),
                parse_mode='Markdown'
            )
            # 删除未关注的消息 30秒后
            context.job_queue.run_once(
                delete_message,
                30,
                data={"chat_id": chat_id, "message_id": warning_message.message_id}
            )
        else:
            # 已关注，发送欢迎信息
            success_message = await bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🎉 太棒了！{username} 已成功订阅我们的频道！\n\n"
                    f"你现在可以随时畅聊，享受群组的互动乐趣啦！\n"
                    f"🤝 有任何问题，请随时与管理员联系。祝你玩得愉快！"
                )
            )
            # 删除已关注的消息 30秒后
            context.job_queue.run_once(
                delete_message,
                30,
                data={"chat_id": chat_id, "message_id": success_message.message_id}
            )
    except Exception as e:
        await bot.send_message(
            chat_id=chat_id,
            text=f"检查用户订阅状态时出现问题：{e}"
        )

    # 删除欢迎消息
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

async def delete_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """删除指定的消息"""
    job_data = context.job.data
    chat_id = job_data["chat_id"]
    message_id = job_data["message_id"]
    bot = context.bot

    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        # 捕获删除消息时的异常，例如消息可能已经被删除
        print(f"删除消息时出现问题：{e}")

# ChatMemberHandler 实例
handle_new_member_handler = ChatMemberHandler(handle_new_member, ChatMemberHandler.CHAT_MEMBER)
