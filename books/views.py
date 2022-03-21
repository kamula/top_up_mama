from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.decorators import api_view


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
            final_data.append(item)
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
    # GET the book characters
    book_characters = data.json()["characters"]
    context["characters"] = book_characters
    return Response(context, status=status.HTTP_200_OK)
