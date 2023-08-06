from datetime import datetime
from pydeequ.analyzers import AnalysisRunner
from pydeequ.analyzers import AnalyzerContext
from pydeequ.analyzers import Compliance
from pydeequ.analyzers import Mean
from pydeequ.analyzers import ApproxCountDistinct
from pydeequ.analyzers import Completeness
from pyspark.sql import functions as fn
from pydeequ.checks import CheckLevel
from pydeequ.verification import Check
from pydeequ.verification import VerificationSuite
from pydeequ.verification import VerificationResult
from .read_dataset import read_connectiontype
from .write_metrics import  write_metrics
import logging
from .get_connection import get_connection_details


def alert_null(metric_value, warning_threshold, error_threshold, information_threshold):
    logging.info("Inside alert null")
    warning = int(warning_threshold)
    error = int(error_threshold)
    information = int(information_threshold)
    if metric_value > information/100:
        return None, None
    elif metric_value <= information/100:
        if metric_value > warning/100:
            return "Information", "NULL values exceed Information limit"
        elif metric_value <= warning/100:
            if metric_value > error/100:
                return "Warning", "NULL values exceed warning limit"
            else:
                return "Error", "NULL values exceed error limit"
        else:
            return None,None
    else:
        return None,None


def alert_compliance(metric_value, warning_threshold, error_threshold, information_threshold):
    logging.info("Inside alert compliance function")
    warning=int(warning_threshold)
    error=int(error_threshold)
    information=int(information_threshold)
    if metric_value > information/100:
        return None, None
    elif metric_value <= information/100:
        if metric_value > warning/100:
            return "Information", "NON-COMPLIANT values exceed Information limit"
        elif metric_value <= warning/100:
            if metric_value > error/100:
                return "Warning", "NON-COMPLIANT values exceed warning limit"
            else:
                return "Error", "NON-COMPLIANT values exceed error limit"
        else:
            return None,None
    else:
        return None,None




def completeness(input_df, final_df, table_data,batchid, spark,dict,config_data):
    logging.info("Inside completeness function")
    metric_field = dict["Columnnames"]
    warning=dict["WARNING_Threshold"]
    error=dict["ERROR_Threshold"]
    info=dict["INFORMATION_Threshold"]
    input_df.show()
    for col in metric_field:
        metrics_data = AnalysisRunner(spark).onData(input_df).addAnalyzer(Completeness(col)).run()
        analysis_result_df = AnalyzerContext.successMetricsAsDataFrame(spark, metrics_data)
        analysis_result_df.show()
        metric_name = analysis_result_df.select("name").collect()[0][0]
        metric_value = analysis_result_df.select("value").collect()[0][0]
        column_name = analysis_result_df.select("instance").collect()[0][0]
        alert_type, alert_message = alert_null(metric_value,warning ,error ,info )
        analysis_result_final_df = (analysis_result_df
                                   .withColumn("domainName", fn.lit(table_data["domainName"]))
                                   .withColumn("subDomainName", fn.lit(table_data["subDomainName"]))
                                   .withColumn("DatasetName", fn.lit(table_data["datasetName"]))
                                   .withColumn("ColumnName", fn.lit(column_name))
                                   .withColumn("MetricName", fn.lit(metric_name))
                                   .withColumn("MetricUOM", fn.lit("Percentage"))
                                   .withColumn("MetricValue", fn.lit(metric_value) * 100)
                                   .withColumn("Insert_Timestamp", fn.lit(datetime.now().isoformat()))
                                   .withColumn("Alert_Type", fn.lit(alert_type))
                                   .withColumn("Alert_Message", fn.lit(alert_message))
                                   .withColumn("ComplianceCondition", fn.lit(None))
                                   .withColumn("RegexPattern", fn.lit(None))
                                   .withColumn("BatchId", fn.lit(batchid))
                                   .drop('entity', 'instance', 'name', 'value'))
        final_df = final_df.union(analysis_result_final_df)
    write_metrics(final_df,config_data)



