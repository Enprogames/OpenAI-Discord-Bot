import json
import datetime as dt
import pickle

from sqlalchemy import create_engine, Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class LogData(Base):
    """A class to encapsulate logging data.

    This class contains methods for logging data, viewing data, searching for data by prompt, searching for data by response,
    and clearing data. The class also creates the SQLite database and table if they don't exist.
    """
    __tablename__ = "log_data"

    uid = Column(Integer, primary_key=True)
    time = Column(DateTime, default=dt.datetime.now)
    user = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False)
    prompt = Column(String)
    response = Column(String)
    tokens = Column(Integer, nullable=True)
    completion_obj = Column(LargeBinary)

    def __str__(self):
        return json.dumps({'LogData': {
            'id': self.uid,
            'time': self.time,
            'prompt': self.prompt,
            'response': self.response,
            'tokens': self.tokens,
            'user': f"{self.user} ({self.user_id})"
        }}, indent=4)

    __repr__ = __str__


class LogDataManager:
    """A class to manage the LogData table."""

    def __init__(self, connection_str: str):
        """Create the engine, session, and table if they don't exist."""
        self.engine = create_engine(connection_str)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def log_data(self, prompt: str, response: str, time=dt.datetime.now(), tokens=None,
                 user: str = None, user_id: int = None,
                 completion_obj: 'OpenAIObject' = None) -> None:
        """Log data to the database.

        Args:
        prompt: str: The prompt for the data to be logged.
        response: str: The response for the data to be logged.

        Returns:
        None
        """
        completion_obj_bytes = pickle.dumps(completion_obj)

        data = LogData(prompt=prompt,
                       response=response,
                       tokens=tokens,
                       time=time,
                       user=user,
                       user_id=int(user_id),
                       completion_obj=completion_obj_bytes)
        self.session.add(data)
        self.session.commit()

    def clear_data(self) -> int:
        """Clear all data from the database.

        Returns:
        int: The number of rows deleted.
        """
        num_rows_deleted = self.session.query(self.LogData).delete()
        self.session.commit()
        return num_rows_deleted

    def view_data(self) -> list:
        """View all data in the database.

        Returns:
        list: A list of rows from the database.
        """
        return self.session.query(self.LogData).all()

    def search_by_prompt(self, prompt: str) -> list:
        """Search for data in the database by prompt.

        Args:
        prompt: str: The prompt to search for.

        Returns:
        list: A list of rows that match the prompt.
        """
        return self.session.query(self.LogData).filter(self.LogData.prompt == prompt).all()

    def search_by_response(self, response: str) -> list:
        """Search for data in the database by response.

        Args:
        response: str: The response to search for.

        Returns:
        list: A list of rows that match the response.
        """
        return self.session.query(LogData).filter(LogData.response == response).all()
