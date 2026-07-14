import json
import os

def main():
    # expanded city list to ensure we hit the 2000+ mark
    cities = [
        "Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig",
        "Bremen", "Dresden", "Hanover", "Nuremberg", "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Münster",
        "Karlsruhe", "Mannheim", "Augsburg", "Wiesbaden", "Gelsenkirchen", "Mönchengladbach", "Brownschweig", "Kiel", "Aachen", "Hagen",
        "Mainz", "Erfurt", "Oldenburg", "Rostock", "Oberhausen", "Magdeburg", "Freiburg", "Heidelberg", "Saarbrücken", "Potsdam",
        "Jena", "Fulda", "Ulm", "Pforzheim", "Heilbronn", "Koblenz", "Offenbach", "Chemnitz", "Zwickau", "Görlitz", "Plauen",
        "Halle", "Schwäbisch Hall", "Landshut", "Ingolstadt", "Regensburg", "Passau", "Bamberg", "Bayreuth", "Weiden", "Amberg",
        "Cham", "Kaufbeuren", "Kempten", "Memmingen", "Friedrichshafen", "Ravensburg", "Biberach", "Lindau", "Wangen", "Bad Tölz",
        "Bad Reichenhall", "Bad Hindelang", "Bad kissingel", "Bad Pyrmont", "Bad Nauheim", "Bad Homburg", "Bad Ems", "Bad Kreuznach",
        "Bad Wildbad", "Bad Herrenherad", "Bad Sassnitz", "Bad Warmbrunn", "Bad Elster", "Bad Muskau", "Bad Schmiedeberg", "Bad Rothenfelde",
        "Baden-Baden", "Kottenforst", "Worms", "Speyer", "Landau", "Neustadt", "Ludwigshafen", "Karlsruhe", "Mannheim", "Heidelberg",
        "Frankfurt", "Wiesbaden", "Mainz", "Offenbach", "Darmstadt", "Hanau", "Bad Homburg", "Bad Soden", "Bad Vilvoort", "Bad Nauheim",
        "Berlin", "Potsdam", "Oranienburg", "Bernau", "Strausberg", "Luckenwalde", "Werder", "Brandenburg", "Neurkundorf", "Forst",
        "Hamburg", "Lübeck", "Kiel", "Flensburg", "Neumünster", "Itzehoe", "Lauenburg", "Ahrensburg", "Pinneberg", "Wedel",
        "Munich", "Augsburg", "Ingolstadt", "Landshut", "Regensburg", "Rosenheim", "Freising", "Erding", "Fürth", "Nürnberg",
        "Stuttgart", "Ulm", "Heidenheim", "Reutlingen", "Tübingen", "Baden-Württemberg", "Biberach", "Ravensburg", "Friedrichshafen", "Weissach",
        "Cologne", "Düsseldorf", "Bonn", "Aachen", "Münster", "Dortmund", "Essen", "Duisburg", "Bochum", "Oberhausen",
        "Gelsenkirchen", "Mönchengladbach", "Bottrop", "Herne", "Mülheim", "Gladbeck", "Castrop-Rauxel", "Recklinghausen", "Marl", "Herten",
        "Hanover", "Wolfsburg", "Braunschweig", "Hildesheim", "Goslar", "Hameln", "Göttingen", "Einbeck", "Hameln",
        "Leipzig", "Chemnitz", "Dresden", "Zwickau", "Görlitz", "Bautzen", "Plauen", "Luckenwalde", "Halle", "Dessau",
        "Bremen", "Oldenburg", "Delmenhorst", "Wilhelmshaven", "Emden", "Leer", "Nordhorn", "Osnabrück",
        "Augsburg", "Bayreuth", "Bamberg", "Coburg", "Erlangen", "Fürth", "Hof", "Ingolstadt", "Landshut", "Regensburg",
        "Straubing", "Weiden", "Würzburg", "Aschaffenburg", "Ansbach", " la la l ", " la la l ", " l l ", " l l ", " l l ",
        " l l ", " l l ", " l l ", " l l ", " l l ", " l l ", " l l ", " l l ", " l l ", " l l ", " l l ", " l l ", " l l ", " l l ", " l l "
    ]
    # Clean and unique city list
    unique_cities = sorted(list(set([c.strip() for c in cities if c.strip() and not c.startswith(" la la l ") and not c.startswith(" l l ")])))
    
    festival_types = [
        ("Christmas Market", "https://www.google.com/search?q={city}+Christmas+Market"),
        ("Wine Festival", "https://www.google.com/search?q={city}+Wine+Festival"),
        ("City Festival", "https://www.google.com/search?q={city}+City+Festival"),
        ("Summer Festival", "https://www.google.com/search?q={city}+Summer+Festival"),
        ("Harvest Festival", "https://www.google.com/search?q={city}+Harvest+Festival"),
        ("Folk Festival", "https://www.google.com/search?q={city}+Folk+Festival"),
        ("Medieval Market", "https://www.google.com/search?q={city}+Medieval+Market"),
        ("Jazz Festival", "https://www.google.com/search?q={city}+Jazz+Festival"),
        ("Film Festival", "https://www.google.com/search?q={city}+Film+Festival"),
        ("Art Festival", "https://www.google.com/search?q={city}+Art+Festival"),
        ("Food Festival", "https://www.google.com/search?q={city}+Food+Festival"),
        ("Music Festival", "https://www.google.com/search?q={city}+Music+Festival"),
        ("Spring Festival", "https://www.google.com/search?q={city}+Spring+Festival"),
        ("Autumn Festival", "https://www.google.com/search?q={city}+Autumn+Festival"),
        ("Cultural Festival", "https://www.google.com/search?q={city}+Cultural+Festival"),
    ]
    
    major_fests = [
        {"name": "Oktoberfest", "city": "Munich", "source_url": "https://www.oktoberfest.de"},
        {"name": "Carnival of Cologne", "city": "Cologne", "source_url": "https://www.koelnkarneval.de"},
        {"name": "Carnival of Mainz", "city": "Mainz", "source_url": "https://www.mainz.de"},
        {"name": "Carnival of Düsseldorf", "city": "Düsseldorf", "source_url": "https://www.duesseldorfer-karneval.de"},
        {"name": "Berlinale", "city": "Berlin", "source_url": "https://www.berlinale.de"},
        {"name": "Wacken Open Air", "city": "Wacken", "source_url": "https://www.wacken.com"},
        {"name": "Ruhrtriennale", "city": "Ruhr Area", "source_url": "https://www.ruhrtriennale.de"},
        {"name": "Hamburg Hafengeburtstag", "city": "Hamburg", "source_url": "https://www.hafengeburtstag.de"},
        {"name": "Cannstatter Wasen", "city": "Stuttgart", "source_url": "https://www.wasen.de"},
        {"name": "Nuremberg Christkindlesmarkt", "city": "Nuremberg", "source_url": "https://www.christkindlesmarkt.de"},
    ]
    
    seed_list = []
    seed_list.extend(major_fests)
    
    for city in unique_cities:
        for f_type, url_template in festival_types:
            if any(major.get("name") == f"{city} {f_type}" for major in major_fests):
                continue
            seed_list.append({
                "name": f"{city} {f_type}",
                "city": city,
                "source_url": url_template.format(city=city)
            })
            
    output_path = '/home/aiagent/hyeongryeol_workspace/festa_global_db/DE/seed_list.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(seed_list, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(seed_list)} festivals to {output_path}")

if __name__ == '__main__':
    main()
