from sqlalchemy import create_engine

from chatbot.config import DB_URL

# pool_pre_ping avoids handing out dead connections -- useful here since
# MySQL is on a different machine, possibly reached over a tunnel, so
# connections can silently drop between requests.
engine = create_engine(DB_URL, pool_pre_ping=True)