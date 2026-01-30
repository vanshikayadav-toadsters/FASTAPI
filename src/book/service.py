from sqlmodel.ext.asyncio.session import AsyncSession
from models import Book
from src.book.schemas import BookCreateModel
from sqlmodel import select
import datetime


class BookService:

    async def get_all_books(self, session: AsyncSession):
        statement=select(Book).order_by(desc(Book.created_at))

        result=await session.exec(statement)

        return result.all()
    


    async def create_book(self,book_data: BookCreateModel, session:AsyncSession):
        book_data_dict=book_data.model_dump()

        new_book=Book(**book_data_dict)


        new_book.published_date=datetime.strptime(book_data_dict['published_date'], "%Y-%m-%d")

        session.add(new_book)

        await session.commit()

        return new_book

