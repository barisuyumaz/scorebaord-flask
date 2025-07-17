#Bu dosya, tek seferlik çalıştırılarak veritabanını oluşturmak için kullanılır.
from app import create_app
from app.extensions import db
from app.models import GameState

app = create_app()

with app.app_context():
    db.create_all()

    # İlk veri satırını da oluştur (gerekiyorsa)
    if not GameState.query.first():
        initial_state = GameState()
        db.session.add(initial_state)
        db.session.commit()
