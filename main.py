import logging
import six

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LaunchRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        speak_output = "Estoy lista para hornear" / "Hoy que quieres hacer?"
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class HelpIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return super().can_handle(handler_input)
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        return super().handle(handler_input)


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Hasta luego!"
        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Nos vemos!", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class HelpMeBakeExceptionHandler(AbstractExceptionHandler):
    
    def can_handle(self, handler_input, exception):
        return 'AskSdk' in exception.__class__.__name__

    def handle(self, handler_input, exception):
        speech_text = "No pude entender tus instrucciones, repite de nuevo por favor"
        return handler_input.response_builder.speak(speech_text).response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())

sb.add_request_handler(CancelAndStopIntentHandler)

sb.add_exception_handler(HelpMeBakeExceptionHandler())