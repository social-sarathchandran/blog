from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination


class APIResponse:

    def __init__(self, message=None, data=None, status=None, error=None):
        """
        Constructor for api response class

        Parameters:
            1. message(str): A message to be included in the response
            2. data(dict): Optional data to be included in the response
            3. error(str): Optional error message included in case of any error

        """
        self.message = message
        self.data = data
        self.error = error
        self.status = status

    def build_response(self):
        """
        Method to build the API response

        Returns:
            1. Response: An instance of response containing the appropriate response data and status code
        """

        if self.error:
            return Response(
                {"message": self.error, "data": self.data},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            response_data = {"message": self.message}
            response_data["data"] = self.data
        return Response(response_data, status=status.HTTP_200_OK)


# Pagination class
class CustomPagination(pagination.PageNumberPagination):
    """
    Custom pagination class for paginating API results

    Attributes:
        1. page_size(init): Number of items per page
        2. page_query_param(str): Name of the query parameter used to specify page number
        3. max_page_size(int): maximum no of items allowed per page

    """

    page_size = 10
    page_query_param = "page_size"
    max_page_size = 100
