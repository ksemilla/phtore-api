import strawberry
from strawberry.file_uploads import Upload
from config.settings import MEDIA_FILES_DIR, MEDIA_FILES_URI
from schema.datafeed import DatafeedInput, Models, DatafeedList, Datafeed
from database.entity import EntityManager
from database.datafeed import DatafeedManager
from database.products import ProductManager

from graphql import GraphQLError

def model_to_manager(argument: Models):
    match argument:
        case Models.ENTITY:
            return EntityManager
        case Models.PRODUCT:
            return ProductManager
        case _:
            return GraphQLError("Invalid model")

@strawberry.field
async def upload(input: DatafeedInput) -> bool:
    model = model_to_manager(input.model)
    
    obj = model.find_by_id(input.object_id)

    _type, sub_type =  input.file.content_type.split("/")

    data = {
        "url": MEDIA_FILES_URI + input.object_id + f"-{input.field}",
        "model": input.model.value,
        "field": input.field,
        "object_id": input.object_id
    }

    
    # TODO: Change input field. not as an input. check if field exist in model
    dir_path = str(MEDIA_FILES_DIR) +"/" + input.object_id + f"-{input.field}"
    content = await input.file.read()

    if input.field in obj and  obj[input.field]:
        DatafeedManager.update(obj[input.field], data)
    else:
        res = DatafeedManager.insert(data)
        model.update(input.object_id, {input.field: res['inserted_id']})
    
    with open(dir_path, "wb") as f:
        f.write(content)
    return True

@strawberry.field
def datafeed(limit: int = 20, skip: int = 0) -> DatafeedList:
    cursor = DatafeedManager.list(filter={}, limit=limit, skip=skip)
    total_count = DatafeedManager.get_collection().count_documents({})
    return DatafeedList(
        list=[Datafeed(**obj) for obj in cursor],
        total_count=total_count
    )