import logging
from telegram import Update
from telegram.ext import ContextTypes, ChatMemberHandler
from config import CHANNEL_ID, CHANNEL_LINK


async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f"处理新成员监听器生效")
    if update.chat_member.new_chat_member.status == 'member':
        user = update.chat_member.new_chat_member.user
        username = f"@{user.username}" if user.username else user.first_name
        chat_id = update.chat_member.chat.id

        logging.info(f"处理新成员：{username}，用户ID：{user.id}，群组ID：{chat_id}")
        # 发送欢迎消息
        try:
            message = await send_message(
                context.bot,
                chat_id,
                (
                    f"✨ 欢迎 {username} 加入我们的群组！\n\n"
                    f"为确保你不错过精彩内容，请在 **60秒内** 订阅我们的频道 [ClawCloud]({CHANNEL_LINK})。\n"
                    f"订阅完成后，你就可以畅聊无阻啦！\n\n"
                    f"⏳ 还在等什么？快行动吧！"
                ),
            )
        except Exception as e:
            logging.error(f"发送欢迎消息失败: {e}")
            return

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

    try:
        # 检查用户是否已订阅频道
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ['member', 'administrator', 'creator']:
            # 未订阅，移出群组
            warning_message = await send_message(
                context.bot,
                chat_id,
                (
                    f"很抱歉 {username}，你没有完成频道订阅。\n\n"
                    f"为了维护群组的秩序，我们不得不暂时移除你。\n"
                    f"请订阅频道 [ClawCloud]({CHANNEL_LINK}) 后再加入！"
                ),
            )
            await context.bot.kick_chat_member(chat_id, user_id)
            schedule_message_deletion(context, chat_id, warning_message.message_id)
        else:
            # 已订阅，发送成功欢迎信息
            success_message = await send_message(
                context.bot,
                chat_id,
                (
                    f"太棒了！{username} 已成功订阅我们的频道！\n\n"
                    f"你现在可以随时畅聊，享受群组的互动乐趣啦！"
                ),
            )
            schedule_message_deletion(context, chat_id, success_message.message_id)
    except Exception as e:
        logging.error(f"检查用户订阅状态时出现问题: {e}")
        await send_message(context.bot, chat_id, f"出现错误: {e}")
    finally:
        # 删除最初的欢迎消息
        await delete_message(context, chat_id, message_id)


async def send_message(bot, chat_id: int, text: str) -> object:
    """发送消息的通用函数"""
    try:
        return await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"发送消息时出错：{e}")
        raise


async def delete_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int) -> None:
    """删除指定的消息"""
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logging.error(f"删除消息时出现问题：{e}")


def schedule_message_deletion(context, chat_id: int, message_id: int, delay: int = 30) -> None:
    """定时删除消息的通用函数"""
    context.job_queue.run_once(
        delete_message,
        delay,
        data={"chat_id": chat_id, "message_id": message_id},
    )


# ChatMemberHandler 实例
handle_new_member_handler = ChatMemberHandler(handle_new_member, ChatMemberHandler.CHAT_MEMBER)