name := "factorial"

version := "1.0"

scalaVersion := "2.10.4"

val akkaVersion = "2.3.1"

libraryDependencies ++ = Seq(
    "com.typesafe.akka" %% "akka-actor" % akkaVersion
  )
