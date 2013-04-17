from scrapy.item import Item, Field

class MemberItem(Item):
    type = Field()
    id = Field()
    name = Field()

class PrivateItem(Item):
    type = Field()
    id = Field()
    birth = Field()
    military = Field()

class SpecialItem(Item):
    type = Field()
    id = Field()
    election = Field()
    party = Field()

class AttendItem(Item):
    type = Field()
    id = Field()
    date = Field()
    meeting = Field()
    status = Field()
