import java.util.Random

import org.apache.log4j.Logger
import org.apache.log4j.Level

import scala.io.Source

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.rdd._
import org.apache.spark.mllib.recommendation.{ALS, Rating, MatrixFactorizationModel}

object MovieLensALS {
  def main(args: Array[String]) {

    Logger.getLogger("org.apache.spark").setLevel(Level.WARN)
    Logger.getLogger("org.eclipse.jetty.server").setLevel(Level.OFF)

    /*val conf = new SparkConf()
      .setMaster("local[4]")
      .setAppName("MovieLensALS")*/
    val sc = new SparkContext("local[16]", "MovieLensALS")

    println("args is  " + args)

    //read movielens ratings.dat
    val ratings = sc.textFile(args(0) + "/ratings.dat").map { line => 
      val fields = line.split("::")
      // format: (timestamp % 10, Rating(userId, movieId, rating))
      (fields(3).toLong % 10, Rating(fields(0).toInt, fields(1).toInt,
        fields(2).toDouble))
    }

    val movies = sc.textFile(args(0) + "/movies.dat").map { line =>
      val fields = line.split("::")
      //movieId, movieName
      (fields(0).toInt, fields(1))
    }.collect.toMap

    //get summary of ratings
    val numRatings = ratings.count
    val numUsers = ratings.map(_._2.user).distinct.count
    val numMovies = ratings.map(_._2.product).distinct.count

    println("Got " + numRatings + " ratings from " + numUsers + " users on "
      + numMovies + " movies.")

    //get ratings of user on top 50 popular movies
    val mostRatedMovieIds = ratings.map(_._2.product) //extract movieId
                                   .countByValue      //count ratings per movie
                                   .toSeq             //convert map to seq
                                   .sortBy(- _._2)    //sort by rating count in decreasing order
                                   .take(50)          //take 50 most rated
                                   .map(_._1)         //get movie ids
    val random = new Random(0)
    val selectedMovies = mostRatedMovieIds.filter(x => random.nextDouble() < 0.2)
                                          .map(x => (x, movies(x)))
                                          .toSeq
    val myRatings = elicitateRatings(selectedMovies)
    //convert received ratings to RDD[Rating], now this can be worked in parallel
    val myRatingsRDD = sc.parallelize(myRatings)

    //create training test and validation set, use persist to hold these in memory
    val numPartitions = 20 //TODO: ?
    val training = ratings.filter(x => x._1 < 6)
                          .values
                          .union(myRatingsRDD)
                          .repartition(numPartitions) 
                          .persist
    val validation = ratings.filter(x => x._1 >= 6 && x._1 < 8)
                          .values
                          .union(myRatingsRDD)
                          .repartition(numPartitions)
                          .persist
    val test = ratings.filter(x => x._1 >= 8).values.persist

    val numTraining = training.count
    val numValidation = validation.count
    val numTest = test.count

    println("Training: " + numTraining + ", validation: " + numValidation + ", test: "
      + numTest)

    //initialize parameters grid to learn model
    val ranks = List(5, 10, 15)
    val lambdas = List(0.01, 0.1, 1)
    val numIters = List(10, 20)

    //Learn models using ALS
    var bestModel: Option[MatrixFactorizationModel] = None
    var bestValidationRmse = Double.MaxValue
    var bestRank = 0
    var bestLambda = -1.0
    var bestNumIter = -1
    for (rank <- ranks; lambda <- lambdas; numIter <- numIters) {
      //learn model for these parameter
      val model = ALS.train(training, rank, numIter, lambda)
      val validationRmse = computeRMSE(model, validation, numValidation)
      println("RMSE (validation) = " + validationRmse + " for model trianed with rank = "
        + rank + " , lambda = " + lambda + ", and numIter = " + numIter + ".")
      if (validationRmse < bestValidationRmse) {
        bestModel = Some(model)
        bestValidationRmse = validationRmse
        bestRank = rank
        bestLambda = lambda
        bestNumIter = numIter
      }
    }
    
    val testRmse = computeRMSE(bestModel.get, test, numTest)
    println("The best model was trained with rank = " + bestRank + " and lambda = "
      + bestLambda + ", and numIter = " + bestNumIter + ".")

    //find best movies for the user
    val myRatedMovieIds = myRatings.map(_.product).toSet
    //generate candidates after taking out already rated movies
    val candidates = sc.parallelize(movies.keys.filter(!myRatedMovieIds.contains(_)).toSeq)
    val recommendations = bestModel.get
                                   .predict(candidates.map((0, _)))
                                   .collect
                                   .sortBy(-_.rating)
                                   .take(50)
    var i = 1
    println("Movies recommendation for you: ")
    recommendations.foreach { r =>
      println("%2d".format(i) + ": " + movies(r.product))
      i += 1
    }


    //compare results with baseline
    val meanRating = training.union(validation).map(_.rating).mean
    val baselineRmse = math.sqrt(test.map(x => (meanRating - x.rating) * (meanRating - x.rating))
                                     .reduce(_+_) / numTest)
    val improvement = (baselineRmse - testRmse)/baselineRmse * 100
    println("The best model improves the baseline by " + "%1.2f".format(improvement) + "%.")


    sc.stop()
  }



 /** compute RMSE **/
 def computeRMSE(model: MatrixFactorizationModel, data: RDD[Rating], n:Long) = {
   val predictions: RDD[Rating] = model.predict(data.map(x => (x.user, x.product)))
   val predictionAndRatings = predictions.map(x => ((x.user, x.product), x.rating))
                                         .join(data.map(x => ((x.user, x.product), x.rating)))
                                         .values
   math.sqrt(predictionAndRatings.map(x => (x._1 - x._2) * (x._1 - x._2)).reduce(_+_) / n)
 }

 /** Elicitate ratings from commandline **/
 def elicitateRatings(movies: Seq[(Int, String)]) = {
   val prompt = "Please rate following movie (1-5(best), or 0 if not seen):"
   println(prompt)
   val ratings = movies.flatMap { x =>

    var rating: Option[Rating] = None
     var valid = false

     while (!valid) {
       print(x._2 + ": ")
       try {
         val r = Console.readInt
         if (r < 0 || r > 5) {
           println(prompt)
         } else {
           valid = true
           if (r > 0) {
             rating = Some(Rating(0, x._1, r))
           }
         }
       } catch {
         case e: Exception => println(prompt)
       }
     }

     rating match {
       case Some(r) => Iterator(r)
       case None => Iterator.empty
     }

   } //end flatMap

   if (ratings.isEmpty) {
     error("No rating provided")
   } else {
     ratings
   }

 }


}//end object




