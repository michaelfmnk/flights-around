from dataclasses import dataclass


@dataclass
class Flight:
    callsign: str
    origin: str
    origin_iata: str
    destination: str
    destination_iata: str
