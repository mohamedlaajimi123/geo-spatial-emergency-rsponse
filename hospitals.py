hospitals = [
    # ── TUNIS ──────────────────────────────────────────────
    {
        "id": 1, "name": "Charles-Nicolle Hospital",
        "lat": 36.802254, "lng": 10.161104, "type": "public",
        "specialties": ["cardiology", "neurology", "trauma", "general"],
        "total_beds": 900, "occupied_beds": 720, "rating": 4.2
    },
    {
        "id": 2, "name": "La Rabta Hospital",
        "lat": 36.802000, "lng": 10.154516, "type": "public",
        "specialties": ["general", "burn unit", "surgery", "cardiology"],
        "total_beds": 700, "occupied_beds": 560, "rating": 3.8
    },
    {
        "id": 3, "name": "Aziza Othmana Hospital",
        "lat": 36.804479, "lng": 10.168527, "type": "public",
        "specialties": ["general", "obstetrics", "surgery"],
        "total_beds": 450, "occupied_beds": 380, "rating": 3.6
    },
    {
        "id": 4, "name": "Habib Thameur Hospital",
        "lat": 36.786261, "lng": 10.176607, "type": "public",
        "specialties": ["cardiology", "general", "surgery"],
        "total_beds": 500, "occupied_beds": 410, "rating": 3.7
    },
    {
        "id": 5, "name": "Béchir-Hamza Children's Hospital",
        "lat": 36.806965, "lng": 10.159248, "type": "public",
        "specialties": ["pediatrics", "general"],
        "total_beds": 300, "occupied_beds": 240, "rating": 4.0
    },
    {
        "id": 6, "name": "Tunis Military Hospital",
        "lat": 36.787159, "lng": 10.178377, "type": "public",
        "specialties": ["trauma", "surgery", "cardiology", "general"],
        "total_beds": 600, "occupied_beds": 420, "rating": 4.1
    },
    {
        "id": 7, "name": "Institut National de Neurologie Mongi-Ben Hamida",
        "lat": 36.805000, "lng": 10.163000, "type": "public",
        "specialties": ["neurology"],
        "total_beds": 150, "occupied_beds": 110, "rating": 4.3
    },
    {
        "id": 8, "name": "Institut Hédi-Raïs d'Ophtalmologie",
        "lat": 36.803000, "lng": 10.159000, "type": "public",
        "specialties": ["general", "surgery"],
        "total_beds": 120, "occupied_beds": 85, "rating": 4.0
    },
    {
        "id": 9, "name": "Institut Salah-Azaïz (Oncology)",
        "lat": 36.800000, "lng": 10.157000, "type": "public",
        "specialties": ["oncology"],
        "total_beds": 200, "occupied_beds": 170, "rating": 4.1
    },
    {
        "id": 10, "name": "Centre de Traumatologie et des Grands Brûlés",
        "lat": 36.798000, "lng": 10.160000, "type": "public",
        "specialties": ["burn unit", "trauma"],
        "total_beds": 180, "occupied_beds": 140, "rating": 4.2
    },

    # ── LA MARSA / ARIANA ───────────────────────────────────
    {
        "id": 11, "name": "Mongi Slim Hospital (La Marsa)",
        "lat": 36.867253, "lng": 10.291239, "type": "public",
        "specialties": ["general", "neurology", "surgery"],
        "total_beds": 350, "occupied_beds": 280, "rating": 3.9
    },
    {
        "id": 12, "name": "Marsa Internal Security Forces Hospital",
        "lat": 36.879069, "lng": 10.324940, "type": "public",
        "specialties": ["trauma", "surgery", "general"],
        "total_beds": 180, "occupied_beds": 120, "rating": 3.7
    },
    {
        "id": 13, "name": "Abderrahmane Mami Hospital (Ariana)",
        "lat": 36.870016, "lng": 10.178232, "type": "public",
        "specialties": ["general", "surgery"],
        "total_beds": 280, "occupied_beds": 210, "rating": 3.5
    },

    # ── MANOUBA / BEN AROUS ─────────────────────────────────
    {
        "id": 14, "name": "Razi Psychiatric Hospital (Manouba)",
        "lat": 36.810356, "lng": 10.082659, "type": "public",
        "specialties": ["psychiatry", "neurology"],
        "total_beds": 400, "occupied_beds": 320, "rating": 3.3
    },
    {
        "id": 15, "name": "Mohamed Bouazizi Burn Hospital (Ben Arous)",
        "lat": 36.750000, "lng": 10.210000, "type": "public",
        "specialties": ["burn unit"],
        "total_beds": 150, "occupied_beds": 90, "rating": 3.8
    },

    # ── BIZERTE ─────────────────────────────────────────────
    {
        "id": 16, "name": "Habib Bougatfa University Hospital",
        "lat": 37.272230, "lng": 9.860213, "type": "public",
        "specialties": ["general", "surgery", "cardiology"],
        "total_beds": 500, "occupied_beds": 390, "rating": 3.7
    },
    {
        "id": 17, "name": "Bizerte Military Hospital",
        "lat": 37.271649, "lng": 9.861823, "type": "public",
        "specialties": ["trauma", "surgery", "general"],
        "total_beds": 200, "occupied_beds": 140, "rating": 3.9
    },
    {
        "id": 18, "name": "Menzel Bourguiba Regional Hospital",
        "lat": 37.164368, "lng": 9.796797, "type": "public",
        "specialties": ["general", "obstetrics"],
        "total_beds": 180, "occupied_beds": 130, "rating": 3.4
    },

    # ── NABEUL ──────────────────────────────────────────────
    {
        "id": 19, "name": "CHU Taher Maamouri (Nabeul)",
        "lat": 36.437974, "lng": 10.674205, "type": "public",
        "specialties": ["general", "surgery", "obstetrics", "cardiology"],
        "total_beds": 220, "occupied_beds": 170, "rating": 3.5
    },

    # ── ZAGHOUAN ────────────────────────────────────────────
    {
        "id": 20, "name": "Zaghouan Regional Hospital",
        "lat": 36.416539, "lng": 10.132128, "type": "public",
        "specialties": ["general", "obstetrics"],
        "total_beds": 100, "occupied_beds": 70, "rating": 3.2
    },

    # ── BÉJA ────────────────────────────────────────────────
    {
        "id": 21, "name": "Béja Regional Hospital",
        "lat": 36.726300, "lng": 9.181600, "type": "public",
        "specialties": ["general", "surgery", "obstetrics"],
        "total_beds": 220, "occupied_beds": 160, "rating": 3.3
    },

    # ── JENDOUBA ────────────────────────────────────────────
    {
        "id": 22, "name": "Jendouba Regional Hospital",
        "lat": 36.637162, "lng": 8.723825, "type": "public",
        "specialties": ["general", "surgery", "obstetrics"],
        "total_beds": 200, "occupied_beds": 155, "rating": 3.3
    },

    # ── LE KEF ──────────────────────────────────────────────
    {
        "id": 23, "name": "Le Kef Regional Hospital",
        "lat": 36.174600, "lng": 8.714800, "type": "public",
        "specialties": ["general", "surgery", "obstetrics"],
        "total_beds": 190, "occupied_beds": 140, "rating": 3.2
    },
    {
        "id": 24, "name": "Clinique Militaire du Kef",
        "lat": 36.182000, "lng": 8.710000, "type": "public",
        "specialties": ["trauma", "general"],
        "total_beds": 80, "occupied_beds": 50, "rating": 3.4
    },

    # ── SILIANA ─────────────────────────────────────────────
    {
        "id": 25, "name": "Siliana Regional Hospital",
        "lat": 36.139637, "lng": 9.374495, "type": "public",
        "specialties": ["general", "obstetrics"],
        "total_beds": 130, "occupied_beds": 90, "rating": 3.1
    },
    {
        "id": 26, "name": "Kesra Hospital",
        "lat": 36.053129, "lng": 9.295114, "type": "public",
        "specialties": ["general"],
        "total_beds": 60, "occupied_beds": 40, "rating": 2.8
    },

    # ── KAIROUAN ────────────────────────────────────────────
    {
        "id": 27, "name": "Ibn El Jazzar University Hospital",
        "lat": 35.799581, "lng": 10.102609, "type": "public",
        "specialties": ["general", "surgery", "cardiology", "neurology"],
        "total_beds": 380, "occupied_beds": 300, "rating": 3.8
    },
    {
        "id": 28, "name": "Polyclinique Militaire de Kairouan",
        "lat": 35.678100, "lng": 10.096300, "type": "public",
        "specialties": ["general", "trauma"],
        "total_beds": 100, "occupied_beds": 65, "rating": 3.5
    },

    # ── KASSERINE ───────────────────────────────────────────
    {
        "id": 29, "name": "Kasserine Regional Hospital",
        "lat": 35.167200, "lng": 8.830500, "type": "public",
        "specialties": ["general", "surgery", "obstetrics", "trauma"],
        "total_beds": 250, "occupied_beds": 195, "rating": 3.3
    },

    # ── SIDI BOUZID ─────────────────────────────────────────
    {
        "id": 30, "name": "Sidi Bouzid Regional Hospital",
        "lat": 35.038100, "lng": 9.485700, "type": "public",
        "specialties": ["general", "surgery", "obstetrics"],
        "total_beds": 200, "occupied_beds": 150, "rating": 3.2
    },

    # ── SOUSSE ──────────────────────────────────────────────
    {
        "id": 31, "name": "Sahloul University Hospital",
        "lat": 35.836529, "lng": 10.589908, "type": "public",
        "specialties": ["cardiology", "trauma", "neurology", "surgery", "general"],
        "total_beds": 700, "occupied_beds": 560, "rating": 4.1
    },
    {
        "id": 32, "name": "Farhat-Hached University Hospital",
        "lat": 35.829801, "lng": 10.627770, "type": "public",
        "specialties": ["general", "oncology", "surgery", "cardiology"],
        "total_beds": 650, "occupied_beds": 520, "rating": 4.0
    },

    # ── MONASTIR ────────────────────────────────────────────
    {
        "id": 33, "name": "Fattouma-Bourguiba University Hospital",
        "lat": 35.770449, "lng": 10.834030, "type": "public",
        "specialties": ["general", "surgery", "neurology", "cardiology"],
        "total_beds": 550, "occupied_beds": 430, "rating": 3.9
    },

    # ── MAHDIA ──────────────────────────────────────────────
    {
        "id": 34, "name": "Tahar-Sfar University Hospital (Mahdia)",
        "lat": 35.510311, "lng": 11.032674, "type": "public",
        "specialties": ["general", "surgery", "obstetrics"],
        "total_beds": 300, "occupied_beds": 220, "rating": 3.6
    },
    {
        "id": 35, "name": "Chebba District Hospital",
        "lat": 35.231700, "lng": 11.119000, "type": "public",
        "specialties": ["general", "obstetrics"],
        "total_beds": 80, "occupied_beds": 55, "rating": 3.0
    },

    # ── SFAX ────────────────────────────────────────────────
    {
        "id": 36, "name": "Habib-Bourguiba Hospital (Sfax)",
        "lat": 34.996072, "lng": 10.696084, "type": "public",
        "specialties": ["general", "surgery", "trauma", "cardiology"],
        "total_beds": 800, "occupied_beds": 640, "rating": 4.0
    },
    {
        "id": 37, "name": "Hédi-Chaker Hospital (Sfax)",
        "lat": 34.740936, "lng": 10.750303, "type": "public",
        "specialties": ["neurology", "oncology", "surgery"],
        "total_beds": 450, "occupied_beds": 360, "rating": 3.8
    },
    {
        "id": 38, "name": "Bou Assida Regional Hospital",
        "lat": 35.029218, "lng": 10.769963, "type": "public",
        "specialties": ["general", "obstetrics"],
        "total_beds": 160, "occupied_beds": 110, "rating": 3.3
    },
    {
        "id": 39, "name": "Mahres Regional Hospital",
        "lat": 34.558597, "lng": 10.510653, "type": "public",
        "specialties": ["general"],
        "total_beds": 80, "occupied_beds": 55, "rating": 3.0
    },
    {
        "id": 40, "name": "Salim El-Hadhri Hospital (Kerkennah)",
        "lat": 34.939206, "lng": 11.110539, "type": "public",
        "specialties": ["general", "obstetrics"],
        "total_beds": 70, "occupied_beds": 45, "rating": 2.9
    },

    # ── GAFSA ───────────────────────────────────────────────
    {
        "id": 41, "name": "Houcine Bouzaiene Regional Hospital (Gafsa)",
        "lat": 34.420263, "lng": 8.796169, "type": "public",
        "specialties": ["general", "surgery", "obstetrics"],
        "total_beds": 250, "occupied_beds": 190, "rating": 3.4
    },

    # ── TOZEUR ──────────────────────────────────────────────
    {
        "id": 42, "name": "Hedi Jaballah Regional Hospital (Tozeur)",
        "lat": 33.916814, "lng": 8.129539, "type": "public",
        "specialties": ["general", "obstetrics"],
        "total_beds": 120, "occupied_beds": 85, "rating": 3.2
    },

    # ── KÉBILI ──────────────────────────────────────────────
    {
        "id": 43, "name": "Kébili Regional Hospital",
        "lat": 33.705400, "lng": 8.965200, "type": "public",
        "specialties": ["general", "obstetrics"],
        "total_beds": 110, "occupied_beds": 75, "rating": 3.0
    },

    # ── GABÈS ───────────────────────────────────────────────
    {
        "id": 44, "name": "Mohammed Ben Sassi Regional Hospital (Gabès)",
        "lat": 34.097372, "lng": 10.176701, "type": "public",
        "specialties": ["general", "surgery"],
        "total_beds": 200, "occupied_beds": 155, "rating": 3.4
    },
    {
        "id": 45, "name": "Gabès Military Hospital",
        "lat": 33.883714, "lng": 10.112561, "type": "public",
        "specialties": ["trauma", "surgery", "general"],
        "total_beds": 150, "occupied_beds": 100, "rating": 3.6
    },

    # ── MÉDENINE ────────────────────────────────────────────
    {
        "id": 46, "name": "Médenine Regional Hospital",
        "lat": 33.354900, "lng": 10.505200, "type": "public",
        "specialties": ["general", "surgery", "obstetrics"],
        "total_beds": 220, "occupied_beds": 165, "rating": 3.3
    },
    {
        "id": 47, "name": "Houmt Souk Regional Hospital (Djerba)",
        "lat": 33.875800, "lng": 10.857200, "type": "public",
        "specialties": ["general", "surgery", "obstetrics"],
        "total_beds": 180, "occupied_beds": 130, "rating": 3.5
    },

    # ── TATAOUINE ───────────────────────────────────────────
    {
        "id": 48, "name": "Tataouine Regional Hospital",
        "lat": 32.929600, "lng": 10.450700, "type": "public",
        "specialties": ["general", "obstetrics", "surgery"],
        "total_beds": 150, "occupied_beds": 100, "rating": 3.1
    },
    {
        "id": 49, "name": "Clinique Militaire de Tataouine",
        "lat": 32.935000, "lng": 10.445000, "type": "public",
        "specialties": ["trauma", "general"],
        "total_beds": 70, "occupied_beds": 45, "rating": 3.3
    },

    # ── INSTITUT SPÉCIALISÉ (TUNIS) ─────────────────────────
    {
        "id": 50, "name": "Institut Mohamed-Kassab d'Orthopédie",
        "lat": 36.812000, "lng": 10.074000, "type": "public",
        "specialties": ["trauma", "surgery"],
        "total_beds": 200, "occupied_beds": 155, "rating": 4.0
    },
]

def get_all_hospitals():
    return hospitals

if __name__ == "__main__":
    print(f"Total hospitals loaded: {len(hospitals)}")
    print("Sample check:")
    for h in hospitals[:3]:
        print(f"  {h['id']}. {h['name']} → ({h['lat']}, {h['lng']})")