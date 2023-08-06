def get_table_data_by_query(session, url, query):
    return session.read.format("jdbc") \
        .option("url", url) \
        .option("user", 'lookpin_system') \
        .option("password", 'FQ2b7d68mLytVP5Z') \
        .option("driver", 'org.postgresql.Driver') \
        .option("query", query) \
        .load()


def load_table_all_data(session, jdbc_url, table_name, column_list):
    connection_properties = {
        'user': 'lookpin_system',
        'password': 'FQ2b7d68mLytVP5Z',
        'driver': 'org.postgresql.Driver',
        'stringtype': 'unspecified'}
    df = session.read.jdbc(jdbc_url, table=table_name, properties=connection_properties)

    select_df = df.select(column_list)
    select_df.show(10)
    return select_df
