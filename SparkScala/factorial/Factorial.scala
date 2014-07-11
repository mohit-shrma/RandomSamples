import scala.annotation.tailrec

object Factorial extends App {
  val factorials = List(20000, 1800, 32000, 2800, 22000, 4200, 55000, 4800, 
                        2000, 18000, 3200, 28000, 2200, 42000, 5500, 48000)

  for (num <- factorials) {
    factor(num)
    //println(s"factorial for $num is ${factor(num)}")
  }

  private def factorOld(num: Int): BigInt = {
    num match {
      case 0 => 1
      case n => n * factor(n - 1)
    }
  }

  private def factor(num: Int) = factorTail(num, 1)

  @tailrec private def factorTail(num: Int, acc: BigInt): BigInt = {
    (num, acc) match {
      case (0, a) => a
      case (n, a) => factorTail(n-1, n * a)
    }
  }




}
