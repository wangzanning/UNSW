from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, CountVectorizer, StringIndexer
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType



def base_features_gen_pipeline(input_descript_col="descript", input_category_col="category", output_feature_col="features", output_label_col="label"):
    tk = Tokenizer( inputCol= input_descript_col, outputCol= "words")
    cv = CountVectorizer (inputCol= "words", outputCol= output_feature_col)
    id = StringIndexer (inputCol = input_category_col, outputCol = output_label_col)
    return Pipeline(stages = [tk, cv, id])

def mapToInt(nb,svm):
    return float( int ( str(int(nb)) + str(int(svm) ), 2 ))



def gen_meta_features(training_df, nb_0, nb_1, nb_2, svm_0, svm_1, svm_2):
    groupNum = training_df.select("group").distinct().count()

    flag = True

    for k in range(5):

        filter_condition = training_df["group"] == k
        df_train = training_df.filter ( ~filter_condition)
        df_genfeature = training_df.filter(filter_condition)

        base_pipeline = Pipeline(stages = [nb_0, nb_1, nb_2, svm_0, svm_1, svm_2])

        if flag:
            result_DF = base_pipeline.fit(df_train).transform(df_genfeature)
            flag = False
        else:
            result_DF = result_DF.union(base_pipeline.fit(df_train).transform(df_genfeature))

    f = udf( mapToInt, DoubleType())
    result_DF = result_DF.withColumn("joint_pred_0", f("nb_pred_0","svm_pred_0")) \
        .withColumn("joint_pred_1", f("nb_pred_1", "svm_pred_1")) \
        .withColumn("joint_pred_2", f("nb_pred_2", "svm_pred_2"))

    return result_DF

    #改成循环时拼接
    #修改flag

def test_prediction(test_df, base_features_pipeline_model, gen_base_pred_pipeline_model, gen_meta_feature_pipeline_model, meta_classifier):

    raw_Test_DF = base_features_pipeline_model.transform(test_df)
    raw_SixDF = gen_base_pred_pipeline_model.transform(raw_Test_DF)
    f = udf (mapToInt, DoubleType())

    raw_Nine_DF = raw_SixDF.withColumn("joint_pred_0", f("nb_pred_0", "svm_pred_0")) \
        .withColumn("joint_pred_1", f("nb_pred_1", "svm_pred_1")) \
        .withColumn("joint_pred_2", f("nb_pred_2", "svm_pred_2"))

    features_DF = gen_meta_feature_pipeline_model.transform(raw_Nine_DF)
    return meta_classifier.transform(features_DF).select("id", "label", "final_prediction")

