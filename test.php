<?php
    $b = 3;
    $c1 = 0 ;
    $a = 1;
    $d = 2;
    while($b < 0){
        if ($a > $d){
            echo 123;
        }
        else if ($d < $a) {
            $d = $d + 1;
        }
        else {
            $c = $c + $i;
        }
        $b = $b-1;
    }
    echo $c1;
    echo $a;
    echo $d;
    echo $b;
    /*$re = readline();*/
    $x = 1 + True; /* Ok */
    echo $x;
    $x = 1 and True; /* Ok */
    echo $x;
    $x = "a" . 1 . True; /* Ok */
    echo $x;
    $x = "a" == "b"; /* Ok, resultado bool: False */
    echo $x;
    function soma($x, $y) {
        $a = $x + $y;
        echo $a;
        /*return $a*/;
    }
    $j =2;
    soma($j,2);
    /*echo $c; */

    /*function soma() {
        $m = 1 + 2;
        $n = 2*$m;
        echo $m;
        echo $n;

        function soma2() {
            $o = 2 + 2;
            $p = 2*$o;
            echo $o;
            echo $p;
        }
    }

    echo $x;
    $b=3;
    soma();
    soma2();*/

?>
