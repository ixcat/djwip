# true wip to patch dj
# immediate goal: hooking queries, query logging, query tuning
# long-run goal: make this modular or find appropriate library
#  perhaps: https://gorilla.readthedocs.io/en/latest/tutorial.html
# usage:
# import djpatch as dj

import sys

import datajoint as dj

djpatch = sys.modules[__name__]
dj_vars = vars(dj)

#
# moveout
#

'''
>>> schema.connection.query('explain DELETE FROM `test_djpatch`.`dj_patch_aux` WHERE (((`patchid`) in (SELECT `patchid` FROM `test_djpatch`.`dj_patch_test` WHERE ((((`patchid`=1)))))))').fetchall()
query explain DELETE FROM `test_djpatch`.`dj_patch_aux` WHERE (((`patchid`) in (SELECT `patchid` FROM `test_djpatch`.`dj_patch_test` WHERE ((((`patchid`=1)))))))
((1, 'DELETE', 'dj_patch_aux', None, 'ALL', None, None, None, None, 1, 100.0, 'Using where'), (2, 'DEPENDENT SUBQUERY', 'dj_patch_test', None, 'const', 'PRIMARY', 'PRIMARY', '4', 'const', 1, 100.0, 'Using index'))


((1, 'DELETE', 'dj_patch_aux', None, 'ALL', None, None, None, None, 1, 100.0, 'Using where'), (2, 'DEPENDENT SUBQUERY', 'dj_patch_test', None, 'const', 'PRIMARY', 'PRIMARY', '4', 'const', 1, 100.0, 'Using index'))

--- via sql:

mysql> explain DELETE FROM `test_djpatch`.`dj_patch_aux` WHERE (((`patchid`) in (SELECT `patchid` FROM `test_djpatch`.`dj_patch_test` WHERE ((((`patchid`=1)))))));
+----+--------------------+---------------+------------+-------+---------------+---------+---------+-------+------+----------+-------------+
| id | select_type        | table         | partitions | type  | possible_keys | key     | key_len | ref   | rows | filtered | Extra       |
+----+--------------------+---------------+------------+-------+---------------+---------+---------+-------+------+----------+-------------+
|  1 | DELETE             | dj_patch_aux  | NULL       | ALL   | NULL          | NULL    | NULL    | NULL  |    1 |   100.00 | Using where |
|  2 | DEPENDENT SUBQUERY | dj_patch_test | NULL       | const | PRIMARY       | PRIMARY | 4       | const |    1 |   100.00 | Using index |
+----+--------------------+---------------+------------+-------+---------------+---------+---------+-------+------+----------+-------------+
2 rows in set (0.01 sec)


https://dev.mysql.com/doc/refman/8.0/en/explain-output.html

DEPENDENT typically signifies the use of a correlated subquery. See Section 13.2.11.7, “Correlated Subqueries”.

DEPENDENT SUBQUERY evaluation differs from UNCACHEABLE SUBQUERY evaluation. For DEPENDENT SUBQUERY, the subquery is re-evaluated only once for each set of different values of the variables from its outer context. For UNCACHEABLE SUBQUERY, the subquery is re-evaluated for each row of the outer context. 

https://dev.mysql.com/doc/refman/8.0/en/correlated-subqueries.html
 A correlated subquery is a subquery that contains a reference to a table that also appears in the outer query. For example:

SELECT * FROM t1
  WHERE column1 = ANY (SELECT column1 FROM t2
                       WHERE t2.column2 = t1.column2);

... further in page:

"
For certain cases, a correlated subquery is optimized. For example:

val IN (SELECT key_val FROM tbl_name WHERE correlated_condition)

Otherwise, they are inefficient and likely to be slow. Rewriting the query as a join might improve performance. 
"
but, we do not 'contains a reference to a table that also appears in the outer query.' : "where WHERE ((((`patchid`=1)))))));" < no outer table

https://dev.mysql.com/doc/refman/8.0/en/semi-joins.html
"The optimizer uses semi-join strategies to improve subquery execution, as described in this section. " < conditions apply to this query

"If a subquery meets the preceding criteria, MySQL converts it to a semi-join and makes a cost-based choice from these strategies:

    Convert the subquery to a join, or use table pullout and run the query as an inner join between subquery tables and outer tables. Table pullout pulls a table out from the subquery to the outer query.

    Duplicate Weedout: Run the semi-join as if it was a join and remove duplicate records using a temporary table.

    FirstMatch: When scanning the inner tables for row combinations and there are multiple instances of a given value group, choose one rather than returning them all. This "shortcuts" scanning and eliminates production of unnecessary rows.

    LooseScan: Scan a subquery table using an index that enables a single value to be chosen from each subquery's value group.

    Materialize the subquery into an indexed temporary table that is used to perform a join, where the index is used to remove duplicates. The index might also be used later for lookups when joining the temporary table with the outer tables; if not, the table is scanned. For more information about materialization, see Section 8.2.2.2, “Optimizing Subqueries with Materialization”. 

"

so - is above explain output valid for large datasets as here?



--- straight join (proper term? anyhow) :

mysql> explain delete dj_patch_aux.* from dj_patch_aux,dj_patch_test where dj_patch_aux.patchid=dj_patch_test.patchid;
+----+-------------+---------------+------------+--------+---------------+---------+---------+-----------------------------------+------+----------+-------------+
| id | select_type | table         | partitions | type   | possible_keys | key     | key_len | ref                               | rows | filtered | Extra       |
+----+-------------+---------------+------------+--------+---------------+---------+---------+-----------------------------------+------+----------+-------------+
|  1 | DELETE      | dj_patch_aux  | NULL       | ALL    | PRIMARY       | NULL    | NULL    | NULL                              |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | dj_patch_test | NULL       | eq_ref | PRIMARY       | PRIMARY | 4       | test_djpatch.dj_patch_aux.patchid |    1 |   100.00 | Using index |
+----+-------------+---------------+------------+--------+---------------+---------+---------+-----------------------------------+------+----------+-------------+
2 rows in set (0.00 sec)









'''


