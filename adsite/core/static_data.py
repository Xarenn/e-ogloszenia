from datetime import datetime

categories = [
    ('Electronics', 'Electronics'),
]

personality = [
    ('Private Person', 'Private Person'),
    ('Company', 'Company'),
]


details = {
    'featured': False,
    'entry_date': datetime.now().isoformat(),
    'bump_date':  datetime.now().isoformat(),
    "photos": {
        "miniature_path": "ad:miniature.jpg",
        "files_path": [
            "ad:FCI1.jpg",
            "ad:picture2.jpg",
            "ad:picture5.jpg"
        ]
    }
}
