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
        $h = $x + $y;
        echo $h;
        function soma2($c, $b){
            echo $c+$b;
        }
        soma2($h, 2);
        return $h;
    }
    $j =2;
    $l= soma($j,2);

    soma2(8, 2);
    echo $j;
    echo $l;

?>
