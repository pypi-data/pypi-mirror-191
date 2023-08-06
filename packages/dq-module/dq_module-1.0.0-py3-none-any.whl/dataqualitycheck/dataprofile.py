from datetime import date, datetime
from .commonutilities import *
try:
    import pyspark
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
    from pyspark.context import SparkContext
    from pyspark.sql.session import SparkSession
except:
    pass


class DataProfile():
    def __init__(self, tables_list, interaction_between_tables, data_read_ob , data_write_ob, data_right_structure , job_id, time_zone = None, no_of_partition=4, output_db_name="data_quality_output" , run_engine ='pyspark'):
        
        self.tables_list = tables_list
        self.interaction_between_tables = interaction_between_tables
        self.data_write_ob = data_write_ob
        self.data_read_ob=data_read_ob
        self.data_right_structure = data_right_structure
        self.no_of_partition = no_of_partition
        self.run_engine=run_engine
        self.dataframes = read_dataset(self.tables_list, self.data_read_ob, self.no_of_partition ,self.run_engine , True)
        self.output_db_name = output_db_name
        self.job_id = job_id
        self.time_zone = time_zone
        if self.run_engine.lower() == 'polars':
           self.data_profiling_schema=[("job_id",pl.Utf8),("source_type",pl.Utf8),("layer",pl.Utf8),("source_name",pl.Utf8),("filename",pl.Utf8),("column_name",pl.Utf8),("column_type",pl.Utf8),( "total_column_count",pl.Utf8),("total_row_count",pl.Utf8),("min",pl.Utf8),("max",pl.Utf8),("avg",pl.Utf8),("sum",pl.Utf8),("stddev",pl.Utf8),("25th_per",pl.Utf8),("50th_per",pl.Utf8),("75th_per",pl.Utf8),("missing_count",pl.Utf8),("unique_count",pl.Utf8),("mode",pl.Utf8),("list_of_uniques",pl.Utf8),("run_date",pl.Utf8)]
        else:
           self.spark = SparkSession(SparkContext.getOrCreate())
           self.data_profiling_schema = StructType([StructField("job_id", StringType(), True),
                                      StructField("source_type",
                                                  StringType(), True),
                                      StructField(
                                          "layer", StringType(), True),
                                          StructField(
                                          "source_name", StringType(), True),
                                     StructField(
                                          "filename", StringType(), True),          
                                      StructField("column_name",
                                                  StringType(), True),
                                      StructField("column_type",
                                                  StringType(), True),
                                      StructField(
                                          "total_column_count", StringType(), True),
                                      StructField("total_row_count",
                                                  StringType(), True),
                                      StructField("min", StringType(), True),
                                      StructField("max", StringType(), True),
                                      StructField("avg", StringType(), True),
                                      StructField("sum", StringType(), True),
                                      StructField(
                                          "stddev", StringType(), True),
                                      StructField(
            "25th_per", StringType(), True),
            StructField(
            "50th_per", StringType(), True),
            StructField(
            "75th_per", StringType(), True),
            StructField("missing_count",
                        StringType(), True),
            StructField("unique_count",
                        StringType(), True),
            StructField("mode", StringType(), True),
            StructField("list_of_uniques",
                        StringType(), True),
            StructField("run_date", StringType(), True)
        ])
        

    def apply_data_profiling_to_column_spark(self, df, source_type, layer, source_name,filename, column_to_be_checked, rows, columns):
        column_type = column_type_identifier(df, column_to_be_checked , self.run_engine)
        list_of_uniq = self.list_of_uniques_spark(df, column_to_be_checked)
        rundate = date.today().strftime("%Y/%m/%d")
        if column_type == "numerical":
            result_data = df.agg(lit(self.job_id),
                                 lit(source_type),
                                 lit(layer),
                                 lit(source_name),
                                 lit(filename),
                                 lit(column_to_be_checked).alias("column_name"),
                                 lit(column_type).alias("column_type"),
                                 lit(columns),
                                 lit(rows),
                                 min(column_to_be_checked).alias("min"),
                                 max(column_to_be_checked).alias("max"),
                                 avg(column_to_be_checked).alias("avg"),
                                 sum(column_to_be_checked).alias("sum"),
                                 stddev(column_to_be_checked).alias("stddev"),
                                 percentile_approx(
                                     column_to_be_checked, 0.25).alias("25th_per"),
                                 percentile_approx(
                                     column_to_be_checked, 0.50).alias("50th_per"),
                                 percentile_approx(
                                     column_to_be_checked, 0.75).alias("75th_per"),
                                 sum(when(col(column_to_be_checked).isNull(), 1).otherwise(
                                     0)).alias("missing_count"),
                                 countDistinct(column_to_be_checked).alias(
                                     "unique_count"),
                                 lit(None).alias("mode"),
                                 lit(list_of_uniq).alias("list_of_uniques"),
                                 lit(rundate).alias("run_date"))

        elif column_type == "categorical":
            mode = self.find_mode_spark(df, column_to_be_checked)
            result_data = df.agg(lit(self.job_id),
                                 lit(source_type),
                                 lit(layer),
                                 lit(source_name),
                                 lit(filename),
                                 lit(column_to_be_checked).alias(
                                     "column_name"),
                                 lit(column_type).alias("column_type"),
                                 lit(columns),
                                 lit(rows),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 sum(when(col(column_to_be_checked).isNull(), 1).otherwise(
                                     0)).alias("missing_count"),
                                 countDistinct(column_to_be_checked).alias(
                                     "unique_count"),
                                 lit(mode).alias("mode"),
                                 lit(list_of_uniq).alias("list_of_uniques"),
                                 lit(rundate).alias("run_date")
                                 )

        else:
            mode = self.find_mode_spark(df, column_to_be_checked)
            result_data = df.agg(lit(self.job_id),
                                 lit(source_type),
                                 lit(layer),
                                 lit(source_name),
                                 lit(filename),
                                 lit(column_to_be_checked).alias(
                                     "column_name"),
                                 lit(column_type).alias("column_type"),
                                 lit(columns),
                                 lit(rows),
                                 min(column_to_be_checked).alias("min"),
                                 max(column_to_be_checked).alias("max"),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 percentile_approx(column_to_be_checked,
                                                   0.25).alias("25th_per"),
                                 percentile_approx(column_to_be_checked,
                                                   0.50).alias("50th_per"),
                                 percentile_approx(column_to_be_checked,
                                                   0.75).alias("75th_per"),
                                 sum(when(col(column_to_be_checked).isNull(),
                                          1).otherwise(0)).alias("missing_count"),
                                 countDistinct(column_to_be_checked).alias(
                                     "unique_count"),
                                 lit(mode).alias("mode"),
                                 lit(list_of_uniq).alias("list_of_uniques"),
                                 lit(rundate).alias("run_date")
                                 )
        return result_data
    
    def apply_data_profiling_to_column_polars(self, df, source_type, layer, source_name, filename, column_to_be_checked, rows, columns):
        column_type = column_type_identifier(df,column_to_be_checked,self.run_engine)
        list_of_uniq = self.list_of_uniques_polars(df, column_to_be_checked)
        rundate = date.today().strftime("%Y/%m/%d")
        if column_type == "numerical":
            result_data = df.select([pl.lit(self.job_id).alias("job_id"),
                                 pl.lit(source_type).alias("source_type"),
                                 pl.lit(layer).alias("layer"),
                                 pl.lit(source_name).alias("source_name"),
                                 pl.lit(filename).alias("filename"),
                                 pl.lit(column_to_be_checked).alias("column_name"),
                                 pl.lit(column_type).alias("column_type"),
                                 pl.lit(columns).alias("total_column_count"),
                                 pl.lit(rows).alias("total_row_count"),
                                 pl.col(column_to_be_checked).min().alias("min"),
                                 pl.col(column_to_be_checked).max().alias("max"),
                                 pl.col(column_to_be_checked).mean().alias("avg"),
                                 pl.col(column_to_be_checked).sum().alias("sum"),
                                 pl.col(column_to_be_checked).std().alias("stddev"),
                                 pl.col(column_to_be_checked).quantile(0.25).alias("25th_per"),
                                 pl.col(column_to_be_checked).quantile(0.50).alias("50th_per"),
                                 pl.col(column_to_be_checked).quantile(0.75).alias("75th_per"),
                                 pl.col(column_to_be_checked).null_count().alias("missing_count"),
                                 pl.col(column_to_be_checked).drop_nulls().n_unique().alias("unique_count"),
                                 pl.lit(None).alias("mode"),
                                 pl.lit(list_of_uniq).alias("list_of_uniques"),
                                 pl.lit(rundate).alias("run_date")])

        elif column_type == "categorical":
            mode = self.find_mode_polars(df, column_to_be_checked)
            result_data =  df.select([pl.lit(self.job_id).alias("job_id"),
                                 pl.lit(source_type).alias("source_type"),
                                 pl.lit(layer).alias("layer"),
                                 pl.lit(source_name).alias("source_name"),
                                 pl.lit(filename).alias("filename"),
                                 pl.lit(column_to_be_checked).alias("column_name"),
                                 pl.lit(column_type).alias("column_type"),
                                 pl.lit(columns).alias("total_column_count"),
                                 pl.lit(rows).alias("total_row_count"),
                                 pl.lit(None).alias("min"),
                                 pl.lit(None).alias("max"),
                                 pl.lit(None).alias("avg"),
                                 pl.lit(None).alias("sum"),
                                 pl.lit(None).alias("stddev"),
                                 pl.lit(None).alias("25th_per"),
                                 pl.lit(None).alias("50th_per"),
                                 pl.lit(None).alias("75th_per"),
                                 pl.col(column_to_be_checked).null_count().alias("missing_count"),
                                 pl.col(column_to_be_checked).drop_nulls().n_unique().alias("unique_count"),
                                 pl.lit(mode).alias("mode"),
                                 pl.lit(list_of_uniq).alias("list_of_uniques"),
                                 pl.lit(rundate).alias("run_date")]
                                 )

        else:
            mode = self.find_mode_polars(df, column_to_be_checked)
            df1=df.sort(column_to_be_checked)
            result_data =df.select([pl.lit(self.job_id).alias("job_id"),
                                 pl.lit(source_type).alias("source_type"),
                                 pl.lit(layer).alias("layer"),
                                 pl.lit(source_name).alias("source_name"),
                                 pl.lit(filename).alias("filename"),
                                 pl.lit(column_to_be_checked).alias("column_name"),
                                 pl.lit(column_type).alias("column_type"),
                                 pl.lit(columns).alias("total_column_count"),
                                 pl.lit(rows).alias("total_row_count"),
                                 pl.col(column_to_be_checked).min().cast(pl.Utf8).alias("min"),
                                 pl.col(column_to_be_checked).max().cast(pl.Utf8).alias("max"),
                                 pl.lit(None).alias("avg"),
                                 pl.lit(None).alias("sum"),
                                 pl.lit(None).alias("stddev"),
                                 df1[int(-1 * ((0.25 * rows)// -1 ))-1][column_to_be_checked].cast(pl.Utf8).alias("25th_per"),
                                 df1[int(-1 * ((0.50 * rows)// -1 ))-1][column_to_be_checked].cast(pl.Utf8).alias("50th_per"),
                                 df1[int(-1 * ((0.75 * rows)// -1 ))-1][column_to_be_checked].cast(pl.Utf8).alias("75th_per"),
                                 pl.col(column_to_be_checked).null_count().alias("missing_count"),
                                 pl.col(column_to_be_checked).drop_nulls().n_unique().alias("unique_count"),
                                 pl.lit(mode).alias("mode"),
                                 pl.lit(list_of_uniq).alias("list_of_uniques"),
                                 pl.lit(rundate).alias("run_date")]
                                 )
        return result_data

    def find_mode_spark(self, df, column_to_be_checked):
        df = df.filter(col(column_to_be_checked).isNotNull()
                       ).groupBy(column_to_be_checked).count()
        mode_val_count = df.agg(max("count")).take(1)[0][0]
        result = df.filter(col("count") == mode_val_count).select(
            column_to_be_checked).rdd.flatMap(lambda x: x).collect()
        return str(result)
    
    def find_mode_polars(self, df, column_to_be_checked):
        df = df.filter(pl.col(column_to_be_checked).is_not_null()).groupby(column_to_be_checked,maintain_order=True).count()
        mode_val_count = df.select(pl.col("count").max()).item()
        result =df.filter(pl.col("count") == mode_val_count).select(pl.col(column_to_be_checked)).get_column(column_to_be_checked).to_list()
        return str(result)
        

    def list_of_uniques_spark(self, df, column_to_be_checked):
        df=df.filter(col(column_to_be_checked).isNotNull())
        result = df.agg(collect_set(column_to_be_checked)).take(1)[0][0]
        result.sort()
        return str(result[:10])
    
    def list_of_uniques_polars(self, df, column_to_be_checked):
        df=df.filter(pl.col(column_to_be_checked).is_not_null())
        result = df.select(pl.col(column_to_be_checked)).unique().get_column(column_to_be_checked).to_list()
        result.sort()
        return str(result[:10])
        
       # ----- Function takes the filepath of source_csv as an input and apply data profiling.
    def apply_data_profiling(self, source_config_df, write_consolidated_report = True):
        try:
          source_config = source_config_df.rows(named=True)
        except:
          source_config = source_config_df.collect()
        new_tables = get_missing_tables(self.tables_list, source_config)
        self.tables_list = {**self.tables_list, **new_tables}
        new_dataframes = read_dataset(new_tables,self.data_read_ob,self.no_of_partition,self.run_engine , True)
        if new_dataframes:
            self.dataframes = {**self.dataframes, **new_dataframes}
        data_profiling_df = self.apply_data_profiling_to_table_list(source_config,write_consolidated_report)
        return data_profiling_df

    def apply_data_profiling_to_table_list(self, source_config , write_consolidated_report):
      if self.run_engine.lower()== 'polars':
        combined_data_profiling_schema=self.data_profiling_schema + [("data_profiling_report_write_location",pl.Utf8)]
        combined_data_profiling_report_data=[]
      else:
        combined_data_profiling_schema=StructType(self.data_profiling_schema.fields+[StructField("data_profiling_report_write_location",StringType(), True)])
        combined_data_profiling_report_df=self.spark.createDataFrame(data=[], schema=combined_data_profiling_schema)
      for table in source_config:
            try:
              data_profiling_data = []
              source = f'''{table["source_type"]}_{table["layer"]}_{table["source_name"]}_{table["filename"]}'''
              if self.run_engine.lower()== 'polars':
                rows = self.dataframes[source].height
                columns = self.dataframes[source].width
                for column in self.dataframes[source].columns:
                    result_df = self.apply_data_profiling_to_column_polars(
                        self.dataframes[source], table["source_type"], table["layer"], table["source_name"],table["filename"], column, rows, columns)

                    data_profiling_data = data_profiling_data + result_df.rows()
                data_profiling_df = pl.DataFrame(data=data_profiling_data, schema=self.data_profiling_schema)
              else:
                data_profiling_df = self.spark.createDataFrame(data=data_profiling_data, schema=self.data_profiling_schema)
                self.dataframes[source].cache()
                rows = self.dataframes[source].count()
                columns = len(self.dataframes[source].columns)
                for column in self.dataframes[source].columns:
                    result_df = self.apply_data_profiling_to_column_spark(
                        self.dataframes[source], table["source_type"], table["layer"], table["source_name"],table["filename"], column, rows, columns )
                    data_profiling_df = data_profiling_df.union(result_df)

              if self.data_right_structure == 'file':
                try:
                    data_profiling_folder_path = get_folder_structure(table,"data_profiling")
                                       
                except Exception as e:
                    raise Exception(f"Incorrect folder path or container name not specified, {e}")
                  
                data_profiling_file_name = f"data_profiling_report_{source}{datetime.now(self.time_zone).strftime('_%d_%m_%Y_%H_%M_%S')}"
                if self.run_engine.lower()== 'polars':
                    data_profiling_report_file_path = self.data_write_ob.write_from_polars( data_profiling_df , data_profiling_folder_path , data_profiling_file_name, table)
                else:
                    data_profiling_report_file_path = self.data_write_ob.write(data_profiling_df, data_profiling_folder_path, data_profiling_file_name, table)
                print(f"Data profiling report for {source} is uploaded successfully at : {data_profiling_report_file_path}")
                
              else:
                  if self.run_engine.lower()=='polars':
                    data_profiling_report_file_path=self.data_write_ob.write_from_polars(data_profiling_df, self.output_db_name, source)
                  else:
                    data_profiling_report_file_path=self.data_write_ob.write(data_profiling_df, self.output_db_name, source)
                  print(f"Data profiling report for {source} is added successfully at : {data_profiling_report_file_path}")

              if self.run_engine.lower()== 'polars':
                data_profiling_report_df=data_profiling_df.with_columns(pl.lit(data_profiling_report_file_path).alias("data_profiling_write_location"))
                combined_data_profiling_report_data =combined_data_profiling_report_data + data_profiling_report_df.rows() 
              else:
                data_profiling_report_df=data_profiling_df.withColumn("data_profiling_write_location",lit(data_profiling_report_file_path))
                combined_data_profiling_report_df=combined_data_profiling_report_df.union(data_profiling_report_df)
              
            except Exception as e:
              if self.run_engine.lower()== 'polars': 
                rundate = date.today().strftime("%Y/%m/%d")
                data_profiling_report_df  = pl.DataFrame(data=[(self.job_id,
                table["source_type"], table["layer"], table["source_name"], table["filename"],
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, rundate, f'Failed to perform profiling, {e}')], schema=combined_data_profiling_schema) 
                combined_data_profiling_report_data= combined_data_profiling_report_data + data_profiling_report_df.rows()
                continue
              else:
                rundate = date.today().strftime("%Y/%m/%d")
                data_profiling_report_df  = self.spark.createDataFrame(data=[(self.job_id,
                table["source_type"], table["layer"], table["source_name"], table["filename"],
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, lit(rundate), f'Failed to perform profiling, {e}')], schema=combined_data_profiling_schema) 
                combined_data_profiling_report_df=combined_data_profiling_report_df.union(data_profiling_report_df)
                continue
        
      if write_consolidated_report==True: 
        if self.run_engine.lower()== 'polars': 
          combined_data_profiling_report_df=pl.DataFrame(data = combined_data_profiling_report_data , schema = combined_data_profiling_schema)
          if self.data_right_structure == 'file' :
              output_report_folder_path = f"{source_config[0]['output_folder_structure']}data_profiling/consolidated_report/"
              combine_profiling_file_name = f"combined_data_profiling_report_{datetime.now(self.time_zone).strftime('_%d_%m_%Y_%H_%M_%S')}"
              combined_data_profiling_report_path=self.data_write_ob.write_from_polars(combined_data_profiling_report_df,output_report_folder_path, combine_profiling_file_name, source_config[0])
              print(f"Combined report is uploaded successfully at : {combined_data_profiling_report_path}")
          else :
              combined_data_profiling_report_path=self.data_write_ob.write_from_polars(combined_data_profiling_report_df, self.output_db_name, 'combined_data_profiling_report')
              print(f"Combined report is added successfully at : {combined_data_profiling_report_path}")
        else:
          if self.data_right_structure == 'file' :
              output_report_folder_path = f"{source_config[0]['output_folder_structure']}/data_profiling/consolidated_report/"
              combine_profiling_file_name = f"combined_data_profiling_report_{datetime.now(self.time_zone).strftime('_%d_%m_%Y_%H_%M_%S')}"
              combined_data_profiling_report_path=self.data_write_ob.write(combined_data_profiling_report_df,output_report_folder_path, combine_profiling_file_name, source_config[0])
              print(f"Combined report is uploaded successfully at : {combined_data_profiling_report_path}")
          else :
              combined_data_profiling_report_path=self.data_write_ob.write(combined_data_profiling_report_df, self.output_db_name, 'combined_data_profiling_report')
              print(f"Combined report is added successfully at : {combined_data_profiling_report_path}")

      else:
          pass
