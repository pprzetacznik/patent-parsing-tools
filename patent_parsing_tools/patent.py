import pickle


class Patent:
    """
    Patent object

    >>> patent = Patent()
    >>> patent.data = "test data"
    >>> patent.serialize("serialized_patent")
    >>> patent2 = Patent.load("serialized_patent")
    >>> print(patent2.data)
    test data
    """

    def serialize(self, filename):
        """
        Serialization method
        """
        with open(filename, "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(source):
        """
        Deserialization static method
        """
        return pickle.load(open(source, "rb"))
