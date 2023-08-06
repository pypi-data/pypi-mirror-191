from datagen_protocol.schema.assets.attributes import *


class AllOf(list):
    def __init__(self, *attributes):
        super().__init__(attributes)


class AnyOf(list):
    def __init__(self, *attributes):
        super().__init__(attributes)


class Exactly(list):
    def __init__(self, *attributes):
        super().__init__(attributes)