def compliance(input_df, final_df, table_data,batchid, spark,dict,config_data):
    logging.info("Inside compliance function")
    metric_field = dict["Columnnames"]
    compliance = dict["Condition"] #separate
    warning = dict["WARNING_Threshold"]
    error = dict["ERROR_Threshold"]
    information = dict["INFORMATION_Threshold"]
    for col in metric_field:
        metrics_data = AnalysisRunner(spark).onData(input_df).addAnalyzer(Compliance(col, compliance)).run()
        analysis_result_df = AnalyzerContext.successMetricsAsDataFrame(spark, metrics_data)
        metric_name = analysis_result_df.select("name").collect()[0][0]
        metric_value = analysis_result_df.select("value").collect()[0][0]
        column_name = analysis_result_df.select("instance").collect()[0][0]
        alert_type, alert_message = alert_compliance(metric_value,warning,error,information)
        analysis_result_final_df = (analysis_result_df
                                   .withColumn("domainName", fn.lit(table_data["domainName"]))
                                   .withColumn("subDomainName", fn.lit(table_data["subDomainName"]))
                                   .withColumn("DatasetName", fn.lit(table_data["datasetName"]))
                                   .withColumn("ColumnName", fn.lit(column_name))
                                   .withColumn("metric_name", fn.lit(metric_name))
                                   .withColumn("MetricUOM", fn.lit("Percentage"))
                                   .withColumn("metric_value", fn.lit(metric_value) * 100)
                                   .withColumn("Insert_Timestamp", fn.lit(datetime.now().isoformat()))
                                   .withColumn("Alert_Type", fn.lit(alert_type))
                                   .withColumn("Alert_Message", fn.lit(alert_message))
                                   .withColumn("ComplianceCondition", fn.lit(compliance))
                                   .withColumn("RegexPattern", fn.lit(None))
                                   .withColumn("BatchId", fn.lit(batchid))
                                   .drop('entity', 'instance', 'name', 'value'))
        final_df = final_df.union(analysis_result_final_df)
    write_metrics(final_df,config_data)


def approx_count_distinct(input_df, final_df, table_data,batchid, spark,dict,config_data):
    logging.info("Inside approx_count_distinct function")
    metric_field = dict["Columnnames"]
    for col in metric_field:
        metrics_data = AnalysisRunner(spark).onData(input_df).addAnalyzer(ApproxCountDistinct(col)).run()
        analysis_result_df = AnalyzerContext.successMetricsAsDataFrame(spark, metrics_data)
        metric_name = analysis_result_df.select("name").collect()[0][0]
        metric_value = analysis_result_df.select("value").collect()[0][0]
        column_name = analysis_result_df.select("instance").collect()[0][0]
        analysis_result_final_df = (analysis_result_df
                                   .withColumn("domainName", fn.lit(table_data["domainName"]))
                                   .withColumn("subDomainName", fn.lit(table_data["subDomainName"]))
                                   .withColumn("DatasetName", fn.lit(table_data["datasetName"]))
                                   .withColumn("ColumnName", fn.lit(column_name))
                                   .withColumn("metric_name", fn.lit(metric_name))
                                   .withColumn("MetricUOM", fn.lit("Count"))
                                   .withColumn("metric_value", fn.lit(metric_value))
                                   .withColumn("Insert_Timestamp", fn.lit(datetime.now().isoformat()))
                                   .withColumn("Alert_Type", fn.lit(None))
                                   .withColumn("Alert_Message", fn.lit(None))
                                   .withColumn("ComplianceCondition", fn.lit(None))
                                   .withColumn("RegexPattern", fn.lit(None))
                                   .withColumn("BatchId", fn.lit(batchid))
                                   .drop('entity', 'instance', 'name', 'value'))
        final_df = final_df.union(analysis_result_final_df)
    write_metrics(final_df,config_data)


