

from datajoint.base_relation import lookup_class_name


def schema_prep(schema):
    ''' not 100% if needed.. zap if needed after restart '''
    schema.connection.dependencies.load()


def table_to_classname(tablename, schema):
    ''' lookup_class_name wrapper which (will handle) aliases '''
    if not tablename.isdigit():
        return lookup_class_name(tablename, schema.context) or tablename
    else:
        raise NotImplementedError('aliased table_to_class')


def table_to_class(tablename, schema):
    ''' return class instance for a given tablename/schema '''
    tname = table_to_classname(tablename, schema)
    return schema.context[tname]


def schema_iterator(schema):
    return (table_to_class(c, schema)
            for c in schema.connection.dependencies.nodes())


def parent_classes(tableclass, schema):
    ''' return parent classes for a given tableclass/schema '''
    return (table_to_class(c, schema) for c in tableclass().parents())


def child_classes(tableclass, schema):
    ''' return child classes for a given tableclass/schema '''
    return (table_to_class(c, schema) for c in tableclass().children())


def get_table_heading(table):
    ''' get the table heading for a given tableclass '''
    table._heading.init_from_database(
        table.connection, table.database, table.table_name)
    return table._heading


def get_table_attributes(table):
    return get_table_heading(table).attributes
