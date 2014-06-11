import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import java.io._


object SparkWordCount {
  def main(args: Array[String]) {
    val sc = new SparkContext("local[4]", "Spark Count")
    val threshold = args(1).toInt

    //read file and split it into words
    val tokenized = sc.textFile(args(0)).flatMap(_.split(" "))

    //count each word occurence
    val wordCounts = tokenized.map((_, 1)).reduceByKey(_+_)

    //filter out less than threshold words
    val filtered = wordCounts.filter(_._2 >= threshold)

    //count characters
    val charCounts = filtered.flatMap(_._1.toCharArray).map((_, 1)).reduceByKey(_+_)

    //val x = charCounts.collect()
    //println("length of x is " + x.length)

    charCounts.saveAsTextFile("hdfs://gnosis-01-01-01.crl.samsung.com:8020/user/m3.sharma/output")

    /*val writer = new PrintWriter(new File("hdfs:////gnosis-01-01-01.crl.samsung.com/user/m3.sharma/output"))

    for (i <- x) {
      writer.write(i + "\n")
    }


    writer.write("length of x is " + x.length)

    writer.close()
     */
    sc.stop()

  }
}
