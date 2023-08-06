from .create_group_call import CreateGroupCall
from .get_group_call import GetGroupCall
from .join_group_call import JoinGroupCall
from .leave_group_call import LeaveGroupCall
from .edit_group_call_participant import EditGroupCallParticipant
from .invite_to_group_call import InviteToGroupCall
from .toggle_group_call_settings import ToggleGroupCallSettings
from .toggle_group_call_record import ToggleGroupCallRecord
from .toggle_group_call_start_subscription import ToggleGroupCallStartSubscription
from .edit_group_call_title import EditGroupCallTitle
from .export_group_call_invite import ExportGroupCallInvite
from .start_scheduled_group_call import StartScheduledGroupCall



class Phone(
    CreateGroupCall,
    GetGroupCall,
    JoinGroupCall,
    LeaveGroupCall,
    EditGroupCallParticipant,
    InviteToGroupCall,
    ToggleGroupCallSettings,
    ToggleGroupCallRecord,
    ToggleGroupCallStartSubscription,
    EditGroupCallTitle,
    ExportGroupCallInvite,
    StartScheduledGroupCall
):
    pass
