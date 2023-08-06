from typing import Union, Optional

from pyrogram import raw



class ToggleGroupCallStartSubscription:
    async def toggle_group_call_start_subscription(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        subscribed: bool,
    ) -> "pyrogram.raw.base.Updates":
        """ Subscribe/Unsubscribe a scheduled group call
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call

        return await self.invoke(
            raw.functions.phone.ToggleGroupCallStartSubscription(
                call=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                ),
                subscribed=subscribed
            )
        )
