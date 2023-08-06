from typing import Union, Optional

from pyrogram import raw



class ToggleGroupCallRecord:
    async def toggle_group_call_record(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        start: bool=True,
        video: bool=True,
        title: bool=None,
        video_portrait: bool=True
    ) -> "pyrogram.raw.base.Updates":
        """ Toggle group call record start/stop
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call

        return await self.invoke(
            raw.functions.phone.ToggleGroupCallRecord(
                call=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                ),
                start=start,
                video=video,
                title=title,
                video_portrait=video_portrait
            )
        )
