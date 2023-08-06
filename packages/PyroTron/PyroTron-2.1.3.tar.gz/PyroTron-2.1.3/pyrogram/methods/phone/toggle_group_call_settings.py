from typing import Union

from pyrogram import raw



class ToggleGroupCallSettings:
    async def toggle_group_call_settings(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        reset_invite_hash: bool=False,
        join_muted: bool=False
    ) -> "pyrogram.raw.base.Updates":
        """ Toggle group call Settings
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call

        return await self.invoke(
            raw.functions.phone.ToggleGroupCallSettings(
                call=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                ),
                reset_invite_hash=reset_invite_hash,
                join_muted=join_muted
            )
        )
