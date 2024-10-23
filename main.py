import os

from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler
from telegram.ext.filters import LOCATION

from flights import FlightsAPI

latitude = 42.4412
longitude = 19.2626
radius_km = 150

TELEGRAM_BOT = os.getenv("TELEGRAM_BOT")
flights = FlightsAPI(
    opensky_url="https://opensky-network.org",
    adsb_url="https://api.adsbdb.com"
)

known_planes = set()


async def check_planes_around_location(context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Checking planes around location", context.job)
    planes = flights.get_planes_around_location(latitude, longitude, radius_km)
    callsigns = list(
        map(lambda plane: plane.get("callsign").strip(), planes)
    )
    print("Planes around location:", callsigns)

    results = []
    for callsign in callsigns:
        if callsign in known_planes:
            continue
        if len(callsign) == 0:
            continue
        known_planes.add(callsign)
        origin, destination = flights.get_destination_by_callsign(callsign)
        results.append((callsign, origin, destination))

    if len(results) > 0:
        message = f"Planes around you: \n"
        message += "\n".join(
            [f"{callsign} from {origin} to {destination}" for callsign, origin, destination in results]
        )
        await context.bot.send_message(context.job.chat_id, message)

    # Remove planes that are no longer in the area
    planes_outside = known_planes - set(callsigns)
    for callsign in planes_outside:
        known_planes.remove(callsign)
    print("Known planes:", known_planes)


async def update_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global latitude, longitude
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    context.bot.send_message(update.message.chat_id, f"Location updated to {latitude}, {longitude}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.job_queue.run_repeating(check_planes_around_location, interval=60, first=0, chat_id=update.message.chat_id)
    await update.message.reply_text("Started tracking planes around your location!")


def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_BOT).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters=LOCATION, callback=update_location))
    app.run_polling()


if __name__ == "__main__":
    main()
