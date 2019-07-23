from django.db import connection


def temporary_models(models):
    def create_models():
        with connection.schema_editor() as schema_editor:
            for model in models:
                schema_editor.create_model(model)

    def delete_models():
        with connection.cursor() as cursor:
            cursor.execute('SET CONSTRAINTS ALL IMMEDIATE;')
            cursor.execute('SET CONSTRAINTS ALL DEFERRED;')
        with connection.schema_editor() as schema_editor:
            for model in reversed(models):
                schema_editor.delete_model(model)

    def wrapper(fn):
        def inner(*args, **kwargs):
            # for safety we remove models at the beginning
            delete_models()
            create_models()
            result = fn(*args, **kwargs)
            delete_models()
            return result
        return inner
    return wrapper
