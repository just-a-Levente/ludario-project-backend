import asyncio
from faker import Faker
from schemas.api_schema import BoardgameCreateRequest

fake = Faker()

fake_tags = [
    "strategy", "family", "cooperative", "social deduction",
    "party", "deck building", "worker placement", "roll and write"
]

def generate_fake_boardgame() -> BoardgameCreateRequest:
    return BoardgameCreateRequest(
        name=fake.catch_phrase(),
        producer=fake.company(),
        description=fake.text(max_nb_chars=200),
        price=str(fake.pyfloat(min_value=5, max_value=100, right_digits=2)),
        numberOfCopies=str(fake.random_int(min=1, max=20)),
        minNumberOfPlayers=str(fake.random_int(min=1, max=4)),
        maxNumberOfPlayers=str(fake.random_int(min=4, max=10)),
        thumbnailURL=fake.image_url(200, 200),
        tags=";".join(fake.random_elements(elements=fake_tags, length=fake.random_int(1, 3), unique=True)),
    )