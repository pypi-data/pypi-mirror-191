def join_recommendation_data(recommendations, review_satisfaction_avg_df):
    return recommendations.join(review_satisfaction_avg_df, on='product_id')


def dataframe_select_columns(df, columns):
    return df.select(columns)


def show_recommend_list(join_data, member_id_list):
    join_data.filter('member_id in (' + ','.join(str(id) for id in member_id_list) + ')').sort('avg_satisfaction',
                                                                                               ascending=False).limit(
        10).show(10)


def dataframe_upsert_opensearch(df, select_columns, username, password, index_name):
    df.select(select_columns).write.format('org.elasticsearch.spark.sql') \
        .option("es.nodes",
                'https://search-recommendataion-es-public-wth6jsurxcs4td4qdmd2bjupaa.ap-northeast-2.es.amazonaws.com') \
        .option("es.port", 443) \
        .option("es.nodes.wan.only", "true") \
        .option("es.net.http.auth.user", username) \
        .option("es.net.http.auth.pass", password) \
        .option("es.write.operation", "index") \
        .option("es.batch.size.bytes", "1mb") \
        .option("es.batch.size.entries", 1000) \
        .option("es.batch.write.retry.wait", "30s") \
        .option("es.mapping.id", "id") \
        .option("es.resource", "{index}/_doc".format(index=index_name)) \
        .mode("append") \
        .save()
