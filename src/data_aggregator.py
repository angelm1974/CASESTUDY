from src.logger import setup_logging

class DataAggregator:
    def __init__(self):
        self.logger = setup_logging()

    def aggregate(self, data):
        if not data:
            self.logger.warning("Brak danych do agregacji.")
            return

        temperatures = []
        pressures = []
        humidities = []

        for station in data:
            try:
                if station.get('temperatura'):
                    temperatures.append(float(station['temperatura']))
                if station.get('cisnienie'):
                    pressures.append(float(station['cisnienie']))
                if station.get('wilgotnosc_wzgledna'):
                    humidities.append(float(station['wilgotnosc_wzgledna']))
            except (ValueError, TypeError):
                continue

        result = {
            'stations_count': len(data),
            'temperature': self._calculate_stats(temperatures, "temperatura"),
            'pressure': self._calculate_stats(pressures, "ciśnienie"),
            'humidity': self._calculate_stats(humidities, "wilgotność")
        }
        self._log_results(result)
        return result

    def _calculate_stats(self, values, metric_name):
        if not values:
            return {"avg": None, "max": None, "min": None}
        return {
            "avg": sum(values) / len(values),
            "max": max(values),
            "min": min(values)
        }

    def _log_results(self, result):
        self.logger.info(f"Liczba stacji: {result['stations_count']}")
        for metric, stats in result.items():
            if metric == 'stations_count':
                continue
            if stats['avg'] is not None:
                self.logger.info(f"Średnia {metric}: {stats['avg']:.1f}")
                self.logger.info(f"Maksymalna {metric}: {stats['max']:.1f}")
                self.logger.info(f"Minimalna {metric}: {stats['min']:.1f}")
            else:
                self.logger.info(f"Brak danych dla {metric}")