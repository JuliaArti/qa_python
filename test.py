import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:
    
    @pytest.mark.parametrize("name,expected", [
        ("Война и мир", True),  
        ("A"*40, True),         
        ("", False),            
        ("A"*41, False),         
    ])
    def test_add_new_book(self, name, expected):
        
        collector = BooksCollector()

        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected


    def test_add_duplicate_book(self):

        collector = BooksCollector()

        collector.add_new_book("Преступление и наказание")
        collector.add_new_book("Преступление и наказание")
        assert len(collector.get_books_genre()) == 1


    @pytest.mark.parametrize("genre,expected", [
        ("Фантастика", "Фантастика"),   
        ("Ужасы", "Ужасы"),             
        ("Роман", ""),                  
        ("", ""),                       
    ])    
    def test_set_book_genre(self,genre, expected):

        collector = BooksCollector()

        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", genre)
        assert collector.get_book_genre("Книга") == expected

    
    def test_set_genre_nonexistent_book(self):

        collector = BooksCollector()
    
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert "Несуществующая книга" not in collector.get_books_genre()


    @pytest.mark.parametrize("genre,expected", [
        ("Фантастика", "Фантастика"),
        ("", None),
    ])
    def test_get_book_genre(self, genre, expected):

        collector = BooksCollector()

        if genre:
            collector.add_new_book("Книга")
            collector.set_book_genre("Книга", genre)
            assert collector.get_book_genre("Книга") == expected
        else:
            assert collector.get_book_genre("Несуществующая книга") is expected

    @pytest.fixture
    def genre_test_data(self):
        
        collector = BooksCollector()
        
        test_books = [
            ("Книга1", "Фантастика"),
            ("Книга2", "Ужасы"),
            ("Книга3", "Фантастика"),
            ("Книга4", "Комедии"),
        ]
        for name, genre in test_books:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        return collector
    
    @pytest.mark.parametrize("genre,expected", [
        ("Фантастика", ["Книга1", "Книга3"]),
        ("Ужасы", ["Книга2"]),
        ("Комедии", ["Книга4"]),
        ("Детективы", []),
        ("Несуществующий", []),
    ])

    def test_get_books_with_specific_genre(self, genre_test_data, genre, expected):
            
        result = genre_test_data.get_books_with_specific_genre(genre)
        assert sorted(result) == sorted(expected)


    def test_get_books_for_children(self, genre_test_data):

        result = genre_test_data.get_books_for_children()
        assert sorted(result) == sorted(["Книга1", "Книга3", "Книга4"])


    @pytest.fixture
    def favorites_test_data(self):
        
        collector = BooksCollector()

        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        return collector
    
    def test_add_book_in_favorites(self, favorites_test_data):
    
        assert "Книга1" in favorites_test_data.get_list_of_favorites_books()
        assert "Книга2" not in favorites_test_data.get_list_of_favorites_books()


    def test_delete_book_from_favorites(self,favorites_test_data):

        favorites_test_data.delete_book_from_favorites("Книга1")
        assert "Книга1" not in favorites_test_data.get_list_of_favorites_books()


    def test_get_list_of_favorites_books(self, favorites_test_data):

        assert favorites_test_data.get_list_of_favorites_books() == ["Книга1"]



