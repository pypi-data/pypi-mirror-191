from typing import Union, Optional

from pyrogram import raw



class SetCallRating:
    async def set_call_rating(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        rating: int,
        comment: str,
        user_initiative: bool=False
    ) -> "pyrogram.raw.base.Updates":
        """ Rate a call
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call

        return await self.invoke(
            raw.functions.phone.SetCallRating(
                peer=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                ),
                rating=rating,
                comment=comment,
                user_initiative=user_initiative
            )
        )
