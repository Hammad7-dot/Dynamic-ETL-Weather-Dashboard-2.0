from database.repository import WeatherRepository


def health_check():
    repo = WeatherRepository()

    try:
        df = repo.get_all()
        return {"status": "healthy", "records": len(df)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