def splain(schema, query):
    for exp in schema.connection.query('EXPLAIN {}'.format(query)).fetchall():
        print(exp)


#
# patched functions
#


def query(self, query, args=(), as_dict=False, suppress_warnings=True,
          reconnect=None):
    print('query', query)
    return self.djpatch_query(query, args, as_dict, suppress_warnings,
                              reconnect)


def delete(self, verbose=True):
    import collections  # NOQA hack imports
    from datajoint.utils import user_choice

    class _rename_map(tuple):
        """ for internal use """
        pass

    """
    Deletes the contents of the table and its dependent tables, recursively.
    User is prompted for confirmation if config['safemode'] is set to True.
    """
    conn = self.connection
    already_in_transaction = conn.in_transaction
    safe = config['safemode']
    if already_in_transaction and safe:
        raise DataJointError('Cannot delete within a transaction in safemode. '
                             'Set dj.config["safemode"] = False or complete the ongoing transaction first.')
    graph = conn.dependencies
    graph.load()
    delete_list = collections.OrderedDict(
        (name, _rename_map(next(iter(graph.parents(name).items()))) if name.isdigit() else FreeTable(conn, name))
        for name in graph.descendants(self.full_table_name))

    # construct restrictions for each relation
    restrict_by_me = set()
    # restrictions: Or-Lists of restriction conditions for each table.
    # Uncharacteristically of Or-Lists, an empty entry denotes "delete everything".
    restrictions = collections.defaultdict(list)
    # restrict by self
    if self.restriction:
        restrict_by_me.add(self.full_table_name)
        restrictions[self.full_table_name].append(self.restriction)  # copy own restrictions
    # restrict by renamed nodes
    restrict_by_me.update(table for table in delete_list if table.isdigit())  # restrict by all renamed nodes
    # restrict by secondary dependencies
    for table in delete_list:
        restrict_by_me.update(graph.children(table, primary=False))   # restrict by any non-primary dependents

    # compile restriction lists
    for name, table in delete_list.items():
        for dep in graph.children(name):
            # if restrict by me, then restrict by the entire relation otherwise copy restrictions
            restrictions[dep].extend([table] if name in restrict_by_me else restrictions[name])

    # apply restrictions
    for name, table in delete_list.items():
        if not name.isdigit() and restrictions[name]:  # do not restrict by an empty list
            table.restrict([
                r.proj() if isinstance(r, FreeTable) else (
                    delete_list[r[0]].proj(**{a: b for a, b in r[1]['attr_map'].items()})
                    if isinstance(r, _rename_map) else r)
                for r in restrictions[name]])
    if safe:
        print('About to delete:')

    if not already_in_transaction:
        self.connection.start_transaction()
    total = 0
    try:
        for name, table in reversed(list(delete_list.items())):
            if not name.isdigit():
                count = table.delete_quick(get_count=True)
                total += count
                if (verbose or safe) and count:
                    print('{table}: {count} items'.format(table=name, count=count))
    except:
        # Delete failed, perhaps due to insufficient privileges. Cancel transaction.
        if not already_in_transaction:
            self.connection.cancel_transaction()
        raise
    else:
        assert not (already_in_transaction and safe)
        if not total:
            print('Nothing to delete')
            if not already_in_transaction:
                self.connection.cancel_transaction()
        else:
            if already_in_transaction:
                if verbose:
                    print('The delete is pending within the ongoing transaction.')
            else:
                if not safe or user_choice("Proceed?", default='no') == 'yes':
                    self.connection.commit_transaction()
                    if verbose or safe:
                        print('Committed.')
                else:
                    self.connection.cancel_transaction()
                    if verbose or safe:
                        print('Cancelled deletes.')


#
# patch installation / 'main'
#

dj_vars['Connection'].djpatch_query = dj_vars['Connection'].query
dj_vars['Connection'].query = query

dj_vars['Table'].djpatch_delete = dj_vars['Table'].delete
dj_vars['Table'].delete = delete


for a in dj.__all__:
    setattr(djpatch, a, dj_vars[a])

__all__ = dj.__all__
