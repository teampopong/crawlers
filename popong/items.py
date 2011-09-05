from scrapy.item import Item, Field

class MemberItem(Item):
    type = Field()
    id = Field()
    name = Field()
