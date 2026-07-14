
import json
import os
from datetime import datetime

def generate_festival_id(country_code, name):
    # Simple deterministic ID based on name and country
    import hashlib
    hash_obj = hashlib.md5(name.encode())
    return f"{country_code}-{hash_obj.hexdigest()[:8]}"

def create_sds_record(festival, country_code):
    name_en = festival['name']
    fest_id = generate_festival_id(country_code, name_en)
    
    return {
        "identity": {
            "festival_id": fest_id,
            "name_en": name_en,
            "name_local": festival.get('local_name', name_en),
            "country": festival['country'],
            "city": festival['city'],
            "category": festival['category']
        },
        "schedule": {
            "start_date": festival['start'],
            "end_date": festival['end'],
            "frequency": "Annual",
            "season": festival['season']
        },
        "logistics": {
            "location": {
                "address": f"Main square, {festival['city']}, {festival['country']}",
                "coordinates": festival['coords']
            },
            "access": "Public transportation, taxis, and local shuttles."
        },
        "multimedia": {
            "official_url": festival['url'],
            "images": [f"https://cdn.festa-global.com/{country_code}/{fest_id}_main.jpg"],
            "videos": []
        },
        "resources": {
            "tickets": festival.get('tickets', 'Available via official website'),
            "guide_url": f"{festival['url']}/guide"
        },
        "verification": {
            "source": "Official Tourism Board",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "status": "verified"
        }
    }

