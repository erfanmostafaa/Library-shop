from rest_framework import viewsets , status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .models import *
from .serializers import *



# Create your views here.

User = get_user_model()

#Filter

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        genre = self.request.get('genre')
        if genre:
            return self.queryset.filter(genre__name=genre)
        return self.queryset


class GenericViewSet(viewsets.ModelsViewSet):
    querset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])

def add_review(request):
    user = request.user
    book_id = request.data.get('bookd_id')
    rating = request.data.get('rating')

    try:
        book = Book.objects.get(id = book_id)

    except Book.DoesNotExist:
        return Response({"error" : "Book not found"} , status = status.HTTP_404_NOT_FOUND )
    

    review , created = Review.objects.update_or_create(user = user , book = book , defaults={'rating' : rating})
    return  Response({"message" : "Review added/update successfuly"} , status=status.HTTP_200_OK)


@api_view(['DELETE'])

def delete_review(request , review_id):
    try:
        review = Review.objects.get(id = review_id , user = request.user)
        review.delete()
        return Response({"message" : "Review delete seccessfuly"} , status=status.HTTP_204_NO_CONTENT)
    except Review.DoesNotExist:
        return Response({"error": "no review found for user"} , status=status.HTTP_404_NOT_FOUND)
    

#suugest by genre


@api_view(['GET'])


def suggest_books(request):
    user = request.user
    reviews = Review.objects.filter(user=user)


    if not reviews.exist():
        return Response({"message": "There is not enough data about you"}, status=status.HTTP_404_NOT_FOUND)    

    genre_ratings = {}
    for review in reviews :
        genre = review.book.genre
        if genre not in genre_ratings:
            genre_ratings[genre] = []
        genre_ratings[genre].append(review.rating)
    

    favorite_genre = max(genre_ratings, key=lambda genre: sum(genre_ratings[genre]) / len(genre_ratings[genre]))
    
    suggested_books = Book.objects.filter(genre=favorite_genre).exclude(review__user=user)

    serializer = BookSerializer(suggested_books, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)





@api_view(['POST'])

def login_user (request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

