from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from annotation.db_seeding import insert_dummy_data_in_database
from user_app.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        insert_dummy_data_in_database()
        return Response(serializer.data)

        # client = MongoClient("mongodb://mongodb:27017")
        # db = client["lms"]
        # collection = db['Data']
        # print("===>> Running Query")
        # start = time.perf_counter()
        # filter_dict = {
        #     "project_id": 1,
        #     "group_id": 7,
        #     "annotations.labeler_id": 273,
        #     "annotations.is_annotated": False
        # }
        # data = collection.find(filter_dict, {"_id": 0})
        # count = collection.count_documents(filter_dict)
        # print("Taken Time=", time.perf_counter() - start)
        #
        # return Response({"total_data_count": count, "list": list(data.limit(100))})
