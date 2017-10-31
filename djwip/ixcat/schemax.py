
from itertools import chain

from datajoint.base_relation import lookup_class_name


_is_initialized = {}


def schema_prep(schema):
    ''' ensure dependencies are loaded '''
    if schema.database not in _is_initialized:
        schema.connection.dependencies.load()
        _is_initialized[schema.database] = True


def get_schema(tableclass):
    ''' get schema for a table '''
    return tableclass.connection.schemas[tableclass.database]


def table_prep(tableclass):
    ''' ensure dependencies are loaded '''
    schema_prep(get_schema(tableclass))


def table_to_classname(tablename, schema):
    ''' lookup_class_name wrapper which (will handle) aliases '''
    schema_prep(schema)
    if not tablename.isdigit():
        return lookup_class_name(tablename, schema.context) or tablename
    else:
        raise NotImplementedError('aliased table_to_class')


def table_to_class(tablename, schema):
    ''' return class instance for a given tablename/schema '''
    schema_prep(schema)
    tname = table_to_classname(tablename, schema)
    return schema.context[tname]


def schema_iterator(schema):
    schema_prep(schema)
    return (table_to_class(c, schema)
            for c in schema.connection.dependencies.nodes())


def parent_classes(tableclass):
    ''' return parent classes for a given tableclass/schema '''
    # TODO: cross-schema traversal?
    schema = get_schema(tableclass)
    schema_prep(schema)
    return (table_to_class(c, schema) for c in tableclass().parents())


def child_classes(tableclass):
    ''' return child classes for a given tableclass/schema '''
    # TODO: cross-schema traversal?
    schema = get_schema(tableclass)
    schema_prep(schema)
    return (table_to_class(c, schema) for c in tableclass().children())


def all_classes(tableclass):
    '''' return all related classes for a given tableclass/schema '''
    schema = get_schema(tableclass)
    schema_prep(schema)
    return chain(parent_classes(tableclass), child_classes(tableclass))


def get_table_heading(tableclass):
    ''' get the table heading for a given tableclass '''
    table_prep(tableclass)
    tableclass._heading.init_from_database(
        tableclass.connection, tableclass.database, tableclass.table_name)
    return tableclass._heading


def get_table_attributes(tableclass):
    table_prep(tableclass)
    return get_table_heading(tableclass).attributes


def get_definition(tableclass):
    ''' need to just memorize this.. anyway'''
    return tableclass().describe()


def get_fkey_details(tableclass):
    ''' print foreign key details '''
    name = tableclass.full_table_name
    depg = tableclass.connection.dependencies
    schema = get_schema(tableclass)

    for x in depg.predecessors_iter(name):

        c = table_to_class(x, schema)
        e = depg.get_edge_data(x, name)

        print('---')
        print('{x} -> {c}'.format(x=str(tableclass), c=str(c)))
        print('  primary: {p}'.format(p=str(e['primary'])))
        print('  referencing_attributes: {r}'
              .format(r=str(e['referencing_attributes'])))
        print('  referenced_attributes: {r}'
              .format(r=str(e['referenced_attributes'])))
        print('  aliased: {a}'.format(a=str(e['aliased'])))
        print('  multi (1:M): {m}'.format(m=str(e['multi'])))