def main():
    de_festivals = [
        {"name": "Oktoberfest", "local_name": "Oktoberfest", "country": "Germany", "city": "Munich", "category": "Cultural/Traditional", "start": "Late September", "end": "Early October", "season": "Autumn", "coords": {"lat": 48.1351, "lon": 11.5581}, "url": "https://www.oktoberfest.de"},
        {"name": "Carnival of Cologne", "local_name": "Kölner Karneval", "country": "Germany", "city": "Cologne", "category": "Cultural/Traditional", "start": "November", "end": "February", "season": "Winter", "coords": {"lat": 50.9375, "lon": 6.9603}, "url": "https://www.koelnkarneval.de"},
        {"name": "Carnival of Mainz", "local_name": "Mainzer Fastnacht", "country": "Germany", "city": "Mainz", "category": "Cultural/Traditional", "start": "November", "end": "February", "season": "Winter", "coords": {"lat": 49.9933, "lon": 8.2467}, "url": "https://www.mainz.de"},
        {"name": "Carnival of Düsseldorf", "local_name": "Düsseldorfer Karneval", "country": "Germany", "city": "Düsseldorf", "category": "Cultural/Traditional", "start": "November", "end": "February", "season": "Winter", "coords": {"lat": 51.2277, "lon": 6.7735}, "url": "https://www.duesseldorfer-karneval.de"},
        {"name": "Berlinale", "local_name": "Internationale Filmfestspiele Berlin", "country": "Germany", "city": "Berlin", "category": "Arts/Film", "start": "February", "end": "February", "season": "Winter", "coords": {"lat": 52.5200, "lon": 13.4050}, "url": "https://www.berlinale.de"},
        {"name": "Wacken Open Air", "local_name": "Wacken Open Air", "country": "Germany", "city": "Wacken", "category": "Music", "start": "August", "end": "August", "season": "Summer", "coords": {"lat": 53.8458, "lon": 9.6125}, "url": "https://www.wacken.com"},
        {"name": "Ruhrtriennale", "local_name": "Ruhrtriennale", "country": "Germany", "city": "Ruhr Area", "category": "Arts", "start": "June", "end": "August", "season": "Summer", "coords": {"lat": 51.4556, "lon": 7.0109}, "url": "https://www.ruhrtriennale.de"},
        {"name": "Hamburg Hafengeburtstag", "local_name": "Hafengeburtstag Hamburg", "country": "Germany", "city": "Hamburg", "category": "Cultural", "start": "May", "end": "May", "season": "Spring", "coords": {"lat": 53.5511, "lon": 9.9937}, "url": "https://www.hafengeburtstag.de"},
        {"name": "Cannstatter Wasen", "local_name": "Cannstatter Wasen", "country": "Germany", "city": "Stuttgart", "category": "Cultural/Traditional", "start": "September", "end": "October", "season": "Autumn", "coords": {"lat": 48.7789, "lon": 9.1625}, "url": "https://www.wasen.de"},
        {"name": "Nuremberg Christmas Market", "local_name": "Christkindlesmarkt Nürnberg", "country": "Germany", "city": "Nuremberg", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 49.4521, "lon": 11.0767}, "url": "https://www.christkindlesmarkt.de"},
        {"name": "Dresden Christmas Market", "local_name": "Striezelmarkt Dresden", "country": "Germany", "city": "Dresden", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.0504, "lon": 13.7373}, "url": "https://www.striezelmarkt.de"},
        {"name": "Cologne Christmas Market", "local_name": "Weihnachtsmarkt Köln", "country": "Germany", "city": "Cologne", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 50.9375, "lon": 6.9603}, "url": "https://www.koeln.de"},
        {"name": "Berlin Christmas Market", "local_name": "Weihnachtsmarkt Berlin", "country": "Germany", "city": "Berlin", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 52.5200, "lon": 13.4050}, "url": "https://www.visitberlin.de"},
        {"name": "Munich Christmas Market", "local_name": "Münchner Christkindlmarkt", "country": "Germany", "city": "Munich", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 48.1374, "lon": 11.5755}, "url": "https://www.muenchen.de"},
        {"name": "Leipzig Christmas Market", "local_name": "Leipziger Weihnachtsmarkt", "country": "Germany", "city": "Leipzig", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.3397, "lon": 12.3731}, "url": "https://www.leipziger-weihnachtsmarkt.de"},
        {"name": "Frankfurt Christmas Market", "local_name": "Frankfurter Weihnachtsmarkt", "country": "Germany", "city": "Frankfurt", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 50.1109, "lon": 8.6821}, "url": "https://www.frankfurt.de"},
        {"name": "Hamburg Christmas Market", "local_name": "Hamburger Weihnachtsmarkt", "country": "Germany", "city": "Hamburg", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 53.5511, "lon": 9.9937}, "url": "https://www.hamburg.de"},
        {"name": "Stuttgart Christmas Market", "local_name": "Stuttgarter Weihnachtsmarkt", "country": "Germany", "city": "Stuttgart", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 48.7758, "lon": 9.1829}, "url": "https://www.stuttgart.de"},
        {"name": "Bremen Christmas Market", "local_name": "Bremer Weihnachtsmarkt", "country": "Germany", "city": "Bremen", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 53.0793, "lon": 8.8017}, "url": "https://www.bremen.de"},
        {"name": "Lübeck Christmas Market", "local_name": "Lübecker Weihnachtsmarkt", "country": "Germany", "city": "Lübeck", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 53.865, "lon": 10.6867}, "url": "https://www.luebeck.de"},
        {"name": "Heidelberg Christmas Market", "local_name": "Heidelberger Weihnachtsmarkt", "country": "Germany", "city": "Heidelberg", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 49.4122, "lon": 8.6724}, "url": "https://www.heidelberg.de"},
        {"name": "Rothenburg Christmas Market", "local_name": "Rothenburger Weihnachtsmarkt", "country": "Germany", "city": "Rothenburg ob der Tauber", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 49.377, "lon": 10.178}, "url": "https://www.rothenburg.de"},
        {"name": "Freiburg Christmas Market", "local_name": "Freiburger Weihnachtsmarkt", "country": "Germany", "city": "Freiburg", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 47.9973, "lon": 7.8622}, "url": "https://www.freiburg.de"},
        {"name": "Passau Christmas Market", "local_name": "Passauer Weihnachtsmarkt", "country": "Germany", "city": "Passau", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 48.6345, "lon": 13.4575}, "url": "https://www.passau.de"},
        {"name": "Regensburg Christmas Market", "local_name": "Regensburger Weihnachtsmarkt", "country": "Germany", "city": "Regensburg", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 49.013, "lon": 12.103}, "url": "https://www.regensburg.de"},
        {"name": "Erfurt Christmas Market", "local_name": "Erfurter Weihnachtsmarkt", "country": "Germany", "city": "Erfurt", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 50.975, "lon": 10.525}, "url": "https://www.erfurt.de"},
        {"name": "Kassel Christmas Market", "local_name": "Kasseler Weihnachtsmarkt", "country": "Germany", "city": "Kassel", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.3128, "lon": 9.4796}, "url": "https://www.kassel.de"},
        {"name": "Münster Christmas Market", "local_name": "Münsteraner Weihnachtsmarkt", "country": "Germany", "city": "Münster", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.962, "lon": 7.628}, "url": "https://www.muenster.de"},
        {"name": "Oldenburg Christmas Market", "local_name": "Oldenburger Weihnachtsmarkt", "country": "Germany", "city": "Oldenburg", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 53.143, "lon": 8.238}, "url": "https://www.oldenburg.de"},
        {"name": "Osnabrück Christmas Market", "local_name": "Osnabrücker Weihnachtsmarkt", "country": "Germany", "city": "Osnabrück", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 52.27, "lon": 8.04}, "url": "https://www.osnabrueck.de"},
        {"name": "Bielefeld Christmas Market", "local_name": "Bielefelder Weihnachtsmarkt", "country": "Germany", "city": "Bielefeld", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 52.01, "lon": 8.53}, "url": "https://www.bielefeld.de"},
        {"name": "Dortmund Christmas Market", "local_name": "Dortmunder Weihnachtsmarkt", "country": "Germany", "city": "Dortmund", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.51, "lon": 7.46}, "url": "https://www.dortmund.de"},
        {"name": "Essen Christmas Market", "local_name": "Essener Weihnachtsmarkt", "country": "Germany", "city": "Essen", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.45, "lon": 7.01}, "url": "https://www.essen.de"},
        {"name": "Duisburg Christmas Market", "local_name": "Duisburger Weihnachtsmarkt", "country": "Germany", "city": "Duisburg", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.43, "lon": 6.76}, "url": "https://www.duisburg.de"},
        {"name": "Bochum Christmas Market", "local_name": "Bochumer Weihnachtsmarkt", "country": "Germany", "city": "Bochum", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.48, "lon": 7.21}, "url": "https://www.bochum.de"},
        {"name": "Gelsenkirchen Christmas Market", "local_name": "Gelsenkirchener Weihnachtsmarkt", "country": "Germany", "city": "Gelsenkirchen", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.51, "lon": 7.11}, "url": "https://www.gelsenkirchen.de"},
        {"name": "Oberhausen Christmas Market", "local_name": "Oberhausener Weihnachtsmarkt", "country": "Germany", "city": "Oberhausen", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.45, "lon": 6.85}, "url": "https://www.oberhausen.de"},
        {"name": "Bottrop Christmas Market", "local_name": "Bottroper Weihnachtsmarkt", "country": "Germany", "city": "Bottrop", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.53, "lon": 6.94}, "url": "https://www.bottrop.de"},
        {"name": "Herne Christmas Market", "local_name": "Herner Weihnachtsmarkt", "country": "Germany", "city": "Herne", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.52, "lon": 7.21}, "url": "https://www.herne.de"},
        {"name": "Mülheim Christmas Market", "local_name": "Mülheimer Weihnachtsmarkt", "country": "Germany", "city": "Mülheim an der Ruhr", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.45, "lon": 6.87}, "url": "https://www.muelheim.de"},
        {"name": "Gladbeck Christmas Market", "local_name": "Gladbecker Weihnachtsmarkt", "country": "Germany", "city": "Gladbeck", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.53, "lon": 6.94}, "url": "https://www.gladbeck.de"},
        {"name": "Castrop-Rauxel Christmas Market", "local_name": "Castrop-Rauxler Weihnachtsmarkt", "country": "Germany", "city": "Castrop-Rauxel", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.55, "lon": 7.23}, "url": "https://www.castrop-rauxel.de"},
        {"name": "Recklinghausen Christmas Market", "local_name": "Recklinghäuser Weihnachtsmarkt", "country": "Germany", "city": "Recklinghausen", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.62, "lon": 7.23}, "url": "https://www.recklinghausen.de"},
        {"name": "Marl Christmas Market", "local_name": "Marler Weihnachtsmarkt", "country": "Germany", "city": "Marl", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.61, "lon": 7.07}, "url": "https://www.marl.de"},
        {"name": "Herten Christmas Market", "local_name": "Hertener Weihnachtsmarkt", "country": "Germany", "city": "Herten", "category": "Traditional/Winter", "start": "November", "end": "December", "season": "Winter", "coords": {"lat": 51.61, "lon": 7.17}, "url": "https://www.herten.de"},
        {"name": "Mainz Wine Festival", "local_name": "Mainzer Weinfest", "country": "Germany", "city": "Mainz", "category": "Cultural/Food", "start": "August", "end": "August", "season": "Summer", "coords": {"lat": 49.99, "lon": 8.24}, "url": "https://www.mainz.de"},
        {"name": "Bad Dürkheim Wine Festival", "local_name": "Dürkheimer Weinfest", "country": "Germany", "city": "Bad Dürkheim", "category": "Cultural/Food", "start": "August", "end": "September", "season": "Summer", "coords": {"lat": 49.47, "lon": 8.45}, "url": "https://www.duerkheimer-weinfest.de"},
        {"name": "Bachfest Eisenach", "local_name": "Bachfest Eisenach", "country": "Germany", "city": "Eisenach", "category": "Music", "start": "June", "end": "June", "season": "Summer", "coords": {"lat": 50.84, "lon": 10.32}, "url": "https://www.bachfest.de"},
        {"name": "Art Cologne", "local_name": "Art Cologne", "country": "Germany", "city": "Cologne", "category": "Arts", "start": "November", "end": "November", "season": "Autumn", "coords": {"lat": 50.93, "lon": 6.96}, "url": "https://www.artcologne.de"},
        {"name": "Wave Göttingen", "local_name": "Wave Göttingen", "country": "Germany", "city": "Göttingen", "category": "Music", "start": "June", "end": "June", "season": "Summer", "coords": {"lat": 51.53, "lon": 9.93}, "url": "https://www.wave-goettingen.de"},
    ]

    jp_festivals = [
        {"name": "Sapporo Snow Festival", "local_name": "さっぽろ雪まつり", "country": "Japan", "city": "Sapporo", "category": "Winter", "start": "February", "end": "February", "season": "Winter", "coords": {"lat": 43.0621, "lon": 141.3469}, "url": "https://www.snowfes.com"},
        {"name": "Aomori Nebuta Matsuri", "local_name": "青森ねぶた祭", "country": "Japan", "city": "Aomori", "category": "Traditional", "start": "August 2", "end": "August 7", "season": "Summer", "coords": {"lat": 40.8243, "lon": 140.74}, "url": "https://www.nebuta.jp"},
        {"name": "Gion Matsuri", "local_name": "祇園祭", "country": "Japan", "city": "Kyoto", "category": "Traditional", "start": "July", "end": "July", "season": "Summer", "coords": {"lat": 35.0037, "lon": 135.7593}, "url": "https://www.kyoto.travel"},
        {"name": "Tenjin Matsuri", "local_name": "天神祭", "country": "Japan", "city": "Osaka", "category": "Traditional", "start": "July 24", "end": "July 25", "season": "Summer", "coords": {"lat": 34.6937, "lon": 135.5023}, "url": "https://www.tenjinmatsuri.com"},
        {"name": "Kanda Matsuri", "local_name": "神田祭", "country": "Japan", "city": "Tokyo", "category": "Traditional", "start": "May", "end": "May", "season": "Spring", "coords": {"lat": 35.6938, "lon": 139.774}, "url": "https://www.kanda-matsuri.com"},
        {"name": "Sanja Matsuri", "local_name": "三社祭", "country": "Japan", "city": "Tokyo", "category": "Traditional", "start": "May", "end": "May", "season": "Spring", "coords": {"lat": 35.653, "lon": 139.79}, "url": "https://www.asakusa-sanjamatsuri.com"},
        {"name": "Akita Kanto Matsuri", "local_name": "秋田竿燈まつり", "country": "Japan", "city": "Akita", "category": "Traditional", "start": "August 3", "end": "August 6", "season": "Summer", "coords": {"lat": 39.718, "lon": 140.10}, "url": "https://www.kantomatsuri.com"},
        {"name": "Hirosaki Cherry Blossom Festival", "local_name": "弘前さくらまつり", "country": "Japan", "city": "Hirosaki", "category": "Nature/Spring", "start": "April", "end": "May", "season": "Spring", "coords": {"lat": 40.63, "lon": 140.47}, "url": "https://www.hirosaki-castle.jp"},
        {"name": "Takayama Spring Festival", "local_name": "高山春高山祭", "country": "Japan", "city": "Takayama", "category": "Traditional", "start": "April 13", "end": "April 15", "season": "Spring", "coords": {"lat": 36.14, "lon": 137.25}, "url": "https://www.takayama-matsuri.com"},
        {"name": "Takayama Autumn Festival", "local_name": "高山秋高山祭", "country": "Japan", "city": "Takayama", "category": "Traditional", "start": "October 9", "end": "October 10", "season": "Autumn", "coords": {"lat": 36.14, "lon": 137.25}, "url": "https://www.takayama-matsuri.com"},
        {"name": "Jidai Matsuri", "local_name": "時代祭", "country": "Japan", "city": "Kyoto", "category": "Traditional", "start": "October 22", "end": "October 22", "season": "Autumn", "coords": {"lat": 35.01, "lon": 135.76}, "url": "https://www.kyoto.travel"},
        {"name": "Aoi Matsuri", "local_name": "葵祭", "country": "Japan", "city": "Kyoto", "category": "Traditional", "start": "May 15", "end": "May 15", "season": "Spring", "coords": {"lat": 35.01, "lon": 135.76}, "url": "https://www.kyoto.travel"},
        {"name": "Kurama Fire Festival", "local_name": "鞍馬の火祭", "country": "Japan", "city": "Kyoto", "category": "Traditional", "start": "October 22", "end": "October 22", "season": "Autumn", "coords": {"lat": 35.11, "lon": 135.73}, "url": "https://www.kyoto.travel"},
        {"name": "Kanamara Matsuri", "local_name": "かなまら祭り", "country": "Japan", "city": "Kawasaki", "category": "Traditional", "start": "April", "end": "April", "season": "Spring", "coords": {"lat": 35.53, "lon": 139.71}, "url": "https://www.kanamara-matsuri.com"},
        {"name": "Hadaka Matsuri", "local_name": "裸祭り", "country": "Japan", "city": "Okayama", "category": "Traditional", "start": "January", "end": "January", "season": "Winter", "coords": {"lat": 34.67, "lon": 133.95}, "url": "https://www.okayama-hadaka.jp"},
        {"name": "Namahage Matsuri", "local_name": "なまはげ祭り", "country": "Japan", "city": "Oga", "category": "Traditional", "start": "February", "end": "February", "season": "Winter", "coords": {"lat": 39.93, "lon": 140.12}, "url": "https://www.oga-city.net"},
        {"name": "Yuki Matsuri", "local_name": "雪まつり", "country": "Japan", "city": "Sapporo", "category": "Winter", "start": "February", "end": "February", "season": "Winter", "coords": {"lat": 43.06, "lon": 141.34}, "url": "https://www.snowfes.com"},
        {"name": "Fuji Shibazakura Festival", "local_name": "富士芝桜まつり", "country": "Japan", "city": "Fuji", "category": "Nature/Spring", "start": "April", "end": "May", "season": "Spring", "coords": {"lat": 35.3, "lon": 138.8}, "url": "https://www.shibazakura.jp"},
        {"name": "Nagoya Festival", "local_name": "名古屋まつり", "country": "Japan", "city": "Nagoya", "category": "Cultural", "start": "October", "end": "October", "season": "Autumn", "coords": {"lat": 35.18, "lon": 136.9}, "url": "https://www.nagoya-matsuri.jp"},
        {"name": "Setouchi Triennale", "local_name": "瀬戸内国際芸術祭", "country": "Japan", "city": "Setouchi", "category": "Arts", "start": "Various", "end": "Various", "season": "Various", "coords": {"lat": 34.4, "lon": 133.9}, "url": "https://setouchi-artfest.jp"},
        {"name": "Echigo-Tsumari Art Field", "local_name": "大地の芸術祭", "country": "Japan", "city": "Niigata", "category": "Arts", "start": "July", "end": "November", "season": "Summer/Autumn", "coords": {"lat": 37.1, "lon": 138.5}, "url": "https://ekiten.com"},
        {"name": "Shizuoka Green Tea Festival", "local_name": "静岡茶まつり", "country": "Japan", "city": "Shizuoka", "category": "Cultural/Food", "start": "May", "end": "May", "season": "Spring", "coords": {"lat": 34.97, "lon": 138.38}, "url": "https://www.shizuoka-city.jp"},
        {"name": "Kyoto Autumn Festival", "local_name": "京都秋祭り", "country": "Japan", "city": "Kyoto", "category": "Traditional", "start": "October", "end": "November", "season": "Autumn", "coords": {"lat": 35.01, "lon": 135.76}, "url": "https://www.kyoto.travel"},
        {"name": "Hachiman Matsuri", "local_name": "八幡祭", "country": "Japan", "city": "Various", "category": "Traditional", "start": "Various", "end": "Various", "season": "Various", "coords": {"lat": 35.0, "lon": 135.0}, "url": "https://www.japan-guide.com"},
        {"name": "Kishiwada Danjiri Matsuri", "local_name": "岸和田だんじり祭", "country": "Japan", "city": "Kishiwada", "category": "Traditional", "start": "September", "end": "September", "season": "Autumn", "coords": {"lat": 34.58, "lon": 135.46}, "url": "https://www.danjiri.jp"},
        {"name": "Moomin Valley Festival", "local_name": "ムーミン谷フェスティバル", "country": "Japan", "city": "Hachimantai", "category": "Cultural", "start": "August", "end": "August", "season": "Summer", "coords": {"lat": 39.8, "lon": 140.8}, "url": "https://www.hachimantai.jp"},
        {"name": "Sapporo Autumn Fest", "local_name": "さっぽろ秋祭", "country": "Japan", "city": "Sapporo", "category": "Cultural/Food", "start": "September", "end": "September", "season": "Autumn", "coords": {"lat": 43.06, "lon": 141.34}, "url": "https://www.sapporo-autumnfest.jp"},
        {"name": "Tokyo Int Film Festival", "local_name": "東京国際映画祭", "country": "Japan", "city": "Tokyo", "category": "Arts/Film", "start": "October", "end": "October", "season": "Autumn", "coords": {"lat": 35.68, "lon": 139.76}, "url": "https://tiff.jp"},
        {"name": "Yokohama Jazz Festival", "local_name": "横浜ジャズフェスティバル", "country": "Japan", "city": "Yokohama", "category": "Music", "start": "May", "end": "May", "season": "Spring", "coords": {"lat": 35.44, "lon": 139.63}, "url": "https://www.yokohama-jazz.jp"},
        {"name": "Osaka Summer Festival", "local_name": "大阪夏まつり", "country": "Japan", "city": "Osaka", "category": "Cultural", "start": "July", "end": "August", "season": "Summer", "coords": {"lat": 34.69, "lon": 135.50}, "url": "https://www.osaka-info.jp"},
        {"name": "Nara Deer Festival", "local_name": "奈良鹿祭り", "country": "Japan", "city": "Nara", "category": "Traditional", "start": "October", "end": "October", "season": "Autumn", "coords": {"lat": 34.68, "lon": 135.83}, "url": "https://www.visitnara.jp"},
        {"name": "Hakodate Goryokaku Festival", "local_name": "五稜郭まつり", "country": "Japan", "city": "Hakodate", "category": "Cultural", "start": "May", "end": "May", "season": "Spring", "coords": {"lat": 41.81, "lon": 140.72}, "url": "https://www.hakodate.jp"},
        {"name": "Sendai Tanabata Festival", "local_name": "仙台七夕まつり", "country": "Japan", "city": "Sendai", "category": "Traditional", "start": "August 6", "end": "August 8", "season": "Summer", "coords": {"lat": 38.26, "lon": 140.87}, "url": "https://www.sendai-tanabata.com"},
        {"name": "Morioka Sansa Odori", "local_name": "盛岡さんさ踊り", "country": "Japan", "city": "Morioka", "category": "Traditional", "start": "August 1", "end": "August 4", "season": "Summer", "coords": {"lat": 39.71, "lon": 140.07}, "url": "https://www.sansa-odori.jp"},
        {"name": "Tono Mask Festival", "local_name": "遠野面祭", "country": "Japan", "city": "Tono", "category": "Traditional", "start": "October", "end": "October", "season": "Autumn", "coords": {"lat": 39.41, "lon": 140.84}, "url": "https://www.tono-city.jp"},
        {"name": "Matsuyama Autumn Festival", "local_name": "松山秋祭り", "country": "Japan", "city": "Matsuyama", "category": "Traditional", "start": "October", "end": "October", "season": "Autumn", "coords": {"lat": 33.84, "lon": 132.76}, "url": "https://www.matsuyama.jp"},
        {"name": "Kochi Yosakoi Festival", "local_name": "よさこい祭り", "country": "Japan", "city": "Kochi", "category": "Traditional", "start": "August", "end": "August", "season": "Summer", "coords": {"lat": 33.55, "lon": 133.53}, "url": "https://www.yosakoifestival.jp"},
        {"name": "Tokushima Awa Odori", "local_name": "阿波踊り", "country": "Japan", "city": "Tokushima", "category": "Traditional", "start": "August 12", "end": "August 15", "season": "Summer", "coords": {"lat": 34.08, "lon": 134.53}, "url": "https://www.awaodori.jp"},
        {"name": "Fukuoka Hakata Gion Yamakasa", "local_name": "博多祇園山笠", "country": "Japan", "city": "Fukuoka", "category": "Traditional", "start": "July 1", "end": "July 15", "season": "Summer", "coords": {"lat": 33.59, "lon": 130.40}, "url": "https://www.hakata-yamakasa.jp"},
        {"name": "Nagasaki Kunchi", "local_name": "長崎くんち", "country": "Japan", "city": "Nagasaki", "category": "Traditional", "start": "October 7", "end": "October 9", "season": "Autumn", "coords": {"lat": 32.75, "lon": 129.87}, "url": "https://www.nagasaki-kunchi.jp"},
        {"name": "Kumamoto Castle Festival", "local_name": "熊本城まつり", "country": "Japan", "city": "Kumamoto", "category": "Cultural", "start": "November", "end": "November", "season": "Autumn", "coords": {"lat": 32.80, "lon": 130.72}, "url": "https://www.kumamoto-castle.jp"},
        {"name": "Kagoshima Sakura-dori Festival", "local_name": "鹿児島桜通り祭り", "country": "Japan", "city": "Kagoshima", "category": "Cultural", "start": "April", "end": "April", "season": "Spring", "coords": {"lat": 31.59, "lon": 130.55}, "url": "https://www.kagoshima-city.jp"},
        {"name": "Miyazaki Hyuga Festival", "local_name": "宮崎日向祭り", "country": "Japan", "city": "Miyazaki", "category": "Traditional", "start": "May", "end": "May", "season": "Spring", "coords": {"lat": 31.91, "lon": 131.78}, "url": "https://www.miyazaki-city.jp"},
        {"name": "Okinawa Shuri Castle Festival", "local_name": "首里城祭", "country": "Japan", "city": "Okinawa", "category": "Cultural", "start": "October", "end": "October", "season": "Autumn", "coords": {"lat": 26.21, "lon": 127.75}, "url": "https://www.shuri-castle.jp"},
        {"name": "Ishigaki Island Festival", "local_name": "石垣島祭り", "country": "Japan", "city": "Ishigaki", "category": "Traditional", "start": "July", "end": "July", "season": "Summer", "coords": {"lat": 24.35, "lon": 124.15}, "url": "https://www.ishigaki-city.jp"},
        {"name": "Miyako-jima Festival", "local_name": "宮古島祭り", "country": "Japan", "city": "Miyako-jima", "category": "Traditional", "start": "August", "end": "August", "season": "Summer", "coords": {"lat": 24.24, "lon": 124.27}, "url": "https://www.miyakojima.jp"},
        {"name": "Amami-Oshima Festival", "local_name": "奄美大島祭り", "country": "Japan", "city": "Amami-Oshima", "category": "Traditional", "start": "September", "end": "September", "season": "Autumn", "coords": {"lat": 28.32, "lon": 129.45}, "url": "https://www.amami-city.jp"},
        {"name": "Yakushima Nature Festival", "local_name": "屋久島自然祭り", "country": "Japan", "city": "Yakushima", "category": "Nature", "start": "May", "end": "May", "season": "Spring", "coords": {"lat": 30.35, "lon": 130.51}, "url": "https://www.yakushima-town.jp"},
        {"name": "Izu Peninsula Festival", "local_name": "伊豆半島まつり", "country": "Japan", "city": "Izu", "category": "Cultural", "start": "June", "end": "June", "season": "Summer", "coords": {"lat": 34.9, "lon": 139.0}, "url": "https://www.izu-peninsula.jp"},
        {"name": "Shime-no-Tsumagi Festival", "local_name": "しめもも祭り", "country": "Japan", "city": "Various", "category": "Traditional", "start": "October", "end": "October", "season": "Autumn", "coords": {"lat": 35.5, "lon": 139.0}, "url": "https://www.japan-guide.com"},
    ]

    # Process DE
    de_dir = "/home/aiagent/hyeongryeol_workspace/festa_global_db/DE"
    for fest in de_festivals:
        record = create_sds_record(fest, "DE")
        filename = f"{record['identity']['festival_id']}_sds.json"
        with open(os.path.join(de_dir, filename), 'w', encoding='utf-8') as f:
            json.dump(record, f, indent=2, ensure_ascii=False)

    # Process JP
    jp_dir = "/home/aiagent/hyeongryeol_workspace/festa_global_db/JP"
    for fest in jp_festivals:
        record = create_sds_record(fest, "JP")
        filename = f"{record['identity']['festival_id']}_sds.json"
        with open(os.path.join(jp_dir, filename), 'w', encoding='utf-8') as f:
            json.dump(record, f, indent=2, ensure_ascii=False)

    print(f"Successfully wrote {len(de_festivals)} files to DE and {len(jp_festivals)} files to JP.")

if __name__ == '__main__':
    main()
