from handlers.start import register_start_handlers
from handlers.delivery import register_delivery_handlers
from handlers.contact import register_contact_handlers
from handlers.messaging import register_messaging_handlers
from handlers.forwarding import register_forwarding_handlers
from handlers.conversion import register_conversion_handlers

def register_handlers(bot):
    register_start_handlers(bot)
    register_delivery_handlers(bot)
    register_contact_handlers(bot)
    register_messaging_handlers(bot)
    register_forwarding_handlers(bot)
    register_conversion_handlers(bot)