"""Golden query templates for seeding brand query sets."""

QUERY_TEMPLATES: dict[str, dict[str, list[str]]] = {
    "saas": {
        "en": [
            "Best {category} tools for remote teams",
            "How much does {brand} cost?",
            "{brand} vs {competitor} comparison",
            "Is {brand} worth it for startups?",
            "What are alternatives to {brand}?",
            "Top software for {category} in 2026",
            "{brand} pricing plans explained",
            "Does {brand} integrate with Slack?",
            "Best free {category} software",
            "{brand} reviews and ratings",
        ],
        "id": [
            "Software {category} terbaik untuk tim remote",
            "Berapa harga {brand}?",
            "Perbandingan {brand} vs {competitor}",
            "Apakah {brand} cocok untuk startup?",
            "Alternatif {brand} apa saja?",
            "Software {category} terbaik tahun 2026",
            "Penjelasan paket harga {brand}",
            "Apakah {brand} terintegrasi dengan Slack?",
            "Software {category} gratis terbaik",
            "Review dan rating {brand}",
        ],
    },
    "local": {
        "en": [
            "Best {category} services near me",
            "How much does {brand} charge?",
            "{brand} vs {competitor} which is better?",
            "Is {brand} reliable?",
            "Top rated {category} in my area",
            "{brand} customer reviews",
            "What services does {brand} offer?",
            "Affordable {category} recommendations",
            "{brand} opening hours and location",
            "Emergency {category} services",
        ],
        "id": [
            "Jasa {category} terbaik di dekat saya",
            "Berapa biaya {brand}?",
            "{brand} vs {competitor} mana lebih bagus?",
            "Apakah {brand} terpercaya?",
            "{category} rating tertinggi di area saya",
            "Review pelanggan {brand}",
            "Layanan apa yang ditawarkan {brand}?",
            "Rekomendasi {category} terjangkau",
            "Jam buka dan lokasi {brand}",
            "Jasa {category} darurat",
        ],
    },
    "ecom": {
        "en": [
            "Best online stores for {category}",
            "Is {brand} legit and trustworthy?",
            "{brand} vs {competitor} product quality",
            "Does {brand} offer free shipping?",
            "Top {category} brands to buy from",
            "{brand} return policy",
            "Where to buy {category} online cheap",
            "{brand} discount codes and deals",
            "Customer reviews for {brand}",
            "Best {category} products 2026",
        ],
        "id": [
            "Toko online terbaik untuk {category}",
            "Apakah {brand} terpercaya?",
            "Kualitas produk {brand} vs {competitor}",
            "Apakah {brand} gratis ongkir?",
            "Brand {category} terbaik untuk dibeli",
            "Kebijakan retur {brand}",
            "Beli {category} online murah di mana?",
            "Kode diskon dan promo {brand}",
            "Review pelanggan {brand}",
            "Produk {category} terbaik 2026",
        ],
    },
}


def render_templates(
    template_key: str,
    brand: str,
    competitor: str,
    category: str = "software",
) -> list[dict]:
    """Return query dicts ready for DB insert."""
    tpl = QUERY_TEMPLATES.get(template_key, QUERY_TEMPLATES["saas"])
    results = []
    for lang, queries in tpl.items():
        for q in queries:
            results.append({
                "text": q.format(brand=brand, competitor=competitor, category=category),
                "lang": lang,
                "category": template_key,
                "is_custom": False,
            })
    return results
