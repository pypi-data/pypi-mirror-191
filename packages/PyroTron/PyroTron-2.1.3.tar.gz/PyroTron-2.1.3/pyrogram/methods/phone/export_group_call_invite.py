from typing import Union, Optional

from pyrogram import raw



class ExportGroupCallInvite:
    async def export_group_call_invite(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        can_self_unmute: bool=False
    ) -> "pyrogram.raw.base.phone.ExportedGroupCallInvite":
        """ Export invite link of a group call
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call

        return await self.invoke(
            raw.functions.phone.ExportGroupCallInvite(
                call=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                ),
                can_self_unmute=can_self_unmute
            )
        )
