from rest_framework.views import APIView
from django.db import connection
from django.http import JsonResponse

class BookListAPI(APIView):

    def my_custom_sql(self):
        with connection.cursor() as cursor:
            cursor.execute("""SELECT
            books.*,
            (SELECT row_to_json(ass.*) FROM books_book_authors as ass WHERE ass.book_id=books.id AND ass.book_id IS NOT NULL LIMIT 1) as a,
            (SELECT ARRAY(SELECT authors.author_id FROM books_book_authors as authors WHERE authors.book_id=books.id)) as author
            FROM books_book AS books
            LIMIT 25
            """)

            "Return all rows from a cursor as a dict"
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]


    def get(self, request, *args, **kwargs):
        data = self.my_custom_sql()
        return JsonResponse(data, safe=False)
