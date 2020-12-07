from pyspark.ml import Pipeline as pip
from pyspark.ml.feature import *
from pyspark.sql.functions import *
from pyspark.sql.types import *


def base_features_gen_pipeline(input_descript_col="descript", input_category_col="category", output_feature_col="features", output_label_col="label"):
    tk = Tokenizer( inputCol= input_descript_col, outputCol= "words_col")
    cv = CountVectorizer (inputCol= "words_col", outputCol= output_feature_col)
    #convert category into label (0.0, 1.0, 2.0)
    id = StringIndexer (inputCol = input_category_col, outputCol = output_label_col)
    output_pip = pip(stages = [tk, cv, id])
    return output_pip

#convert nb and svm into joint
def convert_joint(nb,svm):
    if (nb == 0.0) and (svm == 0.0):
        output = 0.0
    if (nb == 1.0) and (svm == 0.0):
        output = 1.0
    if (nb == 0.0) and (svm == 1.0):
        output = 2.0
    if (nb == 1.0) and (svm == 1.0):
        output = 3.0

    return output

#add the new column "joint_pred_n" to the DF
def generate_joint(DF):
    convert = udf(convert_joint, DoubleType())
    col_joint_0 = convert("nb_pred_0", "svm_pred_0")
    col_joint_1 = convert("nb_pred_1", "svm_pred_1")
    col_joint_2 = convert("nb_pred_2", "svm_pred_2")
    #add the new column to the output
    out_DF = DF.withColumn("joint_pred_0", col_joint_0)
    out_DF = out_DF.withColumn("joint_pred_1", col_joint_1)
    out_DF = out_DF.withColumn("joint_pred_2", col_joint_2)

    return out_DF


def gen_meta_features(training_df, nb_0, nb_1, nb_2, svm_0, svm_1, svm_2):
    #count the number of the group
    groupNum = training_df.select("group").distinct().count()
    flag = first

    for k in range(groupNum):

        filter_condition = (training_df["group"] == k)
        df_genfeature = training_df.filter(filter_condition)
        df_train = training_df.filter(~filter_condition)

        base_pipeline = pip(stages = [nb_0, nb_1, nb_2, svm_0, svm_1, svm_2])

        #fit and transform when the first time run the model
        if flag == first:

            #fit and transform
            train_DF = base_pipeline.fit(df_train)
            result_DF = train_DF.transform(df_genfeature)
            flag = second
        else:

            train_DF = base_pipeline.fit(df_train)
            gen_DF = train_DF.transform(df_genfeature)
            result_DF = result_DF.union(gen_DF)

    #add the joint to the result_DF
    result_DF = generate_joint(result_DF)
    result_DF = result_DF.select("id", "group", "features", "label", "label_0", "label_1", "label_2",\
                                 "nb_pred_0", "nb_pred_1", "nb_pred_2", "svm_pred_0", "svm_pred_1", "svm_pred_2",\
                                 "joint_pred_0", "joint_pred_1", "joint_pred_2")

    return result_DF


def test_prediction(test_df, base_features_pipeline_model, gen_base_pred_pipeline_model, gen_meta_feature_pipeline_model, meta_classifier):

    base_DF = base_features_pipeline_model.transform(test_df)
    #base_DF.show(5)
    #get the svm and nb prediction and add to Six_DF
    gen_Six_DF = gen_base_pred_pipeline_model.transform(base_DF)
    #gen_Six_DF.show(5)

    gen_Nine_DF = generate_joint(gen_Six_DF)
    output_DF = gen_meta_feature_pipeline_model.transform(gen_Nine_DF)
    output = meta_classifier.transform(output_DF)
    #print the DF with "id, label, final_prediction"
    output = output.select("id", "label", "final_prediction")
    #output.show(20)
    return output
