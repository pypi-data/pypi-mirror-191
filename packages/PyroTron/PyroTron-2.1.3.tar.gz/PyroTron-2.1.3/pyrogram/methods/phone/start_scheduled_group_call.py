from typing import Union, Optional

from pyrogram import raw



class StartScheduledGroupCall:
    async def start_scheduled_group_call(
        self: "pyrogram.Client",
        chat_id: Union[int, str]
    ) -> "pyrogram.raw.base.Updates":
        """ Start a scheduled group call
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call

        return await self.invoke(
            raw.functions.phone.StartScheduledGroupCall(
                call=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                )
            )
        )
