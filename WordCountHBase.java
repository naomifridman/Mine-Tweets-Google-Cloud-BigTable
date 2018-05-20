# code is cpied from hadoop tutorials at:
# https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCountHBase {

  /* public static class TokenizerMapper
       extends Mapper<Object, Text, Text, IntWritable>{

    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString());
      while (itr.hasMoreTokens()) {
        word.set(itr.nextToken());
        context.write(word, one);
      }
    }
  } */
  public static class MyMapper extends TableMapper<Text, IntWritable>  {

	private final IntWritable ONE = new IntWritable(1);
   	private Text text = new Text();

   	public void map(ImmutableBytesWritable row, Result value, Context context) throws IOException, InterruptedException {
        	String val = new String(value.getValue(Bytes.toBytes("cf"), Bytes.toBytes("attr1")));
          	text.set(val);     // we can only emit Writables...

        	context.write(text, ONE);
   	}
  }
  
 
  /*public static class IntSumReducer
       extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
  }*/

  public static class MyTableReducer extends TableReducer<Text, IntWritable, ImmutableBytesWritable>  {

 	public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
    		int i = 0;
    		for (IntWritable val : values) {
    			i += val.get();
    		}
    		Put put = new Put(Bytes.toBytes(key.toString()));
    		put.add(Bytes.toBytes("cf"), Bytes.toBytes("count"), Bytes.toBytes(i));

    		context.write(null, put);
   	}
  }
  public static void main(String[] args) throws Exception {
	  /*
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "word count");
	
    job.setJarByClass(WordCount.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
	
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
	
    System.exit(job.waitForCompletion(true) ? 0 : 1);*/
	
	//**********************
	
	Configuration config = HBaseConfiguration.create();
	Job job = new Job(config,"ExampleSummary");
	job.setJarByClass(MySummaryJob.class);     // class that contains mapper and reducer

	Scan scan = new Scan();
	scan.setCaching(500);        // 1 is the default in Scan, which will be bad for MapReduce jobs
	scan.setCacheBlocks(false);  // don't set to true for MR jobs
	// set other scan attrs

	TableMapReduceUtil.initTableMapperJob(
		sourceTable,        // input table
		scan,               // Scan instance to control CF and attribute selection
		MyMapper.class,     // mapper class
		Text.class,         // mapper output key
		IntWritable.class,  // mapper output value
		job);
	TableMapReduceUtil.initTableReducerJob(
		targetTable,        // output table
		MyTableReducer.class,    // reducer class
		job);
	job.setNumReduceTasks(1);   // at least one, adjust as required

	System.exit(job.waitForCompletion(true) ? 0 : 1);
		
  
  }
}