def mean(input_df, final_df, table_data,batchid, spark,dict,config_data):
    logging.info("Inside mean function")
    metric_field = dict["Columnnames"]
    for col in metric_field:
        metrics_data = AnalysisRunner(spark).onData(input_df).addAnalyzer(Mean(col)).run()
        analysis_result_df = AnalyzerContext.successMetricsAsDataFrame(spark, metrics_data)
        metric_name = analysis_result_df.select("name").collect()[0][0]
        metric_value = analysis_result_df.select("value").collect()[0][0]
        column_name = analysis_result_df.select("instance").collect()[0][0]
        analysis_result_final_df = (analysis_result_df
                                   .withColumn("domainName", fn.lit(table_data["domainName"]))
                                   .withColumn("subDomainName", fn.lit(table_data["subDomainName"]))
                                   .withColumn("DatasetName", fn.lit(table_data["datasetName"]))
                                   .withColumn("ColumnName", fn.lit(column_name))
                                   .withColumn("metric_name", fn.lit(metric_name))
                                   .withColumn("MetricUOM", fn.lit("Mean"))
                                   .withColumn("metric_value", fn.lit(metric_value))
                                   .withColumn("Insert_Timestamp", fn.lit(datetime.now().isoformat()))
                                   .withColumn("Alert_Type", fn.lit(None))
                                   .withColumn("Alert_Message", fn.lit(None))
                                   .withColumn("ComplianceCondition", fn.lit(None))
                                   .withColumn("RegexPattern", fn.lit(None))
                                   .withColumn("BatchId", fn.lit(batchid))
                                   .drop('entity', 'instance', 'name', 'value'))
        final_df = final_df.union(analysis_result_final_df)
    write_metrics(final_df,config_data)

def unique_check(input_df, final_df, table_data,batchid, spark,dict,config_data):
    logging.info("Inside unique_check function")
    metric_field = dict["Columnnames"]
    for col in metric_field:
        check = Check(spark, CheckLevel.Warning, "Check Unique of "+col)
        check_data = VerificationSuite(spark).onData(input_df).addCheck(check.isUnique(col)).run()
        check_result_df = VerificationResult.checkResultsAsDataFrame(spark, check_data)

        metric_name = check_result_df.select("check").collect()[0][0]
        metric_value = check_result_df.select("check_status").collect()[0][0]
        column_name = check_result_df.select("constraint").collect()[0][0]
        check_result_final_df = (check_result_df
                                   .withColumn("domainName", fn.lit(table_data["domainName"]))
                                   .withColumn("subDomainName", fn.lit(table_data["subDomainName"]))
                                   .withColumn("DatasetName", fn.lit(table_data["datasetName"]))
                                   .withColumn("ColumnName", fn.lit(column_name))
                                   .withColumn("metric_name", fn.lit(metric_name))
                                   .withColumn("MetricUOM", fn.lit("Value"))
                                   .withColumn("metric_value", fn.lit(metric_value))
                                   .withColumn("Insert_Timestamp", fn.lit(datetime.now().isoformat()))
                                   .withColumn("Alert_Type", fn.lit(None))
                                   .withColumn("Alert_Message", fn.lit(None))
                                   .withColumn("ComplianceCondition", fn.lit(None))
                                   .withColumn("RegexPattern", fn.lit(None))
                                   .withColumn("BatchId", fn.lit(batchid))
                                   .drop('entity', 'instance', 'name', 'value'))
        final_df = final_df.union(check_result_final_df)
    write_metrics(final_df,config_data)

def process_metrics(staging_data, output_schema, spark,batch_id,config_data):
    logging.info("Inside process_metrics function")
    final_df = spark.createDataFrame([], output_schema)
    for table_num, table_data in staging_data.items():
        metric=table_data["metrics"]
        fetch_connection_id=table_data["connectionId"]
        print("conn_id",fetch_connection_id)
        get_connection=get_connection_details(fetch_connection_id)
        fetch_project_id=get_connection['project_id']
        fetch_connection_type=table_data['connectiontype']
        print("Connection type",fetch_connection_type)
        print("fetch project id",fetch_project_id)
        print("fetch schema",table_data["schema"])
        print("fetch table name",table_data["table"])
        dataset_path = fetch_project_id+":"+table_data["schema"]+"."+table_data["table"]
        print("dataset_path",dataset_path)
        batchid = batch_id
        df = read_connectiontype(fetch_connection_type,dataset_path,batchid,spark).cache()
        for dict in metric:
            flag = dict["Flag"]
            if flag == "True":
                metric = dict["metricName"]
                if metric == 'Completeness':
                    completeness(df, final_df, table_data,batchid, spark,dict,config_data)
                elif metric == 'Compliance':
                    compliance(df, final_df, table_data,batchid, spark,dict,config_data)
                elif metric == 'ApproxCountDistinct':
                    approx_count_distinct(df, final_df, table_data,batchid, spark,dict,config_data)
                elif metric == 'Mean':
                    mean(df, final_df, table_data,batchid, spark,dict,config_data)
