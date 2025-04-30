while True:
    import requests

    def get_ip_location(ip):
        ip_url = f"http://ip-api.com/json/{ip}"
        response = requests.get(ip_url)
        data = response.json()
    
        if data["status"] == "fail":
            print("Fehler: Ungültige IP-Adresse oder Zugriff verweigert.")
            return
    
        lat, lon = data['lat'], data['lon']
    
        # Geocoding API von OpenStreetMap (Nominatim) mit User-Agent
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        geo_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&addressdetails=1"
    
        try:
            geo_response = requests.get(geo_url, headers=headers, timeout=5)
            geo_response.raise_for_status()  # Fehler werfen, falls HTTP-Fehler auftreten
            geo_data = geo_response.json()
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei der Geocoding-Anfrage: {e}")
            return
    
        address = geo_data.get("address", {})
        street = address.get("road") or address.get("pedestrian") or address.get("footway") or "Unbekannte Straße"
        house_number = address.get("house_number", "Keine Hausnummer verfügbar")
        city = address.get("city") or address.get("town") or address.get("village") or address.get("suburb") or "Unbekannte Stadt"
        postcode = address.get("postcode", "Keine Postleitzahl verfügbar")
    
        print(f"IP-Adresse: {data['query']}")
        print(f"Land: {data['country']}")
        print(f"Region: {data['regionName']}")
        print(f"Stadt: {city}")
        print(f"Straße: {street}")
        print(f"Hausnummer: {house_number}")
        print(f"Postleitzahl: {postcode}")
        print(f"Internetprovider: {data['isp']}")

    if __name__ == "__main__":
        ip = input("Gib die IP-Adresse ein: ")
        get_ip_location(ip)

        input("Drücke Enter... ")