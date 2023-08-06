from collections.abc import Mapping

from vxsched.event import vxEvent
from vxsched.core import vxscheduler
from vxsched.triggers import vxDailyTrigger
from vxutils import vxWrapper, logger, to_binary


@vxscheduler.event_handler("__init__")
def install_preset_event(context, event):
    for event_type, trigger_params in context.settings.events.items():
        if isinstance(trigger_params, Mapping):
            trigger = vxWrapper.init_by_config(trigger_params)
        elif isinstance(trigger_params, str):
            trigger = vxDailyTrigger(run_time=trigger_params)
        else:
            logger.error(f"不符合设置: {event_type} == {trigger_params}. ")
        preset_event = vxEvent(
            type=send_backend_event,
            data=event_type,
            trigger=trigger,
            channel="__BROKER__",
        )
        vxscheduler.submit_event(preset_event)
        logger.info(f"提交预设事件: {preset_event.type} trigger dt {preset_event.trigger_dt}")


@vxscheduler.event_handler("send_backend_event")
def send_backend_event(context, event):
    backend_event = vxEvent(type=event.data, channel="__BROKER__")
    context.backend_sender.send_multipart(
        [to_binary(backend_event.channel), vxEvent.pack(backend_event)]
    )
