from typing import Union, Optional

from pyrogram import raw



class SaveDefaultGroupCallJoinAs:
    async def save_default_group_call_join_as(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        join_as: Union[int, str],
    ) -> bool:
        """ Set the default peer that will be used to 
            join a group call in a specific dialog
        """
        peer = await self.resolve_peer(chat_id)
        join_as_peer = await self.resolve_peer(join_as)

        return await self.invoke(
            raw.functions.phone.SaveDefaultGroupCallJoinAs(
                peer=peer,
                join_as=join_as_peer
            )
        )
