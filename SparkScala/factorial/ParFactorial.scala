import scala.annotation.tailrec

import akka.actor.{Actor, ActorLogging, ActorSystem, Props}

object ParFactorial extends App {
  val factorials = List(20000, 1800, 32000, 2800, 22000, 4200, 55000, 4800, 
                        2000, 18000, 3200, 28000, 2200, 42000, 5500, 48000)
  val system = ActorSystem("factorial")

  val collector = system.actorOf(Props(new FactorialCollector(factorials)),
    "collector")

}

class FactorialCollector(factorials: List[Int]) extends Actor with ActorLogging {

  var list: List[BigInt] = Nil
  var size = factorials.size
  
  for (num <- factorials) {
    context.actorOf(Props(new FactorialCalculator)) ! num
  }

  def receive = {
    case (num: Int, fac: BigInt) => {
      //log.info(s"factorial for $num is $fac")
      list = num :: list
      size -= 1
      if (size == 0) {
        context.system.shutdown()
      }
    }
  }
}


class FactorialCalculator extends Actor {
  def receive = {
    case num: Int => sender ! (num, factor(num))
  }

  private def factor(num: Int) = factorTail(num, 1)

  private def factorOld(num: Int): BigInt = {
      num match {
        case 0 => 1
        case n => n * factor(n - 1)
      }
  }

  @tailrec private def factorTail(num: Int, acc: BigInt): BigInt = {
    (num, acc) match {
      case (0, a) => a
      case (n, a) => factorTail(n-1, n * a)
    }
  }

}




