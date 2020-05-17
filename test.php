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
        return $a;
    }
    $c = soma(1,2);
?>
