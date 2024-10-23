from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler

from config import Config, load_config
from flights import FlightsAPI, Flight
from log import logger

config: Config = load_config()
flights = FlightsAPI(
    opensky_url=config.opensky_url,
    adsb_url=config.adsb_url
)

known_planes = set()


async def check_planes_around_location(context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Checking planes around location", extra={"job": context.job})

    planes = flights.get_planes_around_location(config.latitude, config.longitude, config.radius_km)
    callsigns = list(map(lambda plane: plane.get("callsign").strip(), planes))
    logger.info("Planes around location", extra={"callsigns": callsigns})

    results: list[Flight] = []
    for callsign in callsigns:
        if callsign in known_planes:
            continue
        if len(callsign) == 0:
            continue
        known_planes.add(callsign)
        flight = flights.get_destination_by_callsign(callsign)
        if flight:
            results.append(flight)

    if results:
        message = "Planes around you:\n" + "\n".join(
            [f"{flight.callsign} from {flight.origin} to {flight.destination}" for flight in results]
        )
        await context.bot.send_message(context.job.chat_id, message)

    # Remove planes that are no longer in the area
    planes_outside = known_planes - set(callsigns)
    for callsign in planes_outside:
        known_planes.remove(callsign)
    logger.info("Known planes updated", extra={"known_planes": list(known_planes)})


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.job_queue.run_repeating(check_planes_around_location, interval=10, first=0, chat_id=update.message.chat_id)
    await update.message.reply_text("Started tracking planes around your location!")


def main() -> None:
    app = ApplicationBuilder().token(config.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    main()
