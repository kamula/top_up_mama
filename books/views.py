import requests
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BookCommentSerializer
from . models import BookComment


@api_view(['GET', ])
def get_name_authors_comments(request):
    url = "https://www.anapioficeandfire.com/api/books"
    final_data = []
    # make request to get books data
    data = requests.get(url)
    # check if response status code == 200
    if data.status_code == status.HTTP_200_OK:
        # convert data into json format
        json_data = data.json()
        # filter the data
        for i in json_data:
            item = {}
            item['name'] = i['name']
            item['authors'] = i['authors']
            item['comment_count'] = len(i['povCharacters'])
            item['released'] = i['released']
            final_data.append(item)
        final_data.sort(key=lambda item: item['released'], reverse=False)
        return Response(final_data, status=status.HTTP_200_OK)
    # if response != 200 return error message + request failed status code
    else:
        item = {}
        item['message'] = 'request failed'
    return Response(item, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def get_character_list(request, id):
    # get character list
    context = {}
    # pass the book id into the url
    url = f"https://www.anapioficeandfire.com/api/books/{id}"
    data = requests.get(url)
    if data.status_code == status.HTTP_200_OK:
        # GET the book characters
        book_characters = data.json()["characters"]
        context["characters"] = book_characters
        return Response(context, status=status.HTTP_200_OK)
    else:
        # return error message and 400 error message if there is an error
        context["message"] = "Error"
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def add_get_comment(request, id):
    # get character list
    context = {}
    # pass the book id into the url
    url = f"https://www.anapioficeandfire.com/api/books/{id}"
    data = requests.get(url)
    if data.status_code == status.HTTP_200_OK:
        book_data = request.data
        book_data['id'] = id
        serializer = BookCommentSerializer(data=book_data)
        list_characters = data.json()['povCharacters']
        # check if serializer is valid
        if serializer.is_valid():
            # save data if valid and return it as response
            serializer.save()
            saved_data_query = BookComment.objects.filter(id=id)
            serialized_data = BookCommentSerializer(
                saved_data_query, many=True)
            for item in serialized_data.data:
                list_characters.append(item['comment'])
            context['comment_count'] = len(list_characters)
            context['book_id'] = id
            context['comments'] = list_characters
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # return error message and 400 error message if there is an error
        context["message"] = "Error"
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
