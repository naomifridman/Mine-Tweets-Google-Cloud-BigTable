

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import java.io.IOException;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;

public class TopNwords {
	
	  

					
	public static class ClasMapper extends Mapper<Text, Text, LongWritable, Text> {
		
		public void map(Text key, Text value, Context context) {
			try {
				int sal = Integer.parseInt(value.toString());
				context.write(new LongWritable(sal), key);
			} catch (Exception e){
				System.out.println(e.getMessage());			
			}
		}
	}



	public static  class ClasReducer extends Reducer<LongWritable, Text, Text, LongWritable> {
		int mCount = 0;
		
		@Override
		protected void setup(Context context) throws IOException, InterruptedException {
			mCount = 0;
		}
		
		public void reduce(LongWritable key, Iterable<Text> values, Context context) {
			if(mCount < 5) {
				try {
					for(Text value: values) {
						context.write(value, key);
						mCount++;
											if(mCount > 5) {
												 break;
											}
					}
				} catch(Exception e) {
					
				}
			}
		}
	}



    public static void main(String[] args) throws Exception {

	
		Configuration conf = new Configuration();
		conf.set("mapreduce.input.keyvaluelinerecordreader.key.value.separator", "\t");
		
		Job job = Job.getInstance(conf);
		
		job.setJobName("Top 10 frequent words");
		job.setJarByClass(TopNwords.class);
		
		job.setNumReduceTasks(1);
		
		job.setMapperClass(ClasMapper.class);
		job.setReducerClass(ClasReducer.class);
		job.setSortComparatorClass(LongWritable.DecreasingComparator.class);
		
		job.setInputFormatClass(KeyValueTextInputFormat.class);
		
		job.setMapOutputKeyClass(LongWritable.class);
		job.setMapOutputValueClass(Text.class);
		
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(LongWritable.class);
		
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}

}