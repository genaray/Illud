
import requests as requests

class Curler:

    """
    A class which curls web-api requests in order to return them as a string or json.
    """

    def curl(self, apiCall : str):

        """
        :param apiCall: The Web-API call we request in order to receive its data.
        :type apiCall: String
        :return: A String containing the curled web-api data.
        :rtype: String
        Curls the web-api request and returns the curled data as a json
        """

        curledJSON = requests.get(apiCall)
        return curledJSON.text