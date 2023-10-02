from other import bitrix


async def bitrix_call_func(method: str, id_item: str, fields_item: dict):
    await bitrix.call(method,
                      [{
                          'ID': id_item,
                          'fields': fields_item
                      }])
