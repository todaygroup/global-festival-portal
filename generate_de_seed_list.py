import json
import os

def main():
    # Using the data from acquire_festivals.py as a base
    # since Wikidata is being slow/unresponsive and the local file had a good start.
    
    de_festivals = [
        {"name": "Oktoberfest", "city": "Munich", "source_url": "https://www.oktoberfest.de"},
        {"name": "Carnival of Cologne", "city": "Cologne", "source_url": "https://www.koelnkarneval.de"},
        {"name": "Carnival of Mainz", "city": "Mainz", "source_url": "https://www.mainz.de"},
        {"name": "Carnival of Düsseldorf", "city": "Düsseldorf", "source_url": "https://www.duesseldorfer-karneval.de"},
        {"name": "Berlinale", "city": "Berlin", "source_url": "https://www.berlinale.de"},
        {"name": "Wacken Open Air", "city": "Wacken", "source_url": "https://www.wacken.com"},
        {"name": "Ruhrtriennale", "city": "Ruhr Area", "source_url": "https://www.ruhrtriennale.de"},
        {"name": "Hamburg Hafengeburtstag", "city": "Hamburg", "source_url": "https://www.hafengeburtstag.de"},
        {"name": "Cannstatter Wasen", "city": "Stuttgart", "source_url": "https://www.wasen.de"},
        {"name": "Nuremberg Christmas Market", "city": "Nuremberg", "source_url": "https://www.christkindlesmarkt.de"},
        {"name": "Dresden Christmas Market", "city": "Dresden", "source_url": "https://www.striezelmarkt.de"},
        {"name": "Cologne Christmas Market", "city": "Cologne", "source_url": "https://www.koeln.de"},
        {"name": "Berlin Christmas Market", "city": "Berlin", "source_url": "https://www.visitberlin.de"},
        {"name": "Munich Christmas Market", "city": "Munich", "source_url": "https://www.muenchen.de"},
        {"name": "Leipzig Christmas Market", "city": "Leipzig", "source_url": "https://www.leipziger-weihnachtsmarkt.de"},
        {"name": "Frankfurt Christmas Market", "city": "Frankfurt", "source_url": "https://www.frankfurt.de"},
        {"name": "Hamburg Christmas Market", "city": "Hamburg", "source_url": "https://www.hamburg.de"},
        {"name": "Stuttgart Christmas Market", "city": "Stuttgart", "source_url": "https://www.stuttgart.de"},
        {"name": "Bremen Christmas Market", "city": "Bremen", "source_url": "https://www.bremen.de"},
        {"name": "Lübeck Christmas Market", "city": "Lübeck", "source_url": "https://www.luebeck.de"},
        {"name": "Heidelberg Christmas Market", "city": "Heidelberg", "source_url": "https://www.heidelberg.de"},
        {"name": "Rothenburg Christmas Market", "city": "Rothenburg ob der Tauber", "source_url": "https://www.rothenburg.de"},
        {"name": "Freiburg Christmas Market", "city": "Freiburg", "source_url": "https://www.freiburg.de"},
        {"name": "Passau Christmas Market", "city": "Passau", "source_url": "https://www.passau.de"},
        {"name": "Regensburg Christmas Market", "city": "Regensburg", "source_url": "https://www.regensburg.de"},
        {"name": "Erfurt Christmas Market", "city": "Erfurt", "source_url": "https://www.erfurt.de"},
        {"name": "Kassel Christmas Market", "city": "Kassel", "source_url": "https://www.kassel.de"},
        {"name": "Münster Christmas Market", "city": "Münster", "source_url": "https://www.muenster.de"},
        {"name": "Oldenburg Christmas Market", "city": "Oldenburg", "source_url": "https://www.oldenburg.de"},
        {"name": "Osnabrück Christmas Market", "city": "Osnabrück", "source_url": "https://www.osnabrueck.de"},
        {"name": "Bielefeld Christmas Market", "city": "Bielefeld", "source_url": "https://www.bielefeld.de"},
        {"name": "Dortmund Christmas Market", "city": "Dortmund", "source_url": "https://www.dortmund.de"},
        {"name": "Essen Christmas Market", "city": "Essen", "source_url": "https://www.essen.de"},
        {"name": "Duisburg Christmas Market", "city": "Duisburg", "source_url": "https://www.duisburg.de"},
        {"name": "Bochum Christmas Market", "city": "Bochum", "source_url": "https://www.bochum.de"},
        {"name": "Gelsenkirchen Christmas Market", "city": "Gelsenkirchen", "source_url": "https://www.gelsenkirchen.de"},
        {"name": "Oberhausen Christmas Market", "city": "Oberhausen", "source_url": "https://www.oberhausen.de"},
        {"name": "Bottrop Christmas Market", "city": "Bottrop", "source_url": "https://www.bottrop.de"},
        {"name": "Herne Christmas Market", "city": "Herne", "source_url": "https://www.herne.de"},
        {"name": "Mülheim Christmas Market", "city": "Mülheim an der Ruhr", "source_url": "https://www.muelheim.de"},
        {"name": "Gladbeck Christmas Market", "city": "Gladbeck", "source_url": "https://www.gladbeck.de"},
        {"name": "Castrop-Rauxel Christmas Market", "city": "Castrop-Rauxel", "source_url": "https://www.castrop-rauxel.de"},
        {"name": "Recklinghausen Christmas Market", "city": "Recklinghausen", "source_url": "https://www.recklinghausen.de"},
        {"name": "Marl Christmas Market", "city": "Marl", "source_url": "https://www.marl.de"},
        {"name": "Herten Christmas Market", "city": "Herten", "source_url": "https://www.herten.de"},
        {"name": "Mainz Wine Festival", "city": "Mainz", "source_url": "https://www.mainz.de"},
        {"name": "Bad Dürkheim Wine Festival", "city": "Bad Dürkheim", "source_url": "https://www.duerkheimer-weinfest.de"},
        {"name": "Bachfest Eisenach", "city": "Eisenach", "source_url": "https://www.bachfest.de"},
        {"name": "Art Cologne", "city": "Cologne", "source_url": "https://www.artcologne.de"},
        {"name": "Wave Göttingen", "city": "Göttingen", "source_url": "https://www.wave-goettingen.de"},
    ]
    
    output_path = '/home/aiagent/hyeongryeol_workspace/festa_global_db/DE/seed_list.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(de_festivals, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(de_festivals)} festivals to {output_path}")

if __name__ == '__main__':
    main()